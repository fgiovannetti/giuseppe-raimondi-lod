# coding: utf-8

""" Base graph :
Quaderni, E52 Time-Span
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

		if collocazione == 'QUADERNI.1':
			time_span = URIRef(base_uri + 'time-span/' + specificazione)
			time_span_label = specificazione
		else:
			time_span = URIRef(base_uri + 'time-span/' + rec_time_span)
			time_span_label = rec_time_span




		# Add quads to base-graph


		d.add((time_span, RDF.type, URIRef('http://erlangen-crm.org/current/E52_Time-Span'), graph_base))
		d.add((time_span, RDFS.label, Literal(time_span_label , lang='it'), graph_base))
		d.add((time_span, RDFS.label, Literal(time_span_label , lang='en'), graph_base))
		d.add((time_span, ti.hasIntervalStartDate, Literal(time_span_label, datatype=XSD.date), graph_base))
		d.add((time_span, ti.hasIntervalEndDate, Literal(time_span_label, datatype=XSD.date), graph_base))

		# Authorship attribution date

		d.add((URIRef(base_uri + 'time-span/' + '1993-03-07'), RDF.type, URIRef('http://erlangen-crm.org/current/P52_Time-Span'), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1993-03-07'), ti.hasIntervalStartDate, Literal('1993-' + '03-07', datatype=XSD.date), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1993-03-07'), ti.hasIntervalEndDate, Literal('1993-' + '03-07', datatype=XSD.date), graph_base))
	 
		# Transfer of custody date
		
		d.add((URIRef(base_uri + 'time-span/' + '1985-1989'), RDF.type, URIRef('http://erlangen-crm.org/current/P52_Time-Span'), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1985-1989'), RDFS.label, Literal("Fine degli anni '80" , lang='it'), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1985-1989'), RDFS.label, Literal('Late 1980s' , lang='en'), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1985-1989'), ti.hasIntervalStartDate, Literal('1985-' + '01-01', datatype=XSD.date), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1985-1989'), ti.hasIntervalEndDate, Literal('1989-' + '12-31', datatype=XSD.date), graph_base))

		d.add((URIRef(base_uri + 'time-span/' + '1996-05'), RDF.type, URIRef('http://erlangen-crm.org/current/P52_Time-Span'), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1996-05'), ti.hasIntervalStartDate, Literal('1996-' + '05-18', datatype=XSD.date), graph_base))
		d.add((URIRef(base_uri + 'time-span/' + '1996-05'), ti.hasIntervalEndDate, Literal('1996-' + '05-31', datatype=XSD.date), graph_base))



# TriG
d.serialize(destination="../../dataset/trig/base-graph-E52_quad.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-E52_quad.nq", format='nquads')