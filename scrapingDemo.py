# Import the `requests` package
import requests

# Import `BeautifulSoup` from the `bs4` package
from bs4 import BeautifulSoup

# URL for Professor Eskandarian's course explorer tool:
url = "https://www.cs.unc.edu/~saba/COMP_classes/spring2023/"

# Get data from the URL
data = requests.get(url)

# Find data text (the HTML!) 
html = data.text

# Parse data using the HTML that we extracted using the `html.parser`, and save output to soup.
soup = BeautifulSoup(html, 'html.parser')

# Now, let's print out the "prettified" version of that HTML!
#print(soup.prettify())

# Find all table elements on the page
tables = soup.find_all("table")

print("Number of tables: " + str(len(tables)))
print("Tables:")
print(tables)

# Select the table
table = tables[0]
table

# Find all rows in the table
rows = table.find_all("tr")

for i in range(0,5):
    print(rows[i])
    print("\n")

# Find all <td> elements in the row
tds = rows[1].find_all("td")

# Iterate over all <td> elements and print them out
for td in tds:
    print(td)

# Iterate over all <td> elements and print out their texts
for td in tds:
    print(td.text)

# Iterate over all rows...
for row in rows:
    
    # Find all <td> elements in the row
    tds = row.find_all("td")

    # Iterate over all <td> elements and print out their texts
    for td in tds:
        print(td.text)
        
    # Add line break between data for each row
    print("\n")

# Let's use some handy Python list notation:
# We can create a subset of list `a` with `a[start_index:end_index:step]`
# So, if we want every other row of `rows`, we can say `row[1::2]`
#     Note: Remember, we start at index 1 because row 0 is our header rows!
#     Note: Leaving end index blank implies we are going until the list ends!

# Iterate over every other row...
for row in rows[1::2]:
    
    # Find all <td> elements in the row
    tds = row.find_all("td")

    # Iterate over all <td> elements and print out their texts
    for td in tds:
        print(td.text)
        
    # Add line break between data for each row
    print("\n")


# Determine column headers
column_headers = ["Class Number", "Class", "Meeting Time", "Instructor", "Room", "Unreserved Enrollment", "Reserved Enrollment", "Wait List"]

#Create list to store final data
final_data_list = []

# Iterate over every other row...
for row in rows[1::2]:
    
    row_data = {}
    
    # Find all <td> elements in the row
    tds = row.find_all("td")

    # Iterate over all <td> elements and print out their texts
    for index, td in enumerate(tds):
        # Get correct column header for the data
        header = column_headers[index]
        # Store the data in the dictionary
        row_data[header] = td.text.replace("\xa0", "")
    
    # Add data to final list    
    final_data_list.append(row_data)

final_data_list

import pandas as pd

df = pd.DataFrame.from_dict(final_data_list)

df.head()