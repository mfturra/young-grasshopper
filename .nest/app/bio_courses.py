import re
import requests
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup

# request HTML page
url = "https://catalog.mit.edu/degree-charts/biology-course-7/"
# data = requests.get(url).text
data = requests.get(url)
tree = html.fromstring(data.content)

# XPath
res_course_xpath = '/html/body/div[4]/div[3]/div/div/table[3]/tbody'
res_elements = tree.xpath(res_course_xpath)
res_courses = []

# Function to clean up course titles
def clean_course_title(title):
    # Match and remove leading numbers and trailing '12'
    cleaned_title = title
    prefix_removed = False

    for i in range(len(title)):
        if title[i].isdigit() or title[i] == '.':
            continue
        else:
            cleaned_title = title[i:]
            prefix_removed = True
            break
    
    if cleaned_title[:3] == '[J]':
        cleaned_title = cleaned_title[3:]

    if cleaned_title.endswith('12'):
        cleaned_title = cleaned_title[:-2]

    cleaned_title = cleaned_title.replace('&', 'and')

    words = cleaned_title.split()
    cleaned_title = ' '.join(words)

    cleaned_title = cleaned_title.strip()

    return cleaned_title

if res_elements:
    rows = res_elements[0].xpath('.//tr')
    for row in rows:
        cells = row.xpath('.//td')
        if len(cells) >= 2:

            raw_title = cells[0].text_content().strip()
            units = cells[1].text_content().strip()
            
            # Clean the raw title
            cleaned_title = clean_course_title(raw_title)
            
            # Append to the results
            res_courses.append({
                "course_title": cleaned_title,
                "course_units": units
            })

df = pd.DataFrame(res_courses)

print(df[['course_title', 'course_units']])

# if res_elements:
#     for element in res_elements:
#         print()

# courses = res_elements.split('12')

# courses = [course.strip() for course in courses if course.strip()]

# for course in res_courses:
#     cleaned_course = clean_course_title(course)
#     res_courses.append(cleaned_course)

# df = pd.DataFrame({
#     'course_title': cleaned_course,
#     'course_units': [12] * len(res_courses)
# })



# if res_elements:
#     for element in res_elements:
#         raw_text = element.text_content()

#         # Replace non-breaking spaces and clean whitespace
#         courses = raw_text.split('12')

#         for course in courses:
#             if course:
#                 course.strip()
        

#         for course in courses:
#             course_units = '12'
#             cleaned_title = clean_course_title(course_title)
#             res_courses.append({"course_title": cleaned_title, "course_units": course_units})
# else:
#     print("No data found at the specified path.")


# res_course_df = pd.DataFrame(res_courses)

# print(res_course_df)
# # parse content
# soup = BeautifulSoup(data, 'html.parser')

# # find classes for tables
# req_table = soup.find('table', {'class': 'sc_courselist'}) #['sc_sctable', 'tbl_girs'['sc_courselist'] ['sc_footnotes'] ['sc_courselist'] ['sc_footnotes'] ['sc_courselist']

# req_courses = []
# res_courses = []

# if req_table:
#     rows = req_table.find_all('tr')
#     print(req_table)
#     # extract biology req courses
#     for row in rows[1:12]:
#         cols = row.find_all('td')
#         if len(cols) == 3:
#             # course_code = cols[0].get_text(strip=True)
#             req_course_title = cols[1].get_text(strip=True)
#             req_course_units = cols[2].get_text(strip=True)
#             req_courses.append({'Title': req_course_title, 'Units': req_course_units})
#         elif len(cols) == 2:
#             req_course_title = cols[1].get_text(strip=True)
#             req_courses.append({'Title': req_course_title, 'Units': '12'})
    
#     # extract biology restricted electives 
#     for row in rows[12:]:
#         if len(cols) == 3:
#             res_course_title = cols[1].get_text(strip=True)
#             res_course_units = cols[2].get_text(strip=True)
#             res_courses.append({'Title': res_course_title, 'Units': res_course_units})
#         elif len(cols) == 2:
#             res_course_title = cols[1].get_text(strip=True)
#             res_courses.append({'Title': res_course_title, 'Units': '12'})

# # create dataframes based off course lists
# req_course_df = pd.DataFrame(req_courses)
res_course_df = pd.DataFrame(res_courses)

print(res_course_df)

# drop unnecessary row
# req_course_df = res_course_df.drop([9])

# output result
# print(req_course_df)



# for req_table in soup.find_all('table'):
#     print(table.get('class'))

# # Create list with all tables
# tables = soup.find_all('tables')
# table = soup.find('table', class_='sc_courselist')

# # create df for data
# df = pd.DataFrame(columns=['Required Subjects', 'Units'])

# # collect data from tables
# for row in table.tbody.find_all('tr'):
#     # find all data in cols
#     columns = row.find_all('td')

#     if(columns != []):
#         print(columns)
        # req_subjects = columns[0].text.strip()
        # units = columns[1].text.string()

# # extract key info
# title = soup.title.string
# paragraphs = soup.find_all('p')

# print(title)
# for p in paragraphs:
#     print(p.text)

# pull table data
# req_courses = tree.xpath('')