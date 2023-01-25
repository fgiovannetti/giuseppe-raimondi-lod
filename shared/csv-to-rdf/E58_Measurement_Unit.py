# coding: utf-8

# MEASUREMENT UNIT (TYPE OF TYPE)


import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

ecrm = Namespace("http://erlangen-crm.org/current/")


g = Graph()


g.bind("ecrm", ecrm)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("skos", SKOS)

base_uri = 'https://w3id.org/ficlitdlo/'

# Measurement unit type
g.add((URIRef(base_uri + 'centimetre'), RDF.type, ecrm.E58_Measurement_Unit))
g.add((URIRef(base_uri + 'centimetre'), RDFS.label, Literal('centimetre (cm)', lang='en')))
g.add((URIRef(base_uri + 'centimetre'), RDFS.label, Literal('centimetro (cm)', lang='it')))
g.add((URIRef(base_uri + 'centimetre'), SKOS.relatedMatch, URIRef('http://vocab.getty.edu/aat/300379098')))

g.add((URIRef(base_uri + 'page'), RDF.type, ecrm.E58_Measurement_Unit))
g.add((URIRef(base_uri + 'page'), RDFS.label, Literal('page', lang='en')))
g.add((URIRef(base_uri + 'page'), RDFS.label, Literal('pagina', lang='it')))
g.add((URIRef(base_uri + 'page'), SKOS.exactMatch, URIRef('http://vocab.getty.edu/aat/300194222')))

g.add((URIRef(base_uri + 'leaf'), RDF.type, ecrm.E58_Measurement_Unit))
g.add((URIRef(base_uri + 'leaf'), RDFS.label, Literal('leaf', lang='en')))
g.add((URIRef(base_uri + 'leaf'), RDFS.label, Literal('carta', lang='it')))
g.add((URIRef(base_uri + 'leaf'), SKOS.exactMatch, URIRef('http://vocab.getty.edu/aat/300115833')))




# RDF/XML
g.serialize(destination="../output/rdf/E58.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/E58.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E58.jsonld", format='json-ld')