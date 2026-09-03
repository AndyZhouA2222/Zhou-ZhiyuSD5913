import requests
from lxml import html

import dotenv
import os
import datetime

# load the environment variables
dotenv.load_dotenv()

# get the year and filename from the environment variables
year = int(os.getenv('YEAR', 2024))
filename = os.getenv('FILENAME', "crawled-page-{year}.html").format(year=year)

# initialize the data list
data = []

# check if the page exists
if not os.path.exists(filename):

    # fetch the page if it doesn't exist
    # Ignore proxy settings inherited from the shell; this URL works directly.
    session = requests.Session()
    session.trust_env = False
    page = session.get(os.getenv('URL'), timeout=30)
    page.raise_for_status()

    # save the page to a file
    with open(filename, 'w', encoding='UTF8') as f:
        f.write(page.text)

    page = page.text

else:
    # if the page exists, read it from the file
    with open(filename, 'r', encoding='UTF8') as f:
        page = f.read()

# parse the page to html
tree = html.fromstring(page)

# get the rows from the table
rows = tree.xpath(os.getenv('ROW_XPATH'))

# print the number of rows
print(len(rows))

# print the rows
for row in rows:
    print(row.text_content())
