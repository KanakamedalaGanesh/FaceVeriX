# FaceVeriX - Smart Face Recognition Attendance System

## 🚀 Introduction
FaceVeriX is an AI-powered face recognition attendance system designed for efficient and secure student attendance tracking. Built using Flask and MySQL, this system allows student registration with both uploaded and live-captured photos, real-time face recognition, and attendance tracking. It features a visually appealing dark-themed admin dashboard for enhanced user experience.

## ✨ Features
- **Face Recognition Attendance** using OpenCV and deep learning.
- **Admin Dashboard** for managing attendance and student data.
- **Student Registration** via photo upload or live camera capture.
- **Real-time Face Detection** with visual feedback indicators.
- **Fake Face Detection (Liveness Check)** using blinking detection.
- **Graphical Attendance Reports** with Chart.js/Recharts.
- **Secure Image Uploads** with validation.
- **Voice Assistant Integration** for speech-based attendance marking.
- **Online Deployment** on Render, Railway, or AWS S3.

## 🛠️ Tech Stack
- **Backend:** Flask, OpenCV, Face Recognition API
- **Frontend:** HTML, CSS, JavaScript (Bootstrap, Chart.js, Recharts)
- **Database:** MySQL
- **Hosting:** Render/Railway/AWS S3 for image storage

## 📜 Project Setup
### Prerequisites
Ensure you have Python and MySQL installed. Recommended versions:
- Python 3.8+
- MySQL 8+

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/FaceVeriX.git
   cd FaceVeriX
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up MySQL database:
   ```sql
   CREATE DATABASE faceverix;
   ```
4. Update `config.py` with your database credentials.
5. Run database migrations:
   ```bash
   python db_setup.py
   ```
6. Start the Flask server:
   ```bash
   python app.py
   ```
7. Access the system at:
   ```
   http://127.0.0.1:5000/
   ```

## 📷 Screenshots
![Admin Login](path/to/admin-login-screenshot.png)
![Dashboard](path/to/dashboard-screenshot.png)
![Registration Page](path/to/registration-screenshot.png)

## 🛡️ Security & Best Practices
- Secure image uploads with validation.
- Encrypt sensitive user data.
- Implement access control for admin functionalities.

## 📩 Contact
For any queries, reach out to **Kanakamedala Ganesh** at **ganeshkanakamedala@gmail.com**

## 📜 License
This project is open-source under the MIT License.

---
FaceVeriX - Smarter Attendance with AI!

