deploy: html commit
	git subtree push --prefix docs/build/html origin gh-pages

commit: 
	git commit -am 'misc'

html:
	cd docs && make html

apidocs:
	sphinx-apidoc -o docs/source . secrets.py sandbox.py old_stuff.py