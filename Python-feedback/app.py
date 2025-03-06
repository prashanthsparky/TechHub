from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pandas as pd
from io import BytesIO
from collections import Counter
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session handling
bcrypt = Bcrypt(app)

# Email Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "iamprashanthb05@gmail.com"  
app.config["MAIL_PASSWORD"] = "ljvt wxit nfzw nujk" 
app.config["MAIL_DEFAULT_SENDER"] = "iamprashanthb05@gmail.com"

mail = Mail(app)

# Secret Key for Token Generation
app.config["SECRET_KEY"] = "your_secret_key"
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["feedbackDB"]
users_collection = db["users"]
feedback_collection = db["feedback"]
questions_collection = db["questions"]

# Constants for user roles
ROLE_STUDENT = "student"
ROLE_FACULTY = "faculty"

# User class to work with Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# This will be used to load the user from the database
@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(str(user_data["_id"]), user_data["username"], user_data["role"])
    return None

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        role = request.form["role"]

        # Check if the username already exists
        if users_collection.find_one({"username": username}):
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("signup"))

        users_collection.insert_one({"username": username, "password": password, "role": role})
        flash("Signup successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("signup.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username})

        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(str(user["_id"]), user["username"], user["role"])
            login_user(user_obj)
            session["username"] = user["username"]
            session["role"] = user["role"]
            if user["role"] == ROLE_STUDENT:
                return redirect(url_for("student_dashboard"))
            elif user["role"] == ROLE_FACULTY:
                # Redirect to faculty's home page (faculty.html)
                return redirect(url_for("faculty_home"))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for("login"))
    return render_template("login.html")

# Forgot Password Route
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = users_collection.find_one({"username": email})  

        if user:
            token = serializer.dumps(email, salt="password-reset-salt")
            reset_link = url_for("reset_password", token=token, _external=True)

            # Send Reset Email
            msg = Message("Password Reset Request", recipients=[email])
            msg.body = f"Click the link to reset your password: {reset_link}"
            mail.send(msg)

            flash("A password reset link has been sent to your email.", "success")
        else:
            flash("No account found with this email.", "danger")

        return redirect(url_for("forgot_password"))

    return render_template("forgot_password.html")


