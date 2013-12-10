#CSCE 470 Final Project

import re, sys, os, json
import math, urllib2, datetime, collections, itertools
from operator import itemgetter
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
        per_page = 1000
        sort = "date_asc"           # sort by distance, date_asc, or date_desc; date_asc means the most recent is the first listed
        start_date = today
        search = "state=" + state + "&zip=" + zipcode + "&query=" + query + "&per_page=" + str(per_page) + "&radius=" + radius + "&show_distance=" + show_distance + "&sort=" + sort + "&start_date=" + start_date
        url = "http://api.amp.active.com/v2/search/?" + search + "&api_key=w6a5z75twefu4vcyrbq33rzg"
        #print url
        try:
            self.contents = urllib2.urlopen(url).read()
        except HTTPException as e:
            print "Got here"
            return e
        
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
        print "The json file has been successfully read!"
        return data

    def index_events(self,events):
        self.myevents = json.loads(events)
        self.num_events = self.myevents['total_results']
        print "\n", self.num_events, "total events\n"
        if (self.num_events < per_page):
            for n in range(0, self.num_events):
                listevents.append(self.myevents['results'][n])
        else:
            for n in range(0, 20):
                listevents.append(self.myevents['results'][n])
        return listevents


    def remove_html_markup(self,s):
        tag = False
        quote = False
        out = ""

        for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c
        return out



    def tokenize_descr(self, num_event,obj):
        text = str(obj)
        st = self.remove_html_markup(text)
        strin = str(num_event)
        descriptions[strin] = st
        return descriptions

    # Extracts attributes from events collected and puts them in a list of dictionaries called listevents
    def get_deets(self,list_events):
        for idx,event in enumerate(list_events):
            try:
                self.eventdetails[idx] = {}
                self.eventdetails[idx]['cosine'] = 0
                if 'assetName' in event.keys():
                    self.eventdetails[idx]['title'] = event['assetName']
                if 'contactPhone' in event.keys():
                    self.eventdetails[idx]['phone'] = event['contactPhone']
                if 'homePageUrlAdr' in event.keys():
                    self.eventdetails[idx]['homePage'] = event['homePageUrlAdr']
                if 'activityEndDate' in event.keys():
                    old_time = datetime.datetime.strptime(str(event['activityEndDate']),str("%Y-%m-%dT%H:%M:%S"))
                    new_format = str("%Y-%m-%d")
                    #print old_time.strftime(new_format)
                    self.eventdetails[idx]['endDate'] = old_time.strftime(new_format)
                if 'activityStartDate' in event.keys():
                    old_time = datetime.datetime.strptime(str(event['activityStartDate']),str("%Y-%m-%dT%H:%M:%S"))
                    new_format = str("%Y-%m-%d")
                    #print old_time.strftime(new_format)
                    self.eventdetails[idx]['eventDate'] = old_time.strftime(new_format)
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
                #if 'priceAmt' in event['assetPrices'].keys():
                #   self.eventdetails[idx]['priceAmt'] = event['assetPrices']['priceAmt']
                #add participants
                #price
                #activity date
                if 'description' in event['assetDescriptions'][idx].keys():
                    self.eventdetails[idx]['description'] = event['assetName']+":"+event['assetDescriptions'][idx]['description']
                self.tokenize_descr(idx,self.eventdetails[idx]['description'])
            except IndexError:
                self.tokenize_descr(idx,self.eventdetails[idx]['title'])
            print self.eventdetails[idx]
            #print ""
        return self.eventdetails

    # Returns global top 6 results based on user interests checked
    def top_results(self, details):
        new_list = tokenize(details)
        query = "+".join(new_list)
        print "There are no results matching your request."
        print "Instead, here are the top six matching your interests in America:"
        url2 = "http://api.amp.active.com/v2/search/?query=" + query + "+running&current_page=1&per_page=20&api_key=w6a5z75twefu4vcyrbq33rzg"
        self.contents = urllib2.urlopen(url2).read()
        return self.contents

    # Returns global top 6 results based on user interests checked
    def state_results(self, state,details):
        new_list = tokenize(details)
        query = "+".join(new_list)
        url3 = "http://api.amp.active.com/v2/search/?state="+state+"&query="+query+"running&current_page=1&per_page=1000&api_key=w6a5z75twefu4vcyrbq33rzg"
        self.contents = urllib2.urlopen(url3).read()
        return self.contents

    # This outputs the events in order of relevance into UI_output.json for easy access into the UI code :)
    def return_deets(self, filename, cos):
        final = filename
        #print final
        for idx, event in enumerate(final):
            index = cos[event]['number']
            self.final_events[idx] = {}
            self.final_events[idx]['cosine'] = cos[event]['cosine']
            
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
            #if 'priceAmt' in self.eventdetails[int(index)].keys():
            #   self.final_events[idx]['priceAmt'] = self.eventdetails[int(index)]['priceAmt']
            if 'description' in self.eventdetails[int(index)].keys():
                self.final_events[idx]['description'] = self.eventdetails[int(index)]['description']
            #print "\n",self.final_events[idx]
            #print self.final_events[idx]['cosine']
        #print self.final_events
        return self.final_events

    # Puts data into JSON file
    def return_data(self, filename):
        f = file(filename, 'wb')
        saved = sys.stdout
        sys.stdout = f
        print json.dumps(self.contents)
        sys.stdout = saved
        f.close()
        return self.contents

