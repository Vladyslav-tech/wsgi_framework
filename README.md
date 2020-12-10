# wsgi_framework
gunicorn simple_wsgi:application
uwsgi --http :8000 --wsgi-file simple_wsgi.py
