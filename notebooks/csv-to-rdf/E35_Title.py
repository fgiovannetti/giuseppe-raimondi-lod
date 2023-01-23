# coding: utf-8

# title

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

g = Graph()

g.bind("crm", crm)
g.bind("dcterms", DCTERMS)

# base_uri = 'https://w3id.org/ficlitdl/'
# base_uri_grf = base_uri + 'giuseppe-raimondi-fonds/a/'

base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'
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

		# physical notebook URI
		rec_object = URIRef(record + 'object')
 		
 		# expression URI
		rec_expression = URIRef(record + 'text')

		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]

		###########################
		#                         #
		# Title of main text      #
		#                         #
		###########################

		g.add((URIRef(rec_expression + 'title'), RDF.type, crm.E35_Title))
		g.add((URIRef(rec_expression + 'title'), DCTERMS.identifier, URIRef(rec_expression + 'title')))
		g.add((URIRef(rec_expression + 'title'), RDFS.label, Literal('Titolo, "' + rec_label[0].replace('*', '') + '"', lang='it')))
		g.add((URIRef(rec_expression + 'title'), RDFS.label, Literal('Title, "' + rec_label[0].replace('*', '') + '"', lang='en')))
		g.add((URIRef(rec_expression + 'title'), RDF.value, Literal(rec_label[0])))
		if rec_label[0].startswith('['):
			g.add((URIRef(rec_expression + 'title'), crm.P2_has_type, URIRef(base_uri + 'title-type/attributed')))
		else:
			g.add((URIRef(rec_expression + 'title'), crm.P2_has_type, URIRef(base_uri + 'title-type/proper')))

		#############################
		#                           #
		# Other titles of main text #
	    # (HA PER ALTRO TITOLO)     #
		#                           #
		#############################

		# rec_altitles = re.findall('HA PER ALTRO TITOLO (\d+) (.+?)(?:;|\Z)', legami[0])
		# for altitle in rec_altitles:
		# 	title = re.sub('\*', '', altitle[1])
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDF.type, crm.E35_Title))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), DCTERMS.identifier, URIRef(record + 'title-' + str(altitle[0]))))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDFS.label, Literal('Titolo, "' + title + '"', lang='it')))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDFS.label, Literal('Title, "' + title + '"', lang='en')))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDF.value, Literal(title)))
		# 	if rec_label.startswith('['):
		# 		g.add((URIRef(record + 'title-' + str(altitle[0])), crm.P2_has_type, URIRef(base_uri + 'title-type/attributed')))
		# 	else:
		# 		g.add((URIRef(record + 'title-' + str(altitle[0])), crm.P2_has_type, URIRef(base_uri + 'title-type/proper')))

		############################
		#                          #
		# Titles of sub-texts      #
		#                          #
		############################

		# if ' ; ' in rec_label:
		# 	rec_label = rec_label.split(' ; ')
		# 	i = 1
		# 	for title in rec_label:
		# 		subrec = URIRef(record + str(i))
		# 		g.add((URIRef(subrec + '/title'), RDF.type, crm.E35_Title))
		# 		g.add((URIRef(subrec + '/title'), DCTERMS.identifier, URIRef(subrec + '/title')))
		# 		g.add((URIRef(subrec + '/title'), RDFS.label, Literal('Titolo, "' + title + '"', lang='it')))
		# 		g.add((URIRef(subrec + '/title'), RDFS.label, Literal('Title, "' + title + '"', lang='en')))
		# 		g.add((URIRef(subrec + '/title'), RDF.value, Literal(title)))

		# 		if title.startswith('['):
		# 			g.add((URIRef(subrec + '/title'), crm.P2_has_type, URIRef(base_uri + 'title-type/attributed')))
		# 		else:
		# 			g.add((URIRef(subrec + '/title'), crm.P2_has_type, URIRef(base_uri + 'title-type/proper')))
		# 		i += 1

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-quaderni-E35.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-E35.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-E35.jsonld", format='json-ld')