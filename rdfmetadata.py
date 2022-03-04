

import re
import string

import tweepy
from spacy.util import minibatch, compounding
import random
import json
from spacy.lang.en import English
from tweepy import OAuthHandler, Stream, StreamListener
from gensim.parsing.preprocessing import remove_stopwords
import spacy
import tagme
# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = "93eb5238-bf49-4293-84e8-302dcf40944b-843339462"

nlp = spacy.load("en_core_web_sm")

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "yzw16SfR4rnfZb4m2JnzRryPr"
consumer_secret = "88OAWEkNfLdSzRplcbI2PQmn0vjSl1AVi5KhRIFMVSiEDfsm9p"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1178352707821658113-xXcRH018zjZX3RfxwH38FEPIjNJIHU"
access_token_secret = "oZvFOW47k13tKWHONSIa7GwIENCu6mbHMb3iMrE3o5QIH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # text = status.text
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
        print(status._json)
        print(tweet)
        name = status.user.screen_name
        tweet_id = status.id
        date = status.created_at
        url = f"https://twitter.com/user/status/{status.id}"
        url2 = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
        """print(text3)"""
        print(name)
        print(tweet_id)
        print(date)
        print(url)
        print(url2)
        sen = nlp(tweet)
        print("\nEntities using SpaCy")
        for entity in sen.ents:
            print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        print("\nAnnotations using TagMe")
        lunch_annotations = tagme.annotate(tweet)

        # Print annotations with a score higher than 0.1
        for ann in lunch_annotations.get_annotations(0.1):
            print(ann)
        print("\nMentions")
        entity_mentions = tagme.mentions(tweet)

        for mention in entity_mentions.mentions:
            if mention.linkprob>0.01:
                print(mention.mention+ " lp="+str(mention.linkprob))
                url_offset = url + "#offset_" + str(mention.begin) + "_" + str(mention.end)
                print(url + "#offset_" + str(mention.begin) + "_" + str(mention.end))
                print(url2 + "#offset_" + str(mention.begin) + "_" + str(mention.end))
                wiki_uri = "https://en.wikipedia.org/wiki/" + mention.mention
                print("https://en.wikipedia.org/wiki/"+mention.mention)
        print("\n")

        # Generating the RDF metadata starts here
        from rdflib import URIRef, BNode, Literal

        tweet_uri = URIRef(url)
        tweet_offset = URIRef(url_offset)
        wikipedia_uri = URIRef(wiki_uri)
        date = Literal(date)
        username = Literal(name)  # passing a string
        text = Literal(tweet)  # passing a python int

        from rdflib import Namespace
        from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
            PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
            VOID, XMLNS, XSD

        BASE = Namespace("http://www.kde.cs.tsukuba.ac.jp/~aregawi/w3c-email/")
        # wp = Namespace("https://en.wikipedia.org/wiki/")

        # wp.mention

        RDF.type
        DC.date
        DC.reference
        DC.isPartOf

        from rdflib import Graph
        g = Graph()
        g.bind("foaf", FOAF)
        g.bind("dc", DC)
        g.bind('', BASE)

        g.add((tweet_uri, FOAF.name, username))
        g.add((tweet_uri, DC.date, date))
        g.add((tweet_uri, BASE.text, text))
        g.add((tweet_uri, DC.isPartOf, tweet_offset))
        g.add((tweet_offset, DC.reference, wikipedia_uri))

        print(g.serialize(format="turtle").decode("utf-8"))
        # RDF metadata generation ends here by serializing it to turtle or xml formats

    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])
stream.filter(track=['Covid-19'], languages=["en"])
