# coding: utf-8

# organization

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS, FOAF

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

g = Graph()

g.bind("crm", crm)
g.bind("foaf", FOAF)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("skos", SKOS)

base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

organization = URIRef(base_uri + 'organization/')

g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), RDF.type, crm.E40_Legal_Body))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), RDFS.label, Literal('Alma Mater Studiorum Università di Bologna', lang='it')))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), RDFS.label, Literal('Alma Mater Studiorum University of Bologna', lang='en')))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), DCTERMS.identifier, URIRef(organization + 'alma-mater-studiorum-university-of-bologna')))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), OWL.sameAs, URIRef('https://w3id.org/zericatalog/organization/alma-mater-studiorum-university-of-bologna')))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q131262')))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), OWL.sameAs, URIRef('https://viaf.org/viaf/155886025')))
g.add((URIRef(organization + 'alma-mater-studiorum-university-of-bologna'), FOAF.homepage, URIRef('https://www.unibo.it')))

g.add((URIRef(organization + 'istituto-per-i-beni-artistici-culturali-e-naturali'), RDF.type, crm.E40_Legal_Body))
g.add((URIRef(organization + 'istituto-per-i-beni-artistici-culturali-e-naturali'), RDFS.label, Literal('Istituto per i beni artistici, culturali e naturali della Regione Emilia-Romagna (IBC)', lang='it')))
g.add((URIRef(organization + 'istituto-per-i-beni-artistici-culturali-e-naturali'), RDFS.label, Literal('Istitute for Cultural and Natural Heritage of the Region Emilia-Romagna (IBC)', lang='en')))
g.add((URIRef(organization + 'istituto-per-i-beni-artistici-culturali-e-naturali'), DCTERMS.identifier, URIRef(organization + 'alma-mater-studiorum-university-of-bologna')))
g.add((URIRef(organization + 'istituto-per-i-beni-artistici-culturali-e-naturali'), OWL.sameAs, URIRef('http://viaf.org/viaf/130841901')))
g.add((URIRef(organization + 'istituto-per-i-beni-artistici-culturali-e-naturali'), FOAF.homepage, URIRef('https://ibc.regione.emilia-romagna.it')))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-E40.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-E40.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E40.jsonld", format='json-ld')