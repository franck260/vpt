BROKER_TRANSPORT = "sqlakombu.transport.Transport"
BROKER_HOST = "sqlite:///vpt_tasks.db"
CELERY_IMPORTS = ("app.notifications.handlers", )
CELERY_IGNORE_RESULT = True