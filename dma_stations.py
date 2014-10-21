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
    print("DEBUG", *objs, file=sys.stderr)

def find_dma_num(name):
  key = name.lower()
  if key not in dma_map:
    return None
  return dma_map[name.lower()]

def lookup_state(state):
  debug('Processing ' + state)
  state_url = 'http://data.fcc.gov/mediabureau/v01/tv/facility/search/' + state + '.json'
  state = urllib.urlopen(state_url)
  obj = json.load(state)
  for searchList in (obj['results']['searchList']):
    if 'facilityList' not in searchList:
      continue
    for facility in searchList['facilityList']:
      callSign = facility['callSign']
      nielsenDma = str(facility['nielsenDma'])
      if nielsenDma == '':
        continue
      nielsenDma = find_dma_num(nielsenDma)
      if nielsenDma == None:
        continue
      if nielsenDma not in dmas:
        dmas[nielsenDma] = Set()
      dmas[nielsenDma].add(callSign),

with open('state_table.csv', 'rb') as csvfile:
  abbrs = Set()
  reader = csv.reader(csvfile)
  header = reader.next()
  for state in reader:
    abbr = state[2]
    abbrs.add(abbr)

  for abbr in abbrs:
    lookup_state(abbr)

  debug(str(len(dmas)) + ' DMAs')

for dma in dmas:
  dmas[dma] = list(dmas[dma])

print(json.dumps(dmas))
