import json
import dbutils
import us
import re
from nytimesparse import getFips 

conn=dbutils.connect()
c=conn.cursor()
data=json.load(open('/home/anovikova/countyresults.JSON'))

statedict=data['counties']

for state in statedict:
    pctreporting=[float(re.sub('[^0-9]', '', num))/100.0 for num in statedict[state]['county_votes']['pct_reporting']]
    fipslist=statedict[state]['county_votes']['location_fips']
    candidates=statedict[state]['candidates']
    statefips=getFips(state)
    for candidate in candidates:
        for x in xrange(0, len(pctreporting)):
            row=[statefips, 'President', 'NULL', candidate['cand_longname'], candidate['party'][0], statedict[state]['county_votes'][candidate['votes_field']][x], pctreporting[x], fipslist[x]]
            c.execute('REPLACE INTO results_2012 (state, office, district, name, party, votes, reporting, fips_county) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)', row)
    conn.commit()
