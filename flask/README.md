# Flask + Apache Phoenix

A Flask web application that uses Apache Phoenix as a backing store.

Prerequisite: Install HBase 2.0 and Phoenix 5.0

```
$ virtualenv e
$ source e/bin/activate
$ pip install -r requirements.txt
$ pushd phoenixdb && python setup.py install && popd
$ $PHOENIX_HOME/bin/queryserver.py start
$ FLASK_APP=flaskr FLASK_DEBUG=true flask init-db
$ FLASK_APP=flaskr FLASK_DEBUG=true flask run
```
