# coding: utf-8

# person

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
ficlitdl = Namespace("https://w3id.org/ficlitdl/ontology/")
pro = Namespace("http://purl.org/spar/pro/")

g = Graph()

g.bind("crm", crm)
g.bind("dcterms", DCTERMS)
g.bind("ficlitdl", ficlitdl)
g.bind("owl", OWL)
g.bind("pro", pro)

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

		# physical notebook URI

		rec_object = URIRef(record + 'object')
 		
 		# expression URI

		rec_expression = URIRef(record + 'text')

		# person URI

		person = URIRef(base_uri + 'person/') 

		###########################
		#                         #
		# Giuseppe Raimondi       #
		#                         #
		###########################

		g.add((URIRef(person + 'giuseppe-raimondi'), RDF.type, crm.E21_Person))
		g.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi' , lang='it')))
		g.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi' , lang='en')))
		g.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('http://viaf.org/viaf/7457679')))
		g.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('https://www.worldcat.org/identities/lccn-n79021749')))
		g.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q3771293')))
		# g.add((URIRef(person + 'giuseppe-raimondi'), ficlitdl.P3_has_biographical_note, Literal('Giuseppe Raimondi (Bologna, 18 luglio 1898 – Bologna, 1985) è stato uno scrittore italiano.' , lang='it')))
		g.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef(rec_expression + '/author')))
		g.add((URIRef(person + 'giuseppe-raimondi'), DCTERMS.identifier, URIRef(person + 'giuseppe-raimondi')))


# persone menzionate nella descrizione isbd (persone menzionate nel testo todo)

my_dict = {}

with open('../input/ner_output_person.tsv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter='\t')
	for row in csv_reader:

		inventario = row["inventario"].lower().replace(' ', '')
		wd = row["wikidata"]
		wd_code = row["wikidata_code"]

		my_dict[inventario] = list()
		my_dict[inventario].append((wd, wd_code))

		record = URIRef(base_uri_grf + inventario + '/')

 		# expression URI
		rec_expression = URIRef(record + 'text')

		# person URI
		person = URIRef(base_uri + 'person/')

		for item in my_dict[inventario]:
			mentioned_person = URIRef(person + item[0].lower().replace(' ', '-').replace('.', '').replace(',', '').replace('è', 'e').replace('é', 'e').replace('à', 'a').replace('á', 'a').replace('ö', 'o').replace('ç', 'c'))
			g.add((mentioned_person, crm.P67i_is_referred_to_by, rec_expression))
			g.add((mentioned_person, RDF.type, crm.E21_Person))
			g.add((mentioned_person, RDFS.label, Literal(item[0], lang='it')))
			g.add((mentioned_person, RDFS.label, Literal(item[0], lang='en')))
			if 'Q' in item[1]:
				g.add((mentioned_person, OWL.sameAs, URIRef('https://www.wikidata.org/wiki/' + item[1])))
			elif 'viaf' in item[1]:
				g.add((mentioned_person, OWL.sameAs, URIRef(item[1])))
			g.add((mentioned_person, DCTERMS.identifier, mentioned_person))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-quaderni-E21.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-E21.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-E21.jsonld", format='json-ld')