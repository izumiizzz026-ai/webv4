"""
Multi-Database Manager for QR Attendance System

This module handles the multi-database architecture where:
- Main database (attendance_main.db) stores teachers with their section/grade assignments
- Each teacher has their own database (teacher_{id}_{grade}_{section}.db) for their students

Grade Levels: 11, 12 (SHS only)
Sections: Custom names entered by admin
"""

import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import pytz
import qrcode
from io import BytesIO

# Philippine timezone
PHILIPPINE_TZ = pytz.timezone('Asia/Manila')

def get_philippine_time():
    """Get current time in Philippine timezone"""
    return datetime.now(PHILIPPINE_TZ)

def get_instance_dir():
    """Get the instance directory for database storage"""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(script_dir, 'dist')
    
    instance_dir = os.path.join(base_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    return instance_dir

# Base for teacher-specific database models
TeacherDBBase = declarative_base()

class TeacherStudent(TeacherDBBase):
    """Student model for teacher's database"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    section = Column(String(50), nullable=False)
    grade_level = Column(String(10), nullable=False)
    qr_code = Column(LargeBinary)
    teacher_id = Column(Integer, nullable=False)  # Reference to main DB teacher
    created_at = Column(DateTime, default=get_philippine_time)
    
    # Guardian information
    guardian_name = Column(String(200), nullable=True)
    guardian_email = Column(String(150), nullable=True)
    guardian_phone = Column(String(20), nullable=True)
    notify_on_checkin = Column(Integer, default=1)  # 1 = True, 0 = False
    notify_on_checkout = Column(Integer, default=1)  # 1 = True, 0 = False
    
    def generate_qr_code(self):
        """Generate QR code for student"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f'STUDENT_{self.id}_{self.teacher_id}_{self.email}'
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.qr_code = buffer.getvalue()
        buffer.close()

class TeacherAttendance(TeacherDBBase):
    """Attendance model for teacher's database"""
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    timestamp = Column(DateTime, default=get_philippine_time)
    check_in_time = Column(DateTime, nullable=True)  # Actual check-in time
    check_out_time = Column(DateTime, nullable=True)  # Actual check-out time
    
    # Attendance status: PRESENT, ABSENT, LATE, CUTTING
    attendance_status = Column(String(20), default='ABSENT')  # PRESENT, ABSENT, LATE, CUTTING
    
    # Record type for tracking: 'check_in' or 'check_out' (for compatibility)
    status = Column(String(20), default='check_in')  # 'check_in' or 'check_out'
    
    date = Column(String(10), nullable=True)  # Date in YYYY-MM-DD format for querying


# Database session cache
_db_sessions = {}

def sanitize_db_name(text):
    """Sanitize text for use in database filename"""
    return text.lower().replace(' ', '_').replace('-', '_').replace('.', '')

def get_teacher_db_name(teacher_id, grade_level, section):
    """Generate database name for a teacher"""
    safe_grade = sanitize_db_name(str(grade_level))
    safe_section = sanitize_db_name(section)
    return f"teacher_{teacher_id}_{safe_grade}_{safe_section}"

def get_teacher_db_path(db_name):
    """Get full path for teacher's database"""
    instance_dir = get_instance_dir()
    return os.path.join(instance_dir, f"{db_name}.db")

def create_teacher_database(teacher_id, grade_level, section):
    """
    Create a new database for a teacher.
    Returns the database name.
    """
    db_name = get_teacher_db_name(teacher_id, grade_level, section)
    db_path = get_teacher_db_path(db_name)
    
    # Create engine and tables
    engine = create_engine(f"sqlite:///{db_path}")
    TeacherDBBase.metadata.create_all(engine)
    
    print(f"Created teacher database: {db_path}")
    return db_name

def get_teacher_db_session(db_name):
    """
    Get or create a database session for a teacher's database.
    Returns a sessionmaker class bound to the teacher's database.
    """
    if db_name in _db_sessions:
        return _db_sessions[db_name]
    
    db_path = get_teacher_db_path(db_name)
    
    if not os.path.exists(db_path):
        # Create the database if it doesn't exist
        engine = create_engine(f"sqlite:///{db_path}")
        TeacherDBBase.metadata.create_all(engine)
    else:
        engine = create_engine(f"sqlite:///{db_path}")
        # Migrate existing database to add missing columns
        migrate_teacher_database(engine)
    
    Session = sessionmaker(bind=engine)
    _db_sessions[db_name] = Session
    return Session

def migrate_teacher_database(engine):
    """Add missing columns to existing teacher database"""
    with engine.connect() as conn:
        # === Migrate students table ===
        result = conn.execute(text("PRAGMA table_info(students)"))
        existing_student_cols = [row[1] for row in result.fetchall()]
        
        student_cols_to_add = [
            ('guardian_name', 'VARCHAR(200)', 'NULL'),
            ('guardian_email', 'VARCHAR(150)', 'NULL'),
            ('guardian_phone', 'VARCHAR(20)', 'NULL'),
            ('notify_on_checkin', 'INTEGER', '1'),
            ('notify_on_checkout', 'INTEGER', '1'),
        ]
        
        for col, typ, default in student_cols_to_add:
            if col not in existing_student_cols:
                try:
                    conn.execute(text(f'ALTER TABLE students ADD COLUMN {col} {typ} DEFAULT {default}'))
                    conn.commit()
                except Exception as e:
                    pass  # Column might already exist
        
        # === Migrate attendance table ===
        result = conn.execute(text("PRAGMA table_info(attendance)"))
        existing_attendance_cols = [row[1] for row in result.fetchall()]
        
        attendance_cols_to_add = [
            ('check_in_time', 'DATETIME', 'NULL'),
            ('check_out_time', 'DATETIME', 'NULL'),
            ('attendance_status', 'VARCHAR(20)', "'ABSENT'"),
            ('date', 'VARCHAR(10)', 'NULL'),
        ]
        
        for col, typ, default in attendance_cols_to_add:
            if col not in existing_attendance_cols:
                try:
                    conn.execute(text(f'ALTER TABLE attendance ADD COLUMN {col} {typ} DEFAULT {default}'))
                    conn.commit()
                except Exception as e:
                    pass  # Column might already exist

def delete_teacher_database(db_name):
    """Delete a teacher's database file"""
    db_path = get_teacher_db_path(db_name)
    
    # Remove from cache
    if db_name in _db_sessions:
        del _db_sessions[db_name]
    
    # Delete file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted teacher database: {db_path}")
        return True
    return False

def find_student_by_email(email, teachers_list):
    """
    Search for a student across all teacher databases.
    
    Args:
        email: Student email to search for
        teachers_list: List of teacher dicts with 'db_name' key
    
    Returns:
        Tuple of (student, teacher_db_name) or (None, None) if not found
    """
    for teacher in teachers_list:
        db_name = teacher.get('db_name')
        if not db_name:
            continue
        
        db_path = get_teacher_db_path(db_name)
        if not os.path.exists(db_path):
            continue
        
        Session = get_teacher_db_session(db_name)
        session = Session()
        try:
            student = session.query(TeacherStudent).filter_by(email=email).first()
            if student:
                return student, db_name
        finally:
            session.close()
    
    return None, None

def get_available_sections(main_db_session, Teacher):
    """
    Get list of all available section/grade combinations from teachers.
    
    Args:
        main_db_session: SQLAlchemy session for main database
        Teacher: Teacher model class from main app
    
    Returns:
        List of dicts with 'section', 'grade_level', 'teacher_name', 'teacher_id'
    """
    teachers = main_db_session.query(Teacher).filter(
        Teacher.section.isnot(None),
        Teacher.grade_level.isnot(None)
    ).all()
    
    sections = []
    for t in teachers:
        sections.append({
            'section': t.section,
            'grade_level': t.grade_level,
            'teacher_name': t.full_name,
            'teacher_id': t.id,
            'db_name': t.db_name
        })
    
    return sections

def list_teacher_databases():
    """List all teacher databases in the instance directory"""
    instance_dir = get_instance_dir()
    databases = []
    
    for filename in os.listdir(instance_dir):
        if filename.startswith('teacher_') and filename.endswith('.db'):
            db_name = filename[:-3]  # Remove .db extension
            db_path = os.path.join(instance_dir, filename)
            databases.append({
                'db_name': db_name,
                'path': db_path,
                'size': os.path.getsize(db_path)
            })
    
    return databases


def init_db_manager(app):
    """
    Initialize the database manager for the Flask app.
    Ensures the instance directory exists and all teacher databases are accessible.
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        # Ensure instance directory exists
        instance_dir = get_instance_dir()
        print(f"✓ Multi-database manager initialized. Instance dir: {instance_dir}")
        
        # List existing teacher databases
        existing_dbs = list_teacher_databases()
        if existing_dbs:
            print(f"✓ Found {len(existing_dbs)} teacher database(s)")
            for db_info in existing_dbs:
                print(f"  - {db_info['db_name']}")
        else:
            print("✓ No teacher databases found yet (will be created when teachers are added)")
        
        return True