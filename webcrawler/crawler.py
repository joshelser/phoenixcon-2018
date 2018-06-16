#!/usr/bin/env python

from db import connect
import urllib2
from bs4 import BeautifulSoup
import urlnorm

def crawl(db, url, urls_crawled={}):
    # Make sure we don't infinite loop, keep track of what we urls_crawled
    # TODO pull this from Phoenix

    # Crawl this website, get all of the outbound URLs
    urls_to_crawl = crawl_one(db, url)
    # Record that we crawled this url
    urls_crawled[url]=None
    
    for url_to_crawl in urls_to_crawl:
        try:
            url_to_crawl = urlnorm.norm(url_to_crawl)
        except urlnorm.InvalidUrl:
            # Try to convert it to an absolute url
            url_to_crawl = urlnorm.norm("%s%s" % (url, url_to_crawl))

        # Don't re-record
        if url_to_crawl in urls_crawled:
            print 'Skipping %s as already crawled' % (url_to_crawl)
        # Only crawl my site
        elif url_to_crawl.startswith('https://penguinsinabox.com'):
            crawl(db, url_to_crawl, urls_crawled)
        else:
            # A website not owned by me
            print 'Skipping %s as not a self-controlled site' % (url_to_crawl)
    print "Finished processing children of %s" % (url)

def crawl_one(db, url):
    print "Crawling %s" % (url)
    try:
        page = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print 'Failed to read %s' % (url)
        return []
    soup = BeautifulSoup(page, 'html.parser')
    # get just the hrefs
    hrefs = get_anchors(soup)
    # build the params to pass to the db
    values = []
    for href in hrefs:
        values.append([url, href])
    # Write to the db
    with db.cursor() as cursor:
        # The site we just crawled
        cursor.execute('UPSERT INTO webcrawler VALUES(?, CURRENT_TIME(), ?)', (url, str(soup.html)))
        # The outbound links from that site
        cursor.executemany('UPSERT INTO outbound_links VALUES (?, ?)', values)
    return hrefs

def get_anchors(soup):
    anchors = soup.findAll('a')
    return [anchor['href'] for anchor in anchors]

if __name__ == '__main__':
    with connect() as db:
        crawl(db, 'https://penguinsinabox.com')
