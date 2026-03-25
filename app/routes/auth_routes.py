from flask import Blueprint, render_template, request, redirect, session, url_for
from app.database.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from app import limiter
from app.services.email_service import send_reset_email
import secrets

auth_bp = Blueprint('auth', __name__)

# 🔥 token storage
reset_tokens = {}


# ================= REGISTER =================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            return "Email and password required"

        hashed = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, 'pending')",
                (email, hashed)
            )
            db.commit()
            return "Registered. Wait for admin approval"
        except:
            return "User already exists"

    return render_template('register.html')


# ================= LOGIN =================
@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):

            if user['role'] == 'pending':
                return "Wait for admin approval"

            session['user'] = user['email']
            session['role'] = user['role']
            session.permanent = True

            return redirect('/')

        return "Invalid credentials"

    return render_template('login.html')


# ================= FORGOT PASSWORD =================
@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        token = secrets.token_urlsafe(16)
        reset_tokens[token] = email

        reset_link = url_for('auth.reset_password', token=token, _external=True)

        # 🔥 SEND EMAIL
        send_reset_email(email, reset_link)

        return "Reset link sent to your email."

    return render_template('forgot.html')


# ================= RESET PASSWORD =================
@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if token not in reset_tokens:
        return "Invalid or expired link"

    if request.method == 'POST':
        new_password = request.form['password']

        hashed = generate_password_hash(new_password)

        db = get_db()
        cursor = db.cursor()

        email = reset_tokens[token]

        cursor.execute(
            "UPDATE users SET password=? WHERE email=?",
            (hashed, email)
        )

        db.commit()

        reset_tokens.pop(token)

        return redirect('/login')

    return render_template('reset.html')


# ================= LOGOUT =================
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')