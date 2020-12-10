from core_pack.core import Application
import views


urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contacts/': views.contacts_view,
}



def secret_controller(request):
    # Front Controller
    request['key'] = 'SOME_TEXT'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)