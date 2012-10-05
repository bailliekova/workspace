from bs4 import BeautifulSoup
import MySQLdb
import json
import random

abtofips=json.load(open('abtofips.JSON', 'rb'))
svg=BeautifulSoup(open('/cygdrive/p/113th_U.S._Congress_House_districts_blank.svg').read())

paths=svg.findall('path')

basestyle='font-size:34.37500000000000000px;font-style:normal;font-weight:400;opacity:1;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.33300000000000002;stroke-linecap:square;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;font-family:MS Shell Dlg 2;fill:'

colors=['#0571B0','#F7F7F7', '#CA0020']

conn=dbutils.connect()
c=conn.cursor()

def getMetaData(fips):
    pass

def getColor(fips):
    c.execute("SELECT mean_Dem, mean_Rep from CD_Estimates_CDRanking where STATE_CD= %s and Type='Unimputed' and SURVEY_ID= MAX(SELECT SURVEY_ID from CD_Estimates_CDRanking where STATE_CD= %s)", [fips, fips])
    data=c.fetchone()
    dif=data[0]-data[1]
    if dif>.05:
        color=0
    elif dif<-.05:
        color=2
    else:
        color=1
    return colors[color]

for path in paths:
    statefips=abtofips[path.id[:2]]
    cd=path.id[-2:]
    fips=statefips * 100 + cd
    path['fips']=fips
    path['style']=basestyle + getColor(fips)
    
conn.close()

print svg.prettify()
