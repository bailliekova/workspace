import json
import dbutils
import us
from nytimesparse import getFips 

conn=dbutils.connect()
c=conn.cursor()
data=json.load(open('/home/anovikova/exits.JSON'))

states=data['2012']['states']

for state in states:
    if state['state']=='US' or state['state']=='':
        fips=0
    else:
        fips=getFips(state['state'])
    for section in state['sections']:
        if section is None:
            continue
        for subsection in section['subsections']:
            if subsection['change']['party']=='dem':
                change=subsection['change']['amount']/100.0
            elif subsection['change']['party']=='rep':
                change=subsection['change']['amount']/-100.0
            else:
                change='NULL'
            try:
                other=subsection['values']['other']/100.0
            except TypeError:
                other='NULL'
            row=[fips, section['title'], subsection['title'], subsection['values']['dem']/100.0, subsection['values']['rep']/100.0, other, subsection['shareOfElectorate']/100.0, change, 2012]
            c.execute('INSERT IGNORE INTO exits_2012 VALUES (%s, %s, %s,%s,%s,%s,%s,%s, %s)', row)
        conn.commit()
