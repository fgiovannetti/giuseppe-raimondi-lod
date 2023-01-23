# coding: utf-8

# expression creation (creating both text and manifestation singleton)

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
g.bind("frbroo", frbroo)
g.bind("dcterms", DCTERMS)

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

		person = URIRef(base_uri + 'person/')

		g.add((URIRef(record + 'creation'), RDF.type, frbroo.F28_Expression_Creation))
		g.add((URIRef(record + 'creation'), RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '", creazione.' , lang='it')))
		g.add((URIRef(record + 'creation'), RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '", creation.' , lang='en')))
		if collocazione == 'QUADERNI.1':
			g.add((URIRef(record + 'creation'), URIRef('http://www.cidoc-crm.org/cidoc-crm/P4_has_time-span'), URIRef(base_uri + 'time-span/' + specificazione)))
		else:
			g.add((URIRef(record + 'creation'), URIRef('http://www.cidoc-crm.org/cidoc-crm/P4_has_time-span'), URIRef(base_uri + 'time-span/' + rec_time_span)))
		g.add((URIRef(record + 'creation'), crm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi')))
		g.add((URIRef(record + 'creation'), crm.P32_used_general_technique, URIRef(base_uri + 'technique-type/handwriting')))
		g.add((URIRef(record + 'creation'), frbroo.R17_created, URIRef(rec_expression)))
		g.add((URIRef(record + 'creation'), frbroo.R18_created, URIRef(rec_object)))
		g.add((URIRef(record + 'creation'), DCTERMS.identifier, URIRef(record + 'creation')))  

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-quaderni-F28.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-F28.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-F28.jsonld", format='json-ld')