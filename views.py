from core_pack.template import render


# page controller
def main_view(request):
    secret = request.get('key')
    return '200: OK', render('index.html', secret=secret)

def about_view(request):
    return '200: OK', render('about.html')

def contacts_view(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        email = data['email']
        text = data['text']

        print(f'Сообщение от  {email} , тема : {title} , текст : {text}')
        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')


def authors_view(request):
    return '200: OK', render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
