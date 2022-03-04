
import tweepy
import json
import spacy
import tagme
import time
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace, Graph
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD
import re
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup as bs

BASE = Namespace("http://www.kde.cs.tsukuba.ac.jp/~aregawi/w3c-email/")

tagme.GCUBE_TOKEN = "93eb5238-bf49-4293-84e8-302dcf40944b-843339462"
nlp = spacy.load("en_core_web_sm")

consumer_key = "yzw16SfR4rnfZb4m2JnzRryPr"
consumer_secret = "88OAWEkNfLdSzRplcbI2PQmn0vjSl1AVi5KhRIFMVSiEDfsm9p"

access_token = "1178352707821658113-xXcRH018zjZX3RfxwH38FEPIjNJIHU"
access_token_secret = "oZvFOW47k13tKWHONSIa7GwIENCu6mbHMb3iMrE3o5QIH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """text2 = status.extended_tweet['full_text']"""
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text
        file = open("tweetstreams_10.json", mode="a")
        json.dump(status._json, file)
        file.write('\n')
        print(status._json)
        print(tweet)


    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])
# we can change or add filtering hashtag, based on popular events
stream.filter(track=['Covid-19'], languages=["en"])