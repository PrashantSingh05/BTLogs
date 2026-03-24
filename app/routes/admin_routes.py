from flask import Blueprint, render_template, session, redirect
from app.database.db import get_db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def admin_panel():
    if session.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template('admin.html', users=users)


@admin_bp.route('/approve/<int:user_id>/<role>')
def approve(user_id, role):
    if session.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor()

    cursor.execute("UPDATE users SET role=? WHERE id=?", (role, user_id))
    db.commit()

    return redirect('/admin')