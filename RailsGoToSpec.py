import sublime, sublime_plugin
import os.path
import re

class RailsGoToSpecCommand(sublime_plugin.WindowCommand):
	def run(self):
		win = self.window
		view = win.active_view()
		current_file = view.file_name()
		spec = self.spec_from_file(current_file)
		self.open_spec(spec)

	def is_enabled(self):
		return self.window.active_view() != None

	# given a file without extension
	# return the spec file
	def spec_from_file(self, file):
		res = re.sub(r'\.rb$', '_spec.rb', file)
		if res == file:
			return ""
		res = re.sub(r'/app/', '/spec/', res)
		if res == file:
			return ""
		return res

	def open_spec(self, file):
		if file == "":
			sublime.status_message("Not a valid .rb file")
			return
		if os.path.exists(file):
			self.window.open_file(file)
			sublime.status_message("Opening " + file)
		else:
			sublime.status_message("Cannot find spec! " +  file)
			if sublime.ok_cancel_dialog("Create spec? " + file):
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
			# if self.is_python:
			# 	open(os.path.join(base, '__init__.py'), 'w').close()
