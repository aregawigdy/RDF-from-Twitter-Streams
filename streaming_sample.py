
import string

import spacy
from gensim.parsing import remove_stopwords
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
from tokenization import nlp

consumer_key = "yzw16SfR4rnfZb4m2JnzRryPr"
consumer_secret = "88OAWEkNfLdSzRplcbI2PQmn0vjSl1AVi5KhRIFMVSiEDfsm9p"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1178352707821658113-xXcRH018zjZX3RfxwH38FEPIjNJIHU"
access_token_secret = "oZvFOW47k13tKWHONSIa7GwIENCu6mbHMb3iMrE3o5QIH"
# # # # Twitter Authenticator # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
# # # # Twitter Streamer # # # #
class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hashtag_list)


# # # # Twitter Stream Listener # # # #
class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:

            """ print(data)"""
            """ Converting text to lowercase """
            small_leter = data.lower()
            """print(small_leter)"""
            """Removing Punctuation marks"""
            rem_punctuation = small_leter.translate(str.maketrans('', '', string.punctuation))
            """print(rem_punctuation)"""
            """Removing white spaces"""
            rem_white = rem_punctuation.strip()
            """print(rem_white)"""
            """Removing stop words"""
            rem_stopwords = remove_stopwords(rem_white)
            """print(rem_stopwords)"""
            """Word Tokenization"""
            doc = nlp(rem_stopwords)
            token_list = []
            for token in doc:
                token_list.append(token)
            """print(token_list)"""
            """Entity Extraction"""
            sp = spacy.load('en_core_web_sm')
            sen = sp(rem_stopwords)
            print(sen.ents)
            """sen = sp(u'Manchester United is looking to sign Harry Kane for $90 million. David demand 100 Million Dollars')
            for entity in sen.ents:
                print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
            """
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
                return True
        except BaseException as e:
            print("Error on data %s" %str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    hashtag_list = ["Covid-19"]
    fetched_tweets_filename = "tweets.txt"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)
