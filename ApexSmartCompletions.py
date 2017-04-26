import sys
import imp
import sublime_plugin
import sublime


# Make sure all dependencies are reloaded on upgrade
reloader_path = 'ApexSmartCompletions.helpers.reloader'
if reloader_path in sys.modules:
	imp.reload(sys.modules[reloader_path])

from .helpers import reloader
reloader.reload()

# from . import logger
# log = logger.get(__name__)
from .helpers import logger
from .helpers import ActionStore as AS
from .helpers import Actions as A


log = logger.get(__name__)


class ShowActionsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.edit = edit
		region = self.view.sel()[0]
		self.subl_line = self.view.line(region)
		self.line = self.view.substr(self.subl_line)
		items = AS.getActions(self.line)
		if items:
			self.view.window().show_quick_panel(list(items), self.onDone)
		else:
			log.info('No quick actions found')

	def onDone(self, index):
		act = A.AddGetterAction()
		act.setView(self.view)
		act.setCode(self.subl_line)
		act.find_class_name()
		act.get_prop_name()
		act.get_prop_type()
		args = {
			'action_name': 'Test',
			'subl_line_start': self.subl_line.a,
			'subl_line_end': self.subl_line.b
		}
		self.view.run_command('run_action', args)


class RunActionCommand(sublime_plugin.TextCommand):
	def run(self, edit, action_name, subl_line_start, subl_line_end):
		action = A.AddGetterAction()
		action.setView(self.view)
		action.setCode(sublime.Region(subl_line_start, subl_line_end))
		action.generate_code(edit)
		del action
