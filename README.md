# wsgi_framework

gunicorn main:application


uwsgi --http :8000 --wsgi-file main.py
