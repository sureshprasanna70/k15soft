import bs4 
import requests
import feedparser
from xml.dom import minidom
import re
def parseRSS(rssURL):
            indivdualPage=requests.get(rssURL);
            links = re.findall(r'<link>(.*?)</link>',indivdualPage.text)
            for link in links:
                if link != "http://www.thehindu.com/":
                    gettheNews(link)
def gettheNews(newsLink):
    try:
            newsArticle=requests.get(newsLink)
            soup=bs4.BeautifulSoup(newsArticle.text)
            article=soup.select('p.body')
            #article=re.findall(r'<div class="article-text">(.*?)</div>',newsArticle.text)
            print newsLink
            for single in article:
                print re.findall(r'<p class="body">(.*?)</p>',single)

    except Exception,e:
       print str(e)
def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        #print soup
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toOpen=link.attrs.get('href')
            parseRSS(toOpen)

main()
