# coding: utf-8

# notebooks as texts

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

ecrm = Namespace("http://erlangen-crm.org/current/")
efrbroo = Namespace("http://erlangen-crm.org/efrbroo/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("efrbroo", efrbroo)



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

		g.add((rec_expression, RDF.type, efrbroo.F2_Expression))

		# Label (it, en)
		# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		g.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '"' , lang='it')))
		g.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + rec_label[0].replace('*', '') + '"' , lang='en')))
		
		# Language		
		g.add((rec_expression, ecrm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita')))

		# Expression creation
		g.add((rec_expression, efrbroo.R17i_was_created_by, URIRef(rec_expression + 'creation')))
		
		# Main title
		g.add((rec_expression, ecrm.P102_has_title, URIRef(rec_expression + '/title')))
		
		# Rights
		g.add((rec_expression, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		
		# Link to physical carrier
		g.add((rec_expression, ecrm.P128i_is_carried_by, rec_object))

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
g.serialize(destination="../output/rdf/quaderni-F2.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-F2.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-F2.jsonld", format='json-ld')