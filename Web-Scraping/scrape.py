import pandas as pd
import requests
from bs4 import BeautifulSoup

club = "computer"
campus = "Columbus"

d = requests.get(
    f'https://activities.osu.edu/involvement/student_organizations/find_a_student_org?v=list&s={club}&c={campus}')
data = d.text
# print(data)

soup = BeautifulSoup(data, 'html.parser')

# Good tutorial:
#https://medium.com/geekculture/web-scraping-tables-in-python-using-beautiful-soup-8bbc31c5803e

# Finding the holy table
table = soup.find('table', class_='c-table')
# print(table)
# Collecting Ddata
df = pd.DataFrame(columns=["name", "topics"])
for row in table.find_all('tr')[1:]:
    # print(f"Our row is {row}")
    # Find all data for each column
    columns = row.find_all('td')
    club_name = columns[0].text.strip()
    topics = columns[2].text.strip().split(",")
    if topics[-1] == '':
        topics.pop()
    df.append({"name":club_name, "topics": topics}, ignore_index=True)
print(df)


# condensed_html = soup("tbody")
# #more_condensed_html = condensed_html("tr", class_="")
# print(condensed_html)

#print(soup.select("ctl00_ContentBody_pageFormControl_panel_listing > div.c-table-container.u-scroll > table > tbody > tr:nth-child(2) > td:nth-child(1) > strong"))
