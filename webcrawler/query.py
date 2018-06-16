#!/usr/bin/env python

from db import connect

def query(db):
    with db.cursor() as c:
        c.execute('SELECT SOURCE, count(1) as "NUM_OUTBOUND" from outbound_links group by source')
        rows = c.fetchall()
    print 'Source => Number of Outbound Links'
    for row in rows:
        print "%s => %s" % (row['SOURCE'], row['NUM_OUTBOUND'])

if __name__ == '__main__':
    with connect() as db:
        query(db)
