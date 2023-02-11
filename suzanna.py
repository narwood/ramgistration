
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'https://catalog.unc.edu/courses/'

def main():
    count = 0
    major_list = []
    minor_list = []
    while count < 5:
        links = BeautifulSoup(urlopen(url, 'html.parser'))
        programs = links.select('a[href^="/courses/"]')
        if len(programs) != 0:
            for program in programs:
                program_url = program.attrs['href']
                program_data = BeautifulSoup(urlopen(program_url), 'html.parser')
            count += 1

    print("programs: " + programs)

if __name__ == "__main__":
    main()