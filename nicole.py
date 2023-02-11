from bs4 import BeautifulSoup
import requests
import re

url = "https://catalog.unc.edu/undergraduate/programs-study/"
data = requests.get(url)
html = data.text
soup = BeautifulSoup(html, 'html.parser')

def majors():
   majors = [] 
   majorTags = soup.find_all("a", string=re.compile("Major"))
   for item in majorTags:
        majors.append(item.get_text())
   del majors[0]
   return majors

def minors():
    minors = []
    minorTags = soup.find_all("a", string=re.compile("Minor"))
    for item in minorTags:
        minors.append(item.get_text())
    del minors[0]
    return minors

def clicky(program):
    clickOn = soup.find_all("a", string=program)[0]
    url2 = clickOn.get("href")[1::]
    source = url + url2 + "#requirementstext"
    dataClicky = requests.get(source)
    htmlClicky = dataClicky.text
    clickySoup = BeautifulSoup(htmlClicky, 'html.parser')
    return clickySoup
    

def main():  
    print(clicky("American Studies Minor").prettify())
    

if __name__ == "__main__":
    main()
