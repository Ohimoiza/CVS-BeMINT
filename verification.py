from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email_username'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_default_email_sender'

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

@app.route('/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Generate a token using the email and secret key
        token = serializer.dumps(form.email.data, salt='email-confirm')

        # Create a confirmation link
        confirmation_link = url_for('confirm_email', token=token, _external=True)

        # Prepare the email message
        subject = 'Email Confirmation'
        message = f'Please click the following link to confirm your email: {confirmation_link}'
        recipients = [form.email.data]
        
        # Send the email
        send_email(subject, message, recipients)

        flash('A confirmation email has been sent. Please check your inbox.', 'success')
        return redirect(url_for('signup'))

    return render_template('signup.html', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        # Verify the token and extract the email
        email = serializer.loads(token, salt='email-confirm', max_age=3600)

        # Perform the necessary actions to mark the email as verified
        # e.g., update the user's database record

        flash('Email verification successful!', 'success')
    except SignatureExpired:
        flash('The email verification link has expired.', 'danger')

    return redirect(url_for('signup'))

def send_email(subject, message, recipients):
    msg = Message(subject, recipients=recipients)
    msg.body = message
    mail.send(msg)

if __name__ == '__main__':
    app.run()