def remove_dups(dictionary):
    seen_values = set()
    dups = {}
    dups.update(dictionary)
    without_duplicates = {}
    
    for event in dictionary:
        value = str(dictionary[event]["title"])
        #print dictionary[event]["title"],dictionary[event]["cosine"]
        if value not in seen_values:
            without_duplicates[event] = {}
            without_duplicates[event] = dictionary[event]
            seen_values.add(value)
        else:
            del(dups[event])
    return dups

def info_recommender(state, zip_code, query_list):
    final = []
    global descriptions
    descriptions = {}
    global listevents
    listevents = []
    tc = CollectData("180",state,zip_code)
    value = tc.return_data('report.json')
    rec = Recommender()
    rec.index_events(value)
    rec.get_deets(listevents)
    #print descriptions
    event = EventSearch()

    if len(descriptions) >= 6:
        final = event.returnable(descriptions,query_list)
        #print final
        ordered = rec.return_deets(final,final)
        print "Number relevant:",len(ordered)#,ordered
        if len(ordered) >= 6:
            print "Got in"
            mydict_values = final.values()
            mydict_values.sort(key=itemgetter("cosine"), reverse = True)
            results = mydict_values
            print results
            return results
        elif len(ordered) < 6:
            print "Got in here"
            #print ordered
            difference = 6 - len(ordered)
            print "Difference is:", difference#, final
            cos_ord = rec.return_deets(ordered, final)
            
            st = rec.state_results(state,query_list)
            current = rec.index_events(st)
            
            state_final = rec.get_deets(current)
            
            final_dic = remove_dups(cos_ord)
            
            state_final.update(final_dic)
            
            result = remove_dups(state_final)

            mydict_values = result.values()
            mydict_values.sort(key=itemgetter("cosine"), reverse = True)
            #print type(mydict_values)
            results= mydict_values#dict(sorted(result.items(),key = lambda x :x[1]['cosine'],reverse = True))
            #print results
            for item in results:
                print item['cosine'], item['title']
            #print len(results)
            #print results
            return results
        else:
            print "here"
            temp = rec.top_results(query_list)
            rec.index_events(temp)
            final = rec.get_deets(listevents)
            #print final
            mydict_values = final.values()
            mydict_values.sort(key=itemgetter("cosine"), reverse = True)
            results = mydict_values
            print results
            return results
    else:
        print "boo"
        temp = rec.top_results(query_list)
        rec.index_events(temp)
        final = rec.get_deets(listevents)
        #print final
        mydict_values = final.values()
        mydict_values.sort(key=itemgetter("cosine"), reverse = True)
        results = mydict_values
        print results
        return results
    


def main():
    
    info_recommender('TX', '77840','5k')

if __name__ == "__main__":
    main()