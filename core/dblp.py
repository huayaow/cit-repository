import requests
import json
import string
import re
import bibtexparser
import time
import random
from termcolor import cprint
from html.parser import HTMLParser

class DBLP:
  def __init__(self):
    self.publ_url = 'https://dblp.org/search/publ/api'
    self.venue_url = 'https://dblp.org/search/venue/api'
    self.scholar_url = 'https://dblp.org/search/author/api'
    self.bib_url = 'https://dblp.org/rec/{}.html?view=bibtex'

  def search_paper(self, keywords, already_have=[], excluded=[], after_year=None) -> list:
    """
    Search papers by keywords, and return a list of identified papers (in json format, with
    'year', 'type', 'author', 'title', 'field', 'tag', 'booktitle', 'abbr', 'vol', 'no',
    'pages', 'doi' fields). The paper titles that are already included in already_have[] and
    excluded[] will be ignored. According to DBLP, the maximum number returned will be 1000.

    @:param keyword: a list of searching keywords
    @:already_have: a list of paper titles that have already been included
    @:excluded: a list of paper titles that shoud be excluded
    @:param after: only search papers that are published after the given year (optional)
    """
    paper_obtained = []   # a list of all papers found
    paper_id = set()      # maintain id for duplication detection
    for keyword in keywords:
      url = self.publ_url + '?q=' + '+'.join(keyword.split(' ')) + '&format=json&h=1000'
      cprint('[dblp] ' + url, 'light_grey', 'on_light_green')
      
      response = requests.post(url)
      data = json.loads(response.text)
      cprint('* Seach "{}" -> hit {} papers'.format(keyword, int(data['result']['hits']['@total'])), 'green')

      cprint('* Filtering and converting format ...', 'light_green')
      if after_year:
        print('* After year: {}'.format(after_year))

      for each in data['result']['hits']['hit']:
        # the paper info field
        info = each['info']

        # skip unwanted results
        if (after_year and int(info['year']) < after_year):
          continue
        if (each['@id'] in paper_id):
          continue
        if ('venue' in info and info['venue'] == 'CoRR'):
          continue

        # there might be a period symbol (.) in the returned title field
        tp_title = info['title'][:-1].lower() if info['title'].endswith('.') else info['title'].lower()

        # skip already-have and exlcuded papers
        if (tp_title in already_have):
          continue
        if (tp_title in excluded):
          continue

        # skip if the dblp item has no author
        if ('authors' not in info):
          continue
        
        # convert the format of each newly found paper (via DBLP APIs)
        print('> find: ' + info['title'])
        paper = self.parse_paper_info(info)
        
        paper_obtained.append(paper)
        paper_id.add(each['@id'])
    assert len(paper_id) == len(paper_obtained)

    # order the final list by year
    paper_ordered = sorted(paper_obtained, key=lambda d: d['year'], reverse=True)
    cprint('[dblp] Find {} new papers (after year {})'.format(len(paper_ordered), after_year), 'light_grey', 'on_light_green')

    return paper_obtained
    
  def search_by_title(self, paper_title) -> dict:
    """
    Determine whether a given paper (title) is included in DBLP. If it is included, return 
    the information of this paper.
    """
    cprint('* getting infomation for "{}"'.format(paper_title), 'green')
    url = self.publ_url + '?q=' + '+'.join(paper_title.split(' ')) + '&format=json'
    response = requests.post(url)
    data = json.loads(response.text)

    if int(data['result']['hits']['@total']) == 0:
      return {}
    else:
      for each in data['result']['hits']['hit']:
        info = each['info']
        hit_title = info['title'].lower().replace('.', '')
        if paper_title.lower() != hit_title.lower():
          cprint('[DBLP] found similar paper title: ' + hit_title, 'yellow')
        else:
          return self.parse_paper_info(info)
  
  def parse_paper_info(self, info):
    """
    Convert the DBLP search return data (of a paper) to the customised format. 
    """
    # manage to convert the publication venue abbr name into its corresponding full name
    # based on the bibTex information of this paper
    bib = self.get_bibtex(info['key'])
    venue, venue_abbr = '', ''
    # 1) for article publications, use DBLP venue API
    if bib['ENTRYTYPE'] == 'article':
      venue_abbr = info['key'].split('/')[1]
      venue = self.extract_venue_text(info['venue'], venue_abbr)
    # 2) else, find the venue from bibTex
    else:
      if bib['ENTRYTYPE'] == 'phdthesis':
        venue = bib['school']
      else:
        # bib['ENTRYTYPE'] == 'inproceedings' or 'incollections', ...
        venue_abbr = info['key'].split('/')[1]
        venue = bib['booktitle']

    # handle authors (based on the info structure)
    authors = info['authors']['author']
    if type(authors) is not list:
      author_str = authors['text'].rstrip(string.digits).strip()
    else:
      author_str = ', '.join([e['text'].rstrip(string.digits).strip() for e in authors])

    # final data
    paper = {
      'type': bib['ENTRYTYPE'],
      'title': info['title'].replace('.', ''),
      'author': author_str,
      'booktitle': venue,
      'abbr': venue_abbr.upper(),
      'vol': info['volume'] if 'volume' in info else '',
      'no': info['number'] if 'number' in info else '',
      'pages': info['pages'] if 'pages' in info else '',
      'year': info['year'],
      'doi': info['doi'] if 'doi' in info else '',
      'field': '',
      'tag': ''
    }
    return paper

  # ------------------------------------------------------------------------------------ #
  # functions to extract detailed information of a given paper
  # ------------------------------------------------------------------------------------ #
  class BibHTMLParser(HTMLParser):
    def __init__(self):
      super().__init__()
      self.data = []
      self.capture = False

    def handle_starttag(self, tag, attrs):
      if tag == 'pre':
        self.capture = True

    def handle_endtag(self, tag):
      if tag == 'pre':
        self.capture = False

    def handle_data(self, data):
      if self.capture:
        self.data.append(data)
        
  def get_bibtex(self, dblp_key):
    """
    Return the bibtex information of a particular paper (specified by the key of DBLP)
    """
    url = self.bib_url.format(dblp_key)
    response = requests.post(url)
    parser = self.BibHTMLParser()
    parser.feed(response.text)

    bib = bibtexparser.loads(parser.data[0])
    bib = bib.entries[0]
    # remove symbols like {, }, and \n from each entry
    for each in bib.keys():
      bib[each] = bib[each].replace('\n', ' ')
      for s in ['{', '}', '\\', '"']:
        bib[each] = bib[each].replace(s, '')
    return bib

  def extract_venue_text(self, text, abbr):
    """
    Use DBLP venue API to extract the full name of a publication venue. 
    :param text: short name of a venue
    :param abbr: abbr of the venue
    :return: full name (if found)
    """ 
    wait_time = random.uniform(1, 3)
    time.sleep(wait_time)

    # try five times
    url = self.venue_url + '?q=' + '+'.join(text.split(' ')) + '&format=json'
    for i in range(5):
      try:
        response = requests.post(url)
      except requests.exceptions.RequestException as e:
        cprint('extract_venue_text: ' + e, 'red')
        wait_time *= 2
      time.sleep(wait_time)
    
    # try to parse the received data
    try:
      data = json.loads(response.text)
    except:
      cprint(response.text, 'red')
      exit(-1)

    if int(data['result']['hits']['@total']) > 0:
      for each in data['result']['hits']['hit']:
        ab = each['info']['url'].split('/')[-2]
        if ab == abbr:
          venue = each['info']['venue']
          venue = re.sub('[\(].*?[\)]', '', venue)
          return venue
    return ''

if __name__ == '__main__':
  dblp = DBLP()
  r = dblp.search_by_title('Algorithmic Optimizations for Deriving Minimal Forbidden Tuples')
  print(r)
