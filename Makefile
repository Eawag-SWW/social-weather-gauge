deploy: html
	git subtree push --prefix docs/build/html origin gh-pages

html:
	cd docs && make html

apidocs:
	sphinx-apidoc -o docs/source . secrets.py sandbox.py old_stuff.py