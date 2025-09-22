import csv

import click

from app import db
from app.models.item_model import ItemModel
from app.models.user_model import UserModel


# Push admin user into db via CLI
@click.command("create-admin")
@click.argument("email_address")
@click.argument("password")
def create_admin_command(email_address, password):
    if UserModel.query.filter_by(email_address=email_address).first():
        click.echo(
            f"Error: User with such email address {email_address} already exists."
        )
        return

    user = UserModel(email_address=email_address, is_active=True, is_admin=True)  # type: ignore
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    click.echo(f"Admin account {email_address} created successfully!")


# Import initial stock to db
@click.command("import-stock")
@click.argument("filename")
def import_stock_command(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = ItemModel(
                name=row["Name"].strip(),  # type: ignore
                category=row["Category"].strip(),  # type: ignore
                language=row["Language"].strip(),  # type: ignore
                quantity=int(row["Quantity"] or 0),  # type: ignore
                price=float(row["Price"]),  # type: ignore
            )
            db.session.add(item)
        db.session.commit()
        click.echo("Successfully imported stock!")


def register_commands(app):
    app.cli.add_command(create_admin_command)
    app.cli.add_command(import_stock_command)
