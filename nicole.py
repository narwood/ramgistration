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

minorList = minors()
majorList = majors()

def clicky(program):
    clickOn = soup.find_all("a", string=program)[0]
    url2 = clickOn.get("href")[1::]
    source = "https://catalog.unc.edu/" + url2 + "#requirementstext"
    dataClicky = requests.get(source)
    htmlClicky = dataClicky.text
    clickySoup = BeautifulSoup(htmlClicky, 'html.parser')
    tables = clickySoup.find_all("table", class_="sc_courselist")
    return tables[0]


def tableReader(table):
    tbody = table.find_all("tbody")[0]
    selected = tbody.find_all(True, {'class':[re.compile("courselistcomment"), 'bubblelink code']})
    return selected

def getCLCnames():
    for program in majorList[27:29]: 
        table = clicky(program) 
        tbody = table.find_all("tbody")[0]
        selected = tbody.find_all(class_=re.compile("courselistcomment"))
        return selected


def rowParseByIndex():
    CLCnames = getCLCnames()
    condList = ["numbered", "higher", "level", "above"]
    setList = ["chosen", "following", "from"]
    parseList = []
    appCheck = False
    for clc in getCLCnames():
        clcstr = clc.get_text()
        for st in condList:
            if not(appCheck) and st in clcstr:
                parseList.append("cond")
                appCheck = True
        for st in setList:
            if not(appCheck) and st in clcstr:
                parseList.append("set")
                appCheck = True
        if not(appCheck):
            parseList.append("none")
        appCheck = False
    return parseList
        
# --------------------- printing/testing functions -------------------------------------

def listy():
    majorsString = ""
    for major in majorList:
        majorsString += major + ", "
    print(majorsString)

    minorsString = ""
    for minor in minorList:
        minorsString += minor + ", "
    print(minorsString)


def clickyDiagnostic():
    sadCount = 0
    problemPrograms = []
    happyCount = 0
    programs = majors() + minors()
    for program in programs:
        if len(clicky(program)) == 0:
            sadCount += 1
            problemPrograms.append(program)
        else:
            happyCount += 1
    print("total: " + str(len(programs)))
    print("sad: " + str(sadCount))
    print("happy: " + str(happyCount))
    print(problemPrograms)


def printTable(program):
     for item in tableReader(clicky(program)):
        print(item.get_text()) 


def printCLCnames():
    for item in getCLCnames():
            print(item.get_text())


def rowParser():
    condList = ["numbered", "higher", "level", "above"]
    setList = ["chosen", "following", "from"]
    conds = []
    lists = []
    leftOut = []
    appCheck = False
    for clc in getCLCnames():
        clcstr = clc.get_text()
        for st in condList:
            if not(appCheck) and st in clcstr:
                conds.append(clcstr)
                appCheck = True
        for st in setList:
            if not(appCheck) and st in clcstr:
                lists.append(clcstr)
                appCheck = True
        if not(appCheck):
            leftOut.append(clcstr)
        appCheck = False

    print("Conditions:")
    print(conds)
    print("\nLists:")
    print(lists)
    print("\nLeft out:")
    print(leftOut)

# ------------------end printing/testing functions -----------------------


def main(): 
    rowParser()
    print(rowParseByIndex())
    

if __name__ == "__main__":
    main()
