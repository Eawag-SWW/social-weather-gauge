server:
	# Start a local server which serves the documentation.
	cd docs/build/html; browser-sync start --server --files="chapters/*.html"

docs:
	# Generate html and pdf docs.
	make html && make pdf
	
deploy-docs: html commit
	# Deploy documentation website.
	git subtree push --prefix docs/build/html origin gh-pages

commit: 
	git commit -am 'docs deploy'

html: apidocs-main apidocs-apis
	cd docs && make html

apidocs-main:
	cd main; sphinx-apidoc -f --separate --no-toc -o ../docs/source/code . config.py secrets.py sandbox.py old_stuff.py;

apidocs-apis:
	cd apis; sphinx-apidoc -f --separate --no-toc -o ../docs/source/code .

pdf:
	cd docs && make latexpdf

dependecies-graph:
	sfood main/twitter_analysis.py --follow --internal | sfood-graph | dot -Tpdf | xargf evince

watch:
	watchman watch . ; watchman -- trigger docs build -- make html 

