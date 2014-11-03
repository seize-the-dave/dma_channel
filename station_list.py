from __future__ import print_function
import sys
import csv
from sets import Set
import urllib
import json

dmas = {}

dma_map = {}

with open('dma.csv', 'rb') as dmafile:
  reader = csv.reader(dmafile)
  for row in reader:
    number = row[0]
    name = row[2].lower().replace(",", "")
    dma_map[name] = str(number)

def debug(*objs):
    print(*objs, file=sys.stderr)

def find_dma_num(name):
  key = name.lower()
  if key not in dma_map:
    return None
  return dma_map[name.lower()]

def lookup_state(stateName):
    state_url = 'http://data.fcc.gov/mediabureau/v01/tv/facility/search/' + stateName + '.json'
    state = urllib.urlopen(state_url)
    obj = json.load(state)
    for searchList in (obj['results']['searchList']):
        if 'facilityList' not in searchList:
            continue
        if searchList['searchType'] != 'State':
            continue
        for facility in searchList['facilityList']:
            fccId = facility['id']
            callSign = facility['callSign']
            service = facility['service']
            if service != 'Digital TV':
                continue
            nielsenDma = str(facility['nielsenDma'])
            if nielsenDma == '':
                nielsenDma = '-'
            partyCity = facility['partyCity']
            partyZip = facility['partyZip1']
            virtualChannel = facility['virtualChannel']
            networkAfil = facility['networkAfil']
            print(str(fccId) + '|' + callSign + '|' + nielsenDma + '|' + virtualChannel + '|' + networkAfil + '|' + stateName + '|' + partyCity + '|' + partyZip)

with open('state_table.csv', 'rb') as csvfile:
  abbrs = Set()
  reader = csv.reader(csvfile)
  header = reader.next()
  for state in reader:
    abbr = state[2]
    abbrs.add(abbr)

  for abbr in abbrs:
    lookup_state(abbr)
