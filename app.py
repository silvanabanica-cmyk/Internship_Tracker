from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, date

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("internships.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            deadline TEXT NOT NULL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_deadline_status(deadline):
    if not deadline:
        return "No deadline"

    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date"

    today = date.today()
    days_left = (deadline_date - today).days

    if days_left < 0:
        return "Overdue"
    elif days_left <= 7:
        return "Due soon"
    else:
        return "On track"


@app.route("/")
def home():
    selected_status = request.args.get("status", "")
    search_query = request.args.get("search", "").strip()
    sort_order = request.args.get("sort", "newest")

    conn = get_db_connection()

    total_count = conn.execute(
        "SELECT COUNT(*) FROM internships"
    ).fetchone()[0]

    saved_count = conn.execute(
        "SELECT COUNT(*) FROM internships WHERE status = ?",
        ("Saved",)
    ).fetchone()[0]

    applied_count = conn.execute(
        "SELECT COUNT(*) FROM internships WHERE status = ?",
        ("Applied",)
    ).fetchone()[0]

    interview_count = conn.execute(
        "SELECT COUNT(*) FROM internships WHERE status = ?",
        ("Interview",)
    ).fetchone()[0]

    rejected_count = conn.execute(
        "SELECT COUNT(*) FROM internships WHERE status = ?",
        ("Rejected",)
    ).fetchone()[0]

    offer_count = conn.execute(
        "SELECT COUNT(*) FROM internships WHERE status = ?",
        ("Offer",)
    ).fetchone()[0]

    if total_count > 0:
        interview_rate = round((interview_count / total_count) * 100)
        offer_rate = round((offer_count / total_count) * 100)
    else:
        interview_rate = 0
        offer_rate = 0

    query = "SELECT * FROM internships WHERE 1=1"
    params = []

    if selected_status and selected_status != "All":
        query += " AND status = ?"
        params.append(selected_status)

    if search_query:
        query += " AND (company LIKE ? OR role LIKE ?)"
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")

    if sort_order == "deadline_asc":
        query += " ORDER BY deadline ASC"
    elif sort_order == "deadline_desc":
        query += " ORDER BY deadline DESC"
    else:
        query += " ORDER BY id DESC"

    internships = conn.execute(query, params).fetchall()
    conn.close()

    internships_with_deadline_status = []

    for internship in internships:
        internship_dict = dict(internship)
        internship_dict["deadline_status"] = get_deadline_status(internship["deadline"])
        internships_with_deadline_status.append(internship_dict)

    return render_template(
        "index.html",
        internships=internships_with_deadline_status,
        selected_status=selected_status,
        search_query=search_query,
        sort_order=sort_order,
        total_count=total_count,
        saved_count=saved_count,
        applied_count=applied_count,
        interview_count=interview_count,
        rejected_count=rejected_count,
        offer_count=offer_count,
        interview_rate=interview_rate,
        offer_rate=offer_rate
    )


@app.route("/add", methods=["POST"])
def add_internship():
    company = request.form["company"]
    role = request.form["role"]
    status = request.form["status"]
    deadline = request.form["deadline"]
    notes = request.form["notes"]

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO internships (company, role, status, deadline, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (company, role, status, deadline, notes)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_internship(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM internships WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


@app.route("/edit/<int:id>")
def edit_internship(id):
    conn = get_db_connection()

    internship = conn.execute(
        "SELECT * FROM internships WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if internship is None:
        return redirect(url_for("home"))

    return render_template("edit.html", internship=internship)


@app.route("/update/<int:id>", methods=["POST"])
def update_internship(id):
    company = request.form["company"]
    role = request.form["role"]
    status = request.form["status"]
    deadline = request.form["deadline"]
    notes = request.form["notes"]

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE internships
        SET company = ?, role = ?, status = ?, deadline = ?, notes = ?
        WHERE id = ?
        """,
        (company, role, status, deadline, notes, id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


@app.route("/api/internships")
def api_internships():
    conn = get_db_connection()

    internships = conn.execute(
        "SELECT * FROM internships ORDER BY id DESC"
    ).fetchall()

    conn.close()

    data = []

    for internship in internships:
        data.append({
            "id": internship["id"],
            "company": internship["company"],
            "role": internship["role"],
            "status": internship["status"],
            "deadline": internship["deadline"],
            "deadline_status": get_deadline_status(internship["deadline"]),
            "notes": internship["notes"]
        })

    return jsonify(data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)