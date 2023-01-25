# coding: utf-8

# organization

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS, FOAF

ecrm = Namespace("http://erlangen-crm.org/current/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("foaf", FOAF)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("skos", SKOS)

base_uri = 'https://w3id.org/ficlitdl/'

organization = URIRef(base_uri + 'org/')

g.add((URIRef(organization + 'unibo'), RDF.type, ecrm.E40_Legal_Body))
g.add((URIRef(organization + 'unibo'), RDFS.label, Literal('Alma Mater Studiorum Università di Bologna', lang='it')))
g.add((URIRef(organization + 'unibo'), RDFS.label, Literal('Alma Mater Studiorum University of Bologna', lang='en')))
g.add((URIRef(organization + 'unibo'), OWL.sameAs, URIRef('https://w3id.org/zericatalog/organization/unibo')))
g.add((URIRef(organization + 'unibo'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q131262')))
g.add((URIRef(organization + 'unibo'), OWL.sameAs, URIRef('https://viaf.org/viaf/155886025')))
g.add((URIRef(organization + 'unibo'), FOAF.homepage, URIRef('https://www.unibo.it')))

g.add((URIRef(organization + 'ibc'), RDF.type, ecrm.E40_Legal_Body))
g.add((URIRef(organization + 'ibc'), RDFS.label, Literal('Istituto per i beni artistici, culturali e naturali della Regione Emilia-Romagna (IBC)', lang='it')))
g.add((URIRef(organization + 'ibc'), RDFS.label, Literal('Istitute for Cultural and Natural Heritage of the Region Emilia-Romagna (IBC)', lang='en')))
g.add((URIRef(organization + 'ibc'), OWL.sameAs, URIRef('http://viaf.org/viaf/130841901')))
g.add((URIRef(organization + 'ibc'), FOAF.homepage, URIRef('https://ibc.regione.emilia-romagna.it')))

# RDF/XML
g.serialize(destination="../output/rdf/E40.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/E40.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/E40.jsonld", format='json-ld')