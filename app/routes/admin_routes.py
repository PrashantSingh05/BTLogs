from flask import Blueprint, render_template, redirect, session
from app.database.db import get_db

admin_bp = Blueprint('admin', __name__)


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            return "Access Denied"
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_bp.route('/admin')
@admin_required
def admin_panel():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template('admin.html', users=users)


@admin_bp.route('/approve/<int:user_id>/<role>')
@admin_required
def approve(user_id, role):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET role=%s WHERE id=%s",
        (role, user_id)
    )
    db.commit()

    return redirect('/admin')