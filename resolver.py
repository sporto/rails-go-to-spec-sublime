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
		if file.find('erb_spec.rb') > -1:
			file = re.sub(r'erb_spec.rb$', 'erb', file)
		else:
			file = re.sub(r'\_spec.rb$', '.rb', file)

		if file.find('/spec/lib/') > -1:
			file = re.sub(r'/spec/lib/', '/lib/', file)
		else:
			file = re.sub(r'/spec/', '/app/', file)

		return file


	def get_spec(self, file):
		file = re.sub(r'\.rb$', '_spec.rb', file)
		if file.find('/lib/') > -1:
			file = re.sub(r'/lib/', '/spec/lib/', file)
		else:
			file = re.sub(r'/app/', '/spec/', file)
		return file