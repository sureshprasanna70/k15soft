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
    adtitle=ad.find('h1','ad_title')
    areas=ad.findAll('ul',id="attrib-vertical-gallery")
    loc=ad.findAll('span', "attribVal newattribVal")
    desc = ad.find('div',id='ad_description')
    contact=ad.find('span','NoVerified-Text')
    print adlink
    print adtitle.text
    print contact.text
    latlong=getlatlong(loc[0].text)
    #print desc.text

def getlatlong(loc):
    googleurl="https://maps.googleapis.com/maps/api/geocode/json?address="+loc
    locresponse=requests.get(googleurl)
    locjson=json.loads(locresponse.text)
    return locjson['results'][0]['geometry']['location']
    
main()
