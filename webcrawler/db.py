#!/usr/bin/env python

import phoenixdb

def connect():
    return phoenixdb.connect('http://localhost:8765', autocommit=True, cursor_factory=phoenixdb.cursor.DictCursor)

def init():
    with connect() as db, db.cursor() as cursor:
        commands = ('DROP TABLE IF EXISTS webcrawler',
            'CREATE TABLE webcrawler(url varchar not null primary key, crawl_time timestamp, content varchar)',
            'DROP TABLE IF EXISTS outbound_links',
            'CREATE TABLE outbound_links(source varchar not null, destination varchar not null, constraint pk primary key(source, destination))'
        )
        for command in commands:
            cursor.execute(command)

if __name__ == '__main__':
    init()
