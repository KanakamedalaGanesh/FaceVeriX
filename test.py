import mysql.connector

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='ganesh',
        database='face_attendance_db'
    )
    print("✅ Database connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Database connection failed:", e)
