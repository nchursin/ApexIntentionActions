import sublime


class ViewHelper():
	def __init__(self, view):
		self.view = view

	def insert_snippet(self, snippet, coords):
		if isinstance(coords, sublime.Region):
			self.insert_to_region(snippet, coords)
		elif isinstance(coords, tuple):
			region = sublime.Region(coords[0], coords[1])
			self.insert_to_region(snippet, region)
		else:
			region = sublime.Region(coords, coords)
			self.insert_to_region(snippet, region)

	def insert_to_region(self, snippet, region):
		self.view.sel().clear()
		self.view.sel().add(region)
		self.view.run_command("insert_snippet", {"contents": snippet})

	def open_menu(self, *kwargs):
		settings = sublime.load_settings('SmartApexPrefs.sublime-settings')
		intention_menu_mode = settings.get("intention_menu_mode")
		if "quickpanel" == intention_menu_mode.lower():
			show_menu = self.view.window().show_quick_panel
		elif "popup" == intention_menu_mode.lower():
			show_menu = self.view.show_popup_menu
		return show_menu(*kwargs)


def get_setting(setting_name, settings_file='SmartApexPrefs.sublime-settings'):
	settings = sublime.load_settings(settings_file)
	result = settings.get(setting_name)
	return result
