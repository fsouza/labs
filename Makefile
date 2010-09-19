deploy:
	@echo 'Deploying...'
	@/usr/local/google_appengine/appcfg.py update .

run:
	@/usr/local/google_appengine/dev_appserver.py .

bootstrap: dependencies
	@echo 'Creating the settings.py file...'
	@python mk_settings.py
	@echo 'Done.'

dependencies: nose coverage mocker lxml

nose:
	@echo 'Installing nose...'
	@python -c 'import nose' 2>/dev/null || pip install nose NoseGAE

coverage:
	@echo 'Installing coverage nose plugin...'
	@python -c 'import coverage' 2>/dev/null || pip install coverage

mocker:
	@echo 'Installing mocker...'
	@python -c 'import mocker' 2>/dev/null || pip install mocker

lxml:
	@echo 'Installing lxml...'
	@python -c 'import lxml' 2>/dev/null || pip install lxml

tests: dependencies clean
	@echo 'Running all tests...'
	@nosetests -s --verbosity=2 -w tests --with-coverage --cover-package=labs --with-gae --gae-application=.

functional: dependencies clean
	@echo 'Running functional tests...'
	@nosetests -s --verbosity=2 -w tests/functional --with-coverage --cover-package=labs --with-gae --gae-application=.

unit: dependencies clean
	@echo 'Running unit tests...'
	@nosetests -s --verbosity=2 -w tests/unit --with-coverage --cover-package=labs --with-gae --gae-application=.

clean:
	@echo 'Cleaning...'
	@find . -name "*.pyc" -exec rm -f {} \;
	@rm -f .coverage
	@echo 'Done.'
