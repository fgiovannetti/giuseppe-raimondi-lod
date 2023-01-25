# coding: utf-8

# dimensions

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

ecrm = Namespace("http://erlangen-crm.org/current/")
efrbroo = Namespace("http://erlangen-crm.org/efrbroo/")
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")
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
g.bind("ficlitdlo", ficlitdlo)
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

		series = URIRef(base_uri + 'record-set' + '/' + 'notebooks')

		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '-' + specificazione)
		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '-2')
		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '-3')

		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Physical notebook URI
		rec_object = URIRef(record + 'object')
 		
 		# Expression URI
		rec_expression = URIRef(record + 'text')

		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]

 		# Dimensions of physical object (height in cm, extent in number of pages and number of leaves)
		height = re.findall("; +(\d+) cm.", row["Descrizione isbd"])
		extent_leaves = re.findall("su (\d+) +c+.", row["Descrizione isbd"])
		extent_pages = re.findall("(\d+) +p.", row["Descrizione isbd"])

		# Dimensioni (h, pagine manoscritte, carte)
		if '449' in inventario[0]: 
			g.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + '10-19' + 'cm')))
			g.add((URIRef(base_uri + 'height/' + '10-19' + 'cm'), RDF.type, ecrm.E54_Dimension))
			g.add((URIRef(base_uri + 'height/' + '10-19' + 'cm'), RDFS.label, Literal('Altezza ' + 'min. 10- max. 19' + ' cm', lang='it')))
			g.add((URIRef(base_uri + 'height/' + '10-19' + 'cm'), RDFS.label, Literal('Height ' + 'min. 10- max. 19' + ' cm' , lang='en')))
			g.add((URIRef(base_uri + 'height/' + '10-19' + 'cm'), ecrm.P91_has_unit, URIRef(base_uri + 'measurement-unit-type/centimetre')))
			g.add((URIRef(base_uri + 'height/' + '10-19' + 'cm'), ecrm.P90_has_value, Literal('10-19')))
			g.add((URIRef(base_uri + 'height/' + '10-19' + 'cm'), ecrm.P2_has_type, ficlitdlo.height))
		
		else:
			g.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), RDF.type, ecrm.E54_Dimension))
			g.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), RDFS.label, Literal('Altezza ' + height[0] + ' cm', lang='it')))
			g.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), RDFS.label, Literal('Height ' + height[0] + ' cm' , lang='en')))
			g.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), ecrm.P91_has_unit, URIRef(base_uri + 'measurement-unit-type/centimetre')))
			g.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), ecrm.P90_has_value, Literal(height[0], datatype=XSD.decimal)))
			g.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), ecrm.P2_has_type, ficlitdlo.height))
			
			g.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), RDF.type, ecrm.E54_Dimension))
			g.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), RDFS.label, Literal(extent_pages[0] + ' pagine', lang='it')))
			g.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), RDFS.label, Literal(extent_pages[0] + ' pages', lang='en')))
			g.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), ecrm.P91_has_unit, URIRef(base_uri + 'measurement-unit-type/page')))
			g.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), ecrm.P90_has_value, Literal(extent_pages[0], datatype=XSD.decimal)))
			g.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), ecrm.P2_has_type, ficlitdlo.extent))

			g.add((URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), RDF.type, ecrm.E54_Dimension))
			g.add((URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), RDFS.label, Literal(extent_leaves[0] + ' carte', lang='it')))
			g.add((URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), RDFS.label, Literal(extent_leaves[0] + ' leaves', lang='en')))
			g.add((URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), ecrm.P91_has_unit, URIRef(base_uri + 'measurement-unit-type/leaf')))
			g.add((URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), ecrm.P90_has_value, Literal(extent_leaves[0], datatype=XSD.decimal)))
			g.add((URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), ecrm.P2_has_type, ficlitdlo.extent))

# RDF/XML
g.serialize(destination="../output/rdf/quaderni-E54.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-E54.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-E54.jsonld", format='json-ld')