from . import logger
from . import TemplateHelper as TH
from . import RegexHelper as re
from . import Actions as A


log = logger.get(__name__)


class PropertyAction(A.Action):
	"""Stores info on property actions"""
	def __init__(self, name):
		super(PropertyAction, self).__init__(name)

	def get_class_code(self):
		return self.full_region(self.code_region)

	def get_prop_name(self):
		result = re.findPropName(self.to_text(self.code_region))
		log.debug('property name >> ' + result)
		return result

	def get_prop_type(self):
		result = re.findPropType(self.to_text(self.code_region))
		log.debug('property type >> ' + result)
		return result

	def generate_code(self):
		raise Exception("generate_code not defined")

	def is_applicable(self):
		prop_regex = r'(public|private|global|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;'
		return re.match_stripped(prop_regex, self.to_text())


class AddGetterAction(PropertyAction):
	def __init__(self):
		super(AddGetterAction, self).__init__(A.ADD_GETTER)

	def generate_code(self, edit):
		template = TH.Template('other/getter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', False)
		template.addVar('indent', self.get_inner_indent())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())

	def is_applicable(self):
		result = super(AddGetterAction, self).is_applicable()
		return result and re.findGetter(self.to_text(self.get_class_code()), self.get_prop_name()) is None


class AddSetterAction(PropertyAction):
	def __init__(self):
		super(AddSetterAction, self).__init__(A.ADD_SETTER)

	def generate_code(self, edit):
		template = TH.Template('other/setter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', False)
		template.addVar('indent', self.get_inner_indent())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())

	def is_applicable(self):
		result = super(AddSetterAction, self).is_applicable()
		return result and re.findSetter(self.to_text(self.get_class_code()), self.get_prop_name()) is None


class AddGetterSetterAction(PropertyAction):
	def __init__(self):
		super(AddGetterSetterAction, self).__init__(A.ADD_GETTER_SETTER)
		self.getter = AddGetterAction()
		self.setter = AddSetterAction()

	def setView(self, view):
		super(AddGetterSetterAction, self).setView(view)
		self.getter.setView(view)
		self.setter.setView(view)

	def setCode(self, code_region):
		super(AddGetterSetterAction, self).setCode(code_region)
		self.getter.setCode(code_region)
		self.setter.setCode(code_region)

	def is_applicable(self):
		return self.getter.is_applicable() and self.setter.is_applicable()

	def generate_code(self, edit):
		self.getter.generate_code(edit)
		self.setter.generate_code(edit)
