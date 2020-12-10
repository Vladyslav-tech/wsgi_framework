from core_pack.template import render


# page controller
def main_view(request):
    secret = request.get('key')
    return '200: OK', render('index.html', secret=secret)

def about_view(request):
    return '200: OK', render('about.html')

def contacts_view(request):
    return '200: OK', render('contacts.html')
