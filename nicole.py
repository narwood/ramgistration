from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://catalog.unc.edu/undergraduate/programs-study/"
source = urlopen(url)
soup = BeautifulSoup(source)

def main():
    int = 0

if __name__ == "__main__":
    main()
