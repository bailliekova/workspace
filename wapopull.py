import urllib2
import json
key=open('wapokey', 'r').read().strip()
n=1
while True:
    try:
        f=urllib2.urlopen('http://api.washingtonpost.com/politics/transcripts/api/v1/issue/' + str(n) + '/?key=' + key)
    except urllib2.HTTPError:
        break
    data=json.load(f)
    print data['name'], data['statement_count']
    n+=1
