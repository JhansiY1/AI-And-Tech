from flask import Flask, render_template, request, redirect, url_for, flash
import random
import smtplib
import psycopg2
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key for session


# Database connection function
def get_db_connection():
    # Fetch the DATABASE_URL from environment variable
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

    # If the email exists, send a new OTP instead of inserting into the database
    if existing_user:
        # Generate a new OTP
        otp = str(random.randint(100000, 999999))

        # Send OTP to the user's email
        if not send_otp_to_email(email, otp):
            conn.close()
            return redirect(url_for('signup'))

        # Update OTP for existing email
        cursor.execute('UPDATE subscribers SET otp = %s WHERE email = %s', (otp, email))
        conn.commit()
        conn.close()

        flash('A 6-digit OTP has been sent to your email. Please verify it below.')
        return render_template('verify.html', email=email)

    # If the email does not exist, proceed with new subscription
    otp = str(random.randint(100000, 999999))

    # Send OTP to the user's email
    if not send_otp_to_email(email, otp):
        conn.close()
        return redirect(url_for('signup'))

    # Insert the email and OTP into the database (without name)
    cursor.execute('INSERT INTO subscribers (name, email, otp) VALUES (%s, %s, %s)', ("Unknown", email, otp))
    conn.commit()
    conn.close()

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

    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the OTP stored in the database for the given email
    cursor.execute('SELECT otp FROM subscribers WHERE email = %s', (email,))
    subscriber = cursor.fetchone()

    if subscriber and subscriber[0] == entered_otp:
        # OTP is correct
        name = request.form.get('name', '')  # Get name, default to an empty string if not provided
        cursor.execute('UPDATE subscribers SET name = %s, otp = NULL WHERE email = %s', (name, email))
        conn.commit()
        conn.close()
        flash('Thank you for subscribing! Your subscription is now confirmed.')
        return redirect(url_for('home'))  # Redirect to homepage after successful verification
    else:
        # OTP is incorrect
        flash('OTP does not match. Please try again.')
        conn.close()
        return redirect(url_for('signup'))  # Redirect back to sign up for re-entry

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
