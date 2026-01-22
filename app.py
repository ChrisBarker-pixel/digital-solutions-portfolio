from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, make_response
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configuration for JWT and Flash messages
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a strong, random key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here' # Change this to a strong, random key
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True # For forms that might send CSRF via form data
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Mock database for users and appointments
users = {
    "testuser": {"password": bcrypt.generate_password_hash("testpass").decode('utf-8'), "email": "test@example.com", "role": "user"},
    "admin": {"password": bcrypt.generate_password_hash("adminpass").decode('utf-8'), "email": "admin@example.com", "role": "admin"}
}

appointments = []
services = ["Consultation", "Therapy", "Check-up"]
available_dates = ["2024-03-01", "2024-03-02", "2024-03-03"]
available_times = ["09:00", "10:00", "11:00", "14:00"]

@app.route('/')
def index():
    return "Welcome to the Appointment Booking API!"

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            flash('Username already exists', 'danger')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users[username] = {"password": hashed_password, "email": email, "role": "user"}
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=username)
            flash('Login successful!', 'success')
            response = make_response(redirect(url_for('protected')))
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return render_template('protected.html', current_user=current_user)

# User logout route
@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    flash('You have been logged out.', 'info')
    return response

@app.route('/services', methods=['GET'])
@jwt_required()
def get_services():
    return jsonify(services), 200

@app.route('/dates', methods=['GET'])
@jwt_required()
def get_dates():
    return jsonify(available_dates), 200

@app.route('/times', methods=['GET'])
@jwt_required()
def get_times():
    return jsonify(available_times), 200

@app.route('/appointments', methods=['GET', 'POST'])
@jwt_required()
def appointments_handler():
    current_user = get_jwt_identity()

    if request.method == 'POST':
        data = request.get_json()
        service = data.get('service')
        date = data.get('date')
        time = data.get('time')

        if not all([service, date, time]):
            return jsonify({"msg": "Missing appointment details"}), 400

        if service not in services:
            return jsonify({"msg": "Invalid service"}), 400
        if date not in available_dates:
            return jsonify({"msg": "Invalid date"}), 400
        if time not in available_times:
            return jsonify({"msg": "Invalid time"}), 400

        appointment = {"user": current_user, "service": service, "date": date, "time": time}
        appointments.append(appointment)
        return jsonify({"msg": "Appointment booked successfully", "appointment": appointment}), 201
    else: # GET request
        user_appointments = [app for app in appointments if app["user"] == current_user]
        return jsonify(user_appointments), 200

if __name__ == '__main__':
    app.run(debug=True)