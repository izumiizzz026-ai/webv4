import importlib.util
import sys
from pathlib import Path

# Load app.py as module named 'app' by path to avoid import issues
root = Path(__file__).resolve().parents[1]
app_path = root / 'app.py'
spec = importlib.util.spec_from_file_location('app', str(app_path))
app_mod = importlib.util.module_from_spec(spec)
sys.modules['app'] = app_mod
spec.loader.exec_module(app_mod)

app = app_mod.app
db = app_mod.db
Student = app_mod.Student
Teacher = app_mod.Teacher
Attendance = app_mod.Attendance
get_db = app_mod.get_db


def run_tests():
    print("Starting DB tests...")
    with app.app_context():
        # Use in-memory DB for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        # ensure a clean schema
        try:
            db.drop_all()
        except Exception:
            pass
        db.create_all()

        # Create a student
        s = Student(full_name='Test Student', email='test@student.com', password_hash='hash')
        db.session.add(s)
        db.session.commit()

        # generate qr
        s.generate_qr_code()
        db.session.commit()
        assert s.qr_code is not None, "QR code was not generated"

        # Create a teacher
        t = Teacher(full_name='Test Teacher', email='test@teacher.com', password_hash='hash')
        db.session.add(t)
        db.session.commit()
        assert t.id is not None, "Teacher not created"

        # Create attendance
        a = Attendance(student_id=s.id, status='check_in')
        db.session.add(a)
        db.session.commit()
        assert a.id is not None, "Attendance not recorded"

    print("All tests passed")


if __name__ == '__main__':
    run_tests()
