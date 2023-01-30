# coding: utf-8

""" Base graph :
Fondo Raimondi, E10 Transfer of Custody
"""

from rdflib import Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, PROV
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
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base/'))
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('seq', seq)
d.bind('ti', ti)
d.bind('tvc', tvc)


# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub-base/')

# Declare a Graph URI to be used to identify a Graph
graph_base = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_base, to the Dataset
d.graph(identifier=graph_base)

# URI Fondo Giuseppe Raimondi
fonds = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-fonds')
fonds_label_en = 'Giuseppe Raimondi Fonds'
fonds_label_it = 'Fondo Giuseppe Raimondi'


# Add quads to base-graph


# Transfer of custody (GR's heirs to SUB ERO)

d.add((URIRef(fonds + '/object/custody-transfer-1'), RDF.type, ecrm.E10_Transfer_Of_Custody, graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-1'), ecrm.P29_custody_received_by, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-1'), ecrm.P30_transferred_custody_of, URIRef(fonds + '/object'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-1'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + '1985-1989'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-1'), RDFS.label, Literal("Acquisto dell'Archivio Giuseppe Raimondi da parte della Soprintendenza archivistica e bibliografica dell'Emilia-Romagna (SAB ERO) alla fine degli anni '80", lang='it'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-1'), RDFS.label, Literal("Purchase of the Giuseppe Raimondi Archive by the Soprintendenza archivistica e bibliografica dell'Emilia-Romagna (SAB ERO) in the late 1980s", lang='en'), graph_base))

# Transfer of custody (SUB ERO to Unibo)

d.add((URIRef(fonds + '/object/custody-transfer-2'), RDF.type, ecrm.E10_Transfer_Of_Custody, graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-2'), ecrm.P28_custody_surrendered_by, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-2'), ecrm.P29_custody_received_by, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-2'), ecrm.P30_transferred_custody_of, URIRef(fonds + '/object'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-2'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + '1996-05'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-2'), RDFS.label, Literal("Trasferimento dell'Archivio Giuseppe Raimondi dallaSoprintendenza archivistica e bibliografica dell'Emilia-Romagna (SAB ERO) al Dipartimento di Italianistica dell'Università di Bologna nel maggio 1996", lang='it'), graph_base))
d.add((URIRef(fonds + '/object/custody-transfer-2'), RDFS.label, Literal("Transfer of custody of the Giuseppe Raimondi Archive from the Soprintendenza archivistica e bibliografica dell'Emilia-Romagna (SAB ERO) to the Department of Italian Studies of the University of Bologna in May 1996", lang='en'), graph_base))








# TriG
d.serialize(destination="../output/trig/base-graph-E10.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E10.nq", format='nquads')