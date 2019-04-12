import os
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.interbrand.com/best-brands/best-global-brands/2018/ranking/#?listFormat=ls'
s = requests.Session()
r = s.get(url)

soup = BeautifulSoup(r.text, features='lxml')
ranking = soup.find_all('li', attrs={'class': 'brand-item'})

datasheet = [['Rank', 'Brand Name', 'Country', 'Region', 'Sector', 'Brand Valuation']]
datasheet.extend([[str(index), company['data-brand-name'], company['data-country'], company['data-region'], company['data-sector'], str(company['data-value'])] for index, company in enumerate(ranking, start=1)])

# Output to CSV file
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
    f.write("# Interbrand Top 100 Global Brands\n\n")
    f.writelines(table)