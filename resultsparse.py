
import json
import dbutils
import re

conn=dbutils.connect()
c=conn.cursor()

for line in open("results.JSON"):
    data=json.loads(line)
    for candidate in data['president']:
        try:
            reporting=float(re.sub('[^0-9]', '', candidate['reporting']))/100
        except ValueError:
            reporting='NULL'
        pct=float(re.sub('%', '', candidate['pct']))/100
        row=[data['state'], 'president', 'NULL', candidate['name'], candidate['party'],pct, candidate['votes'].replace(',', ''), reporting]
        print row
        c.execute('INSERT IGNORE INTO results_2012(state,office,district, name, party, percent, votes, reporting) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', row)
    conn.commit()
    for k in data['house']:
        district=k
        for candidate in data['house'][district]:
            try:
                reporting=float(re.sub('[^0-9]', '', candidate['reporting']))/100
            except ValueError:
                reporting='NULL'
            try:
                pct=float(candidate['pct'])/100
            except ValueError:
                pct='NULL'
            if 'votes' in candidate:
                votes=candidate['votes'].replace(',', '')
            else:
                votes='NULL'
            row=[data['state'], 'house', district, candidate['name'], candidate['party'],pct,votes , reporting]
            print row
            c.execute('REPLACE INTO results_2012(state,office,district, name, party, percent, votes, reporting) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', row)
    conn.commit()
    if 'senate' not in data:
        continue
    for candidate in data['senate']:
        try:
            reporting=float(re.sub('[^0-9]', '', candidate['reporting']))/100
        except ValueError:
            reporting='NULL'
        pct=float(re.sub('%', '', candidate['pct']))/100
        row=[data['state'], 'senate', 'NULL', candidate['name'], candidate['party'],pct, candidate['votes'].replace(',', ''), reporting]
        print row
        c.execute('REPLACE INTO results_2012(state,office,district, name, party, percent, votes, reporting) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', row)

    conn.commit()
conn.close 
