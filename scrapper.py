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
            title=soup.find('h1','detail-title').get_text()
            articlepieces=soup.find_all('p',"body") 
            for article in articlepieces:
                contents+=(article.get_text()).encode('utf8')
            if contents=="":
                res['created']=False
                filewriter("1","no contents",res,newslink)
                print "no content"
            else:
                get_taxonomy(title,contents,date,newslink)
    except Exception,e:
       print "News fails  "+str(e)
def get_taxonomy(title,contents,date,newslink):
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
        sendtoes(hashlib.sha1(newslink).hexdigest(),title,contents,date,taxonomy,newslink)
    except Exception,e:
        print "YQL fails "+str(e)
def sendtoes(newsid,title,contents,date,taxonomy,link):
    doc={}
    news={}
    es=Elasticsearch()
    news['url']=link
    news['title']=title
    news['published']=date
    news['taxonomy']=taxonomy
    news['article']=contents
    doc['news']=news
    res=es.index(index="hindu",doc_type="news",id=newsid,body=doc)
    filewriter(newsid,doc,res,link)
def filewriter(newsid,doc,res,link):
    path=""
    logstring=""
    try:
        path="dump/"+newsid
        f=open(path,'w')
        f.write(str(doc))
        f.close()
    except Exception,e:
        print "Dump writing failed"
    try:
        lf=open("dump/result","a")
        logstring=newsid+"   "+str(res['created'])+"   "+link+"\n";
        print logstring
        lf.write(logstring)
        lf.close()
    except Exception,e:
        print "Log writting failed"+str(e)
def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toopen=link.attrs.get('href')
            parseRSS(toopen)

main()
