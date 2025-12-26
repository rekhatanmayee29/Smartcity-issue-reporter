from flask import Flask, render_template, request
import sqlite3
import uuid
from flask_mail import Mail, Message

app = Flask(__name__)

# ---------------- EMAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR_GMAIL@gmail.com'      # replace
app.config['MAIL_PASSWORD'] = 'YOUR_APP_PASSWORD'         # replace
# ----------------------------------------------

mail = Mail(app)

def get_db_connection():
    return sqlite3.connect("complaints.db")

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/complaint")
def complaint():
    return render_template("complaint.html")

@app.route("/submit", methods=["POST"])
def submit():
    state = request.form["state"]
    district = request.form["district"]
    city = request.form["city"]
    street = request.form["street"]
    issue = request.form["issue"]
    email = request.form["email"]

    ref_id = "SC-" + str(uuid.uuid4())[:8]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            ref_id TEXT,
            state TEXT,
            district TEXT,
            city TEXT,
            street TEXT,
            issue TEXT,
            email TEXT
        )
    """)

    cur.execute(
        "INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?, ?)",
        (ref_id, state, district, city, street, issue, email)
    )

    conn.commit()
    conn.close()

    msg = Message(
        subject="Complaint Registered Successfully",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email],
        body=f"""
Hello,

Your complaint has been registered successfully.

Reference ID: {ref_id}

Thank you for helping improve city infrastructure.
"""
    )
    mail.send(msg)

    return f"""
    <h2 style="text-align:center;color:green;">Complaint Submitted Successfully</h2>
    <p style="text-align:center;">
        Reference ID: <b>{ref_id}</b><br><br>
        A confirmation email has been sent.
    </p>
    """

if __name__ == "__main__":
        app.run()
