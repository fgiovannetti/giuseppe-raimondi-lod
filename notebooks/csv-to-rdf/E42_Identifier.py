# coding: utf-8

# numero di inventario e collocazione

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

g = Graph()

g.bind("crm", crm)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)

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

		# URI Fondo Giuseppe Raimondi
		fonds = URIRef(base_uri_grf + 'record-set' + '/' + 'giuseppe-raimondi-fonds')
		fonds_label_en = 'Giuseppe Raimondi Fonds'
		fonds_label_it = 'Fondo Giuseppe Raimondi'

		# URI Subfondo Archivio in Fondo Giuseppe Raimondi (unico altro subfondo: Biblioteca)
		subfonds = URIRef(base_uri_grf + 'record-set' + '/' + 'giuseppe-raimondi-archive')
		subfonds_label_en = 'Giuseppe Raimondi Fonds, Archive'
		subfonds_label_it = 'Fondo Giuseppe Raimondi, Archivio'

		# URI Subfondo Biblioteca in Fondo Giuseppe Raimondi
		subfonds_b = URIRef(base_uri_grf + 'record-set' + '/' + 'giuseppe-raimondi-library')
		subfonds_b_label_en = 'Giuseppe Raimondi Fonds, Library'
		subfonds_b_label_it = 'Fondo Giuseppe Raimondi, Biblioteca'
		
		# Quaderni
		series = URIRef(base_uri_grf + 'record-set' + '/' + 'notebooks')
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

		record = URIRef(base_uri_grf + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Physical notebook URI
		rec_object = URIRef(record + 'object')

		g.add((URIRef(record + 'inventory-number'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(record + 'inventory-number'), RDFS.label, Literal('Inventario ' + inventario[0], lang='it')))
		g.add((URIRef(record + 'inventory-number'), RDFS.label, Literal('Inventory number ' + inventario[0], lang='en')))
		g.add((URIRef(record + 'inventory-number'), DCTERMS.identifier, URIRef(record + 'inventory-number')))
		g.add((URIRef(record + 'inventory-number'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/inventory-number')))

		g.add((URIRef(record + 'shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(record + 'shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza, lang='it')))
		g.add((URIRef(record + 'shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza, lang='en')))
		g.add((URIRef(record + 'shelfmark'), DCTERMS.identifier, URIRef(record + 'shelfmark')))
		g.add((URIRef(record + 'shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))
	
		# File

		g.add((URIRef(file + '/shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(file + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', ''), lang='it')))
		g.add((URIRef(file + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', ''), lang='en')))
		g.add((URIRef(file + '/shelfmark'), DCTERMS.identifier, URIRef(file + '/shelfmark')))
		g.add((URIRef(file + '/shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))

		# Subseries

		g.add((URIRef(subseries + '/shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(subseries + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' ' + collocazione, lang='it')))
		g.add((URIRef(subseries + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' ' + collocazione, lang='en')))
		g.add((URIRef(subseries + '/shelfmark'), DCTERMS.identifier, URIRef(subseries + '/shelfmark')))
		g.add((URIRef(subseries + '/shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))

		# Series

		g.add((URIRef(series + '/shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(series + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione + ' QUADERNI', lang='it')))
		g.add((URIRef(series + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione + ' QUADERNI', lang='en')))
		g.add((URIRef(series + '/shelfmark'), DCTERMS.identifier, URIRef(series + '/shelfmark')))
		g.add((URIRef(series + '/shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))

		# Subfonds

		g.add((URIRef(subfonds + '/shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(subfonds + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione, lang='it')))
		g.add((URIRef(subfonds + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione, lang='en')))
		g.add((URIRef(subfonds + '/shelfmark'), DCTERMS.identifier, URIRef(subfonds + '/shelfmark')))
		g.add((URIRef(subfonds + '/shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))

		g.add((URIRef(subfonds_b + '/shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(subfonds_b + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione, lang='it')))
		g.add((URIRef(subfonds_b + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione, lang='en')))
		g.add((URIRef(subfonds_b + '/shelfmark'), DCTERMS.identifier, URIRef(subfonds_b + '/shelfmark')))
		g.add((URIRef(subfonds_b + '/shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))

		# Fonds

		g.add((URIRef(fonds + '/shelfmark'), RDF.type, crm.E42_Identifier))
		g.add((URIRef(fonds + '/shelfmark'), RDFS.label, Literal('Collocazione ' + sezione, lang='it')))
		g.add((URIRef(fonds + '/shelfmark'), RDFS.label, Literal('Shelfmark ' + sezione, lang='en')))
		g.add((URIRef(fonds + '/shelfmark'), DCTERMS.identifier, URIRef(fonds + '/shelfmark')))
		g.add((URIRef(fonds + '/shelfmark'), crm.P2_has_type, URIRef(base_uri + 'identifier-type/shelfmark')))

# RDF/XML
g.serialize(destination="../output/rdf/fr-a-quaderni-E42.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-E42.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-E42.jsonld", format='json-ld')