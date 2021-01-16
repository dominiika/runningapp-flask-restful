import os


class Config:
    """Config class for initializing the app and the database"""

    try:
        from runningapp.secret_key import SECRET_KEY
    except ImportError:
        with open(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "secret_key.py"
            ),
            "w",
        ) as file:
            file.write(f'SECRET_KEY="{os.urandom(24)}"')
        from runningapp.secret_key import SECRET_KEY
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
