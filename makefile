all: html pdf deploy

docs:
	make html && make pdf
	
deploy-docs: html commit
	git subtree push --prefix docs/build/html origin gh-pages

commit: 
	git commit -am 'docs deploy'

html: apidocs
	cd docs && make html

apidocs:
	cd main; sphinx-apidoc -f --separate -o ../docs/source/code . config.py secrets.py sandbox.py old_stuff.py

pdf:
	cd docs && make latexpdf

dependecies-graph:
	sfood main/twitter_analysis.py --follow --internal | sfood-graph | dot -Tpdf | xargf evince

watch:
	watchman watch . ; watchman -- trigger docs build -- make html 

