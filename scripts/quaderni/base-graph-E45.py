# coding: utf-8

""" Base graph :
FICLITDL, E45 Address
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


d.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), RDF.type, ecrm.E45_Address, graph_base))
d.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), RDFS.label, Literal('Via Zamboni 32, 40126, Bologna (BO), Italia' , lang='it'), graph_base))
d.add((URIRef(base_uri + 'address/' + 'via-zamboni-32-40126-Bologna-BO'), RDFS.label, Literal('Via Zamboni 32, 40126, Bologna (BO), Italy' , lang='en'), graph_base))








# TriG
d.serialize(destination="../../dataset/trig/base-graph-E45_quad.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-E45_quad.nq", format='nquads')