from bs4 import BeautifulSoup
import requests

url = "https://catalog.unc.edu/undergraduate/programs-study/"
data = requests.get(url)
html = data.text
soup = BeautifulSoup(html, 'html.parser')

def main():
    majors = []
    minors = []
    links = soup.find_all("li")
    for link in links:
        print(link.get('a href'))
        print("\n")

if __name__ == "__main__":
    main()
