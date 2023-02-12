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
    

def getCLCnames(program):
    table = clicky(program) 
    tbody = table.find_all("tbody")[0]
    selected = tbody.find_all(class_=re.compile("courselistcomment"))
    return selected


def rowParseByIndex(program):
    CLCnames = getCLCnames(program)
    condList = ["numbered", "higher", "level", "above"]
    setList = ["chosen", "following", "from"]
    parseList = []
    appCheck = False
    for clc in getCLCnames(program):
        clcstr = clc.get_text()
        for st in condList:
            if not(appCheck) and st in clcstr:
                parseList.append("&c" + str(wordsToInts(clcstr)))
                appCheck = True
        for st in setList:
            if not(appCheck) and st in clcstr:
                parseList.append("&s" + str(wordsToInts(clcstr)))
                appCheck = True
        if not(appCheck):
            parseList.append("&n")
        appCheck = False
    return parseList

def parseRow(row):
    condList = ["numbered", "higher", "level", "above"]
    setList = ["chosen", "following", "from"]
    appCheck = False
    clcstr = row.get_text()
    for st in condList:
        if not(appCheck) and st in clcstr:
            return "&c" + str(wordsToInts(clcstr))
            appCheck = True
    for st in setList:
        if not(appCheck) and st in clcstr:
            return "&s" + str(wordsToInts(clcstr))
            appCheck = True
    return "&n"
    

def wordsToInts(str):
    if "ne course" in str:
        return 1
    elif "wo courses" in str:
        return 2    
    elif "hree courses" in str:
        return 3
    elif "our courses" in str:
        return 4
    elif "ive courses" in str:
        return 5
    elif "ix courses" in str:
        return 6
    elif "even courses" in str:
        return 7
    elif "ight courses" in str:
        return 8
    elif "ine courses" in str:
        return 9
    elif "ne " in str:
        return 1
    elif "wo " in str:
        return 2
    elif "hree " in str:
        return 3
    elif "our " in str:
        return 4
    elif "ive " in str:
        return 5
    elif "ix " in str:
        return 6
    elif "even " in str:
        return 7
    elif "ight " in str:
        return 8
    elif "ine " in str:
        return 9
    else:
        return ""

def tableToDict(table):
    outList = []
    selected = tableReader(table)
    for item in selected:
        if item['class'][0]=="courselistcomment":
            outList.append(parseRow(item))
        else:
            ugly = item.get_text()
            slashdex = ugly.find("\xa0")
            if slashdex == -1:
                outList.append(ugly)
            else:
                end = len(ugly)
                pretty = ugly[0:slashdex] + ugly[slashdex+1:end]
                outList.append(pretty)
    
    dict = {}
    i = 0
    j = 0
    while i < len(outList):
        item = outList[i]
        if item[0] == "&":
            if item[1] == "n":
                pass
            elif len(item) > 2:
                if item[1] == "s":
                    j = i + 1
                    set = []
                    stop = False
                    while j < len(outList) and not(stop):
                        if outList[j][0] == "&":
                            stop = True
                        else:
                            set.append(outList[j])
                            i = j
                        j += 1
                    stop = False
                    if len(set) == 0:
                        pass
                    else:
                        dict[item] = set
                    
                elif item[1] == "c":
                    dict[item] = item[2]
                    #this as-is just gives number of classes needed - needs to also give dept and condition
            else:
                pass
        else:
            dict[item] = 1
        i += 1
    
    return dict

        
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


def printCLCnames(program):
    for item in getCLCnames(program):
            print(item.get_text())


def rowParser(program):
    condList = ["numbered", "higher", "level", "above"]
    setList = ["chosen", "following", "from"]
    conds = []
    lists = []
    leftOut = []
    appCheck = False
    for clc in getCLCnames(program):
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
    program = "Computer Science Major, B.S."
    # printCLCnames(program)
    # rowParser(program)
    # print(rowParseByIndex(program))
    #print(tableToList(clicky(program)))
    print(tableToDict(clicky(program)))
    

if __name__ == "__main__":
    main()
