from core_pack.core import Application, DebugApplication, MockApplication
from core_pack.template import render
from models import Site

from log.logging import Logger, debug



site = Site()
logger = Logger('main')


# page controllers
def main_view(request):
    logger.log('Courses list')
    return '200: OK', render('course_list.html', objects_list=site.courses)


@debug
def create_course(request):
    """Создание курса"""
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_user(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        user_id = data.get('user_id')


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        print(data)
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)

        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)

urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,

}


def secret_controller(request):
    # Front Controller
    request['key'] = 'SOME_TEXT'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)
# application = DebugApplication(urlpatterns, front_controllers)
# application = MockApplication(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)

