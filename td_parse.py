from bs4 import BeautifulSoup
import requests, re, json

qbjson = {}
qblist = []

baseurl = 'http://www.pro-football-reference.com'
qbindex = '/players/qbindex.htm'

stat_title_array = ['year', 'age', 'team', 'pos', 'no', 'g', 'gs', 'qbrec', 'cmp', 'att', 'cpct', 'yards', 'td']

r = requests.get(baseurl + qbindex)

mainsoup = BeautifulSoup(r.content)

for letter in mainsoup.find_all('pre'):
	for qb in letter.find_all('a'):
		qbdict = {}
		qbdict['name'] = qb.text
		qburl = qb['href']
		qbdict['url'] = qburl
		qbdict['pass_stats'] = []
		
		qbpage = requests.get(baseurl + qburl)
		qbsoup = BeautifulSoup(qbpage.content)
		
		for season in qbsoup.find_all('tr', id=re.compile('passing\..')):	# use regex, escape dot
			season_dict = {}
			
			season_stat_array = season.find_all('td')
			for x in range(0,13):
				season_dict[stat_title_array[x]] = season_stat_array[x].text
			
			qbdict['pass_stats'].append(season_dict)
		
		qblist.append(qbdict)

qbjson['qblist'] = qblist

with open('qbstats.js', 'wb') as f:
	f.write(json.dumps(qbjson))