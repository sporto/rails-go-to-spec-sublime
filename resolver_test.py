# to run 
# python resolver_test.py

import unittest
from resolver import *

class ResolverTest(unittest.TestCase):

	def test_is_spec_returns_true(self):
		file = '/app/foo/something_spec.rb'
		r = Resolver().is_spec(file)
		self.assertEqual(r, True)

	def test_is_spec_returns_false(self):
		file = '/app/foo/something.rb'
		r = Resolver().is_spec(file)
		self.assertEqual(r, False)

	def test_get_source(self):
		file = '/spec/something/foo_spec.rb'
		r = Resolver().get_source(file)
		self.assertEqual(r, '/app/something/foo.rb')

	def test_get_source_lib(self):
		file = '/spec/lib/something/foo_spec.rb'
		r = Resolver().get_source(file)
		self.assertEqual(r, '/lib/something/foo.rb')

	def test_finds_spec(self):
		file = '/app/models/user.rb'
		r = Resolver().get_spec(file)
		self.assertEqual(r, '/spec/models/user_spec.rb')

	def test_finds_spec_in_lib(self):
		file = '/lib/foo/utility.rb'
		r = Resolver().get_spec(file)
		self.assertEqual(r, '/spec/lib/foo/utility_spec.rb')

	def test_run(self):
		file = '/app/decorators/namespace/user_decorator.rb'
		r = Resolver().run(file)
		self.assertEqual(r, '/spec/decorators/namespace/user_decorator_spec.rb')

	def test_run_from_lib(self):
		file = '/lib/utilities/namespace/foo.rb'
		r = Resolver().run(file)
		self.assertEqual(r, '/spec/lib/utilities/namespace/foo_spec.rb')

	def test_run_from_spec(self):
		file = '/spec/controllers/namespace/foo_controller_spec.rb'
		r = Resolver().run(file)
		self.assertEqual(r, '/app/controllers/namespace/foo_controller.rb')

	def test_run_from_spec_lib(self):
		file = '/spec/lib/namespace/foo_spec.rb'
		r = Resolver().run(file)
		self.assertEqual(r, '/lib/namespace/foo.rb')

if __name__ == '__main__':
	unittest.main()