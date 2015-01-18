import bs4
import requests
import feedparser
import json
def parseRSS(rssURL):
            indivdualPage=feedparser.parse(rssURL);
            for inds in indivdualPage.entries:
                date=inds.published
                link=inds.links[0]['href']
                if link != "http://www.thehindu.com/":
                    print link
                    print date
                    gettheNews(link,date)
def gettheNews(newsLink,date):
    try:
            contents="";
            newsArticle=requests.get(newsLink)
            soup=bs4.BeautifulSoup(newsArticle.text)
            articlePieces=soup.find_all('p',"body")
            for article in articlePieces:
                contents+=article.renderContents()
            print contents
    except Exception,e:
       print str(e)

def main():
        page = 'http://www.thehindu.com/navigation/?type=rss'
        response = requests.get(page)
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select('div.sitemap ul li a[href^=]')
        for link in links:
            toOpen=link.attrs.get('href')
            parseRSS(toOpen)

main()
