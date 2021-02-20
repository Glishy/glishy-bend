clean:
	@ echo 'cleaning...'
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete


makemigrations:
	@ echo 'creating migrations...'
	python manage.py makemigrations

migrate:
	@ echo 'creating migrations...'
	python manage.py migrate

install:
	@ echo 'Installing dependencies...'
	pipenv install

test:
	coverage run --source=app manage.py test --verbosity=2  && coverage report -m

run:
	@ echo 'starting server...'
	python manage.py runserver


lint:
	@ echo 'Autopep8 linting...'
	autopep8 --in-place --recursive --aggressive --aggressive .

	@ echo 'linting...'
	flake8 .

run_celery:
	celery -A app worker -l info --pool=gevent