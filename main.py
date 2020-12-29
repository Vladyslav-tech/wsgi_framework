from core_pack.core import Application, DebugApplication, FakeApplication
from core_pack.template import render
from models import Site, BaseSerializer, EmailNotifier, SmsNotifier
from core_pack.core_cbv import CreateView, ListView

from log.logging import Logger, debug



site = Site()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

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
            print(category)

            course = site.create_course('record', name, category)
            site.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


# def create_user(request):
#     """Создание Пользователя"""
#     if request['method'] == 'POST':
#         data = request['data']
#         first_name = data['first_name']
#         last_name = data['last_name']
#         user_category = data.get('user_category')
#         print(f"user_category : {user_category}")
#
#         user = site.create_user(user_category, first_name, last_name)
#         if user_category == 'student':
#             site.students.append(user)
#         elif user_category == 'teacher':
#             site.teachers.append(user)
#
#         user_catigories = ['student', 'teacher']
#         return '200 OK', render('create_user.html', user_catigories=user_catigories)
#     else:
#         user_catigories = ['student', 'teacher']
#         return '200 OK', render('create_user.html', user_catigories=user_catigories)



class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


class CategoryListView(ListView):
    """Класс списка категорий"""
    queryset = site.categories
    template_name = 'category_list.html'


class StudentListView(ListView):
    """Класс списка студентов"""
    queryset = site.students
    template_name = 'student_list.html'


class StudentCreateView(CreateView):
    """Класс-создание студентов"""
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)

# def create_category(request):
#     """Создание категории"""
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#         category_id = data.get('category_id')
#         print(f"category_id in create_category : {category_id}")
#
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#
#         return '200 OK', render('create_category.html')
#     else:
#         categories = site.categories
#         return '200 OK', render('create_category.html', categories=categories)

urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': CategoryCreateView(),
    '/student-list/': StudentListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
    '/category-list/': CategoryListView(),
}


def secret_controller(request):
    # Front Controller
    request['key'] = 'SOME_TEXT'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)
# application = DebugApplication(urlpatterns, front_controllers)
# application = FakeApplication(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    """Копирование курса при помощи патерна Decorator"""
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


# @application.add_route('/category-list/')
# def category_list(request):
#     logger.log('Список категорий')
#     return '200 OK', render('category_list.html', objects_list=site.categories)


# @application.add_route('/users_list/')
# def users_list(request):
#     logger.log('Список пользователей')
#     return '200 OK', render('users_list.html', students=site.students, teachers=site.teachers)

@application.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.courses).save()
