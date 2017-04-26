from . import logger
from . import RegexHelper as re
from . import TemplateHelper as TH
import sublime


log = logger.get(__name__)


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

	def requireView(self):
		if not self.view:
			raise ValueError("No view is defined")

	def requireCode(self):
		if not self.code_region:
			raise ValueError("No code is set")

	def full_region_from_indent(self, r):
		self.requireView()
		if self.end_of_view(r.b):
			return self.view.full_line(sublime.Region(r.a - 1, r.b))
		else:
			return self.view.full_line(sublime.Region(r.a - 1, r.b + 1))

	def full_region(self, r, im_inside=True):
		if im_inside:
			result = self.full_region_from_indent(self.view.indented_region(r.a))
		else:
			result = self.view.indented_region(r.a)
		if not self.end_of_view(result.b):
			result = sublime.Region(result.a, result.b - 1)
		log.debug('full_region >> ' + self.view.substr(result))
		return result

	def end_of_view(self, point):
		return point == self.view.size()


class PropertyAction(Action):
	"""Stores info on property actions"""
	def __init__(self, name):
		super(PropertyAction, self).__init__(name)

	def find_class_name(self):
		self.requireView()
		self.requireCode()
		class_region = self.full_region(self.code_region)
		class_def = self.view.substr(self.view.line(class_region.a))
		class_name = re.findClassName(class_def)
		log.debug('class name >> ' + class_name)
		return class_name

	def find_end_of_class(self):
		self.requireView()
		self.requireCode()
		class_region = self.full_region(self.code_region)
		class_end_region = self.view.full_line(class_region.b)
		if not self.end_of_view(class_end_region.b):
			class_end_region = sublime.Region(class_end_region.a, class_end_region.b - 1)
		log.debug('class_end_region >> ' + self.view.substr(class_end_region))
		log.debug('class_end_region >> ' + str(class_end_region.a) + ' : ' + str(class_end_region.b))
		return sublime.Region(class_end_region.a - 1, class_end_region.a - 1)

	def get_prop_name(self):
		result = re.findPropName(self.view.substr(self.code_region))
		log.debug('property name >> ' + result)
		return result

	def get_prop_type(self):
		result = re.findPropType(self.view.substr(self.code_region))
		log.debug('property type >> ' + result)
		return result

	def generate_code(self):
		raise Exception("generate_code not defined")


class AddGetterAction(PropertyAction):
	def __init__(self):
		super(AddGetterAction, self).__init__('AddGetter')

	def generate_code(self, edit):
		template = TH.Template('other/getter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', False)
		template.addVar('indent', '\t\t')
		self.view.insert(edit, self.find_end_of_class().a, template.compile())
