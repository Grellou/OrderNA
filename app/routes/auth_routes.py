from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.forms.auth_forms import LoginForm
from app.models.user_model import UserModel

bp = Blueprint("auth", __name__)


# Login with email address and password
@bp.route("/login", methods=["GET", "POST"])
def login_page():
    # Redirect if user already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home.home_page"))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email_address=form.email_address.data).first()
        # Check if login detail matches
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login succesful!", "success")
            return redirect(url_for("home.home_page"))
        else:
            flash("Invalid email address or password.", "danger")

    return render_template("auth/login.html", form=form)


# Logout
@bp.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out succesfully.", "info")
    return redirect(url_for("home.home_page"))
