import bs4
import requests
import feedparser
import json
import hashlib
import urllib
from dateutil.parser import parse
from elasticsearch import Elasticsearch
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
            taxonomy={}
            i=1
            if i <= 2: 
                for entities in entitiesarray:
                    singleentity={}
                    singleentity['score']=entities['score']
                    singleentity['name']=entities['text']['content']
                    if "wiki_url" in entities:
                            try:
                                singleentity['url']=entities['wiki_url']
                            except Exception,e:
                                singleentity['url']='nil'
                    if 'types' in entities:
                            for details in entities['types']:
                               try:
                                   singleentity['ent_type']=details['content']
                               except Exception,e:
                                   singleentity['ent_type']='nil'
                    key_string="entity"+str(i)
                    taxonomy[key_string]=singleentity
                    i=i+1
        sendtoes(hashlib.sha1(newslink).hexdigest(),contents,date,taxonomy,newslink)
    except Exception,e:
        print "YQL fails"
def sendtoes(newsid,contents,date,taxonomy,link):
    doc={}
    news={}
    es=Elasticsearch()
    news['url']=link
    news['published']=date
    news['taxonomy']=taxonomy
    doc['news']=news
    res=es.index(index="hindu",doc_type="news",id=newsid,body=doc)
    print res
def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toopen=link.attrs.get('href')
            parseRSS(toopen)

main()
