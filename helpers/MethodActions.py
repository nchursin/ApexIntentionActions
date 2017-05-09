from . import logger
from . import Actions as A
from . import RegexHelper as re
from . import TemplateHelper as TH


log = logger.get(__name__)


class MethodAction(A.Action):
	def __init__(self, name):
		super(MethodAction, self).__init__(name)

	def get_class_code(self):
		return self.full_region(self.code_region)

	def get_method_name(self):
		result = re.findPropName(self.to_text())
		log.debug('method name >> ' + result)

	def get_access_level(self):
		result = re.findMethodAccessLevel(self.to_text())
		log.debug('method access level >> ' + result)
		return result

	def get_return_type(self):
		result = re.findMethodReturnType(self.to_text())
		log.debug('method return type >> ' + result)
		return result

	def is_static(self):
		result = re.findMethodIsStatic(self.to_text())
		log.debug('method is static >> ' + result)
		return result

	def get_method_defn(self):
		return self.to_text()

	def is_applicable(self):
		return re.is_method_def(self.to_text())


class AddMethodOverrideAction(MethodAction):
	def __init__(self):
		super(AddMethodOverrideAction, self).__init__(A.ADD_METHOD_OVERRIDE)

	def run(self):
		pass

	def generate_code(self, edit):
		# args_def = re.findMethodArgs(self.to_text)
		template = TH.Template('other/override')
		template.addVar('methodName', self.get_method_name())
		template.addVar('indent', self.get_inner_indent())
		template.addVar('access', self.get_access_level())
		template.addVar('static', self.is_static())
		template.addVar('returnType', self.get_return_type())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())

	def is_applicable(self):
		result = super(AddMethodOverrideAction, self).is_applicable()
		return result and re.find(re.METHOD_DEF_ARGS, self.to_text())
