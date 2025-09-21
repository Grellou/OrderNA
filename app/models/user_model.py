from flask_login import UserMixin

from app import bcrypt, db, login_manager


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(128))

    # Prevent password from being accessed
    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    # Set password hash
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Check if password matches
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# User loader
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))
