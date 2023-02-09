# coding: utf-8

""" Base graph :
Quaderni, E35 Title
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
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])

		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# physical notebook URI

		rec_object = URIRef(record + 'object')
 		
 		# expression URI

		rec_expression = URIRef(record + 'text')
		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]


		# Add quads to base-graph

		###########################
		#                         #
		# Title of main text      #
		#                         #
		###########################

		d.add((URIRef(rec_expression + '/title'), RDF.type, ecrm.E35_Title, graph_base))
		d.add((URIRef(rec_expression + '/title'), RDFS.label, Literal('Titolo, "' + rec_label[0].replace('*', '').replace('[', '').replace(']', '') + '"', lang='it'), graph_base))
		d.add((URIRef(rec_expression + '/title'), RDFS.label, Literal('Title, "' + rec_label[0].replace('*', '').replace('[', '').replace(']', '') + '"', lang='en'), graph_base))
		d.add((URIRef(rec_expression + '/title'), RDF.value, Literal(rec_label[0]), graph_base))
		if rec_label[0].startswith('['):
			d.add((URIRef(rec_expression + '/title-attribution'), RDF.type, ecrm.E13_Attribute_Assignment, graph_base))
			d.add((URIRef(rec_expression + '/title-attribution'), ecrm.P141_assigned, URIRef(rec_expression + '/title'), graph_base))
			d.add((URIRef(rec_expression + '/title-attribution'), ecrm.P14_carried_out_by, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), graph_base))
			d.add((URIRef(rec_expression + '/title-attribution'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + '1993-03-07'), graph_base))

		############################
		#                          #
		# Titles of sub-texts      #
		#                          #
		############################

		if ' ; ' in rec_label[0]:
			rec_label = rec_label[0].split(' ; ')
			i = 1
			for title in rec_label:
				# URI Subexpression
				rec_subexpression = URIRef(rec_expression + '/' + str(i))
				d.add((URIRef(rec_subexpression + '/title'), RDF.type, ecrm.E35_Title, graph_base))
				d.add((URIRef(rec_subexpression + '/title'), RDFS.label, Literal('Titolo, "' + title.replace('[', '').replace(']', '') + '"', lang='it'), graph_base))
				d.add((URIRef(rec_subexpression + '/title'), RDFS.label, Literal('Title, "' + title.replace('[', '').replace(']', '') + '"', lang='en'), graph_base))
				d.add((URIRef(rec_subexpression + '/title'), RDF.value, Literal(title), graph_base))
				i += 1



# TriG
d.serialize(destination="../../dataset/trig/base-graph-E35_quad.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-E35_quad.nq", format='nquads')