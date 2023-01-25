# coding: utf-8

# person

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

ecrm = Namespace("http://erlangen-ecrm.org/current/")
ficlitdl = Namespace("https://w3id.org/ficlitdl/ontology/")
pro = Namespace("http://purl.org/spar/pro/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("dcterms", DCTERMS)
g.bind("ficlitdl", ficlitdl)
g.bind("owl", OWL)
g.bind("pro", pro)


base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'


with open('../../quaderni/input/quaderni.csv', mode='r') as csv_file:
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

		# person URI

		person = URIRef('https://w3id.org/ficlitdl/' + 'person/') 

		###########################
		#                         #
		# Giuseppe Raimondi       #
		#                         #
		###########################

		g.add((URIRef(person + 'giuseppe-raimondi'), RDF.type, ecrm.E21_Person))
		g.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi' , lang='it')))
		g.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi' , lang='en')))
		g.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('http://viaf.org/viaf/7457679')))
		g.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('https://www.worldcat.org/identities/lccn-n79021749')))
		g.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q3771293')))
		g.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef(rec_expression + '/author')))


# persone menzionate nella descrizione isbd (persone menzionate nel testo TODO con trascrizioni)

my_dict = {}

with open('../../quaderni/input/ner_output_person.tsv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter='\t')
	for row in csv_reader:

		inventario = row["inventario"].lower().replace(' ', '')
		wd = row["wikidata"]
		wd_code = row["wikidata_code"]

		my_dict[inventario] = list()
		my_dict[inventario].append((wd, wd_code))

		record = URIRef(base_uri + inventario + '/')

 		# expression URI
		rec_expression = URIRef(record + 'text')

		# person URI
		person = URIRef('https://w3id.org/ficlitdl/' + 'person/')

		for item in my_dict[inventario]:
			mentioned_person = URIRef(person + item[0].lower().replace(' ', '-').replace('.', '').replace(',', '').replace('è', 'e').replace('é', 'e').replace('à', 'a').replace('á', 'a').replace('ö', 'o').replace('ç', 'c'))
			g.add((mentioned_person, ecrm.P67i_is_referred_to_by, rec_expression))
			g.add((mentioned_person, RDF.type, ecrm.E21_Person))
			g.add((mentioned_person, RDFS.label, Literal(item[0], lang='it')))
			g.add((mentioned_person, RDFS.label, Literal(item[0], lang='en')))
			if 'Q' in item[1]:
				g.add((mentioned_person, OWL.sameAs, URIRef('https://www.wikidata.org/wiki/' + item[1])))
			elif 'viaf' in item[1]:
				g.add((mentioned_person, OWL.sameAs, URIRef(item[1])))

# RDF/XML
g.serialize(destination="../output/rdf/E21.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/E21.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/E21.jsonld", format='json-ld')