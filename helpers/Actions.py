from . import logger
from . import RegexHelper as re
import sublime


log = logger.get(__name__)
ADD_GETTER = 'AddGetter'
ADD_SETTER = 'AddSetter'
ADD_GETTER_SETTER = 'AddGetterSetter'

ADD_CONSTRUCTOR = 'AddConstructor'
ADD_INITIALIZER = 'AddInitializer'


class Action():
	"""Stores info on action to take on code"""
	def __init__(self, name):
		super(Action, self).__init__()
		self.name = name
		self.view = None
		self.code_region = None

	def setView(self, view):
		self.view = view

	def setCode(self, code):
		self.code_region = code

	def find_place_to_insert_code(self):
		raise Exception("find_place_to_insert_code not defined")

	def get_class_code(self):
		raise Exception("get_class_code not defined")

	def generate_code(self, edit):
		raise Exception("generate_code not defined")

	def requireView(self):
		if not self.view:
			raise ValueError("No view is defined")

	def requireCode(self):
		if not self.code_region:
			raise ValueError("No code is set")

	def full_region_from_indent(self, r):
		self.requireView()
		if self.end_of_view(r.end()):
			return self.view.full_line(sublime.Region(r.begin() - 1, r.end()))
		else:
			return self.view.full_line(sublime.Region(r.begin() - 1, r.end() + 1))

	def full_region(self, r):
		result = self.full_region_from_indent(self.view.indented_region(r.begin()))
		if not self.end_of_view(result.end()):
			result = sublime.Region(result.begin(), result.end() - 1)
		log.debug('full_region >> ' + self.view.substr(result))
		return result

	def find_class_name(self):
		self.requireView()
		self.requireCode()
		class_region = self.get_class_code()
		class_def = self.view.substr(self.view.line(class_region.begin()))
		class_name = re.findClassName(class_def)
		log.debug('class name >> ' + class_name)
		return class_name

	def find_end_of_class(self):
		self.requireView()
		self.requireCode()
		class_region = self.get_class_code()
		class_end_region = self.view.full_line(class_region.end())
		if not self.end_of_view(class_end_region.end()):
			class_end_region = sublime.Region(class_end_region.begin(), class_end_region.end() - 1)
		log.debug('class_end_region >> ' + self.view.substr(class_end_region))
		log.debug('class_end_region >> ' + str(class_end_region.begin()) + ' : ' + str(class_end_region.end()))
		return sublime.Region(class_end_region.begin() - 1, class_end_region.begin() - 1)

	def find_constructors(self):
		regions = []
		full_region = self.get_class_code()
		start = full_region.begin()
		constructor_region = self.view.find(re.CONSTRUCTOR, start)
		limit = 10
		i = 0
		while constructor_region:
			log.debug('constructor_region >> ' + self.view.substr(constructor_region))
			if full_region.end() > constructor_region.begin():
				regions.append(constructor_region)
				start = constructor_region.end()
				constructor_region = self.view.find(re.CONSTRUCTOR, start)
			else:
				break
			i += 1
			if limit < i:
				log.debug('LIMIT REACHED')
				break
		return regions

	def get_indent(self):
		class_region = self.get_class_code()
		return re.getIndent(self.view.substr(self.view.line(class_region.begin())))

	def get_inner_indent(self):
		return self.get_indent() + '\t'

	def end_of_view(self, point):
		return point == self.view.size()
