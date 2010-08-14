test: unit functional

functional: clean
	@echo 'Running functional tests...'
	@nosetests -s --verbosity=2 -w tests/functional --with-coverage --cover-package=labs --with-gae --gae-application=.

unit: clean
	@echo 'Running unit tests...'
	@nosetests -s --verbosity=2 -w tests/unit --with-coverage --cover-package=labs --with-gae --gae-application=.

clean:
	@echo 'Cleaning...'
	@find . -name "*.pyc" -exec rm -f {} \;
	@rm -f .coverage
	@echo 'Done.'
