test: clean
	@echo 'Running tests...'
	@nosetests -s --verbosity=2 -w tests --with-coverage --cover-package=labs --with-gae --gae-application=.

clean:
	@echo 'Cleaning...'
	@find . -name "*.pyc" -exec rm -f {} \;
	@rm -f .coverage
	@echo 'Done.'
