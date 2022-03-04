
subject = "<https://twitter.com/user/status/1413119774972731395>"
predicate = "<http://purl.org/dc/terms/date>"
object1 = "2021-07-08 12:56:23"
print(subject+" "+predicate+" "+ "\""+object1+"\"")

from rdflib import URIRef, BNode, Literal

tweet = URIRef("https://twitter.com/user/status/1413119774972731395")
tweet_offset = URIRef("https://twitter.com/user/status/1413119774972731395#offset_5_20")
wikipedia = URIRef("https://en.wikipedia.org/wiki/")
date = Literal('2021-07-08 12:56:23')
username = Literal('biden')  # passing a string
text = Literal('Let us make America great again')  # passing a python int

from rdflib import Namespace
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD

BASE = Namespace("http://www.kde.cs.tsukuba.ac.jp/~aregawi/w3c-email/")
# wp = Namespace("https://en.wikipedia.org/wiki/")

# wp.mention

RDF.type
DC.date
DC.title

from rdflib import Graph
g = Graph()
g.bind("foaf", FOAF)
g.bind("dc", DC)
g.bind('',BASE)

g.add((tweet, FOAF.name, username))
g.add((tweet, DC.date, date))
g.add((tweet, BASE.text, text))
g.add((tweet, DC.isPartOf, tweet_offset))
g.add((tweet_offset, DC.reference, wikipedia))

print(g.serialize(format="xml").decode("utf-8"))