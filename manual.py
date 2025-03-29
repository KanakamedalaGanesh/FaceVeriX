from werkzeug.security import generate_password_hash

password = "admin123"  # Replace with your actual password
hashed_password = generate_password_hash(password, method="scrypt")  # Uses scrypt hashing
print("Hashed Password:", hashed_password)
