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
		match = re.search(r'(.erb|.haml|.slim|.jbuilder)_spec.rb$', file)
		related = []

		if match:
			ext = match.group(0)
			regex = re.escape(ext)
			ext = re.sub(r'_spec.rb', '', ext)
			file = re.sub(regex, ext, file)
		else:
			# simply sub .rb to _spec.rb
			# e.g. foo.rb -> foo_spec.rb
			file = re.sub(r'\_spec.rb$', '.rb', file)

		if file.find('/spec/lib/') > -1:
			# file in lib
			related.append(re.sub(r'/spec/lib/', '/lib/', file))
		else:
			related.append(re.sub(r'/spec/', '/app/', file, 1))
			related.append(re.sub(r'/spec/', '/', file, 1))

		return related


	def get_spec(self, file):
		# find erb, haml
		match = re.search(r'erb$|haml$|slim$|jbuilder$', file)
		related = []

		if match:
			ext = match.group(0)
			regex = re.escape(ext) + "$"
			file = re.sub(regex, ext + '_spec.rb', file)
		else:
			file = re.sub(r'\.rb$', '_spec.rb', file)

		if file.find('/lib/') > -1:
			related.append(re.sub(r'/lib/', '/spec/lib/', file))
		elif file.find('/app/') > -1:
			related.append(re.sub(r'/app/', '/spec/', file, 1))
		else:
			related.append('/spec' + file)

		return related
