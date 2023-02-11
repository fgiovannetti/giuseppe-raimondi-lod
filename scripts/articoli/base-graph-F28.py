# coding: utf-8

""" Base graph :
Articoli, F28 Expression Creation
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

with open('../../input/articoli.csv', mode='r') as csv_file:
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

		if collocazione == 'ARTICOLI1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '/' + specificazione)
		elif collocazione == 'ARTICOLI2':
			subseries = URIRef(series + '-2')

		# Declare a URI for each record
		record = URIRef(base_uri + 'article/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each article text
		rec_expression = URIRef(record + 'text')
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]
		

		# specificazione + sequenza
		if sequenza == '00.00':
			rec_time_span = specificazione.replace('?', '') + '-01-01-' + specificazione.replace('?', '') + '-12-31'
		else:
			rec_time_span = specificazione + '-' + sequenza.replace('.', '-').replace(' ', '')
		
		person = URIRef('https://w3id.org/ficlitdl/' + 'person/')


		# Add quads to base-graph


		d.add((URIRef(rec_expression + '/creation'), RDF.type, efrbroo.F28_Expression_Creation, graph_base))
		d.add((URIRef(rec_expression + '/creation'), RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label + '", creazione.' , lang='it'), graph_base))
		d.add((URIRef(rec_expression + '/creation'), RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label + '", creation.' , lang='en'), graph_base))
		d.add((URIRef(rec_expression + '/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + rec_time_span), graph_base))
		d.add((URIRef(rec_expression + '/creation'), ecrm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi'), graph_base))
		d.add((URIRef(rec_expression + '/creation'), ecrm.P32_used_general_technique, ficlitdlo.handwriting, graph_base))
		d.add((URIRef(rec_expression + '/creation'), efrbroo.R17_created, URIRef(rec_expression), graph_base))
		d.add((URIRef(rec_expression + '/creation'), efrbroo.R18_created, URIRef(rec_object), graph_base))



# TriG
d.serialize(destination="../../dataset/trig/articoli_base-graph-F28.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/articoli_base-graph-F28.nq", format='nquads')