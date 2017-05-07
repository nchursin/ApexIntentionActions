from . import logger
from . import RegexHelper as re
import sublime


log = logger.get(__name__)
ADD_GETTER = 'AddGetter'
ADD_SETTER = 'AddSetter'
ADD_GETTER_SETTER = 'AddGetterSetter'
ADD_CONSTRUCTOR_PARAMETER = 'AddConstructorParameter'

ADD_CONSTRUCTOR = 'AddConstructor'
ADD_INITIALIZER = 'AddInitializer'
ADD_CONSTRUCTOR_INITIALIZER = 'AddConstructorInitializer'


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

	def is_applicable(self):
		raise Exception("is_applicable not defined")

	def full_region_from_indent(self, r):
		self.requireView()
		if self.end_of_view(r.end()):
			return self.view.full_line(sublime.Region(r.begin() - 1, r.end()))
		else:
			return self.view.full_line(sublime.Region(r.begin() - 1, r.end() + 1))

	def full_region(self, r):
		log.debug('self.view.indented_region(r.begin()) >> ', self.to_text(self.view.indented_region(r.begin())))
		result = self.full_region_from_indent(self.view.indented_region(r.begin()))
		if not self.end_of_view(result.end()):
			result = sublime.Region(result.begin(), result.end() - 1)
		log.debug('full_region >> ' + self.view.substr(result))
		return result

	def find_class_def(self):
		self.requireView()
		self.requireCode()
		class_region = self.get_class_code()
		class_def = self.view.line(class_region.begin())
		log.debug('class_region.begin() >> ', class_region.begin())
		log.debug('class_def >> ', class_def)
		return class_def

	def find_class_name(self):
		class_def = self.to_text(self.find_class_def())
		class_name = re.findClassName(class_def)
		log.debug('class name >> ' + class_name)
		return class_name

	def find_end_of_class(self):
		self.requireView()
		self.requireCode()
		class_region = self.get_class_code()
		return self.end_of_region(class_region)
		# class_end_region = self.view.full_line(class_region.end())
		# if not self.end_of_view(class_end_region.end()):
		# 	class_end_region = sublime.Region(class_end_region.begin(), class_end_region.end() - 1)
		# log.debug('class_end_region >> ' + self.view.substr(class_end_region))
		# log.debug('class_end_region >> ' + str(class_end_region.begin()) + ' : ' + str(class_end_region.end()))
		# return sublime.Region(class_end_region.begin() - 1, class_end_region.begin() - 1)

	def end_of_region(self, r):
		end_region = self.view.full_line(r.end())
		if not self.end_of_view(end_region.end()):
			end_region = sublime.Region(end_region.begin(), end_region.end() - 1)
		log.debug('end_region >> ' + self.view.substr(end_region))
		log.debug('end_region >> ' + str(end_region.begin()) + ' : ' + str(end_region.end()))
		return sublime.Region(end_region.begin() - 1, end_region.begin() - 1)

	def find_constructors(self):
		regions = []
		full_region = self.get_class_code()
		start = full_region.begin()
		constructor_region = self.view.find(re.CONSTRUCTOR, start)
		while constructor_region:
			full_constructor = self.full_region(self.view.indented_region(constructor_region.end() + 1))
			log.debug('constructor_region >> ' + self.view.substr(full_constructor))
			if full_region.end() > constructor_region.begin():
				regions.append(full_constructor)
				start = full_constructor.end()
				constructor_region = self.view.find(re.CONSTRUCTOR, start)
			else:
				break
		return regions

	def to_text(self, region=None):
		if region is None:
			self.requireCode()
			region = self.code_region
		return self.view.substr(region)

	def get_indent(self):
		class_region = self.get_class_code()
		settings = self.view.settings()
		translate_tabs_to_spaces = settings.get("translate_tabs_to_spaces")
		tab_size = settings.get("tab_size")
		return re.getIndent(self.view.substr(self.view.line(class_region.begin())),
			translate_tabs_to_spaces, tab_size)

	def get_inner_indent(self):
		return self.get_indent() + '\t'

	def end_of_view(self, point):
		return point == self.view.size()
