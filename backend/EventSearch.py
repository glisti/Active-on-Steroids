'''
Created on Sep 2, 2013

@author: GHC
'''
from __future__ import division
import re
from stemming import porter2
import math
import json
import os
import sys
from operator import itemgetter

class EventSearch(object):
    """ A search engine for events. """
    def __init__(self, ranker=None, classifier=None):
        """
        purpose: Create the search engine for events
        parameters:
            database - store events information
        """
        # database will be used to store events
        #self.events = []
        self.database = {}
        # used to store inverted index information for all terms/tokens
        self.inverted_index = {}
        # idf's for terms in collection
        self.idf = {}
        # key: docid value: vector(list) of tfidf's
        self.doc_vectors = {}
    def tokenize(self, text):
        """
        Take a string and split it into tokens on word boundaries.
          
        A token is defined to be one or more alphanumeric characters,
        underscores, or apostrophes.  Remove all other punctuation, whitespace, and
        empty tokens.  Do case-folding to make everything lowercase. This function
        should return a list of the tokens in the input string.
        """
        tokens = re.findall("[\w']+", text.lower())
        return [porter2.stem(token) for token in tokens]

    def read_data(self, filename):
        """
        purpose: read all events from the json file.
        parameter: 
            filename - the path of json file in your local computer 
        return: a list containing all raw events each of which has the data structure of dictionary
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

    
    def _term_tf_idf(self, token, count):
        """
        purpose: Calculate tf-idf for a token in the document
        parameters:
            token - 
            count - the number of occurrence of a term/token in one document
        return: term/token's tf-idf
        """

        return 0 if count == 0 else (1+math.log(count,2))*(self.idf[token])
               
    def CosineSim(self, vec_query, vec_doc):
        """
        purpose: Calculate cosine similarity for two documents (vectors)
        parameters:
            vec_query - the vector with only raw term frequency for query
            vec_doc   - the vector of tf-idf for a document
        return: cosine similarity between the query and a document
        """

        doc_len = math.sqrt(sum(i**2 for i in vec_doc.itervalues()))
        q_len = math.sqrt(sum(i**2 for i in vec_query.itervalues()))

        num = 0

        for term,tfidf in vec_query.iteritems():
            if term in vec_doc:
                num += tfidf*vec_doc[term]
        try:
            return float(num/(doc_len*q_len))
        except:
            return float(num)

        
    def index_events(self,events):
        """
        purpose: process raw events and calculate tf-idf for all terms/tokens in events
        parameters:
          events - an iterator of event dictionaries
        returns: none
        """

        # IN USER INTERFACE:
        #Date, Rating (if it has it), title, description, price, URL, location, address
        #related events
        #every time you log in, recompiles

        for event in events:
            for idx, desc in enumerate(event):
                #print events
                curr_desc = event[desc][0]
                #self.database[idx] = dict(description = curr_desc, title = , rating = , date = , price = , URL = , location = , address = )
                self.database[idx] = dict(number = desc, description = curr_desc, cosine = 0)

#self.eventdetails[idx] = dict(title = event['assetName'], phone = event['contactPhone'], homePage = event['homePageUrlAdr'], date = event['activityEndDate'], location = event['place']['placeName'], addressLine1 = event['place']['addressLine1Txt'], addressLine2 = event['place']['addressLine2Txt'], zipcode = event['place']['postalCode'], city = event['place']['cityName'], participants = event['assetLegacyData']['participationCriteriaTxt'], description = event['assetDescriptions'][idx]['description'])
                #self.database.append(curr_desc)
                self.doc_vectors.setdefault(idx, {})

                for token in self.tokenize(curr_desc):
                    self.inverted_index.setdefault(token, []).append(idx)
                    self.doc_vectors[idx][token] = self.doc_vectors[idx].get(token, 0) + 1

        N = len(self.database)

        # build out term idf
        for term in self.inverted_index:
            self.idf[term] = math.log(float(N/(len(self.inverted_index[term]))),2)

        # build out vectors
        for idx,doc in self.doc_vectors.iteritems():
            for term,tf in doc.iteritems():
                self.doc_vectors[idx][term] = self._term_tf_idf(term,tf)

    def search_results(self, query, zip_code):
        """
        purpose: rank all events we have based on the query using 
                Vector Space Retrieval Model.
        preconditions: index_events() has already processed the corpus
        parameters:
                query - a string of terms
        returns: list of dictionaries containing the events which must have 
                the field "sim" in the data structure. 
        """
        tokens = self.tokenize(query)
        
        # gather doc IDs
        docIDs = []
        for token in tokens:
            print "\nUser Interest Token: ", token, '\n'
            if token in self.inverted_index.keys():
                docIDs += self.inverted_index[token]

        if len(docIDs) == 0:
            print "The activities you selected do not match any of the races in your area. Here are the top races around you:"
            #self.top_results(zip_code) OR self.return_data('report.json') and then only return the top 6 of those

        # remove duplicates
        docIDs = list(set(docIDs))

        # vectorize query
        q_vec = {}
        for token in self.tokenize(query):
            q_vec[token] = query.count(token)

        # determine ranking
        events = []
        for idx in docIDs:
            event = self.database[idx]
            simil = self.CosineSim(q_vec, self.doc_vectors[idx])
            self.database[idx]['cosine'] = simil
            print "\nCosine similarity: ",simil, "Event:", self.database[idx]['description'], "Number:", self.database[idx]['number'], "\n"
            events.append(event)
        
        f = file('events_cos.json', 'wb')
        saved = sys.stdout
        sys.stdout = f
        print json.dumps([x for x in sorted(events, key=lambda k: simil, reverse=True)])
        sys.stdout = saved
        f.close()
        return [x for x in sorted(events, key=lambda k: simil, reverse=True)]

    # Returns global top 6 results from the user's zip code
    #def top_results(self, zipcode):
    #    print "The activities you selected do not match any of the races in your area. Here are the top races around you."
    #    url = "http://api.amp.active.com/v2/search/?query=running&zip=" + zipcode + "&current_page=1&per_page=6&api_key=w6a5z75twefu4vcyrbq33rzg"
    #    self.contents = urllib2.urlopen(url).read()
    
    def create_file(self):
        f = file('events_cos.json', 'wb')
        saved = sys.stdout
        sys.stdout = f
        print json.dumps(self.database)
        sys.stdout = saved
        f.close()

    def returnable(self,filename, query, zip_code):
        print "Test is starting..."
        _searcher = EventSearch()                                       # create our searcher
        events = self.read_data(os.path.join(os.getcwd(), filename))    # read all events from json file
        _searcher.index_events(events) 
        output = _searcher.search_results(query, zip_code)