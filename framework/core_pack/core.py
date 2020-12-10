class Application:

    def __init__(self, urlpatterns, fronts):
        self.urlpatterns = urlpatterns
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        # проверяем заканчивается ли адрес '/'
        # если нет - то добавляем '/'
        if not path.endswith('/'):
            path = path + '/'

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = dict()

            for func in self.fronts:
                func(request)

            code, headers = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [headers.encode('utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b'Not Found']






# gunicorn
# pip install gunicorn
# gunicorn simple_wsgi:application

# uwsgi
# pip install uwsgi
# uwsgi --http :8000 --wsgi-file simple_wsgi.py