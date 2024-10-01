import csv
import json
import pandas as pd

csv_filename = '_data/list.csv'
json_filename = '_data/list.json'

def csv_sort():
  df = pd.read_csv(csv_filename, sep=',', header=0)
  df1 = df.sort_values('year', ascending=False)
  print(df1)
  df1.to_csv(csv_filename, sep=',', encoding='utf-8', index=False, header=True)

def csv_to_json():
  csvfile = open(csv_filename, 'r')
  jsonfile = open(json_filename, 'w')
  reader = csv.DictReader(csvfile)
  rows = list(reader)
  print('[JSON] contain {} papers in "_data/list.json"'.format(len(rows)))
  json.dump(rows, jsonfile, indent=2)

if __name__ == '__main__':
  # csv_sort()
  csv_to_json()
        