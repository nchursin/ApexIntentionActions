import sublime
from . import logger
from . import Actions as A
from . import RegexHelper as re
from . import TemplateHelper as TH
from . import SublimeHelper as SH


log = logger.get(__name__)


class ConstructorAction(A.Action):
	def __init__(self, name):
		super(ConstructorAction, self).__init__(name)

	def get_class_code(self):
		return self.full_region(self.code_region)

	def get_class_name(self):
		result = re.findConstructorClassName(self.to_text())
		log.debug('constructor name >> ', result)
		return result

	def get_access_level(self):
		result = re.findConstructorAccessLevel(self.to_text())
		log.debug('constructor access level >> ', result)
		return result

	def get_constructor_defn(self):
		return self.to_text()

	def is_applicable(self):
		return re.is_constructor_def(self.to_text())

	def get_arguments(self):
		result = re.findConstructorArgs(self.to_text())
		return [el.strip() for el in re.split_arguments(result)]


class AddConstructorOverloadChooseArgAction(ConstructorAction):
	def __init__(self):
		super(AddConstructorOverloadChooseArgAction, self).__init__(A.ADD_CONSTRUCTOR_OVERRIDE)

	def run(self, edit, args):
		self.set_menu()
		args_def = self.get_arguments()
		self.show_menu(list(args_def), self.fire_action)

	def fire_action(self, index):
		if(-1 == index):
			return
		args = {
			'action_name': A.ADD_CONSTRUCTOR_OVERRIDE_CREATE,
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


class AddConstructorOverloadAction(ConstructorAction):
	def __init__(self):
		super(AddConstructorOverloadAction, self).__init__(A.ADD_CONSTRUCTOR_OVERRIDE_CREATE)

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
		prev_line = self.view.line(place_to_insert)
		prev_line = self.to_text(prev_line)
		if not prev_line and ' ' not in prev_line and '\t' not in prev_line:
			indent += '\t'
		else:
			indent = ''
		template = TH.Template('other/ctor-overload')
		template.addVar('className', self.get_class_name())
		template.addVar('indent', indent)
		template.addVar('access', self.get_access_level())
		template.addVar('args', ', '.join(self.args_def))
		template.addVar('argsToPass', ', '.join(self.args_pass))
		code_to_insert = '\n' + template.compile()
		self.insaert_if_none(code_to_insert)

	def insaert_if_none(self, code_to_insert):
		code_splitted = code_to_insert.split('\n')
		for line in code_splitted:
			if line:
				definition = line.strip()
				break
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

	def is_applicable(self):
		result = super(AddConstructorOverloadAction, self).is_applicable()
		return result and re.find(re.CONSTRUCTOR_WITH_ARGS, self.to_text())
