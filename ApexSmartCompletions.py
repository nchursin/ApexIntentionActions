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


class ShowActionsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			print("region >> ", self.view.substr(self.view.line(region)))
