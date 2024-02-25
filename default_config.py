import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

# SQLALCHEMY_DATABASE_URI = "postgres://uojuveuu:syURUwt273sUObUXBv8lgcp_67W2-rBQ@lallah.db.elephantsql.com/uojuveuu"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
# JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
# JWT_BLACKLIST_ENABLED = True
# JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]  # allow blacklisting for access and refresh tokens