# Reset Password Route
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=600)  # 10 min expiry
    except:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        new_password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        users_collection.update_one({"username": email}, {"$set": {"password": hashed_password}})

        flash("Your password has been reset successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)

# Faculty Home Page (Landing page after login)
@app.route("/faculty/home", methods=["GET", "POST"])
@login_required
def faculty_home():
    if session.get("role") != ROLE_FACULTY:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        action = request.form["action"]
        question_text = request.form["question"]
        
        if action == "add":
            questions_collection.insert_one({"faculty": session["username"], "question": question_text})
            flash("Question added successfully.")
        
        elif action == "update":
            new_question = request.form["new_question"]
            questions_collection.update_one(
                {"faculty": session["username"], "question": question_text},
                {"$set": {"question": new_question}}
            )
            flash("Question updated successfully.")
        
        elif action == "delete":
            questions_collection.delete_one({"faculty": session["username"], "question": question_text})
            flash("Question deleted successfully.")

        # Redirect to faculty home to stay on the same page
        return redirect(url_for('faculty_home'))  # Keep user on the same page after submission

    # Fetch questions for the logged-in faculty
    questions = questions_collection.find({"faculty": session["username"]})
    return render_template("faculty.html", questions=questions)


# Faculty Dashboard (Manage Feedback Questions and View Feedback Responses)
@app.route('/faculty/dashboard', methods=['GET', 'POST'])
@login_required
def faculty_dashboard():
    if session.get("role") != ROLE_FACULTY:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        action = request.form["action"]
        question_text = request.form["question"]
        
        if action == "add":
            questions_collection.insert_one({"faculty": session["username"], "question": question_text})
            flash("Question added successfully.")
        
        elif action == "update":
            new_question = request.form["new_question"]
            questions_collection.update_one(
                {"faculty": session["username"], "question": question_text},
                {"$set": {"question": new_question}}
            )
            flash("Question updated successfully.")
        
        elif action == "delete":
            questions_collection.delete_one({"faculty": session["username"], "question": question_text})
            flash("Question deleted successfully.")

    questions = questions_collection.find({"faculty": session["username"]})
    feedback_data = get_feedback_analysis()  # Fetch feedback data for the faculty
    
    return render_template("faculty_dashboard.html", questions=questions, feedback_data=feedback_data)

# Faculty Feedback Analysis (Helper function)
def get_feedback_analysis():
    feedback_data = feedback_collection.find({"faculty": session["username"]})
    positive_feedback = []
    negative_feedback = []
    avg_ratings = []
    comments = []
    
    for feedback in feedback_data:
        responses = feedback["responses"]
        avg_rating = sum(response["rating"] for response in responses) / len(responses) if responses else 0
        feedback_analysis = {
            "student": feedback["student"],
            "responses": responses,
            "avg_rating": avg_rating,
            "comment": feedback.get("comment", ""),
            "submitted_at": feedback["submitted_at"]
        }
        
        avg_ratings.append(avg_rating)
        comments.append(feedback.get("comment", ""))
        
        if avg_rating >= 4:
            positive_feedback.append(feedback_analysis)
        else:
            negative_feedback.append(feedback_analysis)
    
    # Calculate the count of positive and negative feedback
    positive_count = len(positive_feedback)
    negative_count = len(negative_feedback)
    total_count = positive_count + negative_count

    # Calculate the average rating
    avg_rating = sum(avg_ratings) / len(avg_ratings) if avg_ratings else 0

    # Feedback analysis for charts
    feedback_analysis = {
        "positive_feedback": positive_feedback,
        "negative_feedback": negative_feedback,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "avg_rating": avg_rating,
        "comments": comments
    }
    
    return feedback_analysis


# Student Dashboard (Feedback Page)
@app.route("/student", methods=["GET", "POST"])
def student_dashboard():
    if session.get("role") != ROLE_STUDENT:
        return redirect(url_for("login"))
    
    faculties = [f["username"] for f in users_collection.find({"role": ROLE_FACULTY})]
    selected_faculty = request.args.get("faculty")
    questions = []

    if selected_faculty:
        # Retrieve questions for the selected faculty
        questions = list(questions_collection.find({"faculty": selected_faculty}))

    if request.method == "POST":
        faculty = request.form["faculty"]
        responses = []
        comment = request.form.get("comments", "")  # Capturing the comment

        # Loop over each question and get the selected rating
        for key, value in request.form.items():
            if key.startswith("response-"):
                question_id = key.split("-")[1]
                question = questions_collection.find_one({"_id": ObjectId(question_id)})
                responses.append({
                    "question": question["question"],
                    "rating": int(value)
                })

        # Insert the feedback into the "feedback" collection
        feedback_collection.insert_one({
            "student": session["username"],
            "faculty": faculty,
            "responses": responses,
            "comment": comment,  # Storing the comment
            "submitted_at": datetime.utcnow()
        })

        return render_template("thankyou.html")  # Redirect to thank you page

    return render_template("student.html", faculties=faculties, questions=questions, selected_faculty=selected_faculty)

# Download Feedback (Excel File)
@app.route('/download_feedback', methods=['GET'])
@login_required
def download_feedback():
    feedback_data = get_feedback_data()  # Fetch feedback data
    return generate_excel(feedback_data)

def get_feedback_data():
    feedback_data = feedback_collection.find({"faculty": session["username"]})
    feedback_list = []
    
    for feedback in feedback_data:
        for response in feedback["responses"]:
            feedback_list.append({
                "student": feedback["student"],
                "question": response["question"],
                "rating": response["rating"],
                "comment": feedback.get("comment", ""),
                "submitted_at": feedback["submitted_at"]
            })
    
    return feedback_list

def generate_excel(feedback_data):
    df = pd.DataFrame(feedback_data)  # Create DataFrame from feedback data
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="feedback.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Thank You Page After Feedback Submission
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# Logout Route
@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
