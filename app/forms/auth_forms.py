from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# Form used to login
class LoginForm(FlaskForm):
    email_address = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


# Form used to create new account
class CreateAccountForm(FlaskForm):
    email_address = StringField("Email address", validators=[DataRequired(), Email()])
    password1 = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    password2 = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password1")]
    )
    description = StringField("Description")
    submit = SubmitField("Create Account")
