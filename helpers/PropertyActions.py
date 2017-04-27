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
		super(AddGetterAction, self).__init__(A.ADD_GETTER)

	def generate_code(self, edit):
		template = TH.Template('other/getter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', False)
		template.addVar('indent', '\t\t')
		self.view.insert(edit, self.find_end_of_class().a, template.compile())


class AddSetterAction(PropertyAction):
	def __init__(self):
		super(AddSetterAction, self).__init__(A.ADD_SETTER)

	def generate_code(self, edit):
		template = TH.Template('other/setter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', False)
		template.addVar('indent', '\t\t')
		self.view.insert(edit, self.find_end_of_class().a, template.compile())


class AddGetterSetterAction(PropertyAction):
	def __init__(self):
		super(AddGetterSetterAction, self).__init__(A.ADD_GETTER_SETTER)

	def generate_code(self, edit):
		getter = AddGetterAction()
		getter.setView(self.view)
		getter.setCode(self.code_region)
		setter = AddSetterAction()
		setter.setView(self.view)
		setter.setCode(self.code_region)
		getter.generate_code(edit)
		setter.generate_code(edit)
