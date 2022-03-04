
import tweepy
import spacy
import tagme
import time
import functools
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

class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title = ''

    def handle_starttag(self, tag, attributes):
        self.match = tag == 'title'

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False


"""def find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url_media = re.findall(regex, string)
    return [x[0] for x in url_media]"""


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
        print(status._json)
        print(tweet)
        # url_in_tweet = find(tweet)
        name = Literal(status.user.screen_name)
        # tweet_id = status.id
        date = Literal(status.created_at)
        text = Literal(tweet)
        uri = URIRef(f"https://twitter.com/user/status/{status.id}")
        RDF.type
        DC.date
        DC.reference
        DC.isPartOf
        DC.title
        DC.hasPart
        # url2 = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
        # print(text3)
        g = Graph()
        g.bind("foaf", FOAF)
        g.bind("dc", DC)
        g.bind('', BASE)

        g.add((uri, FOAF.name, name))
        g.add((uri, DC.date, date))
        g.add((uri, BASE.text, text))

        # @functools.lru_cache(maxsize=128)
        def create_triples():
            """for x in url_in_tweet:
                # print("Urls: ", x)
                uri2 = URIRef(Literal(x))
                g.add((BASE.text, DC.hasPart, uri2))
                expanded_url = requests.get(f'{x}').url
                # print(expanded_url) # we can print to see the results but not necessary
                # g.add((Literal(x), BASE.expandsTo, Literal(expanded_url))) # we don't need to create triples from this but if we want we can
                # response = requests.get(ur)
                req = requests.get(expanded_url)
                soup = bs(req.content, 'lxml')
                try:
                    # print(soup.select_one('title').text)
                    g.add((uri2, DC.title, Literal(soup.select_one('title').text)))
                except:
                    continue"""
            # print(url2) #we can print to see the results but not necessary

            print("\nMentions")
            entity_mentions = tagme.mentions(tweet)

            for mention in entity_mentions.mentions:
                if mention.linkprob>0.01:
                    print(mention.mention+ " lp="+str(mention.linkprob))
                    uri_offset = URIRef(uri + "#offset_" + str(mention.begin) + "_" + str(mention.end))
                    g.add((uri, DC.isPartOf, uri_offset))
                    # print(uri + "#offset_" + str(mention.begin) + "_" + str(mention.end)) #we can print to see the results but not necessary
                    # print(url2 + "#offset_" + str(mention.begin) + "_" + str(mention.end)) #we can print to see the results but not necessary
                    uri_wiki = URIRef("https://en.wikipedia.org/wiki/")
                    # replace space with %20 as space is invalid in url and add to the graph
                    g.add((uri_offset, DC.reference, uri_wiki+mention.mention.replace(" ", "%20")))
                    # print("https://en.wikipedia.org/wiki/"+mention.mention.replace(" ", "%20")) #we can print to see the results but not necessary
            print("\n")
            print("RDF Triples")
            print("\n")
            file = open("rdfmetadata.ttl", mode="a")
            file.write(g.serialize(format='turtle').decode("utf-8"))
            """g.serialize(destination='/Users/aregawi/Desktop/VIF/RDFMetadata/rdfmetadatav1.ttl', format='turtle')
            ttl_file = g.serialize(format="turtle").decode("utf-8")"""

        start_time = time.time()
        create_triples()
        print(g.serialize(format="turtle").decode("utf-8"))
        print("--- %s seconds ---" % (time.time() - start_time))
        # print(timeit.timeit('create_triples()', globals=globals(), number=1))
        print("\n")
        # create_triples.cache_clear()
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])
# we can change or add filtering hashtag, based on popular events
stream.filter(track=['Covid-19'], languages=["en"])