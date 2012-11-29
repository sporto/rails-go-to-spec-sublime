# import sublime
import re

class Resolver:

	def run(self, file):
		if self.is_spec(file):
			return self.get_source(file)
		else:
			return self.get_spec(file)

	def is_spec(self, file):
		return file.find('_spec.rb') != -1

	def get_source(self, file):
		# find erb, haml
		match = re.search(r'(.erb|.haml)_spec.rb$', file)
		if match:
			ext = match.group(0)
			regex = re.escape(ext)
			ext = re.sub(r'_spec.rb', '', ext)
			file = re.sub(regex, ext, file)
		else:
			file = re.sub(r'\_spec.rb$', '.rb', file)

		if file.find('/spec/lib/') > -1:
			file = re.sub(r'/spec/lib/', '/lib/', file)
		else:
			file = re.sub(r'/spec/', '/app/', file)

		return file


	def get_spec(self, file):
		# find erb, haml
		match = re.search(r'erb$|haml$', file)
		if match:
			ext = match.group(0)
			regex = re.escape(ext) + "$"
			file = re.sub(regex, ext + '_spec.rb', file)
		else:
			file = re.sub(r'\.rb$', '_spec.rb', file)

		if file.find('/lib/') > -1:
			file = re.sub(r'/lib/', '/spec/lib/', file)
		else:
			file = re.sub(r'/app/', '/spec/', file)
		return file