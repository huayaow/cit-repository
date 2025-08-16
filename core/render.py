import csv
import json
from papers import Paper
from tools import Tool
from scholars import Scholar
from jinja2 import Environment, FileSystemLoader

class Data:
  def __init__(self):
    self.papers = []         # list of all papers
    self.scholars = []       # list of all scholars
    self.tools = []          # list of all tools
    self.statistics = None   # statistics data (json)
    self.rank = []           # list of ranked scholars

    paper_filename = 'data/paper.csv'
    scholar_filename = 'data/scholar.csv'
    tools_filename = 'data/tool.csv'
    statistics_filename = 'data/statistic.json'
    rank_filename = 'data/rank.csv'

    with open(paper_filename, 'r') as file:
      for each in csv.DictReader(file):
        p = Paper(each)
        self.papers.append(p)
    
    with open(scholar_filename, 'r') as file:
      for each in csv.DictReader(file):
        p = Scholar(each)
        self.scholars.append(p)
    
    with open(tools_filename, 'r') as file:
      for each in csv.DictReader(file):
        p = Tool(each)
        self.tools.append(p)

    with open(statistics_filename) as file:
      self.statistics = json.load(file)

    with open(rank_filename, 'r') as file:
      for each in csv.DictReader(file):
        p = Scholar(each)
        self.rank.append(p)

class Render:
  def __init__(self):
    self.env = Environment(loader = FileSystemLoader('templates'))
    self.data = Data()
    print('[Render] load data from files')

  def render(self, template_name, context, output_filename):
    template = self.env.get_template(template_name)
    html = template.render(context)
    with open(output_filename, 'w') as f:
      f.write(html)
  
  def render_index(self, update_date):
    """
    * basic descriptions <- Last update date, final year of bar chart
    * stat <- number of papers, scholars, tools
    * chart <- cumulative number of publications, and distribution of research topics
    """
    context = {
      'static_url': '',
      'active_page': 'home',
      'update_date': update_date,
      'final_year': self.data.statistics['cumulative-2000']['year'][-1],
      'stat': {
        "papers": len(self.data.papers),
        "scholars": len(self.data.scholars),
        "tools": len(self.data.tools)
      },
      'chart': {
        'bar': {
          'labels': self.data.statistics['cumulative-2000']['year'],
          'data': self.data.statistics['cumulative-2000']['value']
        },
        'pie': { 
          'labels': self.data.statistics['distribution']['fields'],
          'data': self.data.statistics['distribution']['count']
        }
      }
    }
    self.render('index.j2.html', context, 'index.html')
    self.render('index-chart.j2.js', context, 'assets/index-chart.js')
    print('[Render] generate index.html: {}'.format(update_date))

  def render_paper(self):
    context = {
      'static_url': '../',
      'active_page': 'paper',
      'paper_number': len(self.data.papers),
      'paper_list': self.data.papers
    }
    self.render('paper.j2.html', context, 'render/paper.html')
    print('[Render] generate paper.html: {} papers'.format(context['paper_number']))
  
  def render_tool(self):
    context = {
      'static_url': '../',
      'active_page': 'tool',
      'tool_number': len(self.data.tools),
      'tool_list': self.data.tools
    }  
    self.render('tool.j2.html', context, 'render/tool.html')
    print('[Render] generate tool.html: {} tools'.format(context['tool_number']))

  def render_statistic(self):
    context = {
      'static_url': '../',
      'active_page': 'statistic',
      'chart_annual': {
        'year': self.data.statistics['annual']['year'],
        'value': self.data.statistics['annual']['value']
      },
      'chart_topic': {
        'year': self.data.statistics['annual']['year'],
        'generation': self.data.statistics['topic']['Generation'],
        'application': self.data.statistics['topic']['Application'],
        'evaluation': self.data.statistics['topic']['Evaluation'],
        'optimization': self.data.statistics['topic']['Optimization'],
        'model': self.data.statistics['topic']['Model'],
        'diagnosis': self.data.statistics['topic']['Diagnosis']
      }
    }
    self.render('statistic.j2.html', context, 'render/statistic.html')
    self.render('statistic-chart.j2.js', context, 'assets/statistic-chart.js')
    print('[Render] generate statistic.html')

  def render_rank(self):
    context = {
      'static_url': '../',
      'active_page': 'rank',
      'scholar_list': self.data.rank
    }  
    self.render('rank.j2.html', context, 'render/rank.html')
    print('[Render] generate rank.html')

if __name__ == '__main__':
  r = Render()
  r.render_index('Aug 2025')
  r.render_paper()
  r.render_tool()
  r.render_statistic()
  r.render_rank()
