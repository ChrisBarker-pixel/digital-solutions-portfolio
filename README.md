# Flask Appointment Booking Application Documentation

This document provides comprehensive documentation for the Flask-based appointment booking application, covering its features, API endpoints, setup process, and usage instructions.

## 1. Application Functionality

The Flask Appointment Booking Application provides a secure platform for users to manage their appointments for various services. Key functionalities include:

*   **User Authentication**: Secure user registration and login using username/password combinations, with password hashing for security (`flask-bcrypt`) and JWT for session management (`flask-jwt-extended`). Users can register for new accounts and log in to access protected resources.
*   **Protected Resources**: Access to core application features, such as viewing services, dates, times, and managing appointments, requires a valid user session. Unauthenticated users are redirected to the login page.
*   **Service Management**: The application allows users to view a predefined list of available services.
*   **Date and Time Management**: Users can browse predefined available dates and times for booking appointments.
*   **Appointment Booking**: Authenticated users can book appointments by selecting a service, date, and time. The system stores these appointments associated with the user.
*   **Appointment Viewing**: Users can view a list of their previously booked appointments.
*   **Session Management**: Includes features for logging out, which clears the user's session.

## 2. API Endpoints

The application exposes several API endpoints for managing users and appointments. All protected endpoints require a valid JWT (JSON Web Token) in session cookies.

### Authentication and User Management

*   **`/`**
    *   **Method**: `GET`
    *   **Description**: Root endpoint, returns a welcome message.
    *   **Response**: `"Welcome to the Appointment Booking API!"`

*   **`/register`**
    *   **Method**: `GET`, `POST`
    *   **Description**: Handles user registration. `GET` displays the registration form. `POST` processes new user creation.
    *   **Request Body (POST)**:
        *   `username` (string, required): Unique username.
        *   `email` (string, required): User's email address.
        *   `password` (string, required): User's password.
    *   **Response**: On successful `POST`, redirects to `/login` with a success flash message. On `GET` or failed `POST`, renders `register.html`.

*   **`/login`**
    *   **Method**: `GET`, `POST`
    *   **Description**: Handles user login. `GET` displays the login form. `POST` authenticates the user and sets JWT cookies.
    *   **Request Body (POST)**:
        *   `username` (string, required): User's username.
        *   `password` (string, required): User's password.
    *   **Response**: On successful `POST`, redirects to `/protected` and sets access cookies. On `GET` or failed `POST`, renders `login.html`.

*   **`/logout`**
    *   **Method**: `POST`
    *   **Description**: Logs out the current user by unsetting JWT cookies.
    *   **Response**: Redirects to `/login` with a logout success flash message.

### Protected Application Endpoints

*   **`/protected`**
    *   **Method**: `GET`
    *   **Description**: A protected route accessible only by authenticated users. Displays the logged-in user's name and provides interfaces for services, dates, times, and appointments.
    *   **Authentication**: Requires JWT access token.
    *   **Response**: Renders `protected.html` with `current_user` context.

*   **`/services`**
    *   **Method**: `GET`
    *   **Description**: Returns a list of available services.
    *   **Authentication**: Requires JWT access token.
    *   **Response**: `JSON` array of strings, e.g., `["Consultation", "Therapy", "Check-up"]`

*   **`/dates`**
    *   **Method**: `GET`
    *   **Description**: Returns a list of available booking dates.
    *   **Authentication**: Requires JWT access token.
    *   **Response**: `JSON` array of strings, e.g., `["2024-03-01", "2024-03-02", "2024-03-03"]`

*   **`/times`**
    *   **Method**: `GET`
    *   **Description**: Returns a list of available booking times.
    *   **Authentication**: Requires JWT access token.
    *   **Response**: `JSON` array of strings, e.g., `["09:00", "10:00", "11:00", "14:00"]`

*   **`/appointments`**
    *   **Method**: `GET`, `POST`
    *   **Description**: `GET` retrieves the current user's appointments. `POST` creates a new appointment.
    *   **Authentication**: Requires JWT access token.
    *   **Request Body (POST)**:
        *   `service` (string, required): The chosen service from `/services`.
        *   `date` (string, required): The chosen date from `/dates`.
        *   `time` (string, required): The chosen time from `/times`.
    *   **Response (GET)**: `JSON` array of appointment objects, e.g., `[{ "user": "testuser", "service": "Consultation", "date": "2024-03-01", "time": "09:00" }]`.
    *   **Response (POST)**: `JSON` object confirming booking, e.g., `{ "msg": "Appointment booked successfully", "appointment": {...} }` or error message.

