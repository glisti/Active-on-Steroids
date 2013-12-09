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
import collections
import sys
from operator import *

class EventSearch(object):
    """ A search engine for events. """
    def __init__(self, ranker=None, classifier=None):
        """
        purpose: Create the search engine for events
        parameters:
            database - store events information
        """
        # database will be used to store events
        self.database = {}
        self.database2 = {}
        # used to store inverted index information for all terms/tokens
        self.inverted_index = {}
        # idf's for terms in collection
        self.idf = {}
        # key: docid value: vector(list) of tfidf's
        self.doc_vectors = {}

    def tokenize(self, text):
        tokens = re.findall("[\w']+", text.lower())
        return [porter2.stem(token) for token in tokens]

    def _term_tf_idf(self, token, count):
        return 0 if count == 0 else (1+math.log(count,2))*(self.idf[token])
               
    def CosineSim(self, vec_query, vec_doc):
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
        for idx,event in enumerate(events):
            #for idx, desc in enumerate(event):
            curr_desc = events[event]
            #self.database[idx] = dict(description = curr_desc, title = , rating = , date = , price = , URL = , location = , address = )
            self.database[idx] = dict(number = event, description = curr_desc, cosine = 0)

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

    def search_results(self, query):
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
            if token in self.inverted_index:
                docIDs += self.inverted_index[token]

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
            print "Cosine similarity: ",simil, "Event:", self.database[idx]['description'], "Number:", self.database[idx]['number'], "\n"
            events.append(event)
        self.database = sorted(self.database.items(), key = lambda x : x[1], reverse=True)
        for idx,tup in enumerate(self.database):
            if tup[1]['cosine'] == 0:
                print ""
            else:
                self.database2[idx] = dict(cosine = tup[1]['cosine'], description = tup[1]['description'], number = tup[1]['number'])
        #print self.database2
        return self.database2

    def returnable(self, diction, query):
        # print "Test is starting..."
        _searcher = EventSearch()                                       # create our searcher
        events = diction
        _searcher.index_events(events) 
        output = _searcher.search_results(query)
        #print output
        return output