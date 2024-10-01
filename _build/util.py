import csv
import json
from papers import Paper

def csv_to_json(csvfile, jsonfile):
  # convert csv file into json file
  csv_fd = open(csvfile, 'r')
  json_fd = open(jsonfile, 'w')

  fields = ("year", "type", "author", "title", "field", "tag", "booktitle", 
            "abbr", "vol", "no", "pages", "doi")
  reader = csv.DictReader(csv_fd, fields)
  for row in reader:
    json.dump(row, json_fd)
    json_fd.write(',\n')
  
if __name__ == '__main__':
  # csv_to_json('_data/list.csv', '_data/list.json')
  with open('_data/list_temp.json') as f:
    data = json.load(f)
  # print(data)
  p = Paper()
  p.read_from_json(data[0])
  print(p)
