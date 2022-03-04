
"""from rdflib import URIRef, BNode, Literal, Namespace
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO

mona_lisa = URIRef('http://www.wikidata.org/entity/Q12418')
davinci = URIRef('http://dbpedia.org.resource/Leonardo_da_Vinci')
lajoconde = URIRef('http://data.europeana.eu/item/04802/243FA8618938F4117025F17A8B813C5F9AA4D619')

EX = Namespace('http://example.org/')
bob = EX['Bob']
alice = EX['Alice']

birth_date = Literal("1999-07-04", datatype=XSD['date'])
title = Literal('Mona Lisa', lang='en')
# print(title.value)

from rdflib import Graph
g = Graph()

g.add((bob, RDF.type, FOAF.Person))
g.add((bob, FOAF.knows, alice))
g.add((bob, FOAF['topic_interset'], mona_lisa))
g.add((bob, SDO['birthDate'], birth_date))
g.add((mona_lisa, DCTERMS['creator'], davinci))
g.add((mona_lisa, DCTERMS['title'], title))
g.add((lajoconde, DCTERMS['subject'], mona_lisa))
print(g.serialize(format = 'ttl').decode('u8'))
"""
from rdflib import URIRef, BNode, Literal

bob = URIRef("http://example.org/people/Bob")
linda = BNode()  # a GUID is generated

name = Literal('Bob')  # passing a string
age = Literal(24)  # passing a python int
height = Literal(76.5)  # passing a python float

from rdflib import Namespace

n = Namespace("http://example.org/people/")

n.bob  # = rdflib.term.URIRef(u'http://example.org/people/bob')
n.eve  # = rdflib.term.URIRef(u'http://example.org/people/eve')

from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD

RDF.type
# = rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

FOAF.knows
# = rdflib.term.URIRef("http://xmlns.com/foaf/0.1/knows")

PROF.isProfileOf
# = rdflib.term.URIRef("http://www.w3.org/ns/dx/prof/isProfileOf")

SOSA.Sensor
# = rdflib.term.URIRef("http://www.w3.org/ns/sosa/Sensor")

from rdflib import Graph
g = Graph()
g.bind("foaf", FOAF)

g.add((bob, RDF.type, FOAF.Person))
g.add((bob, FOAF.name, name))
g.add((bob, FOAF.knows, linda))
g.add((linda, RDF.type, FOAF.Person))
g.add((linda, FOAF.name, Literal("Linda")))

print(g.serialize(format="turtle").decode("utf-8"))

"""
from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
# BASE = Namespace("http://www.twitter.com/")
# OLIA = Namespace("http://purl.org/olia/olia.owl#")
# NERD = Namespace("http://nerd.eurecom.fr/ontology#")
# NIF = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
# ITSRDF = Namespace("https://www.w3.org/2005/11/its/rdf#")
# WP = Namespace("https://en.wikipedia.org/wiki/")
# MARL = Namespace("http://www.gsi.dit.upm.es/ontologies/marl/ns#")

# RDFグラフ
g = Graph()
g.bind('',BASE)
g.bind('schema',SDO)
g.bind('foaf',FOAF)
g.bind('owl',OWL)
g.bind('rdf',RDF)
g.bind('rdfs',RDFS)
g.bind('olia',OLIA)
g.bind('nerd',NERD)
g.bind('nif',NIF)
g.bind('itsrdf',ITSRDF)
g.bind('wd',WP)
g.bind('marl',MARL)
"""