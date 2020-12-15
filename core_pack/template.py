from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    environ = Environment()
    environ.loader = FileSystemLoader(folder)

    template = environ.get_template(template_name)

    return template.render(**kwargs)


