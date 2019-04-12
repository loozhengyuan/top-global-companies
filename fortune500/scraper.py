import os
import csv
import json
import requests
from bs4 import BeautifulSoup

urls = ['http://fortune.com/api/v2/list/2386574/expand/item/ranking/asc/{}/100'.format(i) for i in range(0, 501, 100)]
s = requests.Session()

datasheet = [['Current Rank', 'Previous Rank', 'Brand Name', 'Country', 'Industry', 'Sector', 'Revenue', 'Profit', 'Assets']]
for url in urls:
    r = s.get(url)
    data = json.loads(r.text)
    datasheet.extend([[str(company['rank']), str(company['prev_rank']), company['title'], company['meta']['hqcountry'], company['meta']['industry'], company['meta']['sector'], str(company['meta']['revenues']), str(company['meta']['profits']), str(company['meta']['assets'])] for company in data['list-items']])

directory = os.path.dirname(os.path.abspath(__file__))
filename = directory + os.sep + 'output.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(datasheet)

# Output to MD file
directory = os.path.dirname(os.path.abspath(__file__))
filename = directory + os.sep + 'README.md'
table = ["| {} |\n".format(" | ".join(datasheet[0]))]
table.extend(["| {} |\n".format(" | ".join(["---" for i in range(len(datasheet[0]))]))])
table.extend(["| {} |\n".format(" | ".join(company)) for company in datasheet[1:]])
with open(filename, 'w') as f:
    f.write("# Fortune 500 Top Global Brands\n\n")
    f.writelines(table)