# Website Scraper with Phoenix storage

Scrapes a web page, storing all outbound links on that page, the content of that page, and then recurses through all
outbound links that are on the same domain.

```
$ virtualenv e
$ source e/bin/activate
$ pip install -r requirements.txt
$ pushd phoenixdb && python setup.py install && popd
$ python db.py
$ python crawler.py
$ python query.py
```
