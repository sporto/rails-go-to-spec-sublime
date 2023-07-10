# to run
# python resolver_test.py

import unittest
try:
	from .resolver import *
except ImportError:
	from resolver import *


class ResolverTest(unittest.TestCase):

	def test_is_spec_is_true(self):
		file = "/spec/foo/something_spec.rb"
		actual = Resolver().is_spec(file)
		self.assertEqual(actual, True)

	def test_is_spec_returns_true_for_erb_spec(self):
		file = "/spec/views/something.html.erb_spec.rb"
		r = Resolver().is_spec(file)
		self.assertEqual(r, True)

	def test_is_spec_returns_false(self):
		file = "/app/foo/something.rb"
		r = Resolver().is_spec(file)
		self.assertEqual(r, False)

	def test_is_spec_returns_false_for_erb(self):
		file = "/spec/views/something.html.erb.rb"
		r = Resolver().is_spec(file)
		self.assertEqual(r, False)

	def test_is_spec_returns_false_for_jbuilder(self):
		file = "/spec/views/something.json.jbuilder"
		r = Resolver().is_spec(file)
		self.assertEqual(r, False)

	# get_related

	def assert_get_related(self, file, expected):
		actual = Resolver().get_related(file)
		self.assertEqual(actual, expected)

	def test_get_related_controller(self):
		self.assert_get_related(
			"/app/controllers/users_controller.rb",
			[
				"/spec/requests/users_controller_spec.rb",
				"/spec/controllers/users_controller_spec.rb",
			]
		)

	def test_get_related_nested_controller(self):
		self.assert_get_related(
			"/app/controllers/clients/users_controller.rb",
			[
				"/spec/requests/clients/users_controller_spec.rb",
				"/spec/controllers/clients/users_controller_spec.rb",
			]
		)

	def test_get_related_controller_spec(self):
		self.assert_get_related(
			"/spec/controllers/users_controller_spec.rb",
			[
				"/app/controllers/users_controller.rb",
			]
		)

	def test_get_related_nested_controller_spec(self):
		self.assert_get_related(
			"/spec/controllers/clients/users_controller_spec.rb",
			[
				"/app/controllers/clients/users_controller.rb",
			]
		)

	def test_get_related_request_spec(self):
		self.assert_get_related(
			"/spec/requests/users_controller_spec.rb",
			[
				"/app/controllers/users_controller.rb",
			]
		)


	def test_get_related_model(self):
		self.assert_get_related(
			"/app/models/user.rb",
			[
				"/spec/models/user_spec.rb",
			]
		)

	def test_get_related_model_spec(self):
		self.assert_get_related(
			"/spec/models/user_spec.rb",
			[
				"/app/models/user.rb",
			]
		)

	def test_get_related_view(self):
		self.assert_get_related(
			"/app/views/namespace/users/_show.html.erb",
			[
				"/spec/views/namespace/users/_show.html.erb_spec.rb",
			]
		)

	def test_get_related_view_spec(self):
		self.assert_get_related(
			"/spec/views/namespace/users/_show.html.erb_spec.rb",
			[
				"/app/views/namespace/users/_show.html.erb",
			]
		)

	def test_get_related_view_haml(self):
		self.assert_get_related(
			"/app/views/namespace/users/_show.html.haml",
			[
				"/spec/views/namespace/users/_show.html.haml_spec.rb",
			]
		)

	def test_get_related_view_haml_spec(self):
		self.assert_get_related(
			"/spec/views/namespace/users/_show.html.haml_spec.rb",
			[
				"/app/views/namespace/users/_show.html.haml",
			]
		)

	def test_related_lib(self):
		self.assert_get_related(
			"/lib/something/foo.rb",
			[
				"/spec/lib/something/foo_spec.rb",
			]
		)

	def test_related_app_lib(self):
		self.assert_get_related(
			"/app/lib/something/foo.rb",
			[
				"/spec/lib/something/foo_spec.rb",
			]
		)

	def test_related_lib_spec(self):
		self.assert_get_related(
			"/spec/lib/something/foo_spec.rb",
			[
				"/lib/something/foo.rb",
				"/app/lib/something/foo.rb",
			]
		)

	def test_related_initializer(self):
		self.assert_get_related(
			"/config/initializers/foo.rb",
			[
				"/spec/config/initializers/foo_spec.rb",
			]
		)

	def test_related_initializer_spec(self):
		self.assert_get_related(
			"/spec/config/initializers/foo_spec.rb",
			[
				"/config/initializers/foo.rb",
			]
		)

if __name__ == '__main__':
	unittest.main()
