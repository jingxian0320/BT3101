#################
# Project Related Data Crawling
# Tang Jiahui
# A0119415J
# Python Version : Python 3
#################



from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

html_freeapp = urlopen("http://www.apple.com/itunes/charts/free-apps/")
html_paidapp = urlopen("http://www.apple.com/itunes/charts/paid-apps/")

html = [html_freeapp, html_paidapp]
rank = [[],[]]
name = [[],[]]
category = [[],[]]

for i in range(0,2):
    soup = BeautifulSoup(html[i].read())
    lst = soup.find("section",{"class":"apps"})
    apps = lst.find_all("li")

    for app in apps:
        rank[i].append(app.find("strong").get_text()[:-1])
        name[i].append(app.find("h3").get_text())
        category[i].append(app.find("h4").get_text())



with open("projectdata_result_a0119415J.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["rank","free_app_name","category"])
    for i,j,k in zip(rank[0],name[0],category[0]):
        writer.writerow([i,j,k])
    writer.writerow("")

    writer.writerow(["rank","paid_app_name","category"])
    for i,j,k in zip(rank[1],name[1],category[1]):
        writer.writerow([i,j,k])


