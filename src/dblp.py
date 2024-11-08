import requests
import json
import string
import re
import bibtexparser
import time
from html.parser import HTMLParser

TYPE_MATCH = {
  'Journal Articles': 'article',
  'Conference and Workshop Papers': 'inproceedings',
  'Books and Theses': 'book',
  'Parts in Books or Collections': 'book',
  'Informal and Other Publications': 'informal',
}

class DBLP:
  def __init__(self):
    self.publ_url = 'http://dblp.org/search/publ/api'
    self.venue_url = 'https://dblp.org/search/venue/api'
    self.scholar_url = 'https://dblp.org/search/author/api'

  def search_paper(self, keywords=None, already_have=[], excluded=[], after_year=None) -> list:
    """
    Search papers by keywords, and return papers (in formatted type) that are not included in 
    current already_have list (a list of paper titles). According to DBLP, the maximum number 
    returned will be 1000.

    @:param keyword: a list of searching keywords, default = ['combinatorial testing']
    @:already_have: a list of paper titles that have been included
    @:excluded: a list of paper titles that shoud be excluded
    @:param after: only search papers published after the given year
    """
    if keywords is None:
      keywords = ['covering array']

    paper_obtained = []   # list of all papers found
    paper_id = set()      # maintain id for duplication detection
    for keywords in keywords:
      url = self.publ_url + '?q=' + '+'.join(keywords.split(' ')) + '&format=json&h=1000'
      response = requests.post(url)
      print('[dblp] ' + url)
      data = json.loads(response.text)

      print('[dblp] seach "{}" -> hit {} papers'.format(keywords, int(data['result']['hits']['@total'])))
      print('[dblp] filtering and converting format ...')
      for each in data['result']['hits']['hit']:
        # the paper info field
        info = each['info']

        # skip unwanted results
        if (after_year is not None and int(info['year']) < after_year):
          continue
        if (each['@id'] in paper_id):
          continue
        if ('venue' in info and info['venue'] == 'CoRR'):
          continue
        # there might be a period symbol (.) in the returned title field
        tp_title = info['title'][:-1].lower() if info['title'].endswith('.') else info['title'].lower()
        if (tp_title in already_have): # already have
          continue
        if (tp_title in excluded): # shuold be excluded
          continue
        
        print('\t >> ' + info['title'])
        # convert the format of each paper (will call DBLP APIs)
        paper = self.parse_paper_info(info)
        # print(paper)
        paper_obtained.append(paper)
        paper_id.add(each['@id'])
    assert len(paper_id) == len(paper_obtained)

    # order by year
    paper_ordered = sorted(paper_obtained, key=lambda d: d['year'], reverse=True)
    print('[dblp] find {} new papers (after year {})'.format(len(paper_ordered), after_year))
    return paper_obtained
    
  def search_by_title(self, paper_title) -> dict:
    """
    Determine whether a given paper (title) is included in DBLP. If it is included, return the
    cit-repository format of this paper.
    """
    url = self.publ_url + '?q=' + '+'.join(paper_title.split(' ')) + '&format=json'
    response = requests.post(url)
    data = json.loads(response.text)

    if int(data['result']['hits']['@total']) == 0:
      return {'status': 'not included', 'data': {}}
    else:
      for each in data['result']['hits']['hit']:
        info = each['info']
        hit_title = info['title'].lower().replace('.', '')
        if paper_title.lower() != hit_title.lower():
          print('[DBLP] found similar paper title: ' + hit_title)
        else:
          return {'status': 'included', 'data': self.parse_paper_info(info)}
  
  def parse_paper_info(self, info):
    """
    Convert the DBLP search return data (of a paper) to the cit-repository format.
    """
    # the bibTex information of this paper
    bib = self.get_bibtex(info['key'])

    # handle authors
    authors = info['authors']['author']
    if type(authors) is not list:
      author_str = authors['text'].rstrip(string.digits).strip()
    else:
      author_str = ', '.join([e['text'].rstrip(string.digits).strip() for e in authors])

    # handle publication venue
    venue, venue_abbr = '', ''
    # 1) for article publications, use DBLP venue API
    if bib['ENTRYTYPE'] == 'article':
      venue_abbr = info['key'].split('/')[1]
      venue = self.extract_venue_text(info['venue'], venue_abbr)
    # 2) else, find the venue from bibTex
    else:
      if bib['ENTRYTYPE'] == 'inproceedings':
        venue_abbr = info['key'].split('/')[1]
        venue = bib['booktitle']
      elif bib['ENTRYTYPE'] == 'phdthesis':
        venue = bib['school']

    # final data
    paper = {
      'type': TYPE_MATCH[info['type']],
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
    url = 'https://dblp.org/rec/{}.html?view=bibtex'.format(dblp_key)
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
    Use DBLP venue API to extract the full name of a publication venue. This works the best if a match can be found.
    :param text: short name of a venue
    :param abbr: abbr of the venue
    :return: full name (if found)
    """
    time.sleep(1)
    url = self.venue_url + '?q=' + '+'.join(text.split(' ')) + '&format=json'
    response = requests.post(url)
    try:
      data = json.loads(response.text)
    except:
      print(response.text)
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
  r = dblp.search_by_title('Covering arrays on graphs')
  print(r)
