import sqlite3
import os

# Find all teacher databases
instance_dir = r'c:\Users\Lem Jasper\OneDrive\Desktop\Portfolio\QR Attendance\dist\instance'

for f in os.listdir(instance_dir):
    if f.startswith('teacher_') and f.endswith('.db'):
        db_path = os.path.join(instance_dir, f)
        print(f'Fixing {f}...')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Fix students table - add missing columns
        cur.execute('PRAGMA table_info(students)')
        student_cols = [c[1] for c in cur.fetchall()]
        
        student_cols_to_add = [
            ('guardian_name', 'VARCHAR(200)', 'NULL'),
            ('guardian_email', 'VARCHAR(150)', 'NULL'),
            ('guardian_phone', 'VARCHAR(20)', 'NULL'),
            ('notify_on_checkin', 'INTEGER', '1'),
            ('notify_on_checkout', 'INTEGER', '1'),
        ]
        
        for col, typ, default in student_cols_to_add:
            if col not in student_cols:
                try:
                    cur.execute(f'ALTER TABLE students ADD COLUMN {col} {typ} DEFAULT {default}')
                    print(f'  Added students.{col}')
                except Exception as e:
                    print(f'  Error students.{col}: {e}')
        
        # Fix attendance table - add missing columns
        cur.execute('PRAGMA table_info(attendance)')
        attendance_cols = [c[1] for c in cur.fetchall()]
        print(f'  Current attendance columns: {attendance_cols}')
        
        attendance_cols_to_add = [
            ('check_in_time', 'DATETIME', 'NULL'),
            ('check_out_time', 'DATETIME', 'NULL'),
            ('attendance_status', 'VARCHAR(20)', "'ABSENT'"),
            ('date', 'VARCHAR(10)', 'NULL'),
        ]
        
        for col, typ, default in attendance_cols_to_add:
            if col not in attendance_cols:
                try:
                    cur.execute(f'ALTER TABLE attendance ADD COLUMN {col} {typ} DEFAULT {default}')
                    print(f'  Added attendance.{col}')
                except Exception as e:
                    print(f'  Error attendance.{col}: {e}')
        
        conn.commit()
        conn.close()

print('\nAll teacher databases fixed!')
