import requests
import bs4
import json
def main():
    urls=['http://chennai.quikr.com/Cars-Bikes/w466','http://chennai.quikr.com/Mobiles-Tablets/w18224209','http://chennai.quikr.com/Electronics-Appliances/w18222212660','http://chennai.quikr.com/Pets-Pet-Care/w18222212619','http://chennai.quikr.com/Grooms/w502','http://chennai.quikr.com/Brides/w501','http://chennai.quikr.com/Wedding-Planners/w18222211717']
    for url in urls:
       print url
       response=requests.get(url);
       adhtml=bs4.BeautifulSoup(response.text)
       adlinks=adhtml.findAll('a','adttllnk unbold')
       for adlink in adlinks:
            openad(adlink['href'])
def openad(adlink):
    adresponse=requests.get(adlink)
    ad=bs4.BeautifulSoup(adresponse.text)
    fullad={}
    try:
        adtitle=ad.find('h1','ad_title')
        fullad['title']=adtitle.text
    except Exception,e:
        fulladd['title']='nil'
    try:
        areas=ad.findAll('ul',id="attrib-vertical-gallery")
        loc=ad.findAll('span', "attribVal newattribVal") 
        fullad['latlong']=getlatlong(loc[0].text)
    except Exception,e:
        fullad['latlong']='nil'
    try:
        desc = ad.find('div',id='ad_description')
        fullad['desc']=desc.text
    except Exception,e:
        fullad['desc']='nil'
    try:
        contact=ad.find('span','NoVerified-Text')
        fullad['contact']=contact.text
    except,Exception,e:
        fullad['contact']='nil'
    print fullad
def getlatlong(loc):
    try:
        googleurl="https://maps.googleapis.com/maps/api/geocode/json?address="+loc
        locresponse=requests.get(googleurl)
        locjson=json.loads(locresponse.text)
        return locjson['results'][0]['geometry']['location']
    except Exception,e:
        print str(e)
    
main()
