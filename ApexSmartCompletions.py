import sys
import imp
import sublime_plugin
import sublime
import os.path

# 
# Demo piece of code
# Something more here
# And even here
# Well, that's enough
# 

# Make sure all dependencies are reloaded on upgrade
pack_name = os.path.dirname(os.path.realpath(__file__))
pack_name, pack_ext = os.path.splitext(pack_name)
pack_name = os.path.basename(pack_name)

reloader_path = pack_name + '.helpers.reloader'
if reloader_path in sys.modules:
	imp.reload(sys.modules[reloader_path])

from .helpers import reloader
reloader.reload()

from .helpers import logger
from .helpers import ActionStore as AS
from .helpers.SublimeHelper import ViewHelper as VH


log = logger.get(__name__)


class ShowActionsCommand(sublime_plugin.TextCommand):
	def is_enabled(self, edit=None):
		result = self.view.match_selector(0, 'source.apex')
		return result

	def is_visible(self, edit=None):
		return self.is_enabled(edit)

	def run(self, edit):
		self.ViewHelper = VH(self.view)

		self.edit = edit
		region = self.view.sel()[0]
		self.subl_line = self.view.line(region)
		line_text = self.view.substr(self.subl_line)
		while ';' not in line_text and '{' not in line_text:
			next_line_region = self.view.line(self.subl_line.end() + 1)
			self.subl_line = sublime.Region(self.subl_line.begin(), next_line_region.end())
			line_text = self.view.substr(self.subl_line)
		items = AS.getActions(self.view, self.subl_line)
		self.actions = list(items)
		names = self.getActionNames(self.actions)
		if names:
			self.ViewHelper.open_menu(list(names), self.fire_action)
		else:
			log.info('No quick actions found')

	def fire_action(self, index):
		if(-1 == index):
			return
		args = {
			'action_name': self.actions[index].action.name,
			'subl_line_start': self.subl_line.begin(),
			'subl_line_end': self.subl_line.end()
		}
		self.view.run_command('run_action', args)
		del self.actions

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
	def is_enabled(self, edit=None):
		result = self.view.match_selector(0, 'source.apex')
		return result

	def is_visible(self, edit=None):
		return self.is_enabled(edit)

	def run(self, edit, action_name, subl_line_start, subl_line_end, **args):
		log.info("Firing action: " + action_name)
		action = AS.actions[action_name]
		action.setView(self.view)
		action.setCode(sublime.Region(subl_line_start, subl_line_end))
		if action.is_applicable():
			action.run(edit, args)
		else:
			log.info("Action is not applicable.")
		del action


class RunActionCurrentLineCommand(sublime_plugin.TextCommand):
	def is_enabled(self, edit=None):
		result = self.view.match_selector(0, 'source.apex')
		return result

	def is_visible(self, edit=None):
		return self.is_enabled(edit)

	def run(self, edit, action_name, **args):
		log.info("Firing action: " + action_name)
		region = self.view.sel()[0]
		self.subl_line = self.view.line(region)
		action = AS.actions[action_name]
		action.setView(self.view)
		action.setCode(self.subl_line)
		if action.is_applicable():
			action.run(edit, args)
		else:
			log.info("Action is not applicable.")
		del action


class OpenApexInetntionActionsSettingsFileCommand(sublime_plugin.WindowCommand):
	def is_enabled(self, file, platform=None, default='{\n\n}'):
		return platform is None or platform.lower() == sublime.platform().lower()

	def is_visible(self, file, platform=None, default='{\n\n}'):
		return self.is_enabled(file, platform)

	def run(self, file, platform=None, default='{\n\t${0}\n}'):
		path = '${package}/' + file
		package = pack_name
		settings_file = sublime.expand_variables(path, {"package": package})
		settings_file = '${packages}/' + settings_file
		args = {
			'base_file': settings_file,
			'default': default
		}
		self.window.run_command('edit_settings', args)
