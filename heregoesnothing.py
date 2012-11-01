import dbutils

conn=dbutils.connect()
c=conn.cursor()
c.execute("SELECT count(*), unix_timestamp(datetime) FROM tweets_datasift_tweets WHERE date(datetime)='2012-10-04' GROUP BY unix_timestamp(datetime) ORDER BY unix_timestamp(datetime)")
max=0
prev=c.fetchone()[1]
while True:
    r=c.fetchone()
    if not r:
        break
    this=r[1]
    dif=this-prev
    prev=this
    if dif > max:
        max=dif
    continue

print max
conn.close()
