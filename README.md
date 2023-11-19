# About

This project was created as a backend api for placing and searching for ads on the wholesale market of grain crops, fuel, fertilizers, pellets, meal, that is, raw and processed products, as well as related products for cultivation.

The main goal is to make the search convenient for farmers and sales managers by tying ads to locations. It is planned to expand the search tools, creating subscriptions for search parameters, chat for communication, price analytics and comparison with stock prices, respectively, data visualization.

Add calculation of land logistics with navigation route and input of price per ton-kilometer, automatic offers under the budget of the final price, taking into account the average cost of delivery.

Under development still...

# Installation

## Development mode
Go to root directory:
```
cd refactored_graintrade
```

Copy sample of `.env` file and set your variables:
```
cp sample-env .env
```

Run docker containers
```
docker compose up -d
```

Create virtual environment:
```
python3 -m venv env
```

Run environment: 
```
source env/bin/activate
```

Install all dependencies:
```
pip install --upgrade pip setuptools
pip install -r requirements.txt
```
Do migration and create superuser etc.:
```
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```
### Loading fixtures
```
python manage.py loaddata --format json offers/fixtures/*
```

### Run project:
```
python manage.py runserver
```

### Celery
```
celery -A refactored_graintrade worker -l INFO
```


***and open in browser ->*** [http://localhost:8000/](http://localhost:8000/)

## Production mode

