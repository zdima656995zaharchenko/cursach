run:
	python app/manage.py runserver

migrate:
	python app/manage.py migrate

makemigrations:
	python app/manage.py makemigrations

shell:
	python app/manage.py shell_plus --print-sql
worker:
    cd app ; celery -A settings worker -l info

beat:
    cd app ; celery -A settings beat -l info


from currency.tasks import parse_monobank;parse_monobank()

user = User.objects.first()
