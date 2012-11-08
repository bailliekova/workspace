## SCRIPT TO PARSE NYTIMES election results 
## 2012-11-5 

import bs4
import urllib2
import re
import json
import sys

baseurl='http://elections.nytimes.com/2010/results/'
state=sys.argv[1]
try:
    conn=urllib2.urlopen(baseurl+state)
except urllib2.URLError, e:
    print e
data=conn.read()
soup=bs4.BeautifulSoup(data)
divs=soup.findAll('div', {'class':'nytint-results-group'})
datadict=dict()
tabledict=dict()
datadict[state]=dict()

#### CREATE DICTIONARY FROM OFFICE TO RESULT TABLE #####
for div in divs:
    tabledict[div.h3.contents[0].strip()]=div.table

##### GET PRESIDENT #####

#### GET HOUSE #####
table=tabledict['House of Representatives']
candlist=[]
for row in table.tr.next_siblings:
    if type(row)!=bs4.element.Tag:
        continue
    for cell in row.contents:
        if type(cell)!=bs4.element.Tag  or not cell.has_key('class'):
            continue
        if 'nytint-district-col' in cell['class']:
            district=cell.string
        elif 'nytint-vote-pct-dem' in cell['class']:
            demcount=re.sub('[^0-9]','', cell.div.span.abbr['title'])
            demname=cell.div.span.next_sibling.next_sibling.contents[0]
        elif 'nytint-vote-pct-gop' in cell['class']:
            repcount=re.sub('[^0-9]','',cell.div.span.abbr['title'])
            repname=cell.div.span.next_sibling.next_sibling.contents[0]
        else:
            continue
    candlist.append({'party': 'Democrat', 'count':demcount, 'state':state, 'district':district, 'name':demname})
    candlist.append({'party': 'Republican', 'count':repcount, 'state':state, 'district':district, 'name':repname})
datadict[state]['house']=candlist


#### GET SENATE #####
if 'Senate' not in tabledict:
    print json.dumps(datadict)
    sys.exit(0)
table=tabledict['Senate']
candlist=[]
for row in table.tr.next_siblings:
    if type(row)!=bs4.element.Tag or not row.has_key('class'):
        continue
    for cell in row.contents:
        if type(cell)!=bs4.element.Tag or not cell.has_key('class'):
            continue
        if 'nytint-candidate'in cell['class']:
            name=cell.div.string.strip()
        elif 'nytint-party' in cell['class']:
            try:
                party=cell.abbr['title'].strip()
            except TypeError:
                party=unicode(cell.string).strip()
        elif 'nytint-vote-count' in cell['class']:
            count=cell.string.strip().replace(',', '')
        else:
            continue
    candlist.append({'party':party, 'count': count, 'state':state, 'district':'Sen', 'name':name})
datadict[state]['senate']=candlist


print json.dumps(datadict)
