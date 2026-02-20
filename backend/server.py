# from flask import Flask, request, jsonify, send_from_directory, send_file
# from flask_cors import CORS
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer
# from my import SalaryPredictor
# import uuid
# import io
# import os
# import json

# # ------------------- User Storage -------------------
# USERS_FILE = "users.json"

# def load_users():
#     if not os.path.exists(USERS_FILE):
#         return {}
#     with open(USERS_FILE, "r") as f:
#         return json.load(f)

# def save_users(users):
#     with open(USERS_FILE, "w") as f:
#         json.dump(users, f, indent=2)

# # ------------------- App Setup -------------------
# app = Flask(__name__, static_folder="../front-end", static_url_path="")
# CORS(app)

# app.config["SECRET_KEY"] = "SUPER_SECRET_KEY_123"
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = "kowshikthota43@gmail.com"
# app.config['MAIL_PASSWORD'] = "napg irbo zafd dgbi"
# app.config['MAIL_DEFAULT_SENDER'] = "kowshikthota43@gmail.com"

# mail = Mail(app)
# serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# # ------------------- Serve Frontend -------------------
# @app.route("/")
# def serve_index():
#     return send_from_directory(app.static_folder, "index.html")

# @app.route("/login-page")
# def serve_login_page():
#     return send_from_directory(app.static_folder, "login.html")

# @app.route("/signup-page")
# def serve_signup_page():
#     return send_from_directory(app.static_folder, "signup.html")

# # ------------------- Auth Routes -------------------
# @app.route("/signup", methods=["POST"])
# def signup():
#     users = load_users()
#     data = request.json
#     email = data["email"]
#     password = data["password"]

#     if email in users:
#         return jsonify({"message": "User already exists"}), 400

#     users[email] = {"password": password, "verified": False}
#     token = serializer.dumps(email, salt="email-verify")
#     verify_link = f"http://localhost:5000/verify/{token}"

#     try:
#         msg = Message("Verify your account", recipients=[email])
#         msg.body = f"Click to verify your account:\n\n{verify_link}"
#         mail.send(msg)
#     except Exception as e:
#         print("EMAIL ERROR:", e)
#         print("VERIFY LINK (manual):", verify_link)
#         save_users(users)
#         return jsonify({"message": "Email failed"}), 500

#     save_users(users)
#     return jsonify({"message": "Verification email sent"})

# @app.route("/verify/<token>")
# def verify_email(token):
#     users = load_users()
#     try:
#         email = serializer.loads(token, salt="email-verify", max_age=3600)
#         users[email]["verified"] = True
#         save_users(users)
#         return "<h2>Email verified ✅</h2><a href='/login-page'>Login</a>"
#     except Exception as e:
#         return f"<h2>Invalid or expired link</h2><pre>{e}</pre>"

# @app.route("/login", methods=["POST"])
# def login():
#     users = load_users()
#     data = request.json
#     email = data["email"]
#     password = data["password"]

#     if email not in users:
#         return jsonify({"message": "User not found"}), 404
#     if users[email]["password"] != password:
#         return jsonify({"message": "Wrong password"}), 401
#     if not users[email]["verified"]:
#         return jsonify({"message": "Verify email first"}), 403

#     return jsonify({"token": str(uuid.uuid4()), "email": email})

# # ------------------- Salary Predictor -------------------
# predictor = SalaryPredictor()
# predictor.load_saved_model("salary_predictor_model.pkl")

# def growth_projection(current_salary):
#     g1 = current_salary * 1.08
#     g2 = g1 * 1.08
#     g3 = g2 * 1.08
#     return {"year1": round(g1, 2), "year2": round(g2, 2), "year3": round(g3, 2)}

# @app.route("/predict-salary", methods=["POST"])
# def predict_salary():
#     data = request.json
#     jobRole = data.get("jobRole", "")
#     skills = data.get("skills", "")
#     region = data.get("region", "")
#     years = int(data.get("experience", 0))

#     salary = predictor.predict_salary(
#         job_title=jobRole,
#         skills=skills,
#         country=region,
#         years_of_experience=years  # now passed correctly
#     )

#     growth = growth_projection(salary)
#     return jsonify({"currentSalary": round(salary, 2), "growth": growth})

