# coding: utf-8

# right

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
pro = Namespace("http://purl.org/spar/pro/")
proles = Namespace("http://www.essepuntato.it/2013/10/politicalroles/")
prov = Namespace("http://www.w3.org/ns/prov#")
rico = Namespace("https://www.ica.org/standards/RiC/ontology#")
seq = Namespace("http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#")
ti = Namespace("http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")

g = Graph()

g.bind("crm", crm)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("skos", SKOS)

base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

g.add((URIRef(base_uri + 'right/all-rights-reserved'), RDF.type, crm.E30_Right))
g.add((URIRef(base_uri + 'right/all-rights-reserved'), RDFS.label, Literal('Tutti i diritti riservati. Vietata ogni ulteriore riproduzione.', lang='it')))
g.add((URIRef(base_uri + 'right/all-rights-reserved'), RDFS.label, Literal('All rights reserved. Any other reproduction or distribution is prohibited.', lang='en')))
g.add((URIRef(base_uri + 'right/all-rights-reserved'), DCTERMS.identifier, URIRef(base_uri + 'right/all-rights-reserved')))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-E30.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-E30.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E30.jsonld", format='json-ld')