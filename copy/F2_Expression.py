# coding: utf-8

# notebooks as texts


import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")

g = Graph()

g.bind("crm", crm)
g.bind("frbroo", frbroo)
g.bind("dcterms", DCTERMS)


base_uri = 'https://w3id.org/ficlitdl/'
base_uri_grf = base_uri + 'giuseppe-raimondi-fonds/a/'

# persone menzionate in descrizione isbd
my_dict = {}

with open('../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:

		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione']
		sequenza = row['Sequenza']
		#TODO
		#data_inv = row['Data inv.']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd']
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		my_dict[inventario[0]] = list()
		my_dict[inventario[0]].append(specificazione)


		series = URIRef(base_uri_grf + 'notebooks/')
		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '1/')
			file = URIRef(series + specificazione)
			record = URIRef(file + '/' + inventario[0].lower().replace(' ', '') + '/')
		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '2')
			record = URIRef(subseries + '/' + inventario[0].lower().replace(' ', '') + '/')
		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '3')
			record = URIRef(subseries + '/' + inventario[0].lower().replace(' ', '') + '/')

		# Physical notebook URI
		rec_object = URIRef(record + 'object')
 		
 		# Expression URI
		rec_expression = URIRef(record + 'text')

		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]




		# # URI File
		# yyyy = specificazione.replace('[', '').replace(']', '').replace('?', '')
		# file = URIRef(base_uri_grf + 'notebooks/' + '1/' + yyyy)
		
		# # URI Record
		# record = URIRef(file + '/' + inventario[0].lower().replace(' ', '') + '/')
		
		# # URI Record / Physical object
		# rec_object = URIRef(record + 'object')
		# rec_label = re.findall('^(.+?) \/ \[?Giuseppe Raimondi\]?\. \-', descrizione_isbd)[0].replace('*', '')
		
		# # URI Record / Text
		# rec_expression = URIRef(record + 'text')

		


		######################
		#                    #
		# Text description   #
		#                    #
		######################

		g.add((rec_expression, RDF.type, frbroo.F2_Expression))

		# Permalink (for Omeka S)
		g.add((rec_expression, DCTERMS.identifier, rec_expression))

		# Label (it, en)
		# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		g.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '"' , lang='it')))
		g.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + rec_label[0].replace('*', '') + '"' , lang='en')))
		
		# Language		
		g.add((rec_expression, crm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita')))

		# Expression creation
		g.add((rec_expression, frbroo.R17i_was_created_by, URIRef(record + 'creation')))
		
		# Main title
		g.add((rec_expression, crm.P102_has_title, URIRef(record + 'title')))

		# # Alternate titles (= 'HA PER ALTRO TITOLO', N.B. Questa relazione sarebbe da ricondurre al singolo testo, ma ciò non è presente nei dati allo stato attuale)
		# rec_altitles = re.findall('HA PER ALTRO TITOLO (\d+)', legami[0])
		# for altitle in rec_altitles:
			#g.add((rec_expression, crm.P102_has_title, URIRef(record + 'title-' + str(altitle))))
		
		# Rights
		g.add((rec_expression, crm.P104_is_subject_to, URIRef(base_uri + 'right/' + 'all-rights-reserved')))
		
		# Link to physical carrier
		g.add((rec_expression, crm.P128i_is_carried_by, rec_object))

		################################
		#                              #
		# Description of single texts  #
		#                              #
		################################

		# # Subexpressions (as per descrizione_isbd, separated by ';')
		# # The relation 'CONTIENE ANCHE' features this same information
		# if ' ; ' in rec_label:
		# 	rec_label = rec_label.split(' ; ')
		# 	i = 1
		# 	for title in rec_label:
				
		# 		# URI Subexpression
		# 		rec_subexpression = URIRef(rec_expression + '/' + str(i))

		# 		g.add((rec_subexpression, RDF.type, frbroo.F2_Expression))

		# 		# Permalink (for Omeka S)
		# 		g.add((rec_subexpression, DCTERMS.identifier, rec_subexpression))

		# 		# Link to overall expression (whole text in notebook)
		# 		g.add((rec_expression, crm.P165_incorporates, rec_subexpression))
				
		# 		# Label (it, en)
		# 		# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		# 		g.add((rec_subexpression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + title + '"' , lang='it')))
		# 		g.add((rec_subexpression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + title + '"' , lang='en')))

		# 		# # Narrative form type (if available)
		# 		# if 'racconto' in title:
		# 		# 	g.add((rec_subexpression, crm.P2_has_type, URIRef(base_uri + 'narrative-form-type/short-story')))
		# 		# elif 'appunti' in title:
		# 		# 	g.add((rec_subexpression, crm.P2_has_type, URIRef(base_uri + 'narrative-form-type/note')))
		# 		# elif 'articolo' in title:
		# 		# 	g.add((rec_subexpression, crm.P2_has_type, URIRef(base_uri + 'narrative-form-type/article')))			
				
		# 		# Language		
		# 		g.add((rec_subexpression, crm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita')))		
				
		# 		# Main title
		# 		subrec = URIRef(record + str(i))
		# 		g.add((rec_subexpression, crm.P102_has_title, URIRef(subrec + '/title')))

		# 		# Link to physical carrier
		# 		# g.add((rec_subexpression, crm.P128i_is_carried_by, rec_object))

		# 		# Link to overall expression
		# 		g.add((rec_subexpression, crm.P165i_is_incorporated_in, rec_expression))
				
		# 		# How to cite
		# 		g.add((rec_subexpression, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + yyyy + '. Testo manoscritto, ' + '"' + title + '"' + '. Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza + '.')))

		# 		i += 1


# Persone menzionate nella descrizione isbd QUADERNI.1 (persone menzionate nel testo, persone menzionate in QUADERNI.2-3 todo)

with open('../input/ner_output_person.tsv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter='\t')
	for row in csv_reader:

		inventario =  row["inventario"]
		wd = row["wikidata"]
		wd_code = row["wikidata_code"]

		my_dict[inventario].append((wd, wd_code))
		#my_dict[inventario].append(wd_code)

		#specificazione = my_dict[inventario][0]
		specificazione = my_dict[inventario]


		series = URIRef(base_uri_grf + 'notebooks/')
		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '1/')
			file = URIRef(series + specificazione)
			record = URIRef(file + '/' + inventario[0].lower().replace(' ', '') + '/')
		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '2')
			record = URIRef(subseries + '/' + inventario[0].lower().replace(' ', '') + '/')
		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '3')
			record = URIRef(subseries + '/' + inventario[0].lower().replace(' ', '') + '/')
		
 		# Expression URI
		rec_expression = URIRef(record + 'text')

		# Person URI
		person = URIRef(base_uri + 'person/')



		# # URI File
		# specificazione = my_dict[inventario][0]
		# yyyy = specificazione.replace('[', '').replace(']', '').replace('?', '')
		# file = URIRef(base_uri_grf + 'notebooks/' + '1/' + yyyy)
		
		# # URI Record
		# record = URIRef(file + '/' + inventario.lower().replace(' ', '') + '/')
		
		# # URI Record / Physical object
		# rec_object = URIRef(record + 'object')
		
		# # URI Record / Text
		# rec_expression = URIRef(record + 'text')

		# # URI Person
		# person = URIRef(base_uri + 'person/') 


		for item in my_dict[inventario][1:]:
			mentioned_person = URIRef(person + item[0].lower().replace(' ', '-').replace('.', '').replace(',', '').replace('è', 'e').replace('é', 'e').replace('à', 'a').replace('á', 'a').replace('ö', 'o').replace('ç', 'c'))
			g.add((rec_expression, crm.P67_refers_to, mentioned_person))

			print(mentioned_person)

print(my_dict)

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-quaderni-F2.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-F2.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-F2.jsonld", format='json-ld')
