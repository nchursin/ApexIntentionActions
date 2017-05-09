import sublime
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
		result = re.findMethodName(self.to_text())
		log.debug('method name >> ', result)
		return result

	def get_access_level(self):
		result = re.findMethodAccessLevel(self.to_text())
		log.debug('method access level >> ', result)
		return result

	def get_return_type(self):
		result = re.findMethodReturnType(self.to_text())
		log.debug('method return type >> ', result)
		return result

	def is_static(self):
		result = re.findMethodIsStatic(self.to_text())
		log.debug('method is static >> ', result)
		return result

	def get_method_defn(self):
		return self.to_text()

	def is_applicable(self):
		return re.is_method_def(self.to_text())

	def get_arguments(self):
		result = re.findMethodArgs(self.to_text())
		return [el.strip() for el in result.split(',')]


class AddMethodOverrideChooseArgAction(MethodAction):
	def __init__(self):
		super(AddMethodOverrideChooseArgAction, self).__init__(A.ADD_METHOD_OVERRIDE)

	def run(self, edit, args):
		self.set_menu()
		args_def = self.get_arguments()
		self.show_menu(list(args_def), self.fire_action)

	def fire_action(self, index):
		if(-1 == index):
			return
		args = {
			'action_name': A.ADD_METHOD_OVERRIDE_CREATE,
			'subl_line_start': self.code_region.begin(),
			'subl_line_end': self.code_region.end(),
			'arg_number': index
		}
		self.view.run_command('run_action', args)

	def set_menu(self):
		settings = sublime.load_settings('SmartApexPrefs.sublime-settings')
		self.intention_menu_mode = settings.get("intention_menu_mode")
		if "quickpanel" == self.intention_menu_mode.lower():
			self.show_menu = self.view.window().show_quick_panel
		elif "popup" == self.intention_menu_mode.lower():
			self.show_menu = self.view.show_popup_menu


class AddMethodOverrideAction(MethodAction):
	def __init__(self):
		super(AddMethodOverrideAction, self).__init__(A.ADD_METHOD_OVERRIDE_CREATE)

	def run(self, edit, args):
		self.arg_number = args['arg_number']
		self.args_def = self.get_arguments()
		del self.args_def[self.arg_number]
		self.args_pass = [el.strip().split(' ')[-1] for el in self.get_arguments()]
		self.arg_to_overload = self.args_pass[self.arg_number]
		self.generate_code(edit)

	def generate_code(self, edit):
		# args_def = re.findMethodArgs(self.to_text)
		template = TH.Template('other/override')
		template.addVar('methodName', self.get_method_name())
		template.addVar('indent', self.get_inner_indent())
		template.addVar('access', self.get_access_level())
		template.addVar('static', self.is_static())
		template.addVar('returnType', self.get_return_type())
		template.addVar('methodArguments', ', '.join(self.args_def))
		template.addVar('argumentsToPass', ', '.join(self.args_pass))
		code_to_insert = '\n' + template.compile()
		place_to_insert = self.view.line(self.code_region.begin()).begin() - 1
		self.view.insert(edit, place_to_insert, code_to_insert)
		search_start = self.view.line(place_to_insert).end() + 1
		arg_region = self.view.find('(', search_start)
		to_overload = self.view.find(self.arg_to_overload, arg_region.begin())
		self.view.sel().clear()
		self.view.sel().add(to_overload)

	def is_applicable(self):
		result = super(AddMethodOverrideAction, self).is_applicable()
		return result and re.find(re.METHOD_DEF_ARGS, self.to_text())
