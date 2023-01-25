# coding: utf-8

# transfer of custody

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

ecrm = Namespace("http://erlangen-crm.org/current/")
efrbroo = Namespace("http://erlangen-crm.org/efrbroo/")
pro = Namespace("http://purl.org/spar/pro/")
proles = Namespace("http://www.essepuntato.it/2013/10/politicalroles/")
prov = Namespace("http://www.w3.org/ns/prov#")
rico = Namespace("https://www.ica.org/standards/RiC/ontology#")
seq = Namespace("http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#")
ti = Namespace("http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("efrbroo", efrbroo)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("pro", pro)
g.bind("proles", proles)
g.bind("prov", prov)
g.bind("rico", rico)
g.bind("seq", seq)
g.bind("skos", SKOS)
g.bind("ti", ti)
g.bind("tvc", tvc)


base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'


# URI Fondo Giuseppe Raimondi
fonds = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-fonds')
fonds_label_en = 'Giuseppe Raimondi Fonds'
fonds_label_it = 'Fondo Giuseppe Raimondi'

# Transfer of custody (GR's heirs to IBC)

g.add((URIRef(fonds + '/object/custody-transfer-1'), RDF.type, ecrm.E10_Transfer_Of_Custody))
g.add((URIRef(fonds + '/object/custody-transfer-1'), ecrm.P29_custody_received_by, URIRef('https://w3id.org/giuseppe-raimondi-lod/organization/ibc')))
g.add((URIRef(fonds + '/object/custody-transfer-1'), ecrm.P30_transferred_custody_of, URIRef(fonds + '/object')))
g.add((URIRef(fonds + '/object/custody-transfer-1'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + '1985-1989')))
g.add((URIRef(fonds + '/object/custody-transfer-1'), RDFS.label, Literal("Acquisto dell'Archivio Giuseppe Raimondi da parte dell'Istituto regionale per i beni culturali (Ibc) alla fine degli anni '80", lang='it')))
g.add((URIRef(fonds + '/object/custody-transfer-1'), RDFS.label, Literal("Purchase of the Giuseppe Raimondi Archive by the Istituto regionale per i beni culturali (Ibc) in the late 1980s", lang='en')))

# Transfer of custody (IBC to Unibo)

g.add((URIRef(fonds + '/object/custody-transfer-2'), RDF.type, ecrm.E10_Transfer_Of_Custody))
g.add((URIRef(fonds + '/object/custody-transfer-2'), ecrm.P28_custody_surrendered_by, URIRef('https://w3id.org/giuseppe-raimondi-lod/organization/ibc')))
g.add((URIRef(fonds + '/object/custody-transfer-2'), ecrm.P29_custody_received_by, URIRef('https://w3id.org/giuseppe-raimondi-lod/organization/unibo')))
g.add((URIRef(fonds + '/object/custody-transfer-2'), ecrm.P30_transferred_custody_of, URIRef(fonds + '/object')))
g.add((URIRef(fonds + '/object/custody-transfer-2'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + '1996-05')))
g.add((URIRef(fonds + '/object/custody-transfer-2'), RDFS.label, Literal("Trasferimento dell'Archivio Giuseppe Raimondi dall'Istituto regionale per i beni culturali (Ibc) al Dipartimento di Italianistica dell'Università di Bologna nel maggio 1996", lang='it')))
g.add((URIRef(fonds + '/object/custody-transfer-2'), RDFS.label, Literal("Transfer of custody of the Giuseppe Raimondi Archive from the Istituto regionale per i beni culturali (Ibc) to the Department of Italian Studies of the University of Bologna in May 1996", lang='en')))

# RDF/XML
g.serialize(destination="../output/rdf/E10.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/E10.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-E10.jsonld", format='json-ld')