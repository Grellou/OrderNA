from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Initialize
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login_page"  # type: ignore
login_manager.login_message_category = "info"
csrf = CSRFProtect()


def create_app(config_class="Development"):
    app = Flask(__name__)

    # Load config
    from app.config import config_by_name

    app.config.from_object(config_by_name[config_class])

    # Initialize with app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Blueprints
    from app.routes.admin_routes import bp as AdminBlueprint
    from app.routes.auth_routes import bp as AuthBlueprint
    from app.routes.home_routes import bp as HomeBlueprint

    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(HomeBlueprint)
    app.register_blueprint(AdminBlueprint)

    # Register CLI commands
    from app.utils import register_commands

    register_commands(app)

    return app
