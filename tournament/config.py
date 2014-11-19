import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Database connections
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'crunch.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')


# Application threads
THREADS_PER_PAGE = 2


# Enable protection agains *Cross-site Request Forgery (CSRF)*
WTF_CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "beastMode"


# Secret key for signing cookies
SECRET_KEY = 'beastMode'