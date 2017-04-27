from . import logger
from . import Actions as A
from . import TemplateHelper as TH
# from . import RegexHelper as re


log = logger.get(__name__)


class ClassAction(A.Action):
	def __init__(self, name):
		super(ClassAction, self).__init__(name)

	def get_class_code(self):
		log.debug('get_class_code >> ' + self.view.substr(
			self.full_region(self.view.indented_region(self.code_region.end() + 1))))
		return self.full_region(self.view.indented_region(self.code_region.end() + 1))


class AddConstructorAction(ClassAction):
	def __init__(self):
		super(AddConstructorAction, self).__init__(A.ADD_CONSTRUCTOR)

	def generate_code(self, edit):
		template = TH.Template('other/constructor')
		template.addVar('className', self.find_class_name())
		template.addVar('indent', self.get_inner_indent())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())


class AddInitializerAction(ClassAction):
	def __init__(self):
		super(AddInitializerAction, self).__init__(A.ADD_INITIALIZER)

	def generate_code(self, edit):
		# TODO: optimize constructor search
		constr_regions = self.find_constructors()
		template = TH.Template('other/initializer')
		template.addVar('indent', self.get_inner_indent())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())
		init_call = '\n' + self.get_inner_indent() + '\tinit();'
		for i in range(0, len(constr_regions)):
			constr = constr_regions[i]
			self.view.insert(edit, self.end_of_region(constr).begin(), init_call)
			constr_regions = self.find_constructors()
