from werkzeug.security import generate_password_hash
import mysql.connector

# Hash the password
new_password = "admin123"  # Change this to whatever you want
hashed_password = generate_password_hash(new_password)

# Connect to the database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='ganesh',
    database='face_attendance_db'
)
cursor = conn.cursor()

# Update admin password
cursor.execute("UPDATE admin SET password = %s WHERE username = 'admin'", (hashed_password,))
conn.commit()

print("✅ Admin password updated successfully!")

cursor.close()
conn.close()
