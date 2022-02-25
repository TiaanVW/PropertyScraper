import requests
import pandas
from bs4 import BeautifulSoup

l = []

url = f"https://www.privateproperty.co.za/for-sale/mpumalanga/lowveld-and-kruger-park/white-river/white-river/506"
r = requests.get(url)
c = r.content
soup = BeautifulSoup(c, "html.parser")
all = soup.find_all("div", {"class": "infoHolder"})

page_nr = soup.find_all("a", class_="pageNumber")[-2].text


for page in range(1, int(page_nr)):
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

        l.append(d)

df=pandas.DataFrame(l)
df.to_csv("Properties.csv")
