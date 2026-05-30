SECRET_KEY = "astroll-dev-only"
DEBUG = True
ROOT_URLCONF = "config.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "apps.accounts",
    "apps.friends",
    "apps.characters",
    "apps.rooms",
    "apps.board",
    "apps.dice",
    "apps.game_session",
    "apps.administration",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "astroll_old.sqlite3",
    }
}