# # ------------------- PDF Download -------------------
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# @app.route("/download-report", methods=["POST"])
# def download_report():
#     data = request.json
#     jobRole = data.get("jobRole", "")
#     skills = data.get("skills", "")
#     region = data.get("region", "")
#     years = int(data.get("experience", 0))

#     salary = predictor.predict_salary(
#         job_title=jobRole,
#         skills=skills,
#         country=region,
#         years_of_experience=years
#     )
#     growth = growth_projection(salary)

#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()

#     story = [
#         Paragraph("AI Salary Prediction Report", styles["Title"]),
#         Spacer(1, 12),
#         Paragraph(f"Role: {jobRole}", styles["Normal"]),
#         Paragraph(f"Region: {region}", styles["Normal"]),
#         Paragraph(f"Skills: {skills}", styles["Normal"]),
#         Paragraph(f"Years of Experience: {years}", styles["Normal"]),
#         Spacer(1, 12),
#         Paragraph(f"Current Salary: ${salary:,.2f}", styles["Normal"]),
#         Paragraph(f"After 1 Year: ${growth['year1']:,.2f}", styles["Normal"]),
#         Paragraph(f"After 2 Years: ${growth['year2']:,.2f}", styles["Normal"]),
#         Paragraph(f"After 3 Years: ${growth['year3']:,.2f}", styles["Normal"]),
#     ]

#     doc.build(story)
#     buffer.seek(0)

#     return send_file(
#         buffer,
#         as_attachment=True,
#         download_name="salary_report.pdf",
#         mimetype="application/pdf"
#     )

# # ------------------- Run -------------------
# if __name__ == "__main__":
#     app.run(port=5000, debug=False)







from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from my import SalaryPredictor
import uuid
import io
import os
import json

# ✅ ADDED
from pymongo import MongoClient
from dotenv import load_dotenv

# ---------------- ENV ----------------
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
NGROK_URL = os.getenv("NGROK_URL")

# ---------------- USER STORAGE (MONGO - MINIMAL CHANGE) ----------------
client = MongoClient(os.getenv("MONGO_URI"))
print(client.admin.command("ping"))   # <-- add only this line

db = client["AI_Salar_Predictor"]
users_col = db["users"]

# ❌ REMOVED users.json usage
# USERS_FILE = "users.json"

# ---------------- APP SETUP ----------------
app = Flask(__name__, static_folder="../front-end", static_url_path="")
CORS(app)

# 🔐 SECRET KEY
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# 📧 MAIL CONFIGURATION
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# ---------------- FRONTEND ROUTES ----------------
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/login-page")
def serve_login_page():
    return send_from_directory(app.static_folder, "login.html")

@app.route("/signup-page")
def serve_signup_page():
    return send_from_directory(app.static_folder, "signup.html")

# ---------------- AUTH ROUTES ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    # ✅ Mongo check instead of users.json
    if users_col.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    users_col.insert_one({
        "email": email,
        "password": password,
        "verified": False
    })

    token = serializer.dumps(email, salt="email-verify")
    # verify_link = f"{NGROK_URL}/verify/{token}"
    verify_link = f"{request.host_url}verify/{token}"
    
    try:
        msg = Message("Verify your account", recipients=[email])
        msg.body = f"""
Welcome!

Click the link below to verify your account:

{verify_link}

This link expires in 1 hour.
"""
        mail.send(msg)
    except Exception as e:
        print("EMAIL ERROR:", e)
        print("Manual verification link:", verify_link)
        return jsonify({"message": "Email sending failed"}), 500

    return jsonify({"message": "Verification email sent"}), 200


@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = serializer.loads(token, salt="email-verify", max_age=3600)

        # ✅ Mongo update
        result = users_col.update_one({"email": email}, {"$set": {"verified": True}})

        if result.matched_count == 0:
            return "<h2>User not found</h2>"

        return "<h2>Email verified ✅</h2><a href='/login-page'>Login</a>"

    except Exception:
        return "<h2>Invalid or expired link</h2>"


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    # ✅ Mongo lookup
    user = users_col.find_one({"email": email})

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user["password"] != password:
        return jsonify({"message": "Wrong password"}), 401

    if not user["verified"]:
        return jsonify({"message": "Verify email first"}), 403

    return jsonify({
        "token": str(uuid.uuid4()),
        "email": email
    }), 200

