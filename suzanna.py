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
    program_classes = []
    megaprereq = []
    classes = []
    links = soup.select('a[href^="/courses/"]')
    links = links[3:152]

    for link in links:
        #accesses class catalogs for each program
        subUrl = link.attrs['href']
        subObj = BeautifulSoup(urlopen("https://catalog.unc.edu" + subUrl), 'html.parser')
        #program = link.get_text()[0: len(link.get_text()) - 7]
        #abbr = getAbbr(link.get_text())
        #link = (getLink(subObj, subUrl).get('href'))
        program_classes = getClasses(subObj)
        for course in program_classes:
            classes.append(course)
    yeah = getPrereq(BeautifulSoup(urlopen("https://catalog.unc.edu/courses/aero/"), features="html.parser"))
    print(yeah)
    #megaprereq.append(prereqs)
    #print(classes[:15])
    #print(prereqs) #MAKE .JOIN LIST OF PREREQ LISTS
    #for course in megaclass:
       # prereqs = getPrereq(course)
       # geneds = getGens(course)
       # megaprereq.append(', '.join(prereqs))
       # megagens.append(', '.join(geneds))

    #     subObj = BeautifulSoup(urlopen("https://catalog.unc.edu" + subUrl), 'html.parser')
    #     link = getLink(subObj, subUrl)
    #     megalist.append(link.get('href'))
    


def getLink(subObj):
    link_list = []
    clickOn = subObj.find_all("div", {'class':'cols no indent'})

    link = soup.select()
    link_list.append(link)
    return link_list

# def getAbbr(program):
#     abbr = program[len(program) - 5:len(program) -1]
#     return abbr

def getClasses(subObj):
    class_list = []
    classes = subObj.find_all('div',{'class':'cols noindent'})
    for course in classes:
        course = course.get_text()
        #course = course.replace("\xa0", "")
        course = course[:8]
        if(course != "" and course != " "):
            if (course[len(course) - 1] == "."):
                course = course[:7]
            class_list.append(course)

    return (class_list)

#def getPrereq(subObj):

def getPrereq(subObj):
    prereq_list_big = []
    clickOn = subObj.find_all("div", {'class':'courseblock'})
    for course in clickOn:
        print(course)
        final_prereqs = []
        prereq_list = []
        url2 = course.get("href")
        print("URL: " + str(url2))
        if(url2 != ""):
            source = "https://catalog.unc.edu" + str(url2)
            print("src: " + source)
            dataClicky = requests.get(source)
        #prereq page accessed
            htmlClicky = dataClicky.text
            clickySoup = BeautifulSoup(htmlClicky, 'html.parser')
            prereq = getClasses(clickySoup)
            print("pre: " + '. '.join(prereq))
        else: 
            prereq = "None"
        prereq_list.append(prereq)

    #     if (len(prereq_list) == 0):
    #         print("none")
    #         prereq_list_big.append("N/A")
        
    #     else:
    #         print("adding prereqs to list")
    #         for prereq in prereq_list:
    #             prereq = prereq.get_text()
    #             prereq = prereq.replace("\xa0", "")
    #             prereq = prereq.replace(".", ". ")
    #             final_prereqs.append(prereq)
    #         prereq_list_big.append(prereq)
    return prereq_list_big

if __name__ == "__main__":
    main()