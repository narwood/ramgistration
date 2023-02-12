# Add dependencies.
import csv
import os
# Assign variables to load and save files.
file_to_load = os.path.join("Raad", "Spring_2023.csv")

# Nicole and Suzanna's dictionaries, geneds.
major_reqs = {}
prereqs = {}
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
# Retrieve the dictionary of chosen major's requirements.
chosen_major = major_reqs[major]
for course in chosen_major:
    amount = chosen_major[course]
    if "&" not in str(course) and "+" not in str(course) and amount == 1:
        to_take.append(course)
        if prereqs.get(course) is not None:
            to_take.extend(prereqs[course])
    elif 


schedule = []

# Open and read the file.
with open(file_to_load) as spring_2023:
    file_reader = csv.reader(spring_2023)
    # Skip header row.
    headers = next(file_reader)

    for row in file_reader:
        # Retrieve class name.
        subject = row[1]
        catalog_nbr = row[2]
        course_name = (f"{subject} {catalog_nbr}")
