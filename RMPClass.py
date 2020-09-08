import requests
import json
import math
import csv
import os

# This code has been tested using Python 3.6 interpreter and Linux (Ubuntu).
# It should run under Windows, if anything you may need to make some adjustments for the file paths of the CSV files.


class RateMyProfScraper:
    def __init__(self, schoolid):
        self.UniversityId = schoolid
        if not os.path.exists("SchoolID_" + str(self.UniversityId)):
            os.mkdir("SchoolID_" + str(self.UniversityId))
        self.professorlist = self.createprofessorlist()
        self.indexnumber = False

    def createprofessorlist(
        self,
    ):  # creates List object that include basic information on all Professors from the IDed University
        tempprofessorlist = []
        num_of_prof = self.GetNumOfProfessors(self.UniversityId)
        num_of_pages = math.ceil(num_of_prof / 20)
        i = 1
        while i <= num_of_pages:  # the loop insert all professor into list
            page = requests.get(
                "http://www.ratemyprofessors.com/filter/professor/?&page="
                + str(i)
                + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="
                + str(self.UniversityId)
            )
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage["professors"]
            tempprofessorlist.extend(temp_list)
            i += 1
        return tempprofessorlist

    def GetNumOfProfessors(
        self, id
    ):  # function returns the number of professors in the university of the given ID.
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="
            + str(id)
        )  # get request for page
        temp_jsonpage = json.loads(page.content)
        num_of_prof = (
            temp_jsonpage["remaining"] + 20
        )  # get the number of professors at William Paterson University
        return num_of_prof

    def SearchProfessor(self, ProfessorName):
        self.indexnumber = self.GetProfessorIndex(ProfessorName)
        self.PrintProfessorInfo()
        return self.indexnumber

    def GetProfessorIndex(
        self, ProfessorName
    ):  # function searches for professor in list
        for i in range(0, len(self.professorlist)):
            if ProfessorName == (
                self.professorlist[i]["tFname"] + " " + self.professorlist[i]["tLname"]
            ):
                return i
        return False  # Return False is not found

    def PrintProfessorInfo(self):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
        else:
            print(self.professorlist[self.indexnumber])

    def PrintProfessorDetail(self, key):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
            return "error"
        else:
            print(self.professorlist[self.indexnumber][key])
            return self.professorlist[self.indexnumber][key]

    def PrintProfessorList(self):
        for professor in self.professorlist:
            print(professor)

    def GetProfessorList(self):
        return self.professorlist

    def WriteProfessorListToCSV(self):
        csv_columns = [
            "tDept",
            "tSid",
            "institution_name",
            "tFname",
            "tMiddlename",
            "tLname",
            "tid",
            "tNumRatings",
            "rating_class",
            "contentType",
            "categoryType",
            "overall_rating",
        ]
        csv_file = "SchoolID_" + str(self.UniversityId) + ".csv"
        with open(csv_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in self.professorlist:
                writer.writerow(data)

    def createReviewslist(self, tid):
        tempreviewslist = []
        num_of_reviews = self.GetNumOfReviews(tid)
        # RMP only loads 20 reviews per page,
        # so num_of_pages tells us how many pages we need to get all the reviews
        num_of_pages = math.ceil(num_of_reviews / 20)
        i = 1
        while i <= num_of_pages:
            page = requests.get(
                "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
                + str(tid)
                + "&filter=&courseCode=&page="
                + str(i)
            )
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage["ratings"]
            tempreviewslist.extend(temp_list)
            i += 1
        return tempreviewslist

    def GetNumOfReviews(self, id):
        page = requests.get(
            "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
            + str(id)
            + "&filter=&courseCode=&page=1"
        )
        temp_jsonpage = json.loads(page.content)
        num_of_reviews = temp_jsonpage["remaining"] + 20
        return num_of_reviews

    def WriteReviewsListToCSV(self, rlist, tid):
        csv_columns = [
            "attendance",
            "clarityColor",
            "easyColor",
            "helpColor",
            "helpCount",
            "id",
            "notHelpCount",
            "onlineClass",
            "quality",
            "rClarity",
            "rClass",
            "rComments",
            "rDate",
            "rEasy",
            "rEasyString",
            "rErrorMsg",
            "rHelpful",
            "rInterest",
            "rOverall",
            "rOverallString",
            "rStatus",
            "rTextBookUse",
            "rTimestamp",
            "rWouldTakeAgain",
            "sId",
            "takenForCredit",
            "teacher",
            "teacherGrade",
            "teacherRatingTags",
            "unUsefulGrouping",
            "usefulGrouping",
        ]
        csv_file = (
            "./SchoolID_" + str(self.UniversityId) + "/TeacherID_" + str(tid) + ".csv"
        )
        with open(csv_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in rlist:
                writer.writerow(data)


# Time for some examples!
if __name__ == '__main__':

    # Getting general professor info!
    WilliamPatersonUniversity = RateMyProfScraper(1205)
    WilliamPatersonUniversity.SearchProfessor("Cyril Ku")
    WilliamPatersonUniversity.PrintProfessorDetail("overall_rating")

    MassInstTech = RateMyProfScraper(580)
    MassInstTech.SearchProfessor("Robert Berwick")
    MassInstTech.PrintProfessorDetail("overall_rating")

    # Let's try the above class out to get data from a number of schools!
    # William Patterson, Case Western, University of Chicago, CMU, Princeton, Yale, MIT, UTexas at Austin, Duke, Stanford, Rice, Tufts
    # For simple test, try tid 97904 at school 1205
    schools = [1205, 186, 1085, 181, 780, 1222, 580, 1255, 1350, 953, 799, 1040]
    for school in schools:
        print("=== Processing School " + str(school) + " ===")
        rmps = RateMyProfScraper(school)
        rmps.WriteProfessorListToCSV()
        professors = rmps.GetProfessorList()
        for professor in professors:
            reviewslist = rmps.createReviewslist(professor.get("tid"))
            rmps.WriteReviewsListToCSV(reviewslist, professor.get("tid"))
