from flask import Flask, jsonify

from legacy.flask_app.grading import calc_final, late_days
from legacy.flask_app.utils import get_db, load_json

app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"


def seed_from_fixtures(path):
    db = get_db()
    db.executescript("""
        DROP TABLE IF EXISTS students; DROP TABLE IF EXISTS labs; DROP TABLE IF EXISTS submissions;
        CREATE TABLE students(id INTEGER, name TEXT, grp TEXT);
        CREATE TABLE labs(id INTEGER, num INTEGER, deadline TEXT);
        CREATE TABLE submissions(id INTEGER, student_id INTEGER, lab_id INTEGER, score INTEGER, submitted TEXT);
    """)
    data = load_json(path)
    for s in data["students"]:
        db.execute("INSERT INTO students VALUES (?,?,?)", (s["id"], s["name"], s["group"]))
    for l in data["labs"]:
        db.execute("INSERT INTO labs VALUES (?,?,?)", (l["id"], l["num"], l["deadline"]))
    for x in data["submissions"]:
        db.execute("INSERT INTO submissions VALUES (?,?,?,?,?)",
                   (x["id"], x["student_id"], x["lab_id"], x["score"], x["submitted"]))
    db.commit()


@app.route("/api/groups/<group>/grades")
def group_grades(group):
    try:
        db = get_db()
        # запах: SQL конкатенацією
        rows = db.execute("SELECT st.name, l.num, s.score, l.deadline, s.submitted "
                          "FROM submissions s JOIN students st ON st.id = s.student_id "
                          "JOIN labs l ON l.id = s.lab_id WHERE st.grp = '" + group + "' "
                          "ORDER BY st.name, l.num").fetchall()
        out = []
        for r in rows:
            out.append({"student": r["name"], "lab": r["num"], "raw": r["score"],
                        "final": calc_final(r["score"], r["deadline"], r["submitted"]),
                        "late_days": late_days(r["deadline"], r["submitted"])})
        return jsonify({"group": group, "grades": out})
    except:
        return jsonify({"error": "щось пішло не так"}), 500


@app.route("/api/groups/<group>/stats")
def group_stats(group):
    try:
        db = get_db()
        rows = db.execute("SELECT s.score, l.deadline, s.submitted "
                          "FROM submissions s JOIN students st ON st.id = s.student_id "
                          "JOIN labs l ON l.id = s.lab_id WHERE st.grp = '" + group + "'").fetchall()
        total = 0
        n = 0
        late = 0
        for r in rows:  # копіпаст логіки з group_grades
            f = calc_final(r["score"], r["deadline"], r["submitted"])
            if f is not None:
                total += f
                n += 1
            if late_days(r["deadline"], r["submitted"]) > 0:
                late += 1
        avg = round(total / n, 2) if n else 0
        return jsonify({"group": group, "submissions": len(rows), "avg_final": avg, "late_count": late})
    except:
        return jsonify({"error": "щось пішло не так"}), 500


@app.route("/api/submissions/<int:sid>/score")
def submission_score(sid):
    try:
        db = get_db()
        r = db.execute("SELECT s.score, l.deadline, s.submitted FROM submissions s "
                       "JOIN labs l ON l.id = s.lab_id WHERE s.id = " + str(sid)).fetchone()
        if r is None:
            return jsonify({"error": "не знайдено"}), 404
        return jsonify({"id": sid, "raw": r["score"],
                        "final": calc_final(r["score"], r["deadline"], r["submitted"]),
                        "late_days": late_days(r["deadline"], r["submitted"])})
    except:
        return jsonify({"error": "щось пішло не так"}), 500


if __name__ == "__main__":
    app.run(debug=True)
