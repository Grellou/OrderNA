import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import asc

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


@bp.route("/admin/edit-stock", methods=["GET"])
def edit_stock_page():

    # Redirect if user is not admin
    if not current_user.is_admin:
        flash("Insufficient permisions.", "danger")
        return redirect(url_for("home.home_page"))

    # Display all stock
    items = ItemModel.query.order_by(asc(ItemModel.name))

    return render_template("admin/edit_stock.html", items=items)


@bp.route("/admin/edit-stock", methods=["POST"])
def update_stock_page():

    # Debug
    print("FORM DATA:", request.form)

    # Redirect if user is not admin
    if not current_user.is_admin:
        flash("Insufficient permisions.", "danger")
        return redirect(url_for("home.home_page"))

    # Grab item data from saved input
    item_id = request.form.get("item_id")
    quantity = request.form.get("quantity")
    price = request.form.get("price")

    try:
        quantity = int(quantity)  # type: ignore
        price = float(price)  # type: ignore
    except ValueError:
        return "Invalid data", 400

    item = ItemModel.query.get(item_id)
    if not item:
        return "Item not found", 404

    item.quantity = quantity
    item.price = price

    # Add to db
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while editing item data. Please try again.", "danger")
        logging.error(f"Error while editing item data: {e}")

    return render_template("admin/_stock_row.html", item=item)
