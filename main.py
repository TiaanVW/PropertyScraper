import requests
import pandas
from bs4 import BeautifulSoup
from geopy.geocoders import ArcGIS

nom = ArcGIS()

url = f"https://www.privateproperty.co.za/for-sale/mpumalanga/lowveld-and-kruger-park/white-river/white-river/506"
r = requests.get(url)
c = r.content
soup = BeautifulSoup(c, "html.parser")
page_nr = soup.find_all("a", class_="pageNumber")[-2].text

for page in range(1, int(page_nr)):
    print(page)

l = []

for page in range(1, int(page_nr)):
    new_url = url + f"?page={page}"
    r = requests.get(new_url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    all = soup.find_all("div", {"class": "infoHolder"})

    for item in all:
        d = {}
        d["Title"] = item.find("div", {"class": "title"}).text
        d["Price"] = item.find("div", {"class": "priceDescription"}).text
        d["Address"] = (item.find("div", {"class": "address" if (
            item.find("div", {"class": "address"})) else "suburb"}).text)
        d["Suburb"] = item.find("div", {"class": "suburb"}).text
        d["Type"] = item.find("div", {"class": "propertyType"}).text
        for fgroup in item.find_all("div", {"class": "features"}):
            for number, icon in zip(fgroup.find_all("div", {"class": "number"}),
                                    fgroup.find_all("div", {"class": "icon"})):
                d[icon["class"][1]] = number.text

        if d["Address"] == d["Suburb"]:
            full_address = None
        else:
            full_address = nom.geocode(str(d["Address"]) + ", " + str(d["Suburb"]) + ", South Africa")

        if full_address:
            d["lat"] = full_address.point[0]
            d["lon"] = full_address.point[1]
        else:
            d["lat"] = None
            d["lon"] = None

        l.append(d)

df = pandas.DataFrame(l)
df.to_csv("Properties.csv")
