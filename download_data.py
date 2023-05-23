import requests
from bs4 import BeautifulSoup
 
page = requests.get('https://www.cs.put.poznan.pl/mkasprzak/bio/testy.html')
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.select("a")[:-2] #last two links are unimportant

for link in links:
    datapage = requests.get(str('https://www.cs.put.poznan.pl/mkasprzak/bio/ins/' + links[0].text))
    data = BeautifulSoup(datapage.content, 'html.parser')
    with open('data/'+link.text, 'w') as f:
        f.write(data.text)