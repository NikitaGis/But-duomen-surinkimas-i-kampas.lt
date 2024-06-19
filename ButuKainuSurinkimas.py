import datetime
import requests
from bs4 import BeautifulSoup as BS
import json
from openpyxl import Workbook

wb=Workbook()
ws=wb.active
ws.title="Data"
print("surinkti duomenis Lietuvai ar Vilniui? Reikia parašyti lt arba vn")
print("lt/vn?")
pasirinkimas=input()
if pasirinkimas=="lt":
    puslapis="https://www.kampas.lt/butai?page=1"
    url='https://www.kampas.lt/api/classifieds/search-new?query=%7B%22sort%22%3A%22important%22%2C%22type%22%3A%22flat%22%2C%22taxonomyslug%22%3A%22sale%22%2C%22page%22%3A%221%22%2C%22mapView%22%3Afalse%2C%22useMapSearch%22%3Afalse%2C%22elp%22%3Anull%2C%22zoom%22%3Anull%2C%22keyword%22%3A%22%22%7D'
    part1=165
    part2=-123
    urlPart1=url[:part1]
    urlPart2=url[part2:]
elif pasirinkimas=="vn":
    puslapis="https://www.kampas.lt/butai-vilniuje?page=1"
    url='https://www.kampas.lt/api/classifieds/search-new?query=%7B%22sort%22%3A%22important%22%2C%22municipality%22%3A58%2C%22settlement%22%3A19220%2C%22type%22%3A%22flat%22%2C%22taxonomyslug%22%3A%22sale%22%2C%22mapView%22%3Afalse%2C%22useMapSearch%22%3Afalse%2C%22elp%22%3Anull%2C%22zoom%22%3Anull%2C%22keyword%22%3A%22%22%2C%22page%22%3A%221%22%7D'
    part1=335
    part2=-6
    urlPart1=url[:part1]
    urlPart2= url[part2:]
else:
    print("kažkas pasirinkta ne taip")
   
soup = BS(requests.get(puslapis).text, 'html.parser')
pusl_kiekis=int(soup.find('div',attrs={"class":"pages"}).text.split('\n')[-2])

for j in range(pusl_kiekis):     
    urldata=requests.get(url)
    for i in range(len(urldata.json()['hits'])):
        id=(urldata.json()['hits'][i]['id'])
        Kaina=(urldata.json()['hits'][i]['objectprice'])
        Plotas=((urldata.json()['hits'][i]['objectarea']))
        KainaUzMetra=((urldata.json()['hits'][i]['objectpriceperm']))
        Kambariai=((urldata.json()['hits'][i]['totalrooms']))
        Aukstu=((urldata.json()['hits'][i]['totalfloors']))
        Aukstas=((urldata.json()['hits'][i]['objectfloor']))
        Konstrukcija=((urldata.json()['hits'][i]['buildingstructure']))
        #Sildymas=((urldata.json()['hits'][i]['features']))
        Vieta=((urldata.json()['hits'][i]['title']))
        StatybosMetai=((urldata.json()['hits'][i]['yearbuilt']))
        try:
            Latitude=((urldata.json()['hits'][i]['coordinates']['lat']))
            Longtitude=((urldata.json()['hits'][i]['coordinates']['lon']))
        except Exception as ex:
            print(ex)
            print("net koordinat")
        line=[id,Kaina, Plotas, KainaUzMetra, Kambariai, Aukstu, Aukstas,Konstrukcija,Vieta,StatybosMetai,Latitude, Longtitude]
        ws.append(line)
    urlNumber=int(url[part1:part2])+1
    url=urlPart1+str(urlNumber)+urlPart2
    print("puslapis",urlNumber-1,"iš",pusl_kiekis)

now = datetime.datetime.now()
FailPav=("Butu kainos,"+"Vilnius"+','+(str(now).split(' ')[0])+'.csv')
wb.save(FailPav)
