import sys
import imp
import sublime
import sublime_plugin


# Make sure all dependencies are reloaded on upgrade
reloader_path = 'ApexSmartCompletions.helpers.reloader'
if reloader_path in sys.modules:
	imp.reload(sys.modules[reloader_path])

from .helpers import reloader
reloader.reload()

# from . import logger
# log = logger.get(__name__)
from .helpers import ActionStore as AS


class ShowActionsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = self.view.sel()[0]
		line = self.view.substr(self.view.line(region))
		print('line >>> ', line)
		items = AS.getActions(line)
		print('>>> ', items)
		self.view.window().show_quick_panel(list(items), self.onDone)

	def onDone(self, index):
		pass
