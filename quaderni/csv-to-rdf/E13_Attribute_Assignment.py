# coding: utf-8

# authorship attribution

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

		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# physical notebook URI

		rec_object = URIRef(record + 'object')
 		
 		# expression URI

		rec_expression = URIRef(record + 'text')
		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]

		# authorship attribution

		g.add((URIRef(record + 'author-attribution'), RDF.type, ecrm.E13_Attribute_Assignment))
		g.add((URIRef(record + 'author-attribution'), ecrm.P141_assigned, URIRef(rec_expression + '/author')))
		g.add((URIRef(record + 'author-attribution'), ecrm.P140_assigned_attribute_to, URIRef('https://w3id.org/ficlitdl/' + 'person/giuseppe-raimondi')))
		g.add((URIRef(record + 'author-attribution'), ecrm.P14_carried_out_by, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(record + 'author-attribution'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + '1993-03-07')))
		g.add((URIRef(record + 'author-attribution'), RDFS.label, Literal('Attribuzione della paternità del testo manoscritto ' + '"' + rec_label[0].replace('*', '') + '" a Giuseppe Raimondi', lang='it')))
		g.add((URIRef(record + 'author-attribution'), RDFS.label, Literal('Authorship attribution of the manuscript text ' + '"' + rec_label[0].replace('*', '') + '" to Giuseppe Raimondi', lang='en')))
		
# RDF/XML
g.serialize(destination="../output/rdf/quaderni-E13.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-E13.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-E13.jsonld", format='json-ld')