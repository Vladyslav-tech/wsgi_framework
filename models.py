
from patterns.prototype import PrototypeMixin


class User:
    id = 0

    def __init__(self, first_name, last_name):
        self.id = User.id
        User.id += 1
        self.first_name = first_name
        self.last_name = last_name
        self.courses = []


class Teacher(User):
    pass


class Student(User):
    pass


class SimpleFactory:
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    """Класс - фабрика для пользователей"""
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Category:
    id = 0

    def __init__(self, name, category):
        self.id = Category.id
        Category.id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        """Количество курсов конретной категории"""
        count = len(self.courses)
        if self.category:
            count += self.category.course_count()
        return count


class Course(PrototypeMixin):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    """Класс - фабрика для курсов"""
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Site:
    # Интерфейс
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_):
        return UserFactory.create(type_)

    def create_category(self, name, category=None):
        """Создание категории"""
        return Category(name, category)

    def find_category_by_id(self, id):
        """Поиск категории по id"""
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def create_course(self, type_, name, category):
        """Создание курса"""
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None