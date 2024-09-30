import csv


def read_csv_file(filename):
  with open(filename, newline='') as file:
    r = csv.reader(file, delimiter=' ', quotechar='|')
    for row in r:
      print(', '.join(row))

if __name__ == '__main__':
  read_csv_file('data/list.csv')
