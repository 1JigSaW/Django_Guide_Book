{% load poll_extras %}

from django import template
import re

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
	return value.replace(arg, '')

class CurrentTimeNode3(template.Node):
	def __init__(self, format_string, var_name):
		self.format_string = str(format_string)
		self.var_name = var_name

	def render(self, context):
		now = datetime.datetime.now()
		context[self.var_name] = now.strftime(self.format_string)
		return ''

	def do_current_time(parser, token):
		try:
			tag_name, arg = token.contents.split(None, 1)
		except ValueError:
			msg = 'Тег %r требует аргументы' % token.contents[0]
			raise template.TemplateSyntaxError(msg)
		m = re.search(r'(.*?) as (\w+)', arg)
		if m:
			fmt, var_name = m.groups()
		else:
			msg = 'У тега %r недопустимые аргументы' % tag_name
			raise template.TemplateSyntaxError(msg)
		if not (fmt[0] == fmt[-1] and fmt[0] in ('""', '""')):
			msg = 'Аргумент тега %r должен быть в кавычках' % tag_name
			raise template.TemplateSyntaxError(msg)
		return CurrentTimeNode3(fmt[1:-1], var_name)

