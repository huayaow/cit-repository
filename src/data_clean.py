import pandas as pd

def strip_formater(text):
  text = str(text).strip()
  if text == 'not found' or text == 'nan' or text == 'In press':
    text = ''
  return text

def type_formater(text):
  text = text.strip()
  if text in {'inbook', 'incollection'}:
    text = 'inproceedings'
  assert text in {'article', 'inproceedings', 'phdthesis', 'techreport', 'book'}
  return text

def author_formater(text):
  text = text.strip().split(',')
  text = [i.strip() for i in text]
  return ', '.join(text)

csv_filename = 'data/list.csv'
df = pd.read_csv(csv_filename, sep=',', header=0)
print(df.dtypes)

#df['type'] = df['type'].map(type_formater)
#df['author'] = df['author'].map(author_formater)
df['booktitle'] = df['booktitle'].map(venue_formater)
#df['pages'] = df['pages'].map(lambda x: str(x).replace('--', '-'))

df.to_csv(csv_filename, sep=',', encoding='utf-8', index=False, header=True)
