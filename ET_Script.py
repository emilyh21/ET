import urllib2
from urlparse import urljoin
from urlparse import urlparse
from bs4 import BeautifulSoup as soup
import re
import csv
from HTMLParser import HTMLParser
from collections import defaultdict
import requests
import os



def check_web_health(root,max_depth):
    domain = get_domain(root)
    filter_domain = [domain]
    tocrawl = [[root,1]]
    crawled = {}
    count=0;
    while tocrawl:
        crawl_ele = tocrawl.pop()
        link = crawl_ele[0]
        depth = crawl_ele[1]

        if link not in crawled.keys():
            content, status = get_page(link)
            if content == None:
                crawled[link]= status
                continue
            host = get_domain(link)
            if depth <= max_depth and host in filter_domain:
                outlinks = get_all_links(content,link)
                print '-----------------------------------'
                print 'Adding outlinks ' + str(outlinks) + ' for parent page '+link
                print '-----------------------------------'
                add_to_tocrawl(crawled.keys(),tocrawl, outlinks, depth+1)
            crawled[link]= status

    f = open('URl_ouput_codes.csv', 'w')
    for url,status in crawled.iteritems():
        f.write(url)
        f.write('\t')
        f.write('\t')
        f.write(status)
        f.write('\n')
    f.close()

def get_domain(url):
    hostname = urlparse(url).hostname
    if len(re.findall( r'[0-9]+(?:\.[0-9]+){3}', hostname)) > 0:
        return hostname
    elif len(hostname.split('.')) == 0:
        hostname
    elif hostname.find('www.') != -1:
        return hostname.split('.')[0]
    else:
        return hostname.split('.')[1]

def get_page(url):
    print url
    try:
        request_headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": url,
            "Connection": "keep-alive"
        }
        request = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(request)
        return response.read(), 'OK'
    except urllib2.HTTPError,e:
        return None, str(e.code)
    except urllib2.URLError,e:
        print e.args
        return None, 'Invalid Url'
    except:
        return None, 'Wrong Url'


def get_next_target(page,parent):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    url = urljoin(parent,url)
    return url, end_quote

def get_all_links(page,parent):
    links = []
    while True:
        url, endpos = get_next_target(page,parent)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def add_to_tocrawl(crawled, tocrawl, newlinks, depth):
    for link in newlinks:
        if link not in tocrawl and link not in crawled:
            tocrawl.append([link,depth])

check_web_health('http://www.newyorktimes.com',3)
