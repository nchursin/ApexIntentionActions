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


log = logger.get(__name__)


class ShowActionsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.edit = edit
		region = self.view.sel()[0]
		self.subl_line = self.view.line(region)
		items = AS.getActions(self.view, self.subl_line)
		self.actions = list(items)
		names = self.getActionNames(self.actions)
		if names:
			self.view.window().show_quick_panel(list(names), self.onDone)
		else:
			log.info('No quick actions found')

	def onDone(self, index):
		if(-1 == index):
			return
		args = {
			'action_name': self.actions[index].action.name,
			'subl_line_start': self.subl_line.a,
			'subl_line_end': self.subl_line.b
		}
		self.view.run_command('run_action', args)
		del self.actions
		del self.names

	def getActionNames(self, items):
		names = []
		real_actions = []
		for i in items:
			if i.action.is_applicable():
				names.append(i.message)
				real_actions.append(i)
		self.actions = real_actions
		return names


class RunActionCommand(sublime_plugin.TextCommand):
	def run(self, edit, action_name, subl_line_start, subl_line_end):
		log.info("Firing action: " + action_name)
		action = AS.actions[action_name]
		action.setView(self.view)
		action.setCode(sublime.Region(subl_line_start, subl_line_end))
		action.generate_code(edit)
		del action
