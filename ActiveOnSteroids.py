#CSCE 470 Final Project
import json, re
import urllib2
import sys
from stemming import porter2
import os
import math
import datetime

def tokenize(text):
    #Take a string and split it into tokens on word boundaries.

    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

def read_data(filename):
    """
    purpose: read all events from the json file.
    parameter: 
        filename - the path of json file in your local computer 
    return: a list containing all raw tweets each of which has the data structure of dictionary
    """
    data = []
    try:
        with open(filename) as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except:
        print "Failed to read data!"
        return []
    print "The json file has been successfully read!"
    return data


class CollectData():
	def __init__(self):
		today = str(datetime.date.today())+".."
		#near = ""
		#lat_lon = ""
		current_page = "1"
		# how many miles out would you mind going? user will input in form
		radius = "100"
		# when set to true, outputs distance from event
		show_distance = "true" 
		# may just want to use zip and state, not city
		#city =
		state = "TX"
		zipcode = "77840"
		query = "running"
		# the amount of results returned
		global per_page
		per_page = 3
		# sort by distance, date_asc, or date_desc
		# date_asc means the most recent is the first listed
		sort = "date_asc"
		start_date = today
		print start_date
		#end_date =


		search = "state=" + state + "&zip=" + zipcode + "&query=" + query + "&current_page=" + current_page + "&per_page=" + str(per_page) + "&radius=" + radius + "&show_distance=" + show_distance + "&sort=" + sort + "&start_date=" + start_date
		url = "http://api.amp.active.com/v2/search/?" + search + "&api_key=w6a5z75twefu4vcyrbq33rzg"
		#print url
		self.contents = urllib2.urlopen(url).read()
		
	def return_data(self):
		f = file('report.json', 'wb')
		saved = sys.stdout
		sys.stdout = f
		json.dumps(self.contents)
		sys.stdout = saved
		f.close()
		#print self.contents
		return self.contents


class Recommender():
	def __init__(self):
		self.myevents = {}
		self.listevents = []
		self.eventdetails = {}

	def index_events(self,events):
		self.myevents = json.loads(events)
		self.num_events = self.myevents['total_results']
		print self.num_events
		#print self.myevents['results']
		#print self.myevents['results'][0]
		#for result in events2['results']:
			#print result
		#for n in range(self.num_events-1):
		for n in range(0, per_page):
			#print n
			#print ""
			#print self.myevents['results'][n]
			#print ""
			self.listevents.append(self.myevents['results'][n])
		#print self.listevents
		for x in self.listevents:
			print ""
			print x
		return 0

	def get_deets(self):
		
		for idx,event in enumerate(self.listevents):
			self.eventdetails[idx] = dict(title = event['assetName'], phone = event['contactPhone'], homePage = event['homePageUrlAdr'])

		print self.eventdetails

		# 'assetName' ---> The actual name of the event
		# 'contactPhone'
		# 'contactEmailAdr'
		# 'homePageUrlAdr'
		# USE FOR LATER EventID = 'registrationUrlAdr'
		# 'assetTags'['tag']['tagName'] ---> the things they check that they like will match these here
		# 'assetImages'[imageUrlAdr']
		# OR? 'logoUrlAdr'
		# MAYBE, DONT PUT IN YET 'salesStatus' ---> says if registration is closed
		# something???['description'] ---> there is a list of descriptions
		# 'activityEndDate' ---> the last day to sign up for event
		# 'assetAttributes'['attribute']['attributeValue'] ---> the things they check that they like will match these here
		# 'avgUsrRatingTxt'
		# 'participationCriteriaTxt' --> says Kids, Adules, Men, Women, all that stuff
		# 'costAmt'
		# 'placeName'
		# 'addressLine1Txt'
		# 'addressLine2Txt'
		# 'postalCode'
		# 'cityName'

		# 'assetAttributes'['assetPrices']['priceAmt']


		return 0



def main():
    tc = CollectData()
    value = tc.return_data()
    rec = Recommender()
    rec.index_events(value)


if __name__ == "__main__":
    main()
