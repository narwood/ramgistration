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
minorList.remove('Art History Minor')
minorList.remove("Asian Studies Minor")
majorList = majors()

def dept(program):
    table = clicky(program)
    tbody = table.find_all("tbody")[0]
    courses = tbody.find_all(class_="bubblelink code")
    firstCourse = ""
    if len(courses) != 0:
        firstCourse = courses[0].get_text()[0:4]
    return firstCourse

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
                num = re.findall(r'\b\d{3}\b', clcstr)[0]
                parseList.append("&c" + str(wordsToInts(clcstr)) + ">" + dept(program) + num)
                appCheck = True
        for st in setList:
            if not(appCheck) and st in clcstr:
                parseList.append("&s" + str(wordsToInts(clcstr)))
                appCheck = True
        if not(appCheck):
            parseList.append("&n")
        appCheck = False
    return parseList

def parseRow(row, program):
    condList = ["numbered", "higher", "level", "above"]
    setList = ["chosen", "following", "from"]
    appCheck = False
    clcstr = row.get_text()
    for st in condList:
        if not(appCheck) and st in clcstr:
            nums = re.findall(r'\b\d{3}\b', clcstr)
            num = ""
            if len(nums) != 0:
                num = nums[0]
            return "&c" + str(wordsToInts(clcstr)) + ">" + dept(program) + num
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

def tableToDict(table, program):
    outList = []
    selected = tableReader(table)

    for item in selected:
        if item['class'][0]=="courselistcomment":
            outList.append(parseRow(item, program))
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
                    end = len(item)
                    dict[item] = item[2:end]
                    #this as-is just gives number of classes needed - needs to also give dept and condition
            else:
                pass
        else:
            dict[item] = 1
        i += 1
    
    return dict

def bigDictEnergy():
    bigDict = {}
    for major in majorList:
        bigDict[major] = tableToDict(clicky(major), major)
    for minor in minorList:
        bigDict[minor] = tableToDict(clicky(minor), minor)
    return bigDict
        
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
    setList = ["chosen", "following", "from", "list"]
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

    print("\nConditions:")
    print(conds)
    print("\nLists:")
    print(lists)
    print("\nLeft out:")
    print(leftOut)

# ------------------end printing/testing functions -----------------------


def main(): 
    print(bigDictEnergy())
        

    
    

if __name__ == "__main__":
    main()
