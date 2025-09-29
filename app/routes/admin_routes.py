import logging

import pandas as pd
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app import db
from app.forms.auth_forms import CreateAccountForm
from app.models.item_model import ItemModel
from app.models.user_model import UserModel

bp = Blueprint("admin", __name__)


# Main admin page
@bp.route("/admin")
def admin_page():

    # Redirect if user is not admin
    if not current_user.is_admin:
        flash("Insufficient permisions.", "danger")
        return redirect(url_for("home.home_page"))

    return render_template("admin/admin.html")


# Admin page to create new user accounts
@bp.route("/admin/create-account", methods=["GET", "POST"])
def create_account_page():

    # Redirect if user is not admin
    if not current_user.is_admin:
        flash("Insufficient permisions.", "danger")
        return redirect(url_for("home.home_page"))

    form = CreateAccountForm()
    if form.validate_on_submit():
        # Create new user with provided details
        user = UserModel(
            email_address=form.email_address.data, description=form.description.data  # type: ignore
        )
        user.set_password(form.password1.data)

        # Add to db
        try:
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(
                "An error occurred during account creation. Please try again.", "danger"
            )
            logging.error(f"Error while creating account: {e}")
    return render_template("admin/create_account.html", form=form)
