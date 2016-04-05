#!/usr/bin/env python
# -*- coding: utf8 -*-  #https://www.python.org/dev/peps/pep-0263/
import os
import sys
import io, csv, argparse
from bs4 import BeautifulSoup

# Parameters

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',
                    required=True,
                    type=str,
                    default=False,
                    dest="file",
                    metavar="<xml file parser>",
                    help="please use this command first 'pdftohtml -xml -i file.pdf' if you haven't used yet or use python main.py filename.xml > /path/to/destination.csv")

args = parser.parse_args()

# collect and store data in  "data"

soup = BeautifulSoup(open(args.file), "lxml-xml")
f=open("/home/nikhil/Desktop/hell","w")
str1=str(soup)
f.write(str1)

data = {}


for page in soup.find_all('page'):

  pgnb = int(page.get('number'))
  pgheight = int(page.get('height'))
  pgwidth = int(page.get('width'))

  data[pgnb] = {}

  for text in page.find_all('text'):

    top = int(text.get('top'))


    if data[pgnb].has_key(top) is False:  #instead  of  'has_key'  we  can  use  "in"
      data[pgnb][top] = {}

    left = int(text.get('left'))

    data[pgnb][top][left] = text.get_text()

# Expected number of cells per line


numbcells = 0
for page in data:
  for line in data[page]:
    cells = len(data[page][line])
    if numbcells < cells:
      numbcells = cells


# Recover the approximate positions of the columns

pos_of_cols = {}

for page in data:
  for line in data[page]:
    for cell in data[page][line]:
      if pos_of_cols.has_key(cell) is False:
        pos_of_cols[cell] = 1
      else:
        pos_of_cols[cell] += 1

cols = []

#  Frequently we take by limiting the number of cells expected

for cell in sorted(pos_of_cols, key=pos_of_cols.get, reverse=True):
  if len(cols) < numbcells:
    cols.append(cell)

cols.sort()

# Create mini intervals / max possible positions


margin = 10


ranges = {}

for k, col in enumerate(cols):
  mini = col-margin
  if k == 0:
    mini = 0
  try:
    maxi = cols[k+1]-margin-1
  except IndexError:
    maxi = col*2
  ranges[col] = {'mini': mini, 'maxi': maxi}

# sort and view data


sorted_data = sorted(data)

for page in sorted_data:

  sorted_page = sorted(data[page])

  for line in sorted_page:

    sorted_line = sorted(data[page][line])

    nb = len(sorted_line)

    row = {}

    # If fewer cells than expected

    if nb < numbcells:

      # It creates an empty structure with as many columns as expected

      for r in ranges:
        row[r] = ''

      # Is filled with the values ​​according to their positions

      for cell in sorted_line:

        ok = False

        for r in ranges:

          if cell >= ranges[r]['mini'] and cell <= ranges[r]['maxi']:

            row[r] = data[page][line][cell]

            ok = True

        if ok is False:
          print(cell)
          print("Not found in ranges")

    else:

      for cell in sorted_line:

        row[cell] = data[page][line][cell]

    output = io.BytesIO()
    print output

    writer = csv.DictWriter(output, fieldnames=sorted(row.keys()), quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow({k:v.encode('utf8') for k,v in row.items()})
    print(output.getvalue().strip())





