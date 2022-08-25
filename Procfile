release: python manage.py migrate
web: daphne channels_celery_heroku_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A LibraryManagementSystem worker --pool=solo -l info
celerybeat: celery -A LibraryManagementSystem beat -l info -S django
celeryworker2: celery -A LibraryManagementSystem.celery worker & celery -A LibraryManagementSystem beat -l INFO & wait -n
