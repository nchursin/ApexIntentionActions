from . import logger
from . import Actions as A
from . import TemplateHelper as TH
from . import RegexHelper as re
from . import SublimeHelper as SH
import sublime


log = logger.get(__name__)


class ClassAction(A.Action):
	def __init__(self, name):
		super(ClassAction, self).__init__(name)

	def get_class_code(self):
		log.debug('indented get_class_code >> ', self.to_text())
		full_region = self.full_region(self.view.indented_region(
			self.code_region.end() + 1))
		indented_defn = self.to_text(
			self.view.line(
				full_region.begin())).strip()
		log.debug('full_region >> ', self.to_text(full_region))
		if indented_defn != self.to_text().strip():
			class_end = self.view.find(r'\}', self.code_region.end())
			result = sublime.Region(self.code_region.begin(), class_end.end())
		else:
			result = full_region
		log.debug('get_class_code >> ', self.to_text(result))
		return result

	def is_applicable(self):
		class_regex = r'(public|private|global|protected)\s*(virtual|abstract|with sharing|without sharing){0,1}\s+class\s+(\w+)\s*.*{'
		return re.match_stripped(class_regex, self.to_text())


class AddConstructorAction(ClassAction):
	def __init__(self):
		super(AddConstructorAction, self).__init__(A.ADD_CONSTRUCTOR)

	def generate_code(self, edit):
		template = TH.Template('other/constructor')
		template.addVar('className', self.find_class_name())
		template.addVar('indent', self.get_inner_indent())
		if ' extends ' in self.to_text():
			template.addVar('code', 'super();')
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())

	def is_applicable(self):
		result = super(AddConstructorAction, self).is_applicable()
		return result and re.findConstructor(self.to_text(self.get_class_code()), self.find_class_name()) is None


class AddInitializerAction(ClassAction):
	def __init__(self):
		super(AddInitializerAction, self).__init__(A.ADD_INITIALIZER)
		self.init_method_name = 'init'

	def generate_code(self, edit):
		# TODO: optimize constructor search
		constr_regions = self.find_constructors()
		template = TH.Template('other/initializer')
		template.addVar('indent', self.get_inner_indent())
		view_helper = SH.ViewHelper(self.view)
		view_helper.insert_snippet(template.compile(), self.find_end_of_class().begin())
		init_call = '\n' + self.get_inner_indent() + '\t' + self.init_method_name + '();'
		for i in range(0, len(constr_regions)):
			constr = constr_regions[i]
			self.view.insert(edit, self.end_of_region(constr).begin(), init_call)
			constr_regions = self.find_constructors()

	def is_applicable(self):
		result = super(AddInitializerAction, self).is_applicable()
		return result and re.findMethod(self.to_text(self.get_class_code()), self.init_method_name) is None


class AddConstructorInitializerAction(ClassAction):
	def __init__(self):
		super(AddConstructorInitializerAction, self).__init__(A.ADD_CONSTRUCTOR_INITIALIZER)
		self.constructor = AddConstructorAction()
		self.initializer = AddInitializerAction()

	def setView(self, view):
		super(AddConstructorInitializerAction, self).setView(view)
		self.initializer.setView(view)
		self.constructor.setView(view)

	def setCode(self, code_region):
		super(AddConstructorInitializerAction, self).setCode(code_region)
		self.initializer.setCode(code_region)
		self.constructor.setCode(code_region)

	def is_applicable(self):
		return self.initializer.is_applicable() and self.constructor.is_applicable()

	def generate_code(self, edit):
		self.constructor.generate_code(edit)
		self.initializer.generate_code(edit)
