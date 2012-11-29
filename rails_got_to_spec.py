import sublime, sublime_plugin
from resolver import *

class RailsGoToSpecCommand(sublime_plugin.WindowCommand):
	
	def run(self):
		win = self.window
		view = win.active_view()
		current_file = view.file_name()
		other_file = Resolver().run(current_file)
		self.open(other_file)

	def is_enabled(self):
		return self.window.active_view() != None

	def open(self, file):
		if file == "":
			sublime.status_message("Not a valid file")
			return
		if os.path.exists(file):
			self.window.open_file(file)
			sublime.status_message("Opening " + file)
		else:
			sublime.status_message("Cannot find file! " +  file)
			if sublime.ok_cancel_dialog("Create file? " + file):
				self.create(file)
				self.window.open_file(file)

	def create(self, filename):
		base, filename = os.path.split(filename)
		self.create_folder(base)

	def create_folder(self, base):
		if not os.path.exists(base):
			parent = os.path.split(base)[0]
			if not os.path.exists(parent):
				self.create_folder(parent)
			os.mkdir(base)