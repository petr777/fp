# falcon-project.ru

Агрегатор информации торговых процедур по реализации имущества банкротов.
Поиск и визуализация реализуемых на торгах объектах недвижимости.

## Install

[Poetry](https://python-poetry.org/docs/cli/#install)

[Playwright](https://playwright.dev/python/docs/intro/#installation)

Mongo
```
docker run -d -p 127.0.0.1:27017:27017 --name fp_mongo mongo
```

## Usage
```
poetry run fogsoft --help
poetry run fogsoft -p arbitat -s 300 -l 15
```
or 
```
python fogsoft.py --help
python fogsoft.py -p utender -s 1500 -l 25
```
or 
```
from engine.fogsoft.scraper_table_lots import start

start('torgibankrot', 'https://torgibankrot.ru', 500, 40)
```