import pandas
import requests
from bs4 import BeautifulSoup

d = requests.get('https://activities.osu.edu/involvement/student_organizations/find_a_student_org?v=list&s=computer&c=Columbus')
data = d.text
#print(data)

soup = BeautifulSoup(data, 'html.parser')

# condensed_html = soup("tbody")
# #more_condensed_html = condensed_html("tr", class_="")
# print(condensed_html)

print(soup.select("ctl00_ContentBody_pageFormControl_panel_listing > div.c-table-container.u-scroll > table > tbody > tr:nth-child(2) > td:nth-child(1) > strong"))