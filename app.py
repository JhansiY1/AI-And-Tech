from flask import Flask, render_template, request, redirect, url_for, flash, session
import random
import smtplib
import psycopg2
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key for session

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))  # Use the PostgreSQL URL from Render
    conn.autocommit = True
    return conn

# Send OTP via email
def send_otp_to_email(email, otp):
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")  # Replace with environment variable for security
    sender_password = os.getenv("SENDER_PASSWORD")  # Replace with environment variable for security
    msg = MIMEText(f"Your OTP code is {otp}")
    msg["Subject"] = "Newsletter Subscription OTP"
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
    except Exception as e:
        flash("Error sending OTP email")
        return False
    return True


# Homepage route
@app.route('/')
def home():
    return render_template('index.html')


# Route to render signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')


# Route to handle the subscription process
@app.route('/subscribe', methods=['POST'])
def subscribe():
    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the email already exists in the database
    cursor.execute('SELECT * FROM subscribers WHERE email = %s', (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        # If the email already exists, notify the user and do not send OTP
        flash('Account already exists.')
        conn.close()
        return redirect(url_for('signup'))  # Do not send OTP or proceed with subscription

    # If the email does not exist, proceed with new subscription
    otp = str(random.randint(100000, 999999))

    # Send OTP to the user's email
    if not send_otp_to_email(email, otp):
        conn.close()
        return redirect(url_for('signup'))

    # Store the OTP temporarily in the session, no database storage yet
    session['otp'] = otp
    session['email'] = email
    session['name'] = name

    flash('A 6-digit OTP has been sent to your email. Please verify it below.')
    return render_template('verify.html', email=email)


# Route to verify OTP
@app.route('/verify', methods=['POST'])
def verify():
    email = request.form.get('email')  # Safely get email
    entered_otp = request.form.get('otp')  # Safely get OTP

    if not email or not entered_otp:
        flash('Invalid data submitted. Please try again.')
        return redirect(url_for('signup'))

    # Check if the OTP entered matches the one stored in the session
    if entered_otp == session.get('otp'):
        # OTP is correct, store data in the database
        name = session.get('name', '')  # Get name from session
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the email, OTP (which will be cleared), and name into the database
        cursor.execute('INSERT INTO subscribers (name, email, otp) VALUES (%s, %s, %s)', (name, email, session.get('otp')))
        conn.commit()
        conn.close()

        # Clear the session after successful verification
        session.pop('otp', None)
        session.pop('email', None)
        session.pop('name', None)

        flash('Thank you for subscribing! Your subscription is now confirmed.')
        return redirect(url_for('home'))  # Redirect to homepage after successful verification

    else:
        # OTP is incorrect, do not insert/update any data
        flash('OTP is incorrect. Please try again.')
        return redirect(url_for('signup'))  # Redirect back to sign-up page


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
