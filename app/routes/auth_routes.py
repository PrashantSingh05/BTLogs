from flask import Blueprint, render_template, request, redirect, session
from app.database.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from app import limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, 'pending')",
                (username, hashed_password)
            )
            db.commit()
            return "Registered. Wait for admin approval"
        except:
            return "User already exists"

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")   # 🚫 rate limiting
def login():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            if user['role'] == 'pending':
                return "Wait for admin approval"

            session['user'] = user['username']
            session['role'] = user['role']
            session.permanent = True

            return redirect('/')

        return "Invalid credentials"

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')