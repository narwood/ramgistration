from bs4 import BeautifulSoup
import requests
import re

url = "https://catalog.unc.edu/undergraduate/programs-study/"
data = requests.get(url)
html = data.text
soup = BeautifulSoup(html, 'html.parser')

def main():
    majors = []
    minors = []
    minorTags = soup.find_all("a", string=re.compile("Minor"))
    majorTags = soup.find_all("a", string=re.compile("Major"))
    for item in minorTags:
        minors.append(item.get_text())
    del minors[0]
    for item in majorTags:
        majors.append(item.get_text())
    del majors[0]
    
    print(minors)
    print(majors)
    

if __name__ == "__main__":
    main()
