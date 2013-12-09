#CSCE 470 Final Project

import re, sys, os, json
import math, urllib2, datetime
from eventsearch import EventSearch
from stemming import porter2


global descriptions
descriptions = {}

def tokenize(text):
    words = text.split()
    return words

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

# This class talks to the API and  collects necessary data via HTTP Get command
class CollectData():
    def __init__(self, radius, state, zip_code):

        today = str(datetime.date.today())+".."
        current_page = "1"
        # how many miles out would you mind going? user will input in form
        radius = radius
        # when set to true, outputs distance from event
        show_distance = "true" 
        state = state
        zipcode = zip_code
        query = "running"
        # the number of events returned
        global per_page
        per_page = 6
        # sort by distance, date_asc, or date_desc
        # date_asc means the most recent is the first listed
        sort = "date_asc"
        start_date = today
        #end_date = ""
        #near = ""
        #lat_lon = ""
        search = "state=" + state + "&zip=" + zipcode + "&query=" + query + "&current_page=" + current_page + "&per_page=" + str(per_page) + "&radius=" + radius + "&show_distance=" + show_distance + "&sort=" + sort + "&start_date=" + start_date
        url = "http://api.amp.active.com/v2/search/?" + search + "&api_key=w6a5z75twefu4vcyrbq33rzg"
        self.contents = urllib2.urlopen(url).read()
        
    # Puts data into JSON file
    def return_data(self, filename):
        f = file(filename, 'wb')
        saved = sys.stdout
        sys.stdout = f
        print json.dumps(self.contents)
        sys.stdout = saved
        f.close()
        return self.contents


class Recommender():
    def __init__(self):
        self.myevents = {}
        self.listevents = []
        self.eventdetails = {}
        self.eventdescriptions = {}
        #global descriptions = {}
        self.final_events = {}


    # Reads data from a JSON file
    def read_data(self, filename):
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


    def index_events(self,events):
        self.myevents = json.loads(events)
        self.num_events = self.myevents['total_results']
        print "\n", self.num_events, "total events\n"
        if (self.num_events < per_page):
            for n in range(0, self.num_events):
                self.listevents.append(self.myevents['results'][n])
        else:
            for n in range(0, per_page):
                self.listevents.append(self.myevents['results'][n])
        return 0
    """
    # The event description tokenizer
    def tokenize_descr(self,num_event,obj):
        f = file('events.json', 'wb')
        saved = sys.stdout
        sys.stdout = f
        text = str(obj)
        st = re.sub('<[^<]+?>', '', text)
        strin = str(num_event)
        descriptions[strin] = []
        descriptions[strin].append(st)
        print json.dumps(descriptions)
        sys.stdout = saved
        f.close()
    """
    def tokenize_descr(self, num_event,obj):
        text = str(obj)
        st = re.sub('<[^<]+?>', '', text)
        strin = str(num_event)
        descriptions[strin] = st
        return descriptions

    # Extracts attributes from events collected and puts them in a list of dictionaries called self.listevents
    def get_deets(self):
        for idx,event in enumerate(self.listevents):
            try:
                self.eventdetails[idx] = {}
                if 'assetName' in event.keys():
                    self.eventdetails[idx]['title'] = event['assetName']
                if 'contactPhone' in event.keys():
                    self.eventdetails[idx]['phone'] = event['contactPhone']
                if 'homePageUrlAdr' in event.keys():
                    self.eventdetails[idx]['homePage'] = event['homePageUrlAdr']
                if 'activityEndDate' in event.keys():
                    self.eventdetails[idx]['endDate'] = event['activityEndDate']
                if 'placeName' in event['place'].keys():
                    self.eventdetails[idx]['location'] = event['place']['placeName']
                if 'addressLine1' in event['place'].keys():
                    self.eventdetails[idx]['addressLine1'] = event['place']['addressLine1Txt']
                if 'addressLine2' in event['place']:
                    self.eventdetails[idx]['addressLine2'] = event['place']['addressLine2Txt']
                if 'postalCode' in event['place']:
                    self.eventdetails[idx]['zipCode'] = event['place']['postalCode']
                if 'cityName' in event['place']:
                    self.eventdetails[idx]['addressLine2'] = event['place']['cityName']
                #add participants
                if 'description' in event['assetDescriptions'][idx].keys():
                    self.eventdetails[idx]['description'] = event['assetDescriptions'][idx]['description']
                self.tokenize_descr(idx,self.eventdetails[idx]['description'])
            except IndexError:
                self.tokenize_descr(idx,self.eventdetails[idx]['title'])

        return 0

    # Returns global top 6 results based on user interests checked
    def top_results(self, details):
        print "There are no results matching your request."
        print "Instead, here are the top six matching your interests in America:"
        url = "http://api.amp.active.com/v2/search/?query=" + details + "+running&current_page=1&per_page=6&api_key=w6a5z75twefu4vcyrbq33rzg"
        self.contents = urllib2.urlopen(url).read()


    # This outputs the events in order of relevance into UI_output.json for easy access into the UI code :)
    def return_deets(self, filename):
        #final_events_file = filename
        final = filename
        for idx, event in enumerate(final):
            #for idx,event in enumerate(f):
            index = final[event]['number']
            self.final_events[idx] = {}
            if 'title' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['title'] = self.eventdetails[int(index)]['title']
            if 'phone' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['phone'] = self.eventdetails[int(index)]['phone']
            if 'homePage' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['homePage'] = self.eventdetails[int(index)]['homePage']
            if 'endDate' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['endDate'] = self.eventdetails[int(index)]['endDate']
            if 'location' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['location'] = self.eventdetails[int(index)]['location']
            if 'addressLine1' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['addressLine1'] = self.eventdetails[int(index)]['addressLine1']
            if 'addressLine2' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['addressLine2'] = self.eventdetails[int(index)]['addressLine2']
            if 'zipCode' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['zipCode'] = self.eventdetails[int(index)]['zipCode']
            if 'cityName' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['cityName'] = self.eventdetails[int(index)]['cityName']
            if 'description' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['description'] = self.eventdetails[int(index)]['description']

        # print self.final_events
        return self.final_events


    # Puts data into JSON file
    
    def return_data(self, filename):
        f = file(filename, 'wb')
        saved = sys.stdout
        sys.stdout = f
        print json.dumps(self.final_events)
        sys.stdout = saved
        f.close()
        return self.final_events

def info_recommender(state, zip_code, query_list):
    #if len(descriptions) > 0:
    #   descriptions = {}
    tc = CollectData("50",state,zip_code)
    value = tc.return_data('report.json')
    rec = Recommender()
    rec.index_events(value)
    rec.get_deets()
    #print descriptions
    event = EventSearch()
    if len(descriptions) > 0:
        final = event.returnable(descriptions,query_list)
    else:
        rec.top_results(query_list)
        rec.return_data('report.json')
    return rec.return_deets(final)


def main():
    
    info_recommender('TX', '77840','marathon 5k')

if __name__ == "__main__":
    main()