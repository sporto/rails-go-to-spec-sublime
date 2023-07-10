import re

def code_to_spec(file):
	with_spec_ext = add_spec_extension(file)
	return switch_to_spec_dir(with_spec_ext)

def spec_to_code(file):
	without_spec_ext = remove_spec_extension(file)
	return switch_to_code_dir(without_spec_ext)

def switch_to_spec_dir(file):
	if file.startswith("/app/controllers/"):
		return [
			file.replace("/app/controllers/", "/spec/requests/"),
			file.replace("/app/controllers/", "/spec/controllers/"),
		]
	elif file.startswith("/app/"):
		return [
			file.replace("/app/", "/spec/"),
		]
	else:
		return [
			f"/spec{file}"
		]

def switch_to_code_dir(file):
	if file.startswith("/spec/config/initializers/"):
		return [
			file.replace("/spec/", "/"),
		]
	elif file.startswith("/spec/lib/"):
		return [
			file.replace("/spec/", "/"),
			file.replace("/spec/", "/app/"),
		]
	elif file.startswith("/spec/requests/"):
		return [
			file.replace("/spec/requests/", "/app/controllers/"),
		]
	else:
		return [
			file.replace("/spec/", "/app/"),
		]

def is_view_file(file):
	view_regex = re.compile(r'.erb$|.haml$|.slim$')
	return bool(re.search(view_regex, file))

def add_spec_extension(file):
	if is_view_file(file):
		return file\
			.replace(".erb", ".erb_spec.rb")\
			.replace(".haml", ".haml_spec.rb")\
			.replace(".slim", ".slim_spec.rb")
	else:
		return file.replace(".rb", "_spec.rb")

def remove_spec_extension(file):
	return file\
		.replace(".erb_spec.rb", ".erb")\
		.replace(".haml_spec.rb", ".haml")\
		.replace(".slim_spec.rb", ".slim")\
		.replace("_spec.rb", ".rb")

class Resolver:

	def is_spec(self, file):
		return file.find('_spec.rb') != -1

	def get_related(self, file):
		if self.is_spec(file):
			return spec_to_code(file)
		else:
			return code_to_spec(file)
