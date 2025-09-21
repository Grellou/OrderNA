import click

from app import create_app, db
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


def register_commands(app):
    app.cli.add_command(create_admin_command)
