from app import db
from app.models.user_model import UserModel


def create_account(email_address, password, description):

    # Create new user with provided details
    user = UserModel(
        email_address=email_address, description=description  # type: ignore
    )
    user.set_password(password)

    # Add to db
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
