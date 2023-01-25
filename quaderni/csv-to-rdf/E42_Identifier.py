# coding: utf-8

# numero di inventario e collocazione

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

ecrm = Namespace("http://erlangen-crm.org/current/")
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("ficlitdlo", ficlitdlo)
g.bind("owl", OWL)


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

		# URI Fondo Giuseppe Raimondi
		fonds = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-fonds')
		fonds_label_en = 'Giuseppe Raimondi Fonds'
		fonds_label_it = 'Fondo Giuseppe Raimondi'

		# URI Subfondo Archivio in Fondo Giuseppe Raimondi (unico altro subfondo: Biblioteca)
		subfonds = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-archive')
		subfonds_label_en = 'Giuseppe Raimondi Fonds, Archive'
		subfonds_label_it = 'Fondo Giuseppe Raimondi, Archivio'

		# URI Subfondo Biblioteca in Fondo Giuseppe Raimondi
		subfonds_b = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-library')
		subfonds_b_label_en = 'Giuseppe Raimondi Fonds, Library'
		subfonds_b_label_it = 'Fondo Giuseppe Raimondi, Biblioteca'
		
		# Quaderni
		series = URIRef(base_uri + 'record-set' + '/' + 'notebooks')
		series_label_en = 'Giuseppe Raimondi Fonds, Archive, Notebooks'
		series_label_it = 'Fondo Giuseppe Raimondi, Archivio, Quaderni'
		# TODO
		# Articoli
		# Album
		# Corrispondenza
		# Volumi

		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '-1')
			subseries_label_en = 'Giuseppe Raimondi Fonds, Archive, Notebooks, Manuscript Notebooks 1954–1976'
			subseries_label_it = 'Fondo Giuseppe Raimondi, Archivio, Quaderni, Quaderni manoscritti 1954–1976'
			subseries_note = 'Mat. document.-manoscr 3621049 [Quaderni manoscritti]. 1954-[1976] / Giuseppe Raimondi. - 1954-1976. - 308 quaderni ; 22 cm. Prima serie di quaderni di appunti, minute di racconti, recensioni, articoli. Serie ordinata dallo stesso Giuseppe Raimondi in carpette per anno.'

			file = URIRef(subseries + '-' + specificazione)
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Notebooks, Manuscript Notebooks 1954–1976, ' + specificazione
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Quaderni, Quaderni manoscritti 1954–1976, ' + specificazione

		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '-2')
			subseries_label_en = 'Giuseppe Raimondi Fonds, Archive, Notebooks, Manuscript Notebooks 1915–1981'
			subseries_label_it = 'Fondo Giuseppe Raimondi, Archivio, Quaderni, Quaderni manoscritti 1915–1981'
			subseries_note = 'Mat. document.-manoscr 3621048 [Quaderni manoscritti] / Giuseppe Raimondi. - 1915-1981. - 140 quaderni ; 22 cm. Seconda serie di quaderni contenenti appunti, minute di racconti, recensioni, articoli. La serie è stata riordinata cronologicamente in analogia alla prima, cosi organizzata dallo stesso Giuseppe Raimondi.'

		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '-3')

		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Physical notebook URI
		rec_object = URIRef(record + 'object')

		g.add((URIRef(record + 'inventory-number'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(record + 'inventory-number'), RDFS.label, Literal('Inventario ' + inventario[0], lang='it')))
		g.add((URIRef(record + 'inventory-number'), RDFS.label, Literal('Inventory number ' + inventario[0], lang='en')))
		g.add((URIRef(record + 'inventory-number'), ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/inventory-number')))

		g.add((URIRef(record + 'shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(record + 'shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza, lang='it')))
		g.add((URIRef(record + 'shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza, lang='en')))
		g.add((URIRef(record + 'shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))
	
		# File

		g.add((URIRef(file + '/shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(file + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', ''), lang='it')))
		g.add((URIRef(file + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', ''), lang='en')))
		g.add((URIRef(file + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))

		# Subseries

		g.add((URIRef(subseries + '/shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(subseries + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' ' + collocazione, lang='it')))
		g.add((URIRef(subseries + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' ' + collocazione, lang='en')))
		g.add((URIRef(subseries + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))

		# Series

		g.add((URIRef(series + '/shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(series + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' QUADERNI', lang='it')))
		g.add((URIRef(series + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' QUADERNI', lang='en')))
		g.add((URIRef(series + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))

		# Subfonds

		g.add((URIRef(subfonds + '/shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(subfonds + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione, lang='it')))
		g.add((URIRef(subfonds + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione, lang='en')))
		g.add((URIRef(subfonds + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))

		g.add((URIRef(subfonds_b + '/shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(subfonds_b + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione, lang='it')))
		g.add((URIRef(subfonds_b + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione, lang='en')))
		g.add((URIRef(subfonds_b + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))

		# Fonds

		g.add((URIRef(fonds + '/shelfmark'), RDF.type, ecrm.E42_Identifier))
		g.add((URIRef(fonds + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione, lang='it')))
		g.add((URIRef(fonds + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione, lang='en')))
		g.add((URIRef(fonds + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark))

# RDF/XML
g.serialize(destination="../output/rdf/quaderni-E42.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-E42.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-E42.jsonld", format='json-ld')