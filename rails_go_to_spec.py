import sublime, sublime_plugin, os
import RailsGoToSpec.resolver
import re

class RailsGoToSpecCommand(sublime_plugin.WindowCommand):

	def run(self):
		sublime.status_message('Running Rails Go To Spec')
		win = self.window
		view = win.active_view()
		current_file = view.file_name()

		# remove the root dir
		root_path = win.folders()[0]
		current_file = re.sub(root_path, '', current_file)

		if os.name == 'nt':
			current_file = current_file.replace('\\', '/')

		spec_base = view.settings().get('go_to_spec_directory') or 'spec'

		related_files = RailsGoToSpec.resolver.Resolver()\
			.get_related(current_file, spec_base)

		# add the root dir to all files
		for ix, file in enumerate(related_files):
			related_files[ix] = root_path + file

		self.open_any(related_files)

	def is_enabled(self):
		return True
		# return self.window.active_view() != None

	def open_any(self, files):
		if len(files) == 0:
			sublime.status_message("Not a valid file")
			return

		opened = False
		for file in files:
			if not opened:
				opened = self.open(file)

		if opened:
			return

		first = files[0]
		if sublime.ok_cancel_dialog("Create file? " + first):
			self.create(first)
			self.window.open_file(first)


	def open(self, file):
		if file == "":
			sublime.status_message("Not a valid file")
			return False

		if os.path.exists(file):
			sublime.status_message("File exists " + file)
			self.window.open_file(file)
			sublime.status_message("Opening " + file)
			return True
		else:
			return False

	def create(self, filename):
		base, filename = os.path.split(filename)
		self.create_folder(base)

	def create_folder(self, base):
		if not os.path.exists(base):
			parent = os.path.split(base)[0]
			if not os.path.exists(parent):
				self.create_folder(parent)
			os.mkdir(base)
