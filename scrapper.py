import bs4
import requests
import feedparser
import json
import hashlib
import urllib
from dateutil.parser import parse
def parseRSS(rssURL):
            indivdualpage=feedparser.parse(rssURL);
            for inds in indivdualpage.entries:
                date=inds.published
                link=inds.links[0]['href']
                if link != "http://www.thehindu.com/":
                    getthenews(link,date)
def getthenews(newslink,date):
    try:
            contents="";
            blacklist=["b","i","u"]
            newsarticle=requests.get(newslink)
            soup=bs4.BeautifulSoup(newsarticle.text)
            articlepieces=soup.find_all('p',"body") 
            for article in articlepieces:
                contents+=(article.get_text()).encode('utf8')
            if contents=="":
                print "no content"
            else:
               get_taxonomy(contents,date,newslink)
    except Exception,e:
       print "News fails"
def get_taxonomy(contents,date,newslink):
    yahoourl='https://query.yahooapis.com/v1/public/yql?q='
    yahooquery='select * from contentanalysis.analyze where text="'
    dupcontents=contents
    querywithtext=yahooquery+" ".join(dupcontents.split())+'"'
    urlwithquery=yahoourl+querywithtext+"&format=json"
    taxo=requests.get(urlwithquery)
    try:
        taxojson=json.loads(taxo.text)
        pubdate=parse(date).date()
        date=pubdate.strftime("%Y-%m-%d")
        for each in taxojson:
            entitiesarray=taxojson['query']['results']['entities']['entity']
            for entities in entitiesarray:
                taxonomy={}
                taxonomy['score']=entities['score']
                taxonomy['name']=entities['text']['content']
                if "wiki_url" in entities:
                    try:
                        taxonomy['url']=entities['wiki_url']
                    except Exception,e:
                        taxonomy['url']='nil'
                if 'types' in entities:
                    try:
                        taxonomy['ent_type']=entities['types']['type']['content']
                    except Exception,e:
                        taxonomy['ent_type']='nil'

        sendtoes(hashlib.sha1(contents).hexdigest(),contents,date,taxonomy,newslink)
    except Exception,e:
        print "YQL fails"
def sendtoes(index,contents,date,taxonomy,link):
    print date
    print link
    print taxonomy
'''
Sample json doc for es
{"news": {"url":"http://www.google.com","article":"It is great","published":"2015-01-25","taxonomy":{"entity1": {"name": "Obama","score":0.1},"entity2": { "name": "Michelle","score": 0}}}}
'''
def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toopen=link.attrs.get('href')
            parseRSS(toopen)

main()
