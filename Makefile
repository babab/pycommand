.PHONY: make uninstall dev install distrib

help:
	@echo 'dev     - uninstall and create dev install (uses sudo!!)'
	@echo 'install - uninstall and do a wheel install (uses sudo!!)'
	@echo 'distrib - n/a'

uninstall:
	-(pip freeze | grep pycommand && sudo pip uninstall --yes pycommand) || true
dev: uninstall
	rm -rf dist
	sudo pip install -e .

install: uninstall
	python setup.py bdist_wheel
	sudo pip install dist/pycommand-0.3.0-py2.py3-none-any.whl
	rm -rf __pycache__ build pycommand.egg-info
distrib:
	true
