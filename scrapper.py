import bs4
import requests
import feedparser
import json
import hashlib
import urllib
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
               getTaxonomy(contents,date)
    except Exception,e:
       print str(e)
def getTaxonomy(contents,date):
    yahoourl='https://query.yahooapis.com/v1/public/yql?q='
    yahooquery='select * from contentanalysis.analyze where text="'
    dupcontents=contents
    querywithtext=yahooquery+" ".join(dupcontents.split())+'"'
    urlwithquery=yahoourl+querywithtext+"&format=json"
    taxo=requests.get(urlwithquery)
    taxojson=json.loads(taxo.text)
    for each in taxojson:
        entitiesarray=taxojson['query']['results']['entities']['entity']
        for entities in entitiesarray:
            print entities
    #print hashlib.sha1(contents).hexdigest()
    #print contents
    #print date
def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toOpen=link.attrs.get('href')
            parseRSS(toOpen)

main()
