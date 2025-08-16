from librarian import Librarian
from render import Render
import argparse


parser = argparse.ArgumentParser(description='repository management scripts')
parser.add_argument('action', help='the operation to be performed')
parser.add_argument("--after", help='search certain years only', type=int, default=None)
parser.add_argument("--date", help='update date', type=str)

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
  lib.update_table()
  lib.update_statistic()
  
  print('[*] Generate HTML pages ...')
  render = Render()
  render.render_index(update_date=args.date)
  render.render_paper()
  render.render_tool()
  render.render_statistic()

else:
  print('Invalid arguments')
