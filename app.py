from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import os
import base64
from datetime import datetime
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import logging
logging.basicConfig(level=logging.DEBUG)
import time
from flask import Response
import csv
import io


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_PERMANENT'] = True  # Extend session lifetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='ganesh',
        database='face_attendance_db'
    )

# Ensure admin passwords are hashed
def hash_admin_password():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM admin")
        admins = cursor.fetchall()

        for username, password in admins:
            if not password.startswith("pbkdf2:sha256") and not password.startswith("scrypt"):  # Check if already hashed
                hashed_password = generate_password_hash(password)
                cursor.execute("UPDATE admin SET password = %s WHERE username = %s", (hashed_password, username))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error hashing admin passwords: {e}")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            conn = get_db_connection()
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT password FROM admin WHERE username = %s", (username,))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()

            if admin:
                stored_password = admin[0]

                # 🔹 Ensure Flask correctly checks scrypt-hashed passwords
                if stored_password.startswith("scrypt"):
                    is_valid = check_password_hash(stored_password, password)
                else:
                    flash('⚠️ Password hashing mismatch. Ensure passwords are properly hashed.', 'error')
                    return redirect(url_for('login'))

                if is_valid:
                    session['admin'] = username
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password', 'error')
            else:
                flash('Invalid username or password', 'error')

        except Exception as e:
            flash('Database error occurred!', 'error')
            print("Login error:", e)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        return render_template('dashboard.html')
    flash("Please log in first", "error")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'photo' in request.files and request.files['photo'].filename != '':
                photo = request.files['photo'].read()
            elif request.form.get('live_photo_data', ''):
                live_photo_data = request.form['live_photo_data'].split(',')[1]
                photo = base64.b64decode(live_photo_data)
            else:
                flash('Please provide either an uploaded photo or a live photo.', 'error')
                return redirect(url_for('register'))
            
            cursor.execute("INSERT INTO students (name, photo) VALUES (%s, %s)", (name, photo))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Student registered successfully!', 'success')
        except Exception as e:
            flash('Error registering student!', 'error')
            logging.error(f"Registration error: {e}")
        return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/take_attendance')
def take_attendance():
    if 'admin' not in session:
        flash("Please log in first", "error")
        return redirect(url_for('login'))
    
    return render_template('take_attendance.html')
@app.route('/capture_attendance', methods=['POST'])
def capture_attendance():
    if 'admin' not in session:
        return jsonify({'status': 'error', 'message': 'Not authorized'})

    data = request.get_json()
    student_name = data.get('name').strip()
    image_data = data.get('image_data')

    if not image_data or not student_name:
        return jsonify({'status': 'error', 'message': 'Missing data'})

    try:
        save_dir = os.path.join('static', 'attendance_photos')
        os.makedirs(save_dir, exist_ok=True)

        filename = f"{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(image_data.split(',')[1]))

        db_filepath = filepath.replace("\\", "/").replace("static/", "")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (name, date_time, photo_path) VALUES (%s, %s, %s)",
            (student_name, datetime.now(), db_filepath)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Attendance captured successfully'})
    except Exception as e:
        logging.error(f"Error capturing attendance: {e}")
        return jsonify({'status': 'error', 'message': 'Error capturing attendance'})

@app.route('/view_reports')
def view_reports():
    if 'admin' not in session:
        flash("Please log in first", "error")
        return redirect(url_for('login'))

    student_name = request.args.get('student_name', '').strip()
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = "SELECT name, date_time, photo_path FROM attendance WHERE 1"
    params = []

    if student_name:
        query += " AND name LIKE %s"
        params.append(f"%{student_name}%")
    if start_date:
        query += " AND DATE(date_time) >= %s"
        params.append(start_date)
    if end_date:
        query += " AND DATE(date_time) <= %s"
        params.append(end_date)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash('Error retrieving attendance reports!', 'error')
        logging.error(f"View Reports Error: {e}")
        data = []

    return render_template('view_reports.html', data=data)
import io
from flask import Response

def fetch_attendance_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, date_time FROM attendance")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        logging.error(f"Error fetching attendance data: {e}")
        return []

@app.route('/download_csv', methods=['GET'])
def download_csv():
    attendance_data = fetch_attendance_data()

    if not attendance_data:
        return "No attendance records found.", 404

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'name', 'date_time'])
    writer.writeheader()
    for row in attendance_data:
        writer.writerow(row)

    output.seek(0)

    # Return CSV as downloadable file
    response = Response(output.getvalue(), content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=attendance_report.csv"
    return response


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    hash_admin_password()  # Ensure passwords are hashed on startup
    app.run(debug=True, threaded=True)
