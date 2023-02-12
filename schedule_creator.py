# TO DO
# & case chosen major
# + case chosen major
# create empty schedule

# Add dependencies.
from nicole import majors
import csv
import os
# Create the path and import the data
#file_to_load = os.path.join("Resources", "Spring_2023.csv")
#file_to_save = os.path.join("Analysis", "Schedule.txt")

# Nicole and Suzanna's dictionaries, geneds.
#major_reqs = {"math":{"COMP 110": 1, "MATH 383": 1, "MATH 381": 1, "&MATH 521 MATH 533": 1, "+MATH 520": 4}, "engl":{"blah": 1, "+bluj": 2}}
prereqs = {"MATH 383": ["MATH 233"], "MATH 233": ["MATH 231", "MATH 232"]}
geneds = ["CR", "FL", "FL", "FL", "QR", "LF", "PX", "PX/PL", "HS/SS", "HS/SS", "HS", "VP", "LA", "PH", "BN", "CI", "EE", "GL", "NA", "QI/QR", "US", "WB"]

# Inputs
major = input('Enter your major:')
courses_taken = ["COMP 110", "MATH 383", "MATH 381", "PH", "US"]
max_hours = input('Enter your max hours:')
max_hours = int(max_hours)
freshman = input("Are you a freshman? True or False?")
if freshman := "True":
    freshman == True
if freshman := "False":
    freshman == False

# Create an empty list of classes needed to graduate.
to_take = []
# Add geneds to the list.
to_take.extend(geneds)
# Retrieve the chosen major's requirements.
chosen_major = major_reqs[major]
for course in chosen_major:
    amount = chosen_major[course]
    if "&" not in str(course) and "+" not in str(course):
        for i in range(amount):
            to_take.append(course)
    # elif "&" in str(course):
    # elif "+" in str(course):

# Retrieve prereqs.
for course in to_take:
    if prereqs.get(course) is not None:
        to_take.extend(prereqs[course])

# Remove courses taken from list to take.
for course in courses_taken:
    to_take.remove(course)

# Create an empty schedule and initialize tota units at 0.
schedule = []
total_units = 0

# Open and read the file.
with open(file_to_load) as spring_2023:
    file_reader = csv.reader(spring_2023)
    # Skip header row.
    headers = next(file_reader)

    # try to fill schedy with major requirements
    for row in file_reader:
        # if days and times TBA next row.
        if row[10] == "TBA" or row[11] == "TBA":
            continue
        # Retrieve class name.
        subject = row[1]
        catalog_nbr = row[2]
        course_name = (f"{subject} {catalog_nbr}")
        if course_name in to_take:
            units = row[7]
            total_units += units
            if total_units > max_hours:
                total_units -= units
                break
            else:
                # if no time conflict:
                # Check if taken prereqs.
                if prereqs.get(course_name) is not None:
                    for prereq in prereqs[course_name]:
                        if prereq not in courses_taken:
                            break
                # add tha class to the schedule
                schedule.append(course_name)
    
    # fill schedy with geneds if major didnt fill it.
    if total_units < max_hours:
        for row in file_reader:
            # if days and times TBA next row.
            if row[10] == "TBA" or row[11] == "TBA":
                continue
            attributes = row[13]
            for course in to_take:
                if str(course) in str(attributes):
                    units = row[7]
                    total_units += units
                    if total_units > max_hours:
                        total_units -= units
                        break
                    else:
                        # if no time conflict:
                        # Check if taken prereqs.
                        if prereqs.get(course_name) is not None:
                            for prereq in prereqs[course_name]:
                                if prereq not in courses_taken:
                                    break
                        # Add class to schedule.
                        subject = row[1]
                        catalog_nbr = row[2]
                        course_name = (f"{subject} {catalog_nbr}")
                        schedule.append(course_name)

def main():
    print(majors())

if __name__ == "__main__":
    main()

