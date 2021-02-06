release: python manage.py migrate && python manage.py populate_db && cd ecommerce_scraper && python run.py
web: gunicorn backend.wsgi
