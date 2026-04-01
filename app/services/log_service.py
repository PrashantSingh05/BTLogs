from app.database.db import get_db


def calculate_impact(downtime):
    if downtime is None:
        return "low"

    downtime = float(downtime)

    # 🔥 UPDATED LOGIC
    if downtime <= 1:
        return "low"
    elif downtime <= 4:
        return "medium"
    else:
        return "high"


def create_log(data):
    db = get_db()
    cursor = db.cursor()

    downtime = data.get('downtime') or 0
    impact = calculate_impact(downtime)

    cursor.execute("""
        INSERT INTO logs (
            title, description, category, action_type,
            reason, downtime, impact_level, tags,
            system_name, created_by, incident_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get('title'),
        data.get('description'),
        data.get('category'),
        data.get('action_type'),
        data.get('reason'),
        downtime,
        impact,
        data.get('tags'),
        data.get('system_name'),
        data.get('created_by'),
        data.get('incident_date')
    ))

    db.commit()


def get_all_logs():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    return cursor.fetchall()


def filter_logs(start_date=None, end_date=None, system_name=None, search=None):
    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if start_date:
        query += " AND timestamp >= %s"
        params.append(start_date)

    if end_date:
        query += " AND timestamp <= %s"
        params.append(end_date + " 23:59:59")

    if system_name:
        query += " AND system_name ILIKE %s"
        params.append(f"%{system_name}%")

    if search:
        query += " AND (title ILIKE %s OR reason ILIKE %s OR tags ILIKE %s)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY timestamp DESC"

    cursor.execute(query, tuple(params))
    return cursor.fetchall()


def delete_log(log_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM logs WHERE id=%s", (log_id,))
    db.commit()


def update_log(log_id, data):
    db = get_db()
    cursor = db.cursor()

    downtime = data.get('downtime') or 0
    impact = calculate_impact(downtime)

    cursor.execute("""
        UPDATE logs
        SET title=%s, description=%s, category=%s, action_type=%s,
            reason=%s, downtime=%s, impact_level=%s, tags=%s,
            system_name=%s, created_by=%s, incident_date=%s
        WHERE id=%s
    """, (
        data.get('title'),
        data.get('description'),
        data.get('category'),
        data.get('action_type'),
        data.get('reason'),
        downtime,
        impact,
        data.get('tags'),
        data.get('system_name'),
        data.get('created_by'),
        data.get('incident_date'),
        log_id
    ))

    db.commit()