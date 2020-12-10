# wsgi_framework

gunicorn
gunicorn simple_wsgi:application

uwsgi
uwsgi --http :8000 --wsgi-file simple_wsgi.py
