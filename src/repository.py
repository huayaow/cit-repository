from librarian import Librarian
from generate_html import Generator
import argparse


parser = argparse.ArgumentParser(description='repository management scripts')
parser.add_argument('action', help='the operation to be performed')
parser.add_argument("--after", help='search certain years only')
parser.add_argument("--date", help='update date')

args = parser.parse_args()

if args.action == 'search':
  print('[*] Search new papers in DBLP ...')
  lib = Librarian()
  lib.search_new_papers(after_year=args.after)
  print('[*] Please manually check add.csv and copy new paper items to paper.csv')

elif args.action == 'update':
  if not args.date:
    print('[*] Update date is required')
    exit(-1)
  
  print('[*] Update repository data ...')
  lib = Librarian()
  lib.update_scholar()
  lib.update_paper()
  lib.update_statistic()
  
  print('[*] Generate HTML pages ...')
  g = Generator()
  g.generate_index(date=args.date)
  g.generate_papers_list()
  g.generate_tools_list()
  g.generate_statistics()

else:
  print('Invalid arguments')
