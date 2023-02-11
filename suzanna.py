from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

url = 'https://catalog.unc.edu/courses/'
data = requests.get(url)
html = data.text
soup = BeautifulSoup(html, 'html.parser')

def main():
    print("running")
    megaclass = []
    megaprereq = []
    megagens = []
    links = soup.select('a[href^="/courses/"]')
    links = links[3:152]

    for link in links:
        subUrl = link.attrs['href']
        subObj = BeautifulSoup(urlopen("https://catalog.unc.edu" + subUrl), 'html.parser')
        #program = link.get_text()[0: len(link.get_text()) - 7]
        #abbr = getAbbr(link.get_text())
        #link = (getLink(subObj, subUrl).get('href'))
        classes = getClasses(subObj)
       # prereqs = getPrereq(subObj)
        megaclass.append(', '.join(classes))
    print(megaclass[:10])    
        # for course in megaclass:
        #     prereqs = getPrereq(course)
        #     geneds = getGens(course)
        #     megaprereq.append(', '.join(prereqs))
        #     megagens.append(', '.join(geneds))

    #     subObj = BeautifulSoup(urlopen("https://catalog.unc.edu" + subUrl), 'html.parser')
    #     link = getLink(subObj, subUrl)
    #     megalist.append(link.get('href'))
    


# def getLink(subObj, subUrl):
#     link = subObj.find('a', href=re.compile("/courses/"))
#     return link

# def getAbbr(program):
#     abbr = program[len(program) - 5:len(program) -1]
#     return abbr

def getClasses(subObj):
    class_list = []
    classes = subObj.find_all('div',{'class':'cols noindent'})
    for course in classes:
        course = course.get_text()
        course = course.replace("\xa0", "")
        course = course.replace(".", ". ")
        if(course != "" and course != " "):
            class_list.append(course)

    return class_list

#def getPrereq(subObj):



if __name__ == "__main__":
    main()