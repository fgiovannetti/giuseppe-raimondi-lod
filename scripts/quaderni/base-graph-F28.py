# coding: utf-8

""" Base graph :
Quaderni, F28 Expression Creation
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

with open('../../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:

		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione']
		sequenza = row['Sequenza']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		yyyy = re.findall("(.+?) *$", descrizione_isbd[0])
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		# Declare a URI for each record
		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical notebook
		rec_object = URIRef(record + 'object')
 		
 		# Declare a URI for each notebook text
		rec_expression = URIRef(record + 'text')

		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]

		rec_time_span = re.findall('\. \- (.+?)\. \-', descrizione_isbd)[0]
		rec_time_span = rec_time_span.replace('[', '').replace(']', '').replace('?', '').replace('4.', '40-1949').replace('5.', '50-1959').replace('7.', '70-1979').replace('8.', '80-1989')

		person = URIRef('https://w3id.org/ficlitdl/' + 'person/')


		# Add quads to base-graph


		d.add((URIRef(rec_expression + '/creation'), RDF.type, efrbroo.F28_Expression_Creation, graph_base))
		d.add((URIRef(rec_expression + '/creation'), RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '", creazione.' , lang='it'), graph_base))
		d.add((URIRef(rec_expression + '/creation'), RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '", creation.' , lang='en'), graph_base))
		if collocazione == 'QUADERNI.1':
			d.add((URIRef(rec_expression + '/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + specificazione), graph_base))
		else:
			d.add((URIRef(rec_expression + '/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + rec_time_span), graph_base))
		d.add((URIRef(rec_expression + '/creation'), ecrm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi'), graph_base))
		d.add((URIRef(rec_expression + '/creation'), ecrm.P32_used_general_technique, ficlitdlo.handwriting, graph_base))
		d.add((URIRef(rec_expression + '/creation'), efrbroo.R17_created, URIRef(rec_expression), graph_base))
		d.add((URIRef(rec_expression + '/creation'), efrbroo.R18_created, URIRef(rec_object), graph_base))



# TriG
d.serialize(destination="../../dataset/trig/base-graph-F28_quad.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-F28_quad.nq", format='nquads')