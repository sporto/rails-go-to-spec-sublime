import re
from functools import reduce

def pipe(data, *functions):
	return reduce(lambda x, f: f(x), functions, data)

def spec_to_code(file):
	return try_match(
		file,
		[
			view_spec_to_code,
			controller_spec_to_code,
			lib_spec_to_code,
			initializer_spec_to_code,
			generic_spec_to_code,
		]
	)

def code_to_spec(file):
	return try_match(
		file,
		[
			view_code_to_spec,
			controller_code_to_spec,
			lib_root_code_to_spec,
			initializer_code_to_spec,
			generic_code_to_spec,
		]
	)

def try_match(file, fns):
	for fn in fns:
		result = fn(file)
		if result:
			return result
			break
	return None


def switch_to_spec_dir(file):
	return file.replace("/app/", "/spec/")

def switch_to_app_dir(file):
	return file.replace("/spec/", "/app/")

def add_spec_extension(file):
	return file.replace(".rb", "_spec.rb")

def remove_spec_extension(file):
	return file.replace("_spec.rb", ".rb")

def is_controller_code(file):
	return file.find("app/controllers") > -1

def is_controller_spec(file):
	return file.find("spec/controllers") > -1 or file.find("spec/requests") > -1

def is_root_lib_code(file):
	return file.find("app/lib/") == -1 and file.find("/lib/") > -1

def is_view_file(file):
	view_regex = re.compile(r'.erb$|.haml$|.slim$')
	return bool(re.search(view_regex, file))

def is_view_spec(file):
	view_regex = re.compile(r'(.erb|.haml|.slim)_spec.rb$')
	return bool(re.search(view_regex, file))

def view_code_to_spec(file):
	if is_view_file(file):
		view_spec = file \
			.replace("/app/", "/spec/") \
			.replace(".haml", ".haml_spec.rb") \
			.replace(".erb", ".erb_spec.rb") \
			.replace(".slim", ".slim_spec.rb")
		return [view_spec]
	else:
		return None

def view_spec_to_code(file):
	if is_view_spec(file):
		view_file = file \
			.replace("_spec.rb", "") \
			.replace("/spec", "/app")
		return [view_file]
	else:
		return None

def controller_code_to_spec(file):
	if is_controller_code(file):
		controller_file = pipe(file, switch_to_spec_dir, add_spec_extension)
		request_file = controller_file.replace("/controllers/", "/requests/")
		return [request_file, controller_file]
	else:
		return None

def controller_spec_to_code(file):
	is_controller = is_controller_spec(file)
	if is_controller:
		controller_file = pipe(file, remove_spec_extension, switch_to_app_dir).replace("/requests/", "/controllers/")
		return [controller_file]
	else:
		return None

def lib_root_code_to_spec(file):
	if is_root_lib_code(file):
		lib_spec_file = pipe(file, add_spec_extension).replace("/lib/", "/spec/lib/")
		return [lib_spec_file]
	else:
		return None

def lib_spec_to_code(file):
	is_lib = file.find("/spec/lib/") > -1
	if is_lib:
		lib_root_file = remove_spec_extension(file)\
			.replace("/spec/lib/", "/lib/")

		lib_app_file = pipe(file, switch_to_app_dir, remove_spec_extension)
		return [lib_root_file, lib_app_file]
	else:
		return None

def initializer_code_to_spec(file):
	if file.find("/config/initializers") > -1:
		target_file = add_spec_extension(file)\
			.replace("/config/initializers/", "/spec/config/initializers/")

		return [target_file]
	else:
		return None

def initializer_spec_to_code(file):
	if file.find("/spec/config/initializers/") > -1:
		target_file = remove_spec_extension(file)\
			.replace("/spec/", "/")

		return [target_file]
	else:
		return None

def generic_code_to_spec(file):
	spec_file = pipe(file,
		switch_to_spec_dir,
		add_spec_extension
	)
	return [spec_file]

def generic_spec_to_code(file):
	code_file = pipe(file, switch_to_app_dir, remove_spec_extension)
	return [code_file]

class Resolver:

	def is_spec(self, file):
		return file.find('_spec.rb') != -1

	def get_related(self, file):
		if self.is_spec(file):
			return spec_to_code(file)
		else:
			return code_to_spec(file)
