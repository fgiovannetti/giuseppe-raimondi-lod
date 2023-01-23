# coding: utf-8

# data (time-span)

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
pro = Namespace("http://purl.org/spar/pro/")
proles = Namespace("http://www.essepuntato.it/2013/10/politicalroles/")
prov = Namespace("http://www.w3.org/ns/prov#")
rico = Namespace("https://www.ica.org/standards/RiC/ontology#")
seq = Namespace("http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#")
ti = Namespace("http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")

g = Graph()

g.bind("crm", crm)
g.bind("frbroo", frbroo) # aka lrmoo - update namespace
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

# base_uri = 'https://w3id.org/ficlitdl/' # da eliminare
# base_uri_grf = base_uri + 'giuseppe-raimondi-fonds/a/'
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/' # da eliminare
base_uri_grf = base_uri

with open('../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione']
		sequenza = row['Sequenza']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd']
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		record = URIRef(base_uri_grf + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Physical notebook URI
		rec_object = URIRef(record + 'object')
 		
 		# Expression URI
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

		g.add((time_span, RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/P52_Time-Span')))
		g.add((time_span, RDFS.label, Literal(time_span_label , lang='it')))
		g.add((time_span, RDFS.label, Literal(time_span_label , lang='en')))
		g.add((time_span, ti.hasIntervalStartDate, Literal(time_span_label + '-' + '01-01T00:00:00+01:00', datatype=XSD.dateTime)))
		g.add((time_span, ti.hasIntervalEndDate, Literal(time_span_label + '-' + '12-31T23:59:59+01:00', datatype=XSD.dateTime)))
		g.add((time_span, DCTERMS.identifier, time_span))

		# Authorship attribution date

		g.add((URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10'), RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/P52_Time-Span')))
		g.add((URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10'), RDFS.label, Literal('8-10 marzo 1993' , lang='it')))
		g.add((URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10'), RDFS.label, Literal('8th-10th March 1993' , lang='en')))
		g.add((URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10'), ti.hasIntervalStartDate, Literal('1993-' + '03-08T00:00:00+01:00', datatype=XSD.dateTime)))
		g.add((URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10'), ti.hasIntervalEndDate, Literal('1993-' + '03-10T23:59:59+01:00', datatype=XSD.dateTime)))
		g.add((URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10'), DCTERMS.identifier, URIRef(base_uri + 'time-span/' + '1993-03-08_1993-03-10')))
	 
		# Transfer of custody date
		
		g.add((URIRef(base_uri + 'time-span/' + '1985-1989'), RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/P52_Time-Span')))
		g.add((URIRef(base_uri + 'time-span/' + '1985-1989'), RDFS.label, Literal("Fine degli anni '80" , lang='it')))
		g.add((URIRef(base_uri + 'time-span/' + '1985-1989'), RDFS.label, Literal('Late 1980s' , lang='en')))
		g.add((URIRef(base_uri + 'time-span/' + '1985-1989'), ti.hasIntervalStartDate, Literal('1985-' + '01-01T00:00:00+01:00', datatype=XSD.dateTime)))
		g.add((URIRef(base_uri + 'time-span/' + '1985-1989'), ti.hasIntervalEndDate, Literal('1989-' + '01-01T23:59:59+01:00', datatype=XSD.dateTime)))
		g.add((URIRef(base_uri + 'time-span/' + '1985-1989'), DCTERMS.identifier, URIRef(base_uri + 'time-span/' + '1985-1989')))

		g.add((URIRef(base_uri + 'time-span/' + '1996-05'), RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/P52_Time-Span')))
		g.add((URIRef(base_uri + 'time-span/' + '1996-05'), RDFS.label, Literal('maggio 1996' , lang='it')))
		g.add((URIRef(base_uri + 'time-span/' + '1996-05'), RDFS.label, Literal('May 1996' , lang='en')))
		g.add((URIRef(base_uri + 'time-span/' + '1996-05'), ti.hasIntervalStartDate, Literal('1996-' + '05-018T00:00:00+01:00', datatype=XSD.dateTime)))
		g.add((URIRef(base_uri + 'time-span/' + '1996-05'), ti.hasIntervalEndDate, Literal('1996-' + '05-31T23:59:59+01:00', datatype=XSD.dateTime)))
		g.add((URIRef(base_uri + 'time-span/' + '1996-05'), DCTERMS.identifier, URIRef(base_uri + 'time-span/' + '1996-05')))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-quaderni-E52.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-E52.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-E52.jsonld", format='json-ld')