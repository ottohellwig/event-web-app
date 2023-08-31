from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, HiddenField, IntegerField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp, ValidationError
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

# Event creation form
class EventForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Name', validators=[InputRequired()], render_kw={'placeholder': 'Enter the name of the event'})
    location = StringField('Location', validators=[InputRequired()], render_kw={'placeholder': 'Enter the location of the event'})
    genre = StringField('Genre', validators=[InputRequired()], render_kw={'placeholder': 'Enter the genre of the event'})
    artist = StringField('Artist', validators=[InputRequired()], render_kw={'placeholder': 'Enter the artist of the event'})
    date = StringField('Date', validators=[InputRequired()], render_kw={'placeholder': 'Date must be inputted as dd-mm-YYYY (e.g. 09-06-2023)'})
    
    def validate_date(self, field):
        date_str = field.data
        try:
            datetime.strptime(date_str, '%d-%m-%Y')
        except ValueError:
            raise ValidationError('Invalid date format. Please use the format dd-mm-YYYY.')

    description = TextAreaField('Description', validators=[InputRequired()], render_kw={'placeholder': 'Write some descriptive information on the event'})
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')
    ])
    ticket_price = IntegerField('Ticket Price', render_kw={'placeholder': 'Enter the price of a ticket'})
    number_of_tickets = IntegerField('Number of Tickets', render_kw={'placeholder': 'Enter the number of tickets available'})
    submit = SubmitField("Create")


# User login
class LoginForm(FlaskForm):
    emailid = StringField("Email", validators=[InputRequired('Enter email')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_number = StringField("Contact Number", validators=[
        InputRequired(),
        Length(min=10, max=11, message="Contact number must be 10 digits"),
        Regexp('^[0-9]*$', message="Contact number must contain only digits")
    ])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')