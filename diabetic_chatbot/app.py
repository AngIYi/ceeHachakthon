from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
import time
from qa_database import qa_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)

# Define global dictionaries to track connected users and agents
connected_users = {}  # Format: {socket_id: username}
connected_agents = {}  # Format: {socket_id: username}

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'agent'
    marks = db.Column(db.Integer, default=0)

# Load a user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Save Marks Endpoint
@app.route('/save_marks', methods=['POST'])
@login_required
def save_marks():
    marks = request.json.get('marks')
    current_user.marks = marks
    db.session.commit()
    return jsonify({"status": "success", "marks": marks})

# Get Marks Endpoint
@app.route('/get_marks', methods=['GET'])
@login_required
def get_marks():
    return jsonify({"marks": current_user.marks})

# Simulated pending messages
pending_messages = {}  # Format: {username: [message1, message2, ...]}




class DiabeticChatbot:
    def __init__(self):
        self.diabetic_responses = qa_database
        self.default_response = "You are connected to our DIA Guide Assistant."
        self.quiz_questions = [
            {
                "Question": "What is a common symptom of diabetes?",
                "Options": ["Fever", "Blurred vision", "Cough", "Headache"],
                "Answer": "Blurred vision"
            },
            {
                "Question": "Which food should be avoided to prevent diabetes?",
                "Options": ["Vegetables", "Sugar", "Whole grains", "Nuts"],
                "Answer": "Sugar"
            },
            {
                "Question": "How much exercise is recommended per week to prevent diabetes?",
                "Options": ["30 minutes", "60 minutes", "90 minutes", "150 minutes"],
                "Answer": "150 minutes"
            }
        ]

    def get_response(self, choice):
        if choice.lower() in [key.lower() for key in self.diabetic_responses.keys()]:
            correct_key = next(key for key in self.diabetic_responses.keys() if key.lower() == choice.lower())
            return self.diabetic_responses[correct_key]
        elif choice == "Real Person Assistant":
            return "other"
        elif choice == "Quiz":
            return "quiz"
        else:
            return "Invalid choice. Please try again."

    def get_quiz_question(self, index):
        if 0 <= index < len(self.quiz_questions):
            return self.quiz_questions[index]
        return None

    def check_quiz_answer(self, index, user_answer):
        question = self.get_quiz_question(index)
        if question and user_answer == question["Answer"]:
            return "Correct! 🎉"
        return "Incorrect. 😢 The correct answer is: " + question["Answer"]

chatbot = DiabeticChatbot()

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # In production, use password hashing!
            login_user(user)
            print(f"User {user.username} logged in with role: {user.role}")  # Debugging
            if user.role == "agent":
                return redirect(url_for("agent"))  # Redirect agents to the agent interface
            else:
                return redirect(url_for("home"))  # Redirect users to the home page
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")

# Logout route
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def home():
    if current_user.role == "agent":
        return redirect(url_for("agent"))
    return render_template("chatbot.html", current_user=current_user)

@app.route("/agent")
@login_required
def agent():
    if current_user.role != "agent":
        return redirect(url_for("home"))
    return render_template("agent.html")

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    print("Received request:", request.json)
    user_input = request.json["message"]
    print("User input:", user_input)  # Debugging: Print the user input
    response = chatbot.get_response(user_input)
    print("Response:", response)  # Debugging: Print the response
    if response == "other":
        time.sleep(2)
        return jsonify({"response": chatbot.default_response, "redirect": True})
    else:
        return jsonify({"response": response, "redirect": False})

# Socket.IO event handlers
@socketio.on('connect')
@login_required
def handle_connect():
    username = current_user.username
    user_type = current_user.role

    if user_type == "user":
        connected_users[request.sid] = username
        print(f"User {username} connected with socket ID: {request.sid}")
    elif user_type == "agent":
        connected_agents[request.sid] = username
        print(f"Agent {username} connected with socket ID: {request.sid}")

        # Deliver pending messages to the agent when they come online
        if username in pending_messages:
            for message in pending_messages[username]:
                emit('agent_message', {'user_id': username, 'message': message}, room=request.sid)
            del pending_messages[username]  # Clear pending messages after delivering

def handle_custom_question(self, question):
    # Convert the question to lowercase for case-insensitive matching
    question_lower = question.lower()

    # Tokenize the question into words
    words = question_lower.split()

    # Find all matching keywords in the question
    matching_keywords = [keyword for keyword in self.diabetic_responses if any(word in keyword.lower() for word in words)]

    # If no keywords are found, return a default response
    if not matching_keywords:
        return "I'm sorry, I don't have an answer for that question. Please try asking something else."

    # If multiple keywords are found, return all corresponding answers
    if len(matching_keywords) > 1:
        response = "Here are the answers to your questions:\n\n"
        for keyword in matching_keywords:
            response += f"**{keyword.capitalize()}:** {self.diabetic_responses[keyword]}\n\n"
        return response.strip()  # Remove the trailing newline

        # If only one keyword is found, return its corresponding answer
    return self.diabetic_responses[matching_keywords[0]]

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in connected_users:
        username = connected_users[request.sid]
        print(f"User {username} disconnected")
        del connected_users[request.sid]
    elif request.sid in connected_agents:
        username = connected_agents[request.sid]
        print(f"Agent {username} disconnected")
        del connected_agents[request.sid]

@socketio.on('user_message')
@login_required
def handle_user_message(data):
    username = current_user.username
    message = data['message']
    print(f"User {username} sent: {message}")

    if not connected_agents:  # If no agents are online
        # Store the message temporarily
        if username not in pending_messages:
            pending_messages[username] = []
        pending_messages[username].append(message)
        print(f"Message stored for user {username}: {message}")
    else:
        # Broadcast the message to all agents
        for agent_sid in connected_agents:
            emit('agent_message', {'user_id': username, 'message': message}, room=agent_sid)
            print(f"Sent to agent {connected_agents[agent_sid]}")

@socketio.on('agent_message')
@login_required
def handle_agent_message(data):
    user_id = data['user_id']
    message = data['message']
    print(f"Agent replied to user {user_id}: {message}")

    # Send the message to the specific user
    for user_sid, username in connected_users.items():
        if username == user_id:
            emit('user_message', {'message': message}, room=user_sid)
            print(f"Sent to user {username}")

@app.route('/quiz', methods=['POST'])
@login_required
def quiz():
    user_answer = request.json.get('answer')
    question_index = request.json.get('question_index')
    # Logic to check answer and update marks
    question = chatbot.get_quiz_question(question_index)
    if question and user_answer == question["Answer"]:
        current_user.marks += 1
        db.session.commit()
    return jsonify({"status": "success", "marks": current_user.marks})

# Create the database and tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)