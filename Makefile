deploy: production_deps tests
	@echo 'Deploying...'
	@/usr/local/google_appengine/appcfg.py update .

run:
	@/usr/local/google_appengine/dev_appserver.py .

production_deps: update_werkezeug update_jinja2 update_flask update_wtforms update_flask_wtf update_simplejson
	@echo 'Cleaning deps dir'
	@rm -rf deps/*

update_werkzeug:
	@echo 'Updating Werkzeug...'
	@pip install werkzeug -d deps --no-dependencies
	@cd deps && tar -xzvf Werkzeug*
	@cp -r deps/Werkzeug*/werkzeug lib/
	@echo 'Done.'

update_jinja2:
	@echo 'Updating Jinja2...'
	@pip install jinja2 -d deps --no-dependencies
	@cd deps && tar -xzvf Jinja2*
	@cp -r deps/Jinja2*/jinja2 lib/
	@echo 'Done.'

update_flask:
	@echo 'Updating Flask...'
	@pip install flask -d deps --no-dependencies
	@cd deps && tar -xzvf Flask*
	@cp -r deps/Flask*/flask lib/
	@echo 'Done.'

update_wtforms:
	@echo 'Updating WTForms...'
	@pip install wtforms -d deps --no-dependencies
	@cd deps && unzip WTForms*
	@cp -r deps/WTForms*/wtforms lib/
	@echo 'Done.'

update_flask_wtf:
	@echo 'Updating Flask-WTF...'
	@pip install Flask-WTF -d deps --no-dependencies
	@cd deps && tar -xzvf Flask-WTF*
	@cp -r deps/Flask-WTF*/flaskext lib/
	@echo 'Done.'

update_simplejson:
	@echo 'Updating simplejson...'
	@pip install simplejson -d deps --no-dependencies
	@cd deps && tar -xzvf simplejson*
	@cp -r deps/simplejson*/simplejson lib/
	@echo 'Done.'

bootstrap: dependencies
	@echo 'Creating the settings.py file...'
	@python mk_settings.py
	@echo 'Done.'
	@echo 'Creating the deps directory...'
	@mkdir -p deps
	@echo 'Done.'

dependencies: nose coverage mocker lxml

nose:
	@echo 'Installing nose if needed...'
	@python -c 'import nose' 2>/dev/null || pip install nose NoseGAE

coverage:
	@echo 'Installing coverage nose plugin if needed...'
	@python -c 'import coverage' 2>/dev/null || pip install coverage

mocker:
	@echo 'Installing mocker if needed...'
	@python -c 'import mocker' 2>/dev/null || pip install mocker

lxml:
	@echo 'Installing lxml if needed...'
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
