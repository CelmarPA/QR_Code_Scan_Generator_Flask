from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, url_for, redirect, flash
import os
from qr_code import GenerateQRCode
from datetime import date
import smtplib
from werkzeug.utils import secure_filename

# Create the Flask application instance
app = Flask(__name__)

# Configuration for uploading files (used in QR scanning)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.secret_key = os.urandom(24)     # Secret key for sessions and flash messages

# Store the current year to dynamically show in the footer or template
current_year = date.today().year

# Email configuration (should ideally be stored securely, not hardcoded)
MY_EMAIL = "<YOUR EMAIL>"             # Put your email here
PASSWORD = "<YOUR PASSWORD>"          # Password

# Ensure the upload folder exists to avoid runtime errors
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok = True)


@app.route("/")
def home():
    """
    Renders the homepage with the current year.
    This view is also used as a response after form submissions with flash messages.
    """

    return render_template("index.html", year = current_year)


@app.route("/generate", methods=["GET", "POST"])
def generate():
    """
    Handles QR code generation from input text.

    On POST: Accepts form data, generates QR code using `GenerateQRCode` class,
    and returns base64 image to be rendered in the template.
    """

    qr_code_url = None  # Stores base64-encoded QR code image for display

    if request.method == "POST":
        text = request.form.get("qr_text")

        if text:
            # Instantiate and use custom QR code generator class
            generator = GenerateQRCode()
            generator.generate_qr_code(text)

            # Get the QR code image as a base64-encoded data URI
            qr_code_url = generator.get_base64_img()

    return render_template("index.html", qr_code_url=qr_code_url)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    """
    Handles QR code scanning from an uploaded image.

    On POST: Validates uploaded file, saves it, uses OpenCV to scan for QR code,
    and returns decoded result and preview image to the template.
    """

    scan_result = None           # Stores decoded QR data
    scan_image_url = None        # Stores the uploaded image URL to show preview

    if request.method == 'POST':
        if 'image' not in request.files:
            scan_result = "No file part"
            return render_template('index.html', scan_result=scan_result)

        file = request.files['image']
        if file.filename == '':
            scan_result = "No selected file"
            return render_template('index.html', scan_result=scan_result)

        if file:
            # Secure the filename and save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Use the QR code reader method from GenerateQRCode class
            scan_result = GenerateQRCode.scan_qr_code(filepath)
            scan_image_url = url_for('static', filename='uploads/' + filename)

    # Re-render home page with scan result and image preview
    return render_template('index.html', scan_result=scan_result, scan_image_url=scan_image_url, section='scan')


@app.route("/send_message", methods = ["POST"])
def send_message():
    """
    Sends a contact form message via email using SMTP (Gmail).

    Accepts name, email, subject, and message fields from the form,
    constructs an email, and sends it to a predefined recipient.
    Uses flash to display success or error feedback.
    """

    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    msg_text = request.form.get("message")

    # Construct the email message
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = "<YOUR EMAIL>"  # Replace with your email
    msg["Subject"] = f"{subject}"

    # Compose the email body
    body = f"""
    Name: {name}
    Email: {email}
    
    Message:
        {msg_text}
    """

    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()   # Makes the connection secure
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=email,
                                to_addrs="<YOUR EMAIL>",  # Replace with your email
                                msg=msg.as_string())

        flash("Message sent successfully!")     # Success feedback

    except Exception as e:
        flash(f"Error sending email: {e}")      # Error feedback

    # Redirect back to homepage and anchor to contact section
    return redirect(url_for('home') + '#contact')


if __name__ == "__main__":
    # Start the Flask development server
    app.run(debug = True)
