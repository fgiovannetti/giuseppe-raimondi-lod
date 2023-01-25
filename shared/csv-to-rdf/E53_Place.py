# coding: utf-8

# place

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

base_uri = 'https://w3id.org/ficlitdl/'
		
# Biblioteca Ezio Raimondi
		
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDF.type, ecrm.E53_Place))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDFS.label, Literal('Biblioteca Ezio Raimondi, Dipartimento di filologia classica e italianistica, Università di Bologna', lang='it')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDFS.label, Literal('Ezio Raimondi Library, Department of Classical Philology and Italian Studies, University of Bologna', lang='en')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), ecrm.P89_falls_within, URIRef(base_uri + 'place/' + 'bologna')))
g.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), ecrm.P76_has_contact_point, URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO')))
	
# Bologna
		
g.add((URIRef(base_uri + 'place/' + 'bologna'), RDF.type, ecrm.E53_Place))
g.add((URIRef(base_uri + 'place/' + 'bologna'), RDFS.label, Literal('Bologna' , lang='it')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), RDFS.label, Literal('Bologna' , lang='en')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('http://sws.geonames.org/3181928')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q1891')))
g.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('http://dbpedia.org/resource/Bologna')))

# RDF/XML
g.serialize(destination="../output/rdf/E53.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/E53.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/E53.jsonld", format='json-ld')