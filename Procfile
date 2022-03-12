release: python manage.py migrate && python manage.py flush --noinput && python manage.py loaddata */fixtures/*.json
web: gunicorn backend.wsgi
