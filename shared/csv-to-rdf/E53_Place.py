# coding: utf-8

# place

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
		
# Biblioteca Ezio Raimondi
		
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDF.type, crm.E53_Place))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDFS.label, Literal('Biblioteca Ezio Raimondi, Dipartimento di filologia classica e italianistica, Università di Bologna', lang='it')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDFS.label, Literal('Ezio Raimondi Library, Department of Classical Philology and Italian Studies, University of Bologna', lang='en')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), crm.P89_falls_within, URIRef(base_uri + 'place/' + 'bologna')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), crm.P76_has_contact_point, URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), DCTERMS.identifier, URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi')))
	
# Bologna
		
g.add((URIRef(base_uri + 'place/' + 'bologna'), RDF.type, crm.E53_Place))
g.add((URIRef(base_uri + 'place/' + 'bologna'), RDFS.label, Literal('Bologna' , lang='it')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), RDFS.label, Literal('Bologna' , lang='en')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('http://sws.geonames.org/3181928')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q1891')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('http://dbpedia.org/resource/Bologna')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), DCTERMS.identifier, URIRef(base_uri + 'place/' + 'bologna')))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-E53.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-E53.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E53.jsonld", format='json-ld')