
import re
import string

from PIL import Image
import requests
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
        text = status.text
        # geometry = status.coordinates
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
        print(tweet)
        """for media in status.entities.get("media",[{}]):
            # checks if there is any media-entity
            if media.get("type",None) == "photo":
                image_content = requests.get(media["media_url"])
                print(image_content)"""
        if 'media' in status.entities:
            for media in status.extended_entities['media']:
                print(media['media_url'])
        name = status.user.screen_name
        id = status.id
        url = f"https://twitter.com/user/status/{status.id}"
        url2 = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
        """print(text3)"""
        print(name)
        # print(geometry)
        print(id)
        print(url)
        print(url2)
        sen = nlp(tweet)
        print("Entities using SpaCy")
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
                print(url2 + "#offset_" + str(mention.begin) + "_" + str(mention.end))
        print("\n")

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])
stream.filter(track=['Covid-19'], languages=["en"])
