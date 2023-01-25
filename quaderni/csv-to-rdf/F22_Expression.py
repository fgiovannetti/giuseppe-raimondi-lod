# coding: utf-8

# notebooks as texts

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

ecrm = Namespace("http://erlangen-crm.org/current/")
efrbroo = Namespace("http://erlangen-crm.org/efrbroo/")
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("efrbroo", efrbroo)
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
		yyyy = re.findall("(.+?) *$", descrizione_isbd[0])
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Physical notebook URI
		rec_object = URIRef(record + 'object')
 		
 		# Expression URI
		rec_expression = URIRef(record + 'text')

		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]

		######################
		#                    #
		# Text description   #
		#                    #
		######################

		g.add((rec_expression, RDF.type, URIRef('http://erlangen-crm.org/efrbroo/F22_Self-Contained_Expression')))

		# Label (it, en)
		# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		g.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '"' , lang='it')))
		g.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + rec_label[0].replace('*', '') + '"' , lang='en')))
		
		# Language		
		g.add((rec_expression, ecrm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita')))

		# Expression creation
		g.add((rec_expression, efrbroo.R17i_was_created_by, URIRef(rec_expression + '/creation')))

		# Main title
		g.add((rec_expression, ecrm.P102_has_title, URIRef(rec_expression + '/title')))
		
		# Rights
		g.add((rec_expression, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		
		# Link to physical carrier
		g.add((rec_expression, ecrm.P128i_is_carried_by, rec_object))


		################################
		#                              #
		# Description of single texts  #
		#                              #
		################################

		# Subexpressions (as per descrizione_isbd, separated by ';')
		# The relation 'CONTIENE ANCHE' features this same information
		if ' ; ' in rec_label[0]:
			rec_label = rec_label[0].split(' ; ')
			i = 1
			for title in rec_label:
				
				# URI Subexpression
				rec_subexpression = URIRef(rec_expression + '/' + str(i))

				g.add((rec_subexpression, RDF.type, URIRef('http://erlangen-crm.org/efrbroo/F22_Self-Contained_Expression')))

				# Link to overall expression (whole text in notebook)
				g.add((rec_expression, ecrm.P165_incorporates, rec_subexpression))
				
				# Label (it, en)
				# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
				g.add((rec_subexpression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + title + '"' , lang='it')))
				g.add((rec_subexpression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + title + '"' , lang='en')))

				# # Narrative form type (if available)
				if 'racconto' in title:
					g.add((rec_subexpression, ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/short-story')))
				elif 'appunti' in title:
					g.add((rec_subexpression, ecrm.P2_has_type, ficlitdlo.notes))
				elif 'articolo' in title:
					g.add((rec_subexpression, ecrm.P2_has_type, ficlitdlo.article))			
				
				# Language		
				g.add((rec_subexpression, ecrm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita')))		
				
				# Main title
				subrec = URIRef(record + str(i))
				g.add((rec_subexpression, ecrm.P102_has_title, URIRef(rec_subexpression + '/title')))

				# Link to physical carrier
				g.add((rec_subexpression, ecrm.P128i_is_carried_by, rec_object))

				# Link to overall expression
				g.add((rec_subexpression, ecrm.P165i_is_incorporated_in, rec_expression))
				g.add((rec_subexpression, ecrm.P165_incorporates, rec_subexpression))
				
				# Subexpression creation
				g.add((rec_expression, efrbroo.R17i_was_created_by, URIRef(rec_subexpression + '/creation')))
				g.add((URIRef(rec_subexpression + '/creation'), RDF.type, efrbroo.F28_Expression_Creation))
				g.add((URIRef(rec_subexpression + '/creation'), ecrm.P14_carried_out_by, URIRef('https://w3id.org/ficlitdl/person/giuseppe-raimondi')))
				g.add((URIRef(rec_subexpression + '/creation'), ecrm.P32_used_general_technique, ficlitdlo.handwriting))
				g.add((URIRef(rec_subexpression + '/creation'), efrbroo.R17_created, URIRef(rec_subexpression)))


				i += 1

# Persone menzionate nella descrizione isbd (persone menzionate nel testo)

my_dict = {}

with open('../input/ner_output_person.tsv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter='\t')
	for row in csv_reader:

		inventario = row["inventario"].lower().replace(' ', '')
		wd = row["wikidata"]
		wd_code = row["wikidata_code"]

		my_dict[inventario] = list()
		my_dict[inventario].append((wd, wd_code))

		record = URIRef(base_uri + inventario + '/')

 		# Expression URI
		rec_expression = URIRef(record + 'text')

		# Person URI
		person = URIRef('https://w3id.org/ficlitdl/' + 'person/')

		for item in my_dict[inventario]:
			mentioned_person = URIRef(person + item[0].lower().replace(' ', '-').replace('.', '').replace(',', '').replace('è', 'e').replace('é', 'e').replace('à', 'a').replace('á', 'a').replace('ö', 'o').replace('ç', 'c'))
			g.add((rec_expression, ecrm.P67_refers_to, mentioned_person))

# RDF/XML
g.serialize(destination="../output/rdf/quaderni-F22.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-F22.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-F22.jsonld", format='json-ld')