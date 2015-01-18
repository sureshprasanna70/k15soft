import bs4
import requests
import re
import json
def parseRSS(rssURL):
            indivdualPage=requests.get(rssURL);
            links = re.findall(r'<link>(.*?)</link>',indivdualPage.text)
            for link in links:
                if link != "http://www.thehindu.com/":
                    print link
                    gettheNews(link)
def gettheNews(newsLink):
    try:
            contents="";
            newsArticle=requests.get(newsLink)
            soup=bs4.BeautifulSoup(newsArticle.text)
            articlePieces=soup.findAll('p',{"class":"body"})
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
