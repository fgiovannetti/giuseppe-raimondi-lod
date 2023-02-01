# coding: utf-8

""" Base graph :
FICLITDL, E53 Place
"""

from rdflib import Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, OWL, DCTERMS, PROV, FOAF
import csv
import re

# Create an empty Dataset
d = Dataset()

efrbroo = Namespace('http://erlangen-crm.org/efrbroo/')
ecrm = Namespace('http://erlangen-crm.org/current/')
ficlitdl = Namespace('https://w3id.org/ficlitdl/')
ficlitdlo = Namespace('https://w3id.org/ficlitdl/ontology/')
np = Namespace('http://www.nanopub.org/nschema#')
prism = Namespace('http://prismstandard.org/namespaces/basic/2.0/')
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')
ti = Namespace("http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")



# Add a namespace prefix to it, just like for Graph
d.bind('dcterms', DCTERMS)
d.bind('ecrm', ecrm)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('ficlitdl-np', URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base/'))
d.bind('foaf', FOAF)
d.bind("owl", OWL)
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('seq', seq)
d.bind('ti', ti)
d.bind('tvc', tvc)


# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/ficlitdl/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub-base/')

# Declare a Graph URI to be used to identify a Graph
graph_base = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_base, to the Dataset
d.graph(identifier=graph_base)

# Add quads to base-graph


base_uri = 'https://w3id.org/ficlitdl/'


# Biblioteca Ezio Raimondi
		
d.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDF.type, ecrm.E53_Place, graph_base))
d.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDFS.label, Literal('Biblioteca Ezio Raimondi, Dipartimento di filologia classica e italianistica, Università di Bologna', lang='it'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), RDFS.label, Literal('Ezio Raimondi Library, Department of Classical Philology and Italian Studies, University of Bologna', lang='en'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), ecrm.P89_falls_within, URIRef(base_uri + 'place/' + 'bologna'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi'), ecrm.P76_has_contact_point, URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), graph_base))
	
# Bologna
		
d.add((URIRef(base_uri + 'place/' + 'bologna'), RDF.type, ecrm.E53_Place, graph_base))
d.add((URIRef(base_uri + 'place/' + 'bologna'), RDFS.label, Literal('Bologna' , lang='it'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'bologna'), RDFS.label, Literal('Bologna' , lang='en'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('http://sws.geonames.org/3181928'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q1891'), graph_base))
d.add((URIRef(base_uri + 'place/' + 'bologna'), OWL.sameAs, URIRef('http://dbpedia.org/resource/Bologna'), graph_base))







# TriG
d.serialize(destination="../output/trig/base-graph-E53.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E53.nq", format='nquads')