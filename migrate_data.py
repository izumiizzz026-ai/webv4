import sqlite3

# Connect to both databases
old_db = sqlite3.connect('dist/instance/attendance.db.bak')
new_db = sqlite3.connect('dist/instance/attendance.db')

old_cur = old_db.cursor()
new_cur = new_db.cursor()

# Copy teachers
print('=== Migrating Teachers ===')
old_cur.execute('SELECT * FROM teachers')
teachers = old_cur.fetchall()
for t in teachers:
    try:
        new_cur.execute('INSERT INTO teachers (id, full_name, email, password_hash, section, grade_level, db_name, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', t)
        print(f'  Migrated teacher: {t[1]} ({t[2]})')
    except Exception as e:
        print(f'  Error: {e}')

new_db.commit()

# Copy students (with new columns set to NULL)
print('\n=== Migrating Students ===')
old_cur.execute('SELECT id, full_name, email, password_hash, section, qr_code, created_at FROM students')
students = old_cur.fetchall()
for s in students:
    try:
        new_cur.execute('INSERT INTO students (id, full_name, email, password_hash, section, qr_code, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)', s)
        print(f'  Migrated student: {s[1]} ({s[2]})')
    except Exception as e:
        print(f'  Error: {e}')

new_db.commit()

print('\n=== Migration Complete! ===')
print('Your teacher and student accounts have been restored.')
old_db.close()
new_db.close()
