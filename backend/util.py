#CSCE 470 Final Project

import re, sys, os, json
import math, urllib2, datetime
from EventSearch import EventSearch
from stemming import porter2


global descriptions
descriptions = {}
global listevents
listevents = []

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
        radius = radius             # how many miles out would you mind going? user will input in form
        show_distance = "true"      # when set to true, outputs distance from event
        state = state
        zipcode = zip_code
        query = "running"
        global per_page             # the number of events returned
        per_page = 6
        sort = "date_asc"           # sort by distance, date_asc, or date_desc; date_asc means the most recent is the first listed
        start_date = today
        search = "state=" + state + "&zip=" + zipcode + "&query=" + query + "&current_page=" + current_page + "&per_page=" + str(per_page) + "&radius=" + radius + "&show_distance=" + show_distance + "&sort=" + sort + "&start_date=" + start_date
        url = "http://api.amp.active.com/v2/search/?" + search + "&api_key=w6a5z75twefu4vcyrbq33rzg"
        print url
        try:
            self.contents = urllib2.urlopen(url).read()
        except HTTPException as e:
            # print "Got here"
            return e
        
    # Puts data into JSON file
    def return_data(self, filename):
        f = file(filename, 'wb')
        saved = sys.stdout
        sys.stdout = f
        # print json.dumps(self.contents)
        sys.stdout = saved
        f.close()
        return self.contents

class Recommender():

    def __init__(self):
        self.myevents = {}
        listevents = []
        self.eventdetails = {}
        self.eventdescriptions = {}
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
        # print "The json file has been successfully read!"
        return data

    def index_events(self,events):
        self.myevents = json.loads(events)
        self.num_events = self.myevents['total_results']
        # print "\n", self.num_events, "total events\n"
        if (self.num_events < per_page):
            for n in range(0, self.num_events):
                listevents.append(self.myevents['results'][n])
        else:
            for n in range(0, per_page):
                listevents.append(self.myevents['results'][n])
        return 0

    def tokenize_descr(self, num_event,obj):
        text = str(obj)
        st = re.sub('<[^<]+?>', '', text)
        strin = str(num_event)
        descriptions[strin] = st
        return descriptions

    # Extracts attributes from events collected and puts them in a list of dictionaries called listevents
    def get_deets(self,list_events):
        for idx,event in enumerate(list_events):
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
                if 'activityStartDate' in event.keys():
                    self.eventdetails[idx]['eventDate'] = event['activityStartDate']
                if 'placeName' in event['place'].keys():
                    self.eventdetails[idx]['location'] = event['place']['placeName']
                    #print "", self.eventdetails[idx]['location']
                if 'addressLine1' in event['place'].keys():
                    self.eventdetails[idx]['addressLine1'] = event['place']['addressLine1Txt']
                    #print "", self.eventdetails[idx]['addressLine1']
                if 'addressLine2' in event['place'].keys():
                    self.eventdetails[idx]['addressLine2'] = event['place']['addressLine2Txt']
                if 'postalCode' in event['place'].keys():
                    self.eventdetails[idx]['zipCode'] = event['place']['postalCode']
                if 'cityName' in event['place'].keys():
                    self.eventdetails[idx]['cityName'] = event['place']['cityName']
                #add participants
                #price
                #activity date
                if 'description' in event['assetDescriptions'][idx].keys():
                    self.eventdetails[idx]['description'] = event['assetName']+":"+event['assetDescriptions'][idx]['description']
                self.tokenize_descr(idx,self.eventdetails[idx]['description'])
            except IndexError:
                self.tokenize_descr(idx,self.eventdetails[idx]['title'])
            # print self.eventdetails[idx]
            # print ""
        return self.eventdetails

    # Returns global top 6 results based on user interests checked
    def top_results(self, details):
        new_list = tokenize(details)
        query = "+".join(new_list)
        # print "There are no results matching your request."
        # print "Instead, here are the top six matching your interests in America:"
        url2 = "http://api.amp.active.com/v2/search/?query=" + query + "+running&current_page=1&per_page=6&api_key=w6a5z75twefu4vcyrbq33rzg"
        self.contents = urllib2.urlopen(url2).read()
        return self.contents

    # Returns global top 6 results based on user interests checked
    def state_results(self, state):
        # print "There are no results matching your request."
        url3 = "http://api.amp.active.com/v2/search/?state="+state+"&query=running&current_page=1&per_page=6&api_key=w6a5z75twefu4vcyrbq33rzg"
        self.contents = urllib2.urlopen(url3).read()
        return self.contents

    # This outputs the events in order of relevance into UI_output.json for easy access into the UI code :)
    def return_deets(self, filename):
        final = filename
        for idx, event in enumerate(final):
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
            if 'eventDate' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['eventDate'] = self.eventdetails[int(index)]['eventDate']
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
            # print "\n",self.final_events[idx]
        #print self.final_events
        return self.final_events

    # Puts data into JSON file
    def return_data(self, filename):
        f = file(filename, 'wb')
        saved = sys.stdout
        sys.stdout = f
        # print json.dumps(self.contents)
        sys.stdout = saved
        f.close()
        return self.contents

def info_recommender(state, zip_code, query_list):
    final = []
    global descriptions 
    descriptions = {}
    global listevents
    listevents = []
    tc = CollectData("120",state,zip_code)
    value = tc.return_data('report.json')
    rec = Recommender()
    rec.index_events(value)
    rec.get_deets(listevents)
    #print descriptions
    event = EventSearch()

    #print "These are the top 6 in your state:"
    state_url = "http://api.amp.active.com/v2/search/?state=" + state + "&current_page=1&per_page=6&query=running&api_key=w6a5z75twefu4vcyrbq33rzg"
    zip_url = "http://api.amp.active.com/v2/search/?zip=" + zip_code + "&current_page=1&per_page=6&query=running&api_key=w6a5z75twefu4vcyrbq33rzg"
    #print state_url
    #self.contents = urllib2.urlopen(state_url).read()


    if len(descriptions) >= 6:
        final = event.returnable(descriptions,query_list)
        # print "Number relevant:",len(final)
        if len(final) >= 6:
            # print "got in"
            return rec.return_deets(final)
        elif len(final) < 6:
            # print "got in here"
            difference = 6 - len(final)
            # print "difference is:", difference
            rec.state_results(state)
            temp = rec.return_data('report.json')
            rec.index_events(temp)
            state_final = rec.get_deets(listevents)
            final_dic = dict(final)
            final_dic.update(state_final)
            # print final_dic
            return final_dic
        else:
            print "here"
    else:
        rec.top_results(query_list)
        temp = rec.return_data('report.json')
        rec.index_events(temp)
        final = rec.get_deets(listevents)
        # print final
        return final
