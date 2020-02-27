install:
	python2 setup.py build
	python2 setup.py install
release:
	python2 setup.py register
	python2 setup.py sdist upload