# ---------------- SALARY MODEL ----------------
predictor = SalaryPredictor()
predictor.load_saved_model("salary_predictor_model.pkl")

# ---------------- PPP + FX ----------------
PPP_FACTOR = {
    "United States": 1.0,
    "India": 0.32,
    "Germany": 1.05,
    "United Kingdom": 1.02,
    "Canada": 1.03,
    "Australia": 1.01,
    "Japan": 0.95,
    "France": 1.01,
    "China": 0.45,
    "Brazil": 0.55,
    "South Africa": 0.41,
    "Singapore": 1.12
}

DEFAULT_PPP = 0.75

EXCHANGE_RATE = {
    "United States": 1.0,
    "India": 83.0,
    "Germany": 0.92,
    "United Kingdom": 0.78,
    "Canada": 1.35,
    "Australia": 1.52,
    "Japan": 150.0,
    "France": 0.92,
    "China": 7.2,
    "Brazil": 5.0,
    "South Africa": 18.5,
    "Singapore": 1.35
}

CURRENCY_MAP = {
    "United States": {"symbol": "$", "code": "USD"},
    "India": {"symbol": "₹", "code": "INR"},
    "Germany": {"symbol": "€", "code": "EUR"},
    "United Kingdom": {"symbol": "£", "code": "GBP"},
    "Canada": {"symbol": "C$", "code": "CAD"},
    "Australia": {"symbol": "A$", "code": "AUD"},
    "Japan": {"symbol": "¥", "code": "JPY"},
    "France": {"symbol": "€", "code": "EUR"},
    "China": {"symbol": "¥", "code": "CNY"},
    "Brazil": {"symbol": "R$", "code": "BRL"},
    "South Africa": {"symbol": "R", "code": "ZAR"},
    "Singapore": {"symbol": "S$", "code": "SGD"}
}

DEFAULT_CURRENCY = {"symbol": "$", "code": "USD"}

ROLE_MULTIPLIER = {
    "frontend developer": 0.35,
    "backend developer": 0.6,
    "full stack developer": 0.7,
    "software engineer": 0.75,
    "data scientist": 1.0,
    "machine learning engineer": 1.1,
    "ai engineer": 1.15,
    "devops engineer": 0.9,
    "qa engineer": 0.4,
    "tester": 0.35,
    "intern": 0.2
}

def apply_ppp_and_fx(usd_salary, country):
    fx = EXCHANGE_RATE.get(country, 1)
    ppp = PPP_FACTOR.get(country, DEFAULT_PPP)
    nominal_usd = usd_salary
    ppp_adjusted_local = usd_salary * fx * ppp
    return round(nominal_usd, 2), round(ppp_adjusted_local, 2)

def growth_projection(current_salary):
    g1 = current_salary * 1.08
    g2 = g1 * 1.08
    g3 = g2 * 1.08
    return {"year1": round(g1, 2), "year2": round(g2, 2), "year3": round(g3, 2)}

@app.route("/predict-salary", methods=["POST"])
def predict_salary():
    data = request.json

    jobRole = data.get("jobRole", "")
    skills = data.get("skills", "")
    region = data.get("region", "")
    years = int(data.get("yearsOfExperience", 0))

    # ✅ ONLY NECESSARY VALIDATION ADDED
    if jobRole.lower().strip() not in ROLE_MULTIPLIER:
        return jsonify({"error": "Invalid job role. Please select a valid role."}), 400

    base_salary = predictor.predict_salary(
        job_title=jobRole,
        skills=skills,
        country=region,
        years_of_experience=years
    )

    role_key = jobRole.lower().strip()
    multiplier = ROLE_MULTIPLIER.get(role_key, 0.6)
    salary = base_salary * multiplier

    nominal_salary, ppp_salary = apply_ppp_and_fx(salary, region)
    currency = CURRENCY_MAP.get(region, DEFAULT_CURRENCY)

    return jsonify({
        "usdSalary": round(salary, 2),
        "nominalSalaryUSD": nominal_salary,
        "pppSalaryLocal": ppp_salary,
        "currency": currency
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)