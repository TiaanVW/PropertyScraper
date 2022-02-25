import requests
from bs4 import BeautifulSoup

r = requests.get(
    "https://www.privateproperty.co.za/for-sale/mpumalanga/lowveld-and-kruger-park/white-river/white-river/506")
c = r.content

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("div", {"class": "infoHolder"})

for item in all:
    d = {}
    d["Title"] = item.find("div", {"class": "title"}).text
    d["Price"] = item.find("div", {"class": "priceDescription"}).text
    d["Adress"] = (item.find("div", {"class": "address" if (
        item.find("div", {"class": "address"})) else "suburb"}).text)
    d["Type"] = item.find("div", {"class": "propertyType"}).text
    for fgroup in item.find_all("div", {"class": "features"}):
        for number, icon in zip(fgroup.find_all("div", {"class": "number"}), fgroup.find_all("div", {"class": "icon"})):
            d[icon["class"][1]] = number.text

    print(d)
