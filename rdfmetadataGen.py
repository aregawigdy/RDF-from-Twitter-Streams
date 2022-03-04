
import tweepy
import spacy
import tagme
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace, Graph
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD

BASE = Namespace("http://www.kde.cs.tsukuba.ac.jp/~aregawi/w3c-email/")

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
        name = Literal(status.user.screen_name)
        tweet_id = status.id
        date = Literal(status.created_at)
        text = Literal(tweet)
        uri = URIRef(f"https://twitter.com/user/status/{status.id}")
        RDF.type
        DC.date
        DC.reference
        DC.isPartOf
        url2 = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
        """print(text3)"""
        g = Graph()
        g.bind("foaf", FOAF)
        g.bind("dc", DC)
        g.bind('', BASE)

        g.add((uri, FOAF.name, name))
        g.add((uri, DC.date, date))
        g.add((uri, BASE.text, text))
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
                uri_offset = URIRef(uri + "#offset_" + str(mention.begin) + "_" + str(mention.end))
                g.add((uri, DC.isPartOf, uri_offset))
                print(uri + "#offset_" + str(mention.begin) + "_" + str(mention.end))
                print(url2 + "#offset_" + str(mention.begin) + "_" + str(mention.end))
                uri_wiki = URIRef("https://en.wikipedia.org/wiki/")
                g.add((uri_offset, DC.reference, uri_wiki+mention.mention.replace(" ", "%20")))
                print("https://en.wikipedia.org/wiki/"+mention.mention.replace(" ", "%20"))
        print("\n")
        print(g.serialize(format="turtle").decode("utf-8"))
        """ creating turtle file
        g.serialize(destination="rdfmetadatgen.ttl")"""
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])
stream.filter(track=['Covid-19'], languages=["en"])