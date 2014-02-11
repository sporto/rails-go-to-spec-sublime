import sublime, sublime_plugin, os
import RailsGoToSpec.resolver

class RailsGoToSpecCommand(sublime_plugin.WindowCommand):

	def run(self):
		sublime.status_message('Running Rails Go To Spec')
		win = self.window
		view = win.active_view()
		current_file = view.file_name()
		if os.name == 'nt':
			current_file = current_file.replace('\\', '/')
		other_file = RailsGoToSpec.resolver.Resolver().run(current_file)
		self.open(other_file)

	def is_enabled(self):
		return self.window.active_view() != None

	def open(self, file):
		sublime.status_message("Trying to open " + file)
		if file == "":
			sublime.status_message("Not a valid file")
			return
		if os.path.exists(file):
			sublime.status_message("File exists " + file)
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
