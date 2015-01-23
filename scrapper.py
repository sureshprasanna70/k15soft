import bs4
import requests
import feedparser
import json
import hashlib
def parseRSS(rssURL):
            indivdualPage=feedparser.parse(rssURL);
            for inds in indivdualPage.entries:
                date=inds.published
                link=inds.links[0]['href']
                if link != "http://www.thehindu.com/":
                    gettheNews(link,date)
def gettheNews(newsLink,date):
    try:
            contents="";
            blacklist=["b","i","u"]
            newsArticle=requests.get(newsLink)
            soup=bs4.BeautifulSoup(newsArticle.text)
            articlePieces=soup.find_all('p',"body") 
            for article in articlePieces:
                contents+=(article.get_text()).encode('utf8')
            if contents=="":
                print "no content"
            else:
               getSha1(contents,date)
    except Exception,e:
       print str(e)
def getSha1(contents,date):
    print hashlib.sha1(contents).hexdigest()
    print contents
    print date
def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toOpen=link.attrs.get('href')
            parseRSS(toOpen)

main()
