# Importing necessary modules and libraries
from datetime import datetime  # For working with dates and times
from flask import Flask, render_template, request, \
    flash  # Flask framework components for app, templates, and form handling
from flask_sqlalchemy import SQLAlchemy  # For database integration with SQLAlchemy ORM
from flask_mail import Mail, Message  # For sending emails through Flask
import os  # For accessing environment variables

# Creating the Flask application instance
app = Flask(__name__)

# Configuring the application settings
app.config["SECRET_KEY"] = "myapplication123"  # Secret key for secure session management
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # Database URI for SQLite
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Mail server configuration
app.config["MAIL_PORT"] = 465  # Port number for secure SMTP
app.config["MAIL_USE_SSL"] = True  # Using SSL for secure email transmission
app.config["MAIL_USERNAME"] = os.getenv("FORM_EMAIL")  # Email username from environment variable
app.config["MAIL_PASSWORD"] = os.getenv("FORM_PASSWORD")  # Email password from environment variable

# Initializing SQLAlchemy for database management
db = SQLAlchemy(app)

# Initializing Flask-Mail for email functionality
mail = Mail(app)


# Defining the database model for form submissions
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key field
    first_name = db.Column(db.String(80))  # First name of the user
    last_name = db.Column(db.String(80))  # Last name of the user
    email = db.Column(db.String(80))  # Email of the user
    date = db.Column(db.Date)  # Date of the form submission
    occupation = db.Column(db.String(80))  # Occupation of the user


# Defining the route for the homepage, supporting GET and POST methods
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":  # If the form is submitted
        # Retrieving form data from the request
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Parsing the date into a datetime object
        occupation = request.form["occupation"]

        # Creating a new Form object with the submitted data
        form = Form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=date_obj,
            occupation=occupation
        )

        # Adding the new form entry to the database
        db.session.add(form)
        db.session.commit()

        # Composing the email body
        message_body = f"Thank you for your submission {first_name}." \
                       f"Here is your data: \n{first_name}\n{last_name}\n{date}\n"

        # Creating the email message
        message = Message(
            subject='New Form Submission',  # Email subject
            sender=app.config["MAIL_USERNAME"],  # Sender email address
            recipients=[email],  # Recipient email address
            body=message_body  # Email body content
        )

        # Sending the email
        mail.send(message)

        # Flashing a success message to the user
        flash(f"{first_name}, Your form was submitted successfully!", "success")

    # Rendering the index.html template for GET and POST requests
    return render_template("index.html")


# Running the application
if __name__ == "__main__":
    with app.app_context():  # Ensuring the app context is available
        db.create_all()  # Creating all database tables
        app.run(debug=True, port=5001)  # Running the app in debug mode on port 5001
