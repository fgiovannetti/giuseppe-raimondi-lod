# coding: utf-8

""" Base graph :
Album, E13 Attribute Assignment
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


with open('../input/Corrispondenza.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] #?1954
		sequenza = row['Sequenza'] #00.00
		data_inv = row['Data inv.']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"]) # HA PER ALTRO TITOLO

		series = URIRef(base_uri + 'record-set' + '/' + 'articles')

		if collocazione == 'Corrispondenza1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '/' + specificazione)
		elif collocazione == 'Corrispondenza2':
			subseries = URIRef(series + '-2')

		# Declare a URI for each record
		record = URIRef(base_uri + 'article/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each article text
		rec_expression = URIRef(record + 'text')
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]

		# Add quads to base-graph




		# Authorship attribution
		if '[Giuseppe' in descrizione_isbd:

			d.add((URIRef(rec_expression + '/author-attribution'), RDF.type, ecrm.E13_Attribute_Assignment, graph_base))
			d.add((URIRef(rec_expression + '/author-attribution'), ecrm.P141_assigned, URIRef(rec_expression + '/author'), graph_base))
			d.add((URIRef(rec_expression + '/author-attribution'), ecrm.P140_assigned_attribute_to, URIRef('https://w3id.org/ficlitdl/' + 'person/giuseppe-raimondi'), graph_base))
			d.add((URIRef(rec_expression + '/author-attribution'), ecrm.P14_carried_out_by, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), graph_base))
			d.add((URIRef(rec_expression + '/author-attribution'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + '1993-03'), graph_base))
			d.add((URIRef(rec_expression + '/author-attribution'), RDFS.label, Literal('Attribuzione della paternità del testo manoscritto ' + '"' + rec_label + '" a Giuseppe Raimondi', lang='it'), graph_base))
			d.add((URIRef(rec_expression + '/author-attribution'), RDFS.label, Literal('Authorship attribution of the manuscript text ' + '"' + rec_label + '" to Giuseppe Raimondi', lang='en'), graph_base))




# TriG
d.serialize(destination="../output/trig/base-graph-E13.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E13.nq", format='nquads')