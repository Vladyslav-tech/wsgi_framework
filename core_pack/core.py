from chardet.universaldetector import UniversalDetector

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

        # данные из запроса
        method = environ['REQUEST_METHOD']
        input_data = self.get_wsgi_input_data(environ)
        input_data = self.decode_wsgi_input_data(input_data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = dict()

            request['method'] = method
            request['data'] = input_data
            request['request_params'] = request_params

            for func in self.fronts:
                func(request)

            code, headers = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [headers.encode('utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b'Not Found']


    def get_wsgi_input_data(self, environ):
        """Получаем данные из post запроса в байтах"""
        if environ.get('CONTENT_LENGTH'):
            length_data = int(environ.get('CONTENT_LENGTH'))
        else:
            length_data = 0

        if length_data > 0:
            data = environ['wsgi.input'].read(length_data)
        else:
            data = b''

        return data

    def parse_input_data(self, data: str):
        """Разбираем адрес на параметры"""
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    def decode_wsgi_input_data(self, data: bytes):
        """
        Декодируем полученное сообщение из байт в строку
        Разбираем сообщение на параметры
        """
        result = {}
        encoding = self.encoding_detecting(data)
        print(encoding)

        if data:
            data_str = data.decode(encoding=encoding)
            result = self.parse_input_data(data_str)
        return result

    def encoding_detecting(self, data):
        """Определяем кодировку"""
        detector = UniversalDetector()
        detector.feed(data)
        detector.close()
        return detector.result['encoding']

