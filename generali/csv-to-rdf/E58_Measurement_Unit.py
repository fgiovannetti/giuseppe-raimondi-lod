# coding: utf-8

# MEASUREMENT UNIT (TYPE OF TYPE)


import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")


g = Graph()


g.bind("crm", crm)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("skos", SKOS)

base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Measurement unit type
g.add((URIRef(base_uri + 'measurement-unit-type/centimetre'), RDF.type, crm.E58_Measurement_Unit))
g.add((URIRef(base_uri + 'measurement-unit-type/centimetre'), RDFS.label, Literal('centimetre (cm)', lang='en')))
g.add((URIRef(base_uri + 'measurement-unit-type/centimetre'), RDFS.label, Literal('centimetro (cm)', lang='it')))
g.add((URIRef(base_uri + 'measurement-unit-type/centimetre'), SKOS.relatedMatch, URIRef('http://vocab.getty.edu/aat/300379098')))
g.add((URIRef(base_uri + 'measurement-unit-type/centimetre'), DCTERMS.identifier, URIRef(base_uri + 'measurement-unit-type/centimetre')))

g.add((URIRef(base_uri + 'measurement-unit-type/page'), RDF.type, crm.E58_Measurement_Unit))
g.add((URIRef(base_uri + 'measurement-unit-type/page'), RDFS.label, Literal('page', lang='en')))
g.add((URIRef(base_uri + 'measurement-unit-type/page'), RDFS.label, Literal('pagina', lang='it')))
g.add((URIRef(base_uri + 'measurement-unit-type/page'), SKOS.exactMatch, URIRef('http://vocab.getty.edu/aat/300194222')))
g.add((URIRef(base_uri + 'measurement-unit-type/page'), DCTERMS.identifier, URIRef(base_uri + 'measurement-unit-type/page')))

g.add((URIRef(base_uri + 'measurement-unit-type/leaf'), RDF.type, crm.E58_Measurement_Unit))
g.add((URIRef(base_uri + 'measurement-unit-type/leaf'), RDFS.label, Literal('leaf', lang='en')))
g.add((URIRef(base_uri + 'measurement-unit-type/leaf'), RDFS.label, Literal('carta', lang='it')))
g.add((URIRef(base_uri + 'measurement-unit-type/leaf'), SKOS.exactMatch, URIRef('http://vocab.getty.edu/aat/300115833')))
g.add((URIRef(base_uri + 'measurement-unit-type/leaf'), DCTERMS.identifier, URIRef(base_uri + 'measurement-unit-type/leaf')))




# RDF/XML
g.serialize(destination="../output/rdf/fr-a-E58.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-E58.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E58.jsonld", format='json-ld')