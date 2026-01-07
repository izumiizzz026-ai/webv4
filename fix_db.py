import sqlite3
import os

# Fix all databases
dbs_to_fix = [
    'instance/attendance.db',
    'dist/instance/attendance.db',
]

student_columns = [
    ('grade_level', 'VARCHAR(10)', 'NULL'),
    ('teacher_id', 'INTEGER', 'NULL'),
    ('guardian_name', 'VARCHAR(200)', 'NULL'),
    ('guardian_email', 'VARCHAR(150)', 'NULL'),
    ('guardian_phone', 'VARCHAR(20)', 'NULL'),
    ('notify_on_checkin', 'BOOLEAN', '1'),
    ('notify_on_checkout', 'BOOLEAN', '1'),
]

admin_columns = [
    ('smtp_email', 'VARCHAR(150)', "'lj.xnkzk@gmail.com'"),
    ('smtp_password', 'VARCHAR(255)', "'qkxe lmgl gazz khil'"),
    ('smtp_server', 'VARCHAR(100)', "'smtp.gmail.com'"),
    ('smtp_port', 'INTEGER', '587'),
]

for db_path in dbs_to_fix:
    if not os.path.exists(db_path):
        print(f"Skipping {db_path} - does not exist")
        continue
        
    print(f"\n=== Fixing {db_path} ===")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fix students table
    cursor.execute('PRAGMA table_info(students)')
    existing = [col[1] for col in cursor.fetchall()]
    
    for col_name, col_type, default in student_columns:
        if col_name not in existing:
            try:
                cursor.execute(f'ALTER TABLE students ADD COLUMN {col_name} {col_type} DEFAULT {default}')
                print(f'  Added students.{col_name}')
            except Exception as e:
                print(f'  Error students.{col_name}: {e}')
    
    # Fix admin_config table
    cursor.execute('PRAGMA table_info(admin_config)')
    existing = [col[1] for col in cursor.fetchall()]
    
    for col_name, col_type, default in admin_columns:
        if col_name not in existing:
            try:
                cursor.execute(f'ALTER TABLE admin_config ADD COLUMN {col_name} {col_type} DEFAULT {default}')
                print(f'  Added admin_config.{col_name}')
            except Exception as e:
                print(f'  Error admin_config.{col_name}: {e}')
    
    conn.commit()
    conn.close()

print("\n=== All databases fixed! ===")
