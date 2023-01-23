# coding: utf-8

# address

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

base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

g.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), RDF.type, crm.E45_Address))
g.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), RDFS.label, Literal('Via Zamboni 32, 40126, Bologna (BO), Italia' , lang='it')))
g.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), RDFS.label, Literal('Via Zamboni 32, 40126, Bologna (BO), Italy' , lang='en')))
g.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), DCTERMS.identifier, URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO')))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-E45.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-E45.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E45.jsonld", format='json-ld')