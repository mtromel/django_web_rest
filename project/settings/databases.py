import os

from .environment import BASE_DIR

if os.environ.get("DEBUG") == "1":
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DATABASE_ENGINE"),
            "NAME": BASE_DIR / os.environ.get("DATABASE_NAME", "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DATABASE_ENGINE"),
            "NAME": os.environ.get("DATABASE_NAME"),
            "USER": os.environ.get("DATABASE_USER"),
            "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
            "HOST": os.environ.get("DATABASE_HOST"),
            "PORT": os.environ.get("DATABASE_PORT"),
        }
    }
