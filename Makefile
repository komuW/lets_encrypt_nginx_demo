
# for dev debugging.
superuser:
	@python manage.py createsuperuser --settings=settings.development

shell:
	@python manage.py shell_plus --settings=settings.development

mk:
	@python manage.py makemigrations lets_encrypt_demo --settings=settings.development

flush:
	@python manage.py flush --no-initial-data --settings=settings.development

reload:
	@ansible-playbook devops/deploy.yml -i devops/inventory/development --limit=all


run3:
	@sudo killall -9 supervisord | echo 
	@sudo killall -9 gunicorn | echo
	@python manage.py validate --settings=settings.development &
	@python manage.py collectstatic --noinput --settings=settings.development &
	@python manage.py syncdb --settings=settings.development &
	@python manage.py migrate --settings=settings.development &
	@export DJANGO_SETTINGS_MODULE="settings.development" & \
	authbind /home/vagrant/.virtualenvs/lets_encrypt_demo/bin/gunicorn wsgi:application \
    --workers=3 \
    --bind="0.0.0.0:3000" \
    --log-level debug \
    --reload

configure:
	@ansible-playbook devops/site.yml -i devops/inventory/staging --limit=all

deploy:
	@ansible-playbook devops/deploy.yml -i devops/inventory/staging --limit=all 
