import dbutils
import codecs

conn=dbutils.connect()
c=conn.cursor()

c.execute('SELECT id, userid, text, latitude, longitude from tweets_onepercent_tweets where latitude IS NOT NULL and longitude IS NOT NULL LIMIT 200')
rs=c.fetchall()

outfile=codecs.open('sample.csv', 'w', encoding='utf8')

outfile.write(','.join(['id','uid', 'text', 'lat', 'lon'])+'\n')

for result in rs:
    for thing in result:
        print thing
    outfile.write(','.join([unicode(x) for x in result])+'\n')
    outfile.flush()

outfile.close()
conn.close()

