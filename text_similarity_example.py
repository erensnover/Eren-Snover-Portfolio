'''
This was originally written in Google Colab so the formatting and sequence of events are a bit disorganized from that,
but this file was used to join two data sets based on individual names from both data sets. However, in both data sets
the names were often spelled differently between them (Ex: "Joe Smith" vs "Joseph P Smith"). This file uses the text
similarity model known as Cosign Similarity to determine if two strings were reffering to the same individual.
'''


from google.colab import drive

drive.mount('/content/gdrive')

import pandas as pd

dataPP=pd.read_excel(r'file path',1)



dataIE=pd.read_excel(r'file path',0)

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


similarity_score = similar("Apple", "Apple")
print(similarity_score)

try:
  dataPP['PROPERTY ADDRESS'] = dataPP['PROPERTY ADDRESS'].apply(lambda x: int(x) if x == x else "")

except:
  dataPP['PROPERTY ADDRESS'] = dataPP['PROPERTY ADDRESS']

display(dataPP)

display(dataIE)

dataPP.insert(7,"PROPER ADDRESS FORMAT",str(dataPP.iloc[20,dataPP.columns.get_loc('PROPERTY ADDRESS2')]) + " " + str("{:04d}".format(dataPP.iloc[20,dataPP.columns.get_loc('PROPERTY ADDRESS')])),True)

for x in range(len(dataPP['PROPER ADDRESS FORMAT'])) :
  try:
    dataPP['PROPER ADDRESS FORMAT'][x] = str(dataPP.iloc[x,dataPP.columns.get_loc('PROPERTY ADDRESS2')]).strip() + " " + "{:04d}".format(dataPP.iloc[x,dataPP.columns.get_loc('PROPERTY ADDRESS')])
  except:
    dataPP['PROPER ADDRESS FORMAT'][x] = dataPP['PROPER ADDRESS FORMAT'][x]

display(dataPP)

from sklearn.metrics.pairwise import cosine_similarity

import math
import re
from collections import Counter

WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

print(PPIDS1)

PPIDS1 = {'tenant IE':[],
         'tenant PP':[],
         'uniqueID':[],
         'property address PP':[],
         'property address IE':[]}
