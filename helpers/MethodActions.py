import sublime
from . import logger
from . import Actions as A
from . import RegexHelper as re
from . import TemplateHelper as TH
from . import ConstructorActions as CA
from . import SublimeHelper as SH


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
		return [el.strip() for el in re.split_arguments(result)]

	def get_argument_types(self):
		result = re.findMethodArgs(self.to_text())
		return [el.strip() for el in re.split_argument_types(result)]


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
		arg_to_overload = self.args_pass[self.arg_number]
		self.args_pass[self.arg_number] = '${1:' + arg_to_overload + '}'
		self.generate_code(edit)

	def generate_code(self, edit):
		# args_def = re.findMethodArgs(self.to_text)
		place_to_insert = self.view.line(self.code_region.begin()).begin() - 1
		indent = self.get_indent()
		log.info('indent >> ', indent)
		prev_line = self.view.line(place_to_insert)
		prev_line = self.to_text(prev_line)
		if not prev_line and ' ' not in prev_line and '\t' not in prev_line:
			indent += '\t'
		else:
			indent = ''
		template = TH.Template('other/overload')
		template.addVar('methodName', self.get_method_name())
		template.addVar('indent', indent)
		template.addVar('access', self.get_access_level())
		template.addVar('static', self.is_static())
		template.addVar('returnType', self.get_return_type())
		template.addVar('methodArguments', ', '.join(self.args_def))
		template.addVar('argumentsToPass', ', '.join(self.args_pass))
		code_to_insert = '\n' + template.compile()
		self.insaert_if_none(code_to_insert)

	def insaert_if_none(self, code_to_insert):
		code_splitted = code_to_insert.split('\n')
		for line in code_splitted:
			if line:
				definition = line.strip()
				break
		log.info('definition >> ', self.expand_definition(definition))
		definition = self.expand_definition(definition)
		definition = definition.translate(str.maketrans({
			"(": r"\(",
			")": r"\)",
			"{": r"\{",
			"}": r"\}",
			".": r"\."
		}))
		log.info('definition >> ', definition)
		log.info('definition in view >> ', self.view.find(definition, 0, sublime.IGNORECASE))
		# log.info('definition in view >> ', self.view.find('public void activateOrdersAuto\\(Map<Id, Shit> ShitsMap\\){', 0, sublime.IGNORECASE))
		if self.view.find_all(definition, sublime.IGNORECASE):
			self.view.show_popup(
				content='Overload already generated!',
				flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY)
		else:
			view_helper = SH.ViewHelper(self.view)
			place_to_insert = self.view.line(self.code_region.begin()).begin() - 1
			view_helper.insert_snippet(code_to_insert, place_to_insert)

	def expand_definition(self, definition):
		args_line = re.findMethodArgs(definition)
		arg_types = [el.strip() for el in re.split_argument_types(args_line)]
		log.info('arg_types >> ', arg_types)
		arg_types = r' \w+, '.join(arg_types) + r' \w+'
		log.info('arg_types >> ', arg_types)
		if args_line and arg_types:
			result = definition.replace(args_line, arg_types)
		else:
			result = definition
		return result

	def is_applicable(self):
		result = super(AddMethodOverrideAction, self).is_applicable()
		return result and re.find(re.METHOD_DEF_ARGS, self.to_text())


class ChooseOverloadAction(A.Action):
	def __init__(self):
		super(ChooseOverloadAction, self).__init__(A.ADD_METHOD_OVERLOAD)
		self.method_overload = AddMethodOverrideChooseArgAction()
		self.constr_overload = CA.AddConstructorOverloadChooseArgAction()

	def setView(self, view):
		super(ChooseOverloadAction, self).setView(view)
		self.method_overload.setView(view)
		self.constr_overload.setView(view)

	def setCode(self, code_region):
		super(ChooseOverloadAction, self).setCode(code_region)
		self.method_overload.setCode(code_region)
		self.constr_overload.setCode(code_region)

	def is_applicable(self):
		return self.method_overload.is_applicable() or self.constr_overload.is_applicable()

	def run(self, edit, args):
		if self.method_overload.is_applicable():
			self.method_overload.run(edit, args)
		if self.constr_overload.is_applicable():
			self.constr_overload.run(edit, args)
