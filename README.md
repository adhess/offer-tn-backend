
# Backend

## install dependency
`pip install pipenv`
`pipenv install`
`pipenv shell`

## migrate database
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## populate database with data (except for product data)
use this when you want to generate the data necessary for the scrapper only

`python3 manage.py populate_db`

## populate entire database
python3 manage.py populate_db --all