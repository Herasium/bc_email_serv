from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    # Parse the incoming JSON data
    data = request.json
    key = data.get('key')
    if key != os.environ["key"]:
        return jsonify({"error": "Invalid key"}), 403
    email_address = data.get('email')
    login_address = data.get('login')
    password = data.get('password')
    message_data = data.get('data')
    message_subject = data.get('subject')
    destination_address = data.get('destination')

    if not email_address or not password or not message_data or not destination_address or not login_address or not message_subject:
        return jsonify({"error": "Missing required parameters"}), 400

    # Prepare the email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = destination_address
    msg['Subject'] = message_subject
    msg.attach(MIMEText(message_data, 'html'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(login_address, password)
        text = msg.as_string()
        server.sendmail(email_address, destination_address, text)
        server.quit()
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
