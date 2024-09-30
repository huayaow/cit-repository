import csv
import json

def csv_to_json(csvfile, jsonfile):
  # convert csv file into json file
  csvfile = open(csvfile, 'r')
  jsonfile = open(jsonfile, 'w')

  fields = ("year", "type", "author", "title", "field", "tag", "booktitle", 
            "abbr", "vol", "no", "pages", "doi")
  reader = csv.DictReader(csvfile, fields)
  for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(',\n')

if __name__ == '__main__':
  csv_to_json('_data/list.csv', '_data/list.json')
