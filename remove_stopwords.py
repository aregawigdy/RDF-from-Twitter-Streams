
import re
import string
import spacy
import json
from spacy.lang.en import English
from tweepy import OAuthHandler, Stream, StreamListener
from gensim.parsing.preprocessing import remove_stopwords

nlp = spacy.load('en_core_web_sm')

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "yzw16SfR4rnfZb4m2JnzRryPr"
consumer_secret = "88OAWEkNfLdSzRplcbI2PQmn0vjSl1AVi5KhRIFMVSiEDfsm9p"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1178352707821658113-xXcRH018zjZX3RfxwH38FEPIjNJIHU"
access_token_secret = "oZvFOW47k13tKWHONSIa7GwIENCu6mbHMb3iMrE3o5QIH"


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        # Load pre-existing spacy model
        np = spacy.load('en_core_web_sm')
        # Getting the pipeline component
        ner = np.get_pipe("ner")
        # training data
        TRAIN_DATA = [
            ("Walmart is a leading e-commerce company", {"entities": [(0, 7, "ORG")]}),
            ("Covid-19 is a pandemic disease found in 2019", {"entities": [(0, 8, "DISEASE")]}),
            ("I reached Chennai yesterday.", {"entities": [(19, 28, "GPE")]}),
            ("I recently ordered a book from Amazon", {"entities": [(24, 32, "ORG")]}),
            ("I was driving a BMW", {"entities": [(16, 19, "PRODUCT")]}),
            ("I ordered this from ShopClues", {"entities": [(20, 29, "ORG")]}),
            ("Fridge can be ordered in Amazon ", {"entities": [(0, 6, "PRODUCT")]}),
            ("I bought a new Washer", {"entities": [(16, 22, "PRODUCT")]}),
            ("I bought a old table", {"entities": [(16, 21, "PRODUCT")]}),
            ("I bought a fancy dress", {"entities": [(18, 23, "PRODUCT")]}),
            ("I rented a camera", {"entities": [(12, 18, "PRODUCT")]}),
            ("I rented a tent for our trip", {"entities": [(12, 16, "PRODUCT")]}),
            ("I rented a screwdriver from our neighbour", {"entities": [(12, 22, "PRODUCT")]}),
            ("I repaired my computer", {"entities": [(15, 23, "PRODUCT")]}),
            ("I got my clock fixed", {"entities": [(16, 21, "PRODUCT")]}),
            ("I got my truck fixed", {"entities": [(16, 21, "PRODUCT")]}),
            ("Flipkart started it's journey from zero", {"entities": [(0, 8, "ORG")]}),
            ("I recently ordered from Max", {"entities": [(24, 27, "ORG")]}),
            ("Flipkart is recognized as leader in market", {"entities": [(0, 8, "ORG")]}),
            ("I recently ordered from Swiggy", {"entities": [(24, 29, "ORG")]})
        ]
        # Adding labels to the `ner`
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])
        json_load = json.loads(data)
        texts = json_load['text']
        coded = texts.encode('utf-8')
        s = str(coded)
        """print(s[2:-1])"""
        """ Converting text to lowercase """
        arr = s[2:-1]
        small_leter = arr.lower()
        print(small_leter)
        """Remove URLs from a sample string"""
        rem_url = re.sub(r"http\S+", "", small_leter)
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
        sen = sp(small_leter)
        """print(sen.ents)
        sen = sp(u'Manchester United is looking to sign Harry Kane for $90 million. David demand 100 Million Dollars')"""
        for entity in sen.ents:
            print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        print("\n")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['Covid-19'], languages=["en"])
