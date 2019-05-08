# -------------------------------------
# MAKEFILE
# -------------------------------------


#
# commands for artifact cleanup
#

.PHONY: clean
clean: clean.build clean.pyc

.PHONY: clean.build
clean.build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

.PHONY: clean.pyc
clean.pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete


#
# commands for testing
#

.PHONY: test
test: test.unittests test.flake8

.PHONY: test.flake8
test.flake8:
	flake8 .

.PHONY: test.unittests
test.unittests:
	PYTHONPATH=${PYTHONPATH} python runtests.py


#
# commands for packaging and deploying to pypi
#

.PHONY: sdist
sdist: test
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: release
release: clean sdist
	twine upload dist/*