def findPPID(i):
  vector = text_to_vector(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]))
  marker = None
  x = 0
  y = ''
  trackerLoc = ''
  knownLocation = str(dataIE.iloc[i,dataIE.columns.get_loc('Property Address')]).strip()
  print(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]))
  for j in range(len(dataPP['PROPERTY ADDRESS'])):
    if get_cosine(text_to_vector(str(knownLocation)),text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('PROPER ADDRESS FORMAT')]).strip())) > 0.666667:
      if get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('TAX PAYER')]))) > x:
        x = get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('TAX PAYER')])))
        marker = j
        trackerLoc = 'TAX PAYER'
      elif get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('DBA')]))) > x:
        x = get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('DBA')])))
        marker = j
        trackerLoc = 'DBA'
      elif get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('IN CARE OF')]))) > x:
        x = get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('IN CARE OF')])))
        marker = j
        trackerLoc = 'IN CARE OF'
  if(x < 0.3334):
    for k in range(len(dataPP['PROPERTY ADDRESS'])):
      if get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('TAX PAYER')]))) > x :
        x = get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('TAX PAYER')])))
        trackerLoc = 'TAX PAYER'
        marker = k
      elif get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('DBA')]))) > x :
        x = get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('DBA')])))
        marker = k
        trackerLoc = 'DBA'
      elif get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('IN CARE OF')]))) > x :
        x = get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('IN CARE OF')])))
        marker = k
        trackerLoc = 'IN CARE OF'
  if marker == None :
    PPIDS1['tenant IE'].append(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')])
    PPIDS1['tenant PP'].append('didnt find')
    PPIDS1['uniqueID'].append('didnt find')
    PPIDS1['property address PP'].append('didnt find')
    PPIDS1['property address IE'].append(knownLocation)
  else:
    PPIDS1['tenant IE'].append(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')])
    PPIDS1['tenant PP'].append(dataPP.iloc[marker,dataPP.columns.get_loc(trackerLoc)])
    PPIDS1['uniqueID'].append(dataPP.iloc[marker,dataPP.columns.get_loc('UNIQUE ID')])
    PPIDS1['property address PP'].append(dataPP.iloc[marker,dataPP.columns.get_loc('PROPER ADDRESS FORMAT')])
    PPIDS1['property address IE'].append(knownLocation)

def findPPIDSIMILAR(i):
  marker = None
  vector = text_to_vector(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]))
  x = 0
  y = ''
  trackerLoc = ''
  knownLocation = dataIE.iloc[i,dataIE.columns.get_loc('Property Address')]
  for j in range(len(dataPP['PROPERTY ADDRESS'])):
    if similar(str(knownLocation),str(dataPP.iloc[j,dataPP.columns.get_loc('PROPER ADDRESS FORMAT')]))*0.2+get_cosine(text_to_vector(str(knownLocation)),text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('PROPER ADDRESS FORMAT')]))) > 1.2:
      if similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[j,dataPP.columns.get_loc('TAX PAYER')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('TAX PAYER')]))) > x:
        x = similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[j,dataPP.columns.get_loc('TAX PAYER')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('TAX PAYER')])))
        marker = j
        trackerLoc = 'TAX PAYER'
      elif similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[j,dataPP.columns.get_loc('DBA')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('DBA')]))) > x:
        x = similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[j,dataPP.columns.get_loc('DBA')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('DBA')])))
        marker = j
        trackerLoc = 'DBA'
      elif similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[j,dataPP.columns.get_loc('IN CARE OF')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('IN CARE OF')]))) > x:
        x = similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[j,dataPP.columns.get_loc('IN CARE OF')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[j,dataPP.columns.get_loc('IN CARE OF')])))
        marker = j
        trackerLoc = 'IN CARE OF'

  if(x < 0.75):
    for k in range(len(dataPP['PROPERTY ADDRESS'])):
      if similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[k,dataPP.columns.get_loc('TAX PAYER')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('TAX PAYER')]))) > x :
        x = similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[k,dataPP.columns.get_loc('TAX PAYER')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('TAX PAYER')])))
        if x > 0.6:
          trackerLoc = 'TAX PAYER'
          marker = k
      elif similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[k,dataPP.columns.get_loc('DBA')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('DBA')]))) > x :
        x = similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[k,dataPP.columns.get_loc('DBA')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('DBA')])))
        if x > 0.6:
          marker = k
          trackerLoc = 'DBA'
      elif similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[k,dataPP.columns.get_loc('IN CARE OF')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('IN CARE OF')]))) > x :
        x = similar(str(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')]),str(dataPP.iloc[k,dataPP.columns.get_loc('IN CARE OF')]))*0.2+get_cosine(vector,text_to_vector(str(dataPP.iloc[k,dataPP.columns.get_loc('IN CARE OF')])))
        if x > 0.6:
          marker = k
          trackerLoc = 'IN CARE OF'
  print(marker)
  if x < 0.75 :
    PPIDS['tenant IE'].append(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')])
    PPIDS['tenant PP'].append('didnt find')
    PPIDS['uniqueID'].append('didnt find')
    PPIDS['property address PP'].append('didnt find')
    PPIDS['property address IE'].append(knownLocation)
  else:
    PPIDS['tenant IE'].append(dataIE.iloc[i,dataIE.columns.get_loc('TENANT NAME')])
    PPIDS['tenant PP'].append(dataPP.iloc[marker,dataPP.columns.get_loc(trackerLoc)])
    PPIDS['uniqueID'].append(dataPP.iloc[marker,dataPP.columns.get_loc('UNIQUE ID')])
    PPIDS['property address PP'].append(dataPP.iloc[marker,dataPP.columns.get_loc('PROPER ADDRESS FORMAT')])
    PPIDS['property address IE'].append(knownLocation)

PPIDS = {'tenant IE':[],
         'tenant PP':[],
         'uniqueID':[],
         'property address PP':[],
         'property address IE':[]}

string1 = 'COCOS GROOMING'
string2 = 'PROFESSIONAL DOG GROOMING'
string3 = 'BRENNER VICTORIA'
print(get_cosine(text_to_vector(string1),text_to_vector(string2)))
print(similar(string1,string2))
print(get_cosine(text_to_vector(string1),text_to_vector(string3)))
print(similar(string1,string3))

string1 = 'PROFESSIONAL DOG GROOMING'
string2 = 'COCOS GROOMING'
string3 = ''
print(get_cosine(text_to_vector(string1),text_to_vector(string2))+similar(string1,string2))
print(similar(string1,string2))
print(get_cosine(text_to_vector(string1),text_to_vector(string3))+similar(string1,string3))
print(similar(string1,string3))

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Usage
similarity_score = similar("MASON STREET 0123", "MASON STREET 0115 UN 2")  # Example similarity score
print(similarity_score)

print(get_cosine(text_to_vector('WEST PUTNAM AVENUE 0177'),text_to_vector('MASON STREET 0170')))
print(similar('IVEY BARNUM & OMARA LLC','IVY BARNUM OMARA'))
print(str(dataPP.iloc[3054,dataPP.columns.get_loc('DBA')]))
print(str(dataIE.iloc[28,dataIE.columns.get_loc('TENANT NAME')]))

print(PPIDS)



for x in range(2840,3270):
  findPPID(x)

for x in range(60,70) :
  findPPIDSIMILAR(x)

for x in range(1100,1500) :
  findPPID(x)

for x in range(len(dataIE['TENANT NAME'])) :
  try:
    findPPID(x)
  except:
    PPIDS['tenant IE'].append(dataIE.iloc[x,dataIE.columns.get_loc('TENANT NAME')])
    PPIDS['tenant PP'].append('didnt find')
    PPIDS['uniqueID'].append('didnt find')
    PPIDS['property address PP'].append('didnt find')
    PPIDS['property address IE'].append(dataIE.iloc[x,dataIE.columns.get_loc('Property Address')])

print(list(range(len(PPIDS))))



UNIQUEIDS1 = pd.DataFrame(PPIDS1,list(range(2840,3264)))

UNIQUEIDS = pd.DataFrame(PPIDS,list(range(50,60)))

UNIQUEIDS = pd.DataFrame(PPIDS,list(range(len(PPIDS['tenant PP']))))

UNIQUEIDS1

UNIQUEIDS


UNIQUEIDS1.to_excel('file path', sheet_name='Sheet1', index=False, engine='xlsxwriter')
