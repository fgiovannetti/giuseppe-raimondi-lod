# coding: utf-8

""" Base graph :
Album, E89 Propositional Object
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

with open('../../input/album.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] 
		data_inv = row['Data inv.']
		identificativo = row['Id.']
		precisazione = row['Precisazione inventario']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"]) # HA PER ALTRO TITOLO

		# URI Serie Album
		series = URIRef(base_uri + 'record-set' + '/' + 'album')
		series_label_en = 'Giuseppe Raimondi Fonds, Archive, Album'
		series_label_it = 'Fondo Giuseppe Raimondi, Archivio, Album'

		# URI Album
		specificazione = specificazione.replace('[', '').replace(']', '').replace('?', '')
		file = URIRef(base_uri + 'record-set/album-' + specificazione.lower() + '/' + inventario[0].lower().replace(' ', ''))
		file_object = URIRef(file + '/object')
		label = re.findall('^(.+?)\. \-', descrizione_isbd)

		file_label_en = 'Giuseppe Raimondi Fonds, Archive, ' + label[0]
		file_label_it = 'Fondo Giuseppe Raimondi, Archivio, ' + label[0]

		
		# URI Subfondo Archivio
		subfonds = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-archive')

		# Series description 

		d.add((URIRef(series), RDF.type, URIRef('http://erlangen-crm.org/current/E89_Propositional_Object'), graph_base))
		d.add((URIRef(series), RDFS.label, Literal(series_label_it, lang='it'), graph_base))
		d.add((URIRef(series), RDFS.label, Literal(series_label_en, lang='en'), graph_base))
		d.add((URIRef(series), ecrm.P2_has_type, ficlitdlo.series, graph_base))
		d.add((URIRef(series), ficlitdlo.formsConceptuallyPartOf, URIRef(subfonds), graph_base)) # Archivio (FR.A)
		d.add((URIRef(series), ficlitdlo.isConceptuallyComposedOf, URIRef(file), graph_base))



# TriG
d.serialize(destination="../../dataset/trig/album_base-graph-E89.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/album_base-graph-E89.nq", format='nquads')