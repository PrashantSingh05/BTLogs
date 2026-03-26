from flask import Blueprint, request, render_template, redirect, session
from app.services.log_service import create_log, get_all_logs, delete_log, update_log
from app.database.db import get_db

log_bp = Blueprint('logs', __name__)


# 🔐 Login protection
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# 📊 Dashboard
@log_bp.route('/')
@login_required
def dashboard():
    logs = get_all_logs()

    # Safe sorting (in case timestamp missing/null)
    logs = sorted(
        logs,
        key=lambda x: x['timestamp'] if x['timestamp'] else '',
        reverse=True
    )

    latest_logs = logs[:5]

    total = len(logs)
    high = len([l for l in logs if l['impact_level'] == 'high'])
    medium = len([l for l in logs if l['impact_level'] == 'medium'])
    low = len([l for l in logs if l['impact_level'] == 'low'])

    return render_template(
        'dashboard.html',
        logs=latest_logs,
        all_logs=logs,
        total=total,
        high=high,
        medium=medium,
        low=low
    )


# ➕ Add Log
@log_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_log():
    # 🚫 Viewer restriction
    if session.get('role') == 'viewer':
        return "Access Denied"

    if request.method == 'POST':
        create_log(request.form)
        return redirect('/')  # ✅ triggers refresh

    return render_template('add_log.html')


# 📄 View Logs
@log_bp.route('/logs')
@login_required
def view_logs():
    logs = get_all_logs()
    return render_template('view_logs.html', logs=logs)


# ❌ Delete
@log_bp.route('/delete/<int:log_id>')
@login_required
def delete(log_id):
    if session.get('role') == 'viewer':
        return "Access Denied"

    delete_log(log_id)
    return redirect('/logs')  # ✅ refresh after delete


# ✏ Edit
@log_bp.route('/edit/<int:log_id>', methods=['GET', 'POST'])
@login_required
def edit(log_id):
    if session.get('role') == 'viewer':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        update_log(log_id, request.form)
        return redirect('/logs')  # ✅ refresh after edit

    cursor.execute("SELECT * FROM logs WHERE id=%s", (log_id,))
    log = cursor.fetchone()

    return render_template('edit_log.html', log=log)