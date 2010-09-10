deploy:
	@echo 'Deploying...'
	@/usr/local/google_appengine/appcfg.py update .

run:
	@/usr/local/google_appengine/dev_appserver.py .

bootstrap:
	@echo 'Installing all dependencies for development :)'
	@echo ''
	@echo 'Remember that you should have pip installed'
	@pip install -r dev-reqs.txt
	@echo 'Creating the settings.py file...'
	@python mk_settings.py
	@echo 'Done.'

tests: clean
	@echo 'Running all tests...'
	@nosetests -s --verbosity=2 -w tests --with-coverage --cover-package=labs --with-gae --gae-application=.

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
