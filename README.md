
# Backend

## Install dependency
```
pip install pipenv
pipenv install
pipenv shell
```

## Migrate database
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Init database
Use this when you want to generate the data necessary for the scrapper only

`python3 manage.py populate_db`

## Populate database with fake data
`python3 manage.py populate_db --all`
