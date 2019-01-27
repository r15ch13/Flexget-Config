#!/usr/bin/env python3
import feedparser, re, requests, threading
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Einstellungen:
sites = ('neues', 'top-rls', 'movies', 'Old_Stuff', 'Cinedubs')
hoster = ["share online", "uploaded"]
rssname = "HDArea.xml"

# Skript startet hier:
threads = []

rss = open(rssname, "w")
rss.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
rss.write("<rss version=\"2.0\">\n")
rss.write("<channel>\n")
rss.write("<title>HDAreaOrg RSS-Generator</title>\n")
rss.write("<description>Hd-area.org RSS Generator for Flexget</description>\n")
rss.write("<link>Hd-area.org</link>\n")
rss.write("<ttl> </ttl>\n")

def make_rss(title, link):
    rss.write("<item>\n")
    rss.write("<title>"+title+"</title>\n")
    rss.write("<link>"+link+"</link>\n")
    rss.write("</item>\n")

def fetch_releases(site):
    address = ('https://hd-area.org/index.php?s=' + site)
    page = urlopen(address).read()
    soup = BeautifulSoup(page, "lxml")

    for release in soup.find_all("div", {"class" : "topbox"}):
        imdb_url = ""
        title = release.select_one("div.boxlinks > #title > a")["title"]

        season = re.compile('.*S\d|\Sd{2}|eason\d|eason\d{2}.*')
        if not season.match(title):

            links = release.find_next("div", {"class" : "download"})
            links = links.select("div.beschreibung > span[style='display:inline;'] > a")
            for link in links:
                url = link["href"]
                if link.text.lower() in hoster:
                    print("> " + title)
                    print("  " + url + "\n")
                    make_rss(title, url)

class HDAreaThread(threading.Thread):
    def __init__(self, site):
        threading.Thread.__init__(self)
        self.site = site
    def run(self):
        fetch_releases(self.site)

for site in sites:
    thread = HDAreaThread(site)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()

rss.write("</channel>\n")
rss.write("</rss>")
rss.close()
