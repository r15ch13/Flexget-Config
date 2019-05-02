#!/usr/bin/env python3
import feedparser, re, requests, threading, sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Einstellungen:
hoster = ["share online", "share-online", "share-online.biz"]
rssname = "HDAreaSearch.xml"

# Skript startet hier:
threads = []

rss = open(rssname, "w")
rss.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
rss.write("<rss version=\"2.0\">\n")
rss.write("<channel>\n")
rss.write("<title>HDAreaOrg Search RSS-Generator</title>\n")
rss.write("<description>Hd-area.org RSS Generator for Flexget</description>\n")
rss.write("<link>Hd-area.org</link>\n")
rss.write("<ttl> </ttl>\n")

def make_rss(guid, title, link):
    rss.write("<item>\n")
    rss.write("<guid>"+guid+"</guid>\n")
    rss.write("<title>"+title+"</title>\n")
    rss.write("<link>"+link+"</link>\n")
    rss.write("</item>\n")

class HDAreaThread(threading.Thread):
    def __init__(self, release):
        threading.Thread.__init__(self)
        self.release = release
    def run(self):
        fetch_download(self.release)

def fetch_download(result):
    if not result:
        return ''
    page = urlopen(result["url"]).read()
    soup = BeautifulSoup(page, "lxml")

    links = soup.select("div.beschreibung > div > span[style='display:inline;'] > a")
    for link in links:
        url = link["href"]
        if link.text.lower() in hoster:
            print("title:   " + result["title"])
            print("url:     " + url + "\n")
            make_rss(result["url"], result["title"], url)

def search(query):
    url = ("http://www.hd-area.org/?s=search&q=" + query)
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")

    for link in soup.select("div#content > div > a"):
        result = {
            "url": link["href"],
            "title": link["title"]
        }
        thread = HDAreaThread(result)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

for arg in sys.argv[1:]:
    search(arg)

rss.write("</channel>\n")
rss.write("</rss>")
rss.close()
