from bs4 import BeautifulSoup
import json
import sys
abtofips=json.load(open('abrevtofips.JSON', 'rb'))
svg=BeautifulSoup(open('113th_U.S._Congress_House_districts_blank.svg').read())
paths=svg.findAll('path')

### MAKE DICTIONARY FOR BINS
fipstobin={}
f=open(sys.argv[1])
for line in f:
    tokens=line.split()
    if len(tokens[0])==3:
        tokens[0]='0'+tokens[0]
    fipstobin[tokens[0]]=int(tokens[-1].strip())

basestyle='font-size:34.37500000000000000px;font-style:normal;font-weight:400;opacity:1;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.33300000000000002;stroke-linecap:square;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;font-family:MS Shell Dlg 2;fill:'

#colors=['#67001F','#B2182B', '#D6604D', '#F4A582', 'FDDBC7', '#F7F7F7','#D1E5F0', '#92C5DE','#4393C3', '#2166AC', '#053061' ]
colors=['#A50F15', '#DE2D26', '#FB6A4A','#FC9272', '#FCBBA1', 'FEE5D9', '#F7F7F7', '#D1E5F0']


def getMetaData(fips):
    pass

def getColor(fips):
    try:
        color=fipstobin[fips]-1
        if len(str(color))>2:
            return '#575757'
        else:
            return colors[color]
    except KeyError as e:
        raise e
   
for path in paths:
    if path['id']=='Dividing_line':
        continue
    statefips=str(abtofips[path['id'][:2]])
    cd=path['id'][-2:]
    if cd=='AL':
        cd='01'
    fips=statefips + cd
    path['fips']=fips
    path['style']=basestyle + getColor(fips)

print svg.prettify()
