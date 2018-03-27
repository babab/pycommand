.PHONY: help uninstall dev install distrib readme

VERSION = '0.4.0'

help:
	@echo 'dev     - uninstall and create dev install (uses sudo!!)'
	@echo 'install - uninstall and do a wheel install (uses sudo!!)'
	@echo 'distrib - n/a'
	@echo 'readme  - concat README and CHANGELOG and convert with rst2html'

uninstall:
	-(pip freeze | grep pycommand && sudo pip uninstall --yes pycommand) || true
dev: uninstall
	rm -rf dist
	sudo pip install -e .

install: uninstall distrib
	sudo pip install dist/pycommand-${VERSION}-py2.py3-none-any.whl
	rm -rf __pycache__ build pycommand.egg-info
distrib:
	python setup.py sdist bdist_wheel
readme:
	cat README.rst > index.rst
	echo >> index.rst
	cat CHANGELOG.rst >> index.rst
	rst2html.py index.rst > index.html
	rm index.rst
