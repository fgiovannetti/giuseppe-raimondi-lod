# coding: utf-8

""" Base graph :
FICLITDL, E40 Legal Body
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

org = URIRef(base_uri + 'org/')

d.add((URIRef(org + 'unibo'), RDF.type, ecrm.E40_Legal_Body, graph_base))
d.add((URIRef(org + 'unibo'), RDFS.label, Literal('Alma Mater Studiorum Università di Bologna', lang='it'), graph_base))
d.add((URIRef(org + 'unibo'), RDFS.label, Literal('Alma Mater Studiorum University of Bologna', lang='en'), graph_base))
d.add((URIRef(org + 'unibo'), OWL.sameAs, URIRef('https://w3id.org/zericatalog/org/unibo'), graph_base))
d.add((URIRef(org + 'unibo'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q131262'), graph_base))
d.add((URIRef(org + 'unibo'), OWL.sameAs, URIRef('https://viaf.org/viaf/155886025'), graph_base))
d.add((URIRef(org + 'unibo'), FOAF.homepage, URIRef('https://www.unibo.it'), graph_base))

d.add((URIRef(org + 'ibc'), RDF.type, ecrm.E40_Legal_Body, graph_base))
d.add((URIRef(org + 'ibc'), RDFS.label, Literal('Istituto per i beni artistici, culturali e naturali della Regione Emilia-Romagna (IBC)', lang='it'), graph_base))
d.add((URIRef(org + 'ibc'), RDFS.label, Literal('Istitute for Cultural and Natural Heritage of the Region Emilia-Romagna (IBC)', lang='en'), graph_base))
d.add((URIRef(org + 'ibc'), OWL.sameAs, URIRef('http://viaf.org/viaf/130841901'), graph_base))
d.add((URIRef(org + 'ibc'), FOAF.homepage, URIRef('https://ibc.regione.emilia-romagna.it'), graph_base))

d.add((URIRef(org + 'sab-ero'), RDF.type, ecrm.E40_Legal_Body, graph_base))
d.add((URIRef(org + 'sab-ero'), RDFS.label, Literal("Soprintendenza archivistica e bibliografica dell'Emilia Romagna (SAB ERO)", lang='it'), graph_base))
d.add((URIRef(org + 'sab-ero'), FOAF.homepage, URIRef('https://sab-ero.cultura.gov.it'), graph_base))








# TriG
d.serialize(destination="../../dataset/trig/quaderni_base-graph-E40.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/quaderni_base-graph-E40.nq", format='nquads')