## 3. Setup Instructions

To set up and run the Flask Appointment Booking Application, follow these steps:

### 3.1. Directory Structure

Ensure your project has the following directory structure:

```
/content/AI_Council_Projects/appointment_booking_app/
├── app.py
├── run.py
└── templates/
    ├── register.html
    ├── login.html
    └── protected.html
```

### 3.2. Dependency Installation

The application requires several Python packages. Install them using `pip`:

```bash
pip install pyngrok flask-bcrypt flask-jwt-extended flask-cors flask groq openai requests
```

### 3.3. Environment Variable Configuration

**NGROK_AUTH_TOKEN**: The application uses `ngrok` to expose the Flask server to the internet. You must provide your `NGROK_AUTH_TOKEN`. In a Colab environment, it is recommended to store this token in Colab secrets.

*   Open the "Secrets" tab (key icon) on the left sidebar in Google Colab.
*   Add a new secret with the key `NGROK_AUTH_TOKEN` and your ngrok authtoken as the value.
*   Ensure "Notebook access" is toggled on for this secret.

### 3.4. `app.py` Content

The `app.py` file contains the core Flask application logic. The content has been provided in a previous step and saved to /content/AI_Council_Projects/appointment_booking_app/app.py. Key configurations within `app.py` include:

*   `SECRET_KEY`: A secret key for Flask sessions and message flashing.
*   `JWT_SECRET_KEY`: A secret key for signing JWTs.
*   `JWT_TOKEN_LOCATION`: Configured to use cookies.
*   `JWT_COOKIE_CSRF_PROTECT`: Enabled for CSRF protection with JWT cookies.
*   Mock databases for `users`, `appointments`, `services`, `available_dates`, and `available_times` are defined for demonstration purposes.

### 3.5. `run.py` Content

The `run.py` file is the entry point for running the Flask application. It ensures the project directory is added to the Python path and runs `app.py` on a specified port. The content has been provided in a previous step and saved to /content/AI_Council_Projects/appointment_booking_app/run.py. It is configured to run on `0.0.0.0:5000` with debug mode enabled.

### 3.6. HTML Templates

*   **`register.html`**: Located at /content/AI_Council_Projects/appointment_booking_app/templates/register.html, this template provides the user interface for new user registration.
*   **`login.html`**: Located at /content/AI_Council_Projects/appointment_booking_app/templates/login.html, this template provides the user interface for existing user login.
*   **`protected.html`**: Located at /content/AI_Council_Projects/appointment_booking_app/templates/protected.html, this template is the main dashboard for authenticated users, displaying their username, available services, dates, times, and a form to book and view appointments.

## 4. Usage Guidelines

To interact with the Flask Appointment Booking Application via its web interface:

1.  **Access the Application**: Once the `run.py` script is executed and the ngrok tunnel is established, access the application through the `public_url` provided by ngrok (e.g., `https://xxxxxx.ngrok-free.dev`).

2.  **Register a New User**:
    *   Navigate to the `/register` endpoint (or click the "Register here" link on the login page).
    *   Fill in the `Username`, `Email`, and `Password` fields.
    *   Click the "Register" button.
    *   Upon successful registration, you will be redirected to the login page with a success message.

3.  **Log In**:
    *   Navigate to the `/login` endpoint (or click the "Login here" link on the register page).
    *   Enter your registered `Username` and `Password`.
    *   Click the "Login" button.
    *   If successful, you will be redirected to the `/protected` page.

4.  **Explore the Protected Page**:
    *   On the `/protected` page, you will see a welcome message with your username.
    *   Lists of "Available Services", "Available Dates", and "Available Times" will be displayed.

5.  **Book an Appointment**:
    *   On the `/protected` page, locate the "Book New Appointment" form.
    *   Select a `Service`, `Date`, and `Time` from the dropdown menus.
    *   Click the "Book Appointment" button. An alert will confirm the booking.

6.  **View Your Appointments**:
    *   After booking, your new appointment will appear under the "Your Appointments" section on the `/protected` page.

7.  **Log Out**:
    *   On the `/protected` page, click the "Logout" button.
    *   You will be logged out and redirected back to the `/login` page with a logout confirmation message.
