BROKER_URL = "sqla+sqlite:///vpt_tasks.db"
CELERY_ACCEPT_CONTENT = ["pickle"]
CELERY_IGNORE_RESULT = True
CELERY_IMPORTS = ("app.notifications.handlers", )