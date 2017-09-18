Rails Go to Spec
================

A Sublime Text 3 plug-in. From a .rb file this plug-in will open the relevant spec. If the spec doesn't exist it asks if it should be created.

Only supports _spec.rb files at the moment.

Installation
------------

Using Sublime Package Control
http://wbond.net/sublime_packages/package_control

Install rails_go_to_spec

By default, specs are assumed to live in "/spec", but if you have a nonstandard
location, you can override with the "go_to_spec_directory" setting in your preferences.

Usage
-----
- Run from menu > Goto > Rails Go to Spec
- Default key binding is command + shift + y
- Or run from command palette 'Rails Go to Spec'

Dev
----

git clone git@github.com:sporto/rails_go_to_spec.git RailsGoToSpec

Testing
-------

  python resolver_test.py

Acknowledgements
-----------

Thanks to [reInteractive](http://www.reinteractive.net/) for providing the time to work on this.
