## SCRIPT TO PARSE NYTIMES election results 
## 2012-11-5 

import bs4
import urllib2
import json
import sys
import us

def getFips(state):
    return us.states.lookup(state).fips

##### GET PRESIDENT #####
def getPresident(soup):
    candlist=[]
    table=soup.find(lambda tag: tag.name=='div' and tag.attrs and tag.has_key('class') and 'president' in tag['class'] and 'table' in tag['class'])
    pctreporting=unicode(table.thead.tr.th.span.string).strip()
    for row in table.tbody.find_all('tr'):
        try:
            name=unicode(row.find('td', {'class':'candidate'}).div.string)
            party=unicode(row.find('td', {'class':'party'}).string).strip()[0]
            pct=unicode(row.find('td', {'class':'pct'}).string).strip()
            votes=unicode(row.find('td', {'class':'votes'}).string).strip()
            candlist.append({'name': name, 'party': party, 'pct': pct, 'reporting': pctreporting, 'votes':votes})
        except: 
            continue
    return candlist

#### GET HOUSE #####
def getHouse(soup):
    districtdict={}
    table=soup.find('div', {'class': 'house-of-representatives'})
    districts=table.tbody.find_all('tr')
    for district in districts:
        candlist=[]
        try:
            districtnum=district.find('td', {'class':'district'}).string.strip()
        except:
            continue
        try:
            reporting=district.find('td', {'class':'rpt'}).string.strip()
        except:
            reporting='NULL'
        try:
            dem=district.find('td', {'class':'dem'})
            demname=dem.div.span.next_sibling.replace('*', '')
            dempct=dem.div.span.string.replace('%', '')
        except:
            demname='NULL'
            dempct='NULL'
        candlist.append({'party': 'D', 'name':demname, 'pct': dempct, 'reporting':reporting})
        try:
            rep=district.find('td', {'class': 'rep'})
            repname=rep.div.span.next_sibling.replace('*', '')
            reppct=rep.div.span.string.replace('%', '')
        except:
            repname='NULL'
            reppct='NULL'
        candlist.append({'party': 'R', 'name': repname, 'pct':reppct, 'reporting':reporting})
        districtdict[districtnum]=candlist
    return districtdict
        
## get Senate ####
def getSenate(soup):
    candlist=[]
    tables=soup.find_all('div', {'class':'senate'})
    if not tables:
        return []
    for t in tables:
        if 'table' in t['class']: 
            table=t
    reporting=table.thead.tr.th.span.string.strip()
    rows=table.tbody.find_all('tr')
    for row in rows:
        try:
            name=unicode(row.find('td', {'class':'candidate'}).div.string)
        except:
            continue
        party=unicode(row.find('td', {'class':'party'}).string).strip()[0]
        pct=unicode(row.find('td', {'class':'pct'}).string).strip()
        votes=unicode(row.find('td', {'class':'votes'}).string).strip()
        candlist.append({'name': name, 'party': party, 'pct': pct, 'reporting': reporting, 'votes':votes})
    return candlist

if __name__=='__main__':
    baseurl='http://elections.nytimes.com/2012/results/states/'
    state=sys.argv[1]
    fips=getFips(state.replace('-', ' '))
    try:
        conn=urllib2.urlopen(baseurl+state)
    except urllib2.URLError, e:
        print e
    data=conn.read()
    soup=bs4.BeautifulSoup(data)
    datadict=dict()
    datadict['state']=fips
    datadict['president']=getPresident(soup)
    datadict['house']=getHouse(soup)
    datadict['senate']=getSenate(soup)
    print json.dumps(datadict)
