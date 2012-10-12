from bs4 import BeautifulSoup
import urllib2
import re
import codecs
import us


#req=urllib2.Request('http://en.wikipedia.org/wiki/United_States_House_of_Representatives_elections,_2010', headers={'User-Agent' : "Magic Browser"})
#con=urllib2.urlopen(req)
#data=con.read()
#datafile=codecs.open('2010.txt', 'w')
#datafile.write(data)
data=codecs.open('2010.txt', 'r', encoding='utf-8').read()
soup=BeautifulSoup(data)
tables=soup.findAll('table', {'class':'wikitable'})
outfile=codecs.open('2010results.txt', 'w', encoding='utf-8')
statetofips=us.states.mapping('name', 'fips')

for t in tables[3:]:
    try:
        rows=t.findAll('tr')
        for row in rows[1:]:
            data=[re.sub('<[^>]*>', '', x.renderContents()) for x in row.findAll('td')]
            print data
            cands=data[len(data)-1].decode('utf-8').split(u'\n')
            data=data[:-1]
            toks= [x.strip() for x in data[0].split()]
            try:
                state=str(statetofips[' '.join(toks[:-1])])
                
                if toks[-1]in ['at-large', 'At Large']:
                    district='01'
                else:
                    district=toks[-1].strip()
                    if len(district)==1:
                        district='0'+district
                statecd=state+district
            except Exception as e:
                statecd=prevstatecd
            data[0]=statecd
            data[1]=data[1].decode('utf-8')
            if len(data)>=4:
                data[3]=str(data[3])
            data=[d.replace('\n', ' ') for d in data]
            result=['NULL','NULL','NULL','NULL']
            for cand in cands[:2]:
                tokens=cand.split()
                if tokens[len(tokens)-1]in ['unopposed', '(unopposed)']:
                    percent='1'
                elif tokens[len(tokens)-1] in ['re-election', 'renomination', 'Re-elected', 'contest', 'Retired', 'Governor', '(R)']:
                    result=prevresult
                    if len(data)<5:
                        for x in range(0, 5-len(data)):
                            data.append('NULL')
                    outfile.write('\t'.join(data[:5])+'\t')
                    outfile.write('\t'.join(result)+'\n')
                    break

                else:
                    percent=str(float(tokens[len(tokens)-1].replace('%', '').replace('(WI)', ''))/100)
                party=re.sub('[()]', '', tokens[len(tokens)-2])
                name=' '.join(tokens[0:len(tokens)-2])
                if party=='D':
                    result[0]=name
                    result[1]=percent
                elif party=='R':
                    result[2]=name
                    result[3]=percent
            if len(data)<5:
                for x in range(0, 5-len(data)):
                    data.append('NULL')
            outfile.write('\t'.join(data[:5])+'\t')
            outfile.write('\t'.join(result)+'\n')
            prevresult=result
            prevstatecd=statecd
            outfile.flush()
    except urllib2.HTTPError as e:
        raise e
                    
outfile.close()

            
            
            
