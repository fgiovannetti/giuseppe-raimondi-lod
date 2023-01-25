# coding: utf-8

# title

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

ecrm = Namespace("http://erlangen-crm.org/current/")
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("dcterms", DCTERMS)
g.bind("ficlitdlo", ficlitdlo)

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
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

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

		g.add((URIRef(rec_expression + '/title'), RDF.type, ecrm.E35_Title))
		g.add((URIRef(rec_expression + '/title'), RDFS.label, Literal('Titolo, "' + rec_label[0].replace('*', '').replace('[', '').replace(']', '') + '"', lang='it')))
		g.add((URIRef(rec_expression + '/title'), RDFS.label, Literal('Title, "' + rec_label[0].replace('*', '').replace('[', '').replace(']', '') + '"', lang='en')))
		g.add((URIRef(rec_expression + '/title'), RDF.value, Literal(rec_label[0])))
		if rec_label[0].startswith('['):
			g.add((URIRef(rec_expression + '/title-attribution'), RDF.type, ecrm.E13_Attribute_Assignment))
			g.add((URIRef(rec_expression + '/title-attribution'), ecrm.P141_assigned, URIRef(rec_expression + '/title')))
			g.add((URIRef(rec_expression + '/title-attribution'), ecrm.P14_carried_out_by, URIRef('https://w3id.org/ficlitdl/org/ibc')))
			g.add((URIRef(rec_expression + '/title-attribution'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + '1993-03-07')))

		#############################
		#                           #
		# Other titles of main text #
	    # (HA PER ALTRO TITOLO)     #
		#                           #
		#############################

		# rec_altitles = re.findall('HA PER ALTRO TITOLO (\d+) (.+?)(?:;|\Z)', legami[0])
		# for altitle in rec_altitles:
		# 	title = re.sub('\*', '', altitle[1])
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDF.type, ecrm..E35_Title))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), DCTERMS.identifier, URIRef(record + 'title-' + str(altitle[0]))))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDFS.label, Literal('Titolo, "' + title + '"', lang='it')))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDFS.label, Literal('Title, "' + title + '"', lang='en')))
		# 	g.add((URIRef(record + 'title-' + str(altitle[0])), RDF.value, Literal(title)))
		# 	if rec_label.startswith('['):
		# 		g.add((URIRef(record + 'title-' + str(altitle[0])), ecrm..P2_has_type, URIRef(base_uri + 'title-type/attributed')))
		# 	else:
		# 		g.add((URIRef(record + 'title-' + str(altitle[0])), ecrm..P2_has_type, URIRef(base_uri + 'title-type/proper')))

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
				g.add((URIRef(rec_subexpression + '/title'), RDF.type, ecrm.E35_Title))
				g.add((URIRef(rec_subexpression + '/title'), RDFS.label, Literal('Titolo, "' + title.replace('[', '').replace(']', '') + '"', lang='it')))
				g.add((URIRef(rec_subexpression + '/title'), RDFS.label, Literal('Title, "' + title.replace('[', '').replace(']', '') + '"', lang='en')))
				g.add((URIRef(rec_subexpression + '/title'), RDF.value, Literal(title)))

				# if title.startswith('['):
				# 	g.add((URIRef(rec_subexpression + '/title'), ecrm.P2_has_type, URIRef(base_uri + 'title-type/attributed')))
				# else:
				# 	g.add((URIRef(rec_subexpression + '/title'), ecrm.P2_has_type, URIRef(base_uri + 'title-type/proper')))
				i += 1

# RDF/XML
g.serialize(destination="../output/rdf/quaderni-E35.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-E35.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-E35.jsonld", format='json-ld')