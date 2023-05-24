import requests
from bs4 import BeautifulSoup
import os
 
page = requests.get('https://www.cs.put.poznan.pl/mkasprzak/bio/testy.html')
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.select("a")[:-2] #last two links are unimportant

if not os.path.isdir("./data"):
    os.mkdir("./data")

for link in links:
    datapage = requests.get(str('https://www.cs.put.poznan.pl/mkasprzak/bio/ins/' + links[0].text))
    data = BeautifulSoup(datapage.content, 'html.parser')
    with open('data/'+link.text+".txt", 'w') as f:
        f.write(data.text)