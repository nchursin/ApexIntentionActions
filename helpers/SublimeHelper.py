import sublime


class SublimeHelper():
	def __init__(self, view):
		super(SublimeHelper, self).__init__()
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
