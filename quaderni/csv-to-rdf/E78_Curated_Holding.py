# coding: utf-8

# record sets as curated holdings

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

ecrm = Namespace('http://erlangen-crm.org/current/')
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")

g = Graph()

g.bind('ecrm', ecrm)
g.bind('dcterms', DCTERMS)
g.bind('ficlitdlo', ficlitdlo)
g.bind('seq', seq)

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

		# File description (Solo in Quaderni 1, Fascicoli per anno)
		# Physical (E78)
		g.add((URIRef(file + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding')))
		g.add((URIRef(file + '/object'), RDFS.label, Literal(file_label_it, lang='it')))
		g.add((URIRef(file + '/object'), RDFS.label, Literal(file_label_en, lang='en')))
		g.add((URIRef(file + '/object'), ecrm.P1_is_identified_by, URIRef(file + '/shelfmark')))		
		g.add((URIRef(file + '/object'), ecrm.P2_has_type, ficlitdlo.file))
		g.add((URIRef(file + '/object'), ecrm.P46i_forms_part_of, URIRef(subseries + '/object'))) # Quaderni manoscritti 1954-1976
		g.add((URIRef(file + '/object'), ecrm.P46_is_composed_of, rec_object))
		g.add((URIRef(file + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo')))
		g.add((URIRef(file + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(file + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi')))
		g.add((URIRef(file + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		
		# # Conceptual (E89)
		# g.add((file, RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding')))
		# g.add((file, RDFS.label, Literal(file_label_it, lang='it')))
		# g.add((file, RDFS.label, Literal(file_label_en, lang='en')))
		# g.add((file, ecrm.P1_is_identified_by, URIRef(file + '/shelfmark')))		
		# g.add((file, ecrm.P2_has_type, ficlitdlo.file))
		# g.add((file, ecrm:P102_has_title, URIRef(file + '/title')))
		# g.add((file, ficlitdlo.formsConceptuallyPartOf, URIRef(subseries))) # [Quaderni manoscritti] 1954-[1976]
		# g.add((file, ficlitdlo.isConceptuallyComposedOf, rec_object))	
		
		# How to cite
		g.add((URIRef(file + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + '.')))

		# Subseries description (Quaderni 1-2-3)

		g.add((URIRef(subseries + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding')))
		g.add((URIRef(subseries + '/object'), RDFS.label, Literal(subseries_label_it, lang='it')))
		g.add((URIRef(subseries + '/object'), RDFS.label, Literal(subseries_label_en, lang='en')))
		g.add((URIRef(subseries + '/object'), ecrm.P1_is_identified_by, URIRef(subseries + '/shelfmark')))		
		g.add((URIRef(subseries + '/object'), ecrm.P2_has_type, ficlitdlo.series))
		g.add((URIRef(subseries + '/object'), ecrm.P3_has_note, Literal(subseries_note , lang='it')))
		g.add((URIRef(subseries + '/object'), ecrm.P46i_forms_part_of, URIRef(series + '/object'))) # Quaderni
		if collocazione == 'QUADERNI.1':
			g.add((URIRef(subseries + '/object'), ecrm.P46_is_composed_of, URIRef(file + '/object')))
		g.add((URIRef(subseries + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo')))
		g.add((URIRef(subseries + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(subseries + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi')))
		g.add((URIRef(subseries + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		g.add((URIRef(subseries + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' ' + collocazione + '.')))

		# Series description 

		g.add((URIRef(series + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding')))
		g.add((URIRef(series + '/object'), RDFS.label, Literal(series_label_it, lang='it')))
		g.add((URIRef(series + '/object'), RDFS.label, Literal(series_label_en, lang='en')))
		g.add((URIRef(series + '/object'), ecrm.P1_is_identified_by, URIRef(series + '/shelfmark')))		
		g.add((URIRef(series + '/object'), ecrm.P2_has_type, ficlitdlo.series))
		g.add((URIRef(series + '/object'), ecrm.P46i_forms_part_of, URIRef(subfonds + '/object'))) # Archivio (FR.A)
		g.add((URIRef(series + '/object'), ecrm.P46_is_composed_of, URIRef(subseries + '/object')))
		g.add((URIRef(series + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo')))
		g.add((URIRef(series + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(series + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi')))
		g.add((URIRef(series + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		g.add((URIRef(series + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' QUADERNI.')))

		# Subfonds description
	
		# Archive

		g.add((URIRef(subfonds + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding')))
		g.add((URIRef(subfonds + '/object'), RDFS.label, Literal(subfonds_label_it, lang='it')))
		g.add((URIRef(subfonds + '/object'), RDFS.label, Literal(subfonds_label_en, lang='en')))
		g.add((URIRef(subfonds + '/object'), ecrm.P1_is_identified_by, URIRef(subfonds + '/shelfmark')))		
		g.add((URIRef(subfonds + '/object'), ecrm.P2_has_type, ficlitdlo.fonds))
		g.add((URIRef(subfonds + '/object'), ecrm.P46i_forms_part_of, URIRef(fonds + '/object'))) # Fondo Giuseppe Raimondi (Archivio e Biblioteca)
		g.add((URIRef(subfonds + '/object'), ecrm.P46_is_composed_of, URIRef(series + '/object')))
		g.add((URIRef(subfonds + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo')))
		g.add((URIRef(subfonds + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(subfonds + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi')))
		g.add((URIRef(subfonds + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		g.add((URIRef(subfonds + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Archivio. Biblioteca Ezio Raimondi, Università di Bologna.')))

		# Library

		g.add((URIRef(subfonds_b + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object')))
		g.add((URIRef(subfonds_b + '/object'), RDFS.label, Literal(subfonds_b_label_it, lang='it')))
		g.add((URIRef(subfonds_b + '/object'), RDFS.label, Literal(subfonds_b_label_en, lang='en')))
		g.add((URIRef(subfonds_b + '/object'), ecrm.P1_is_identified_by, URIRef(subfonds_b + '/shelfmark')))		
		g.add((URIRef(subfonds_b + '/object'), ecrm.P2_has_type, ficlitdlo.fonds))
		g.add((URIRef(subfonds_b + '/object'), ecrm.P46i_forms_part_of, URIRef(fonds + '/object'))) # Fondo Giuseppe Raimondi (Archivio e Biblioteca)
		g.add((URIRef(subfonds_b + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo')))
		g.add((URIRef(subfonds_b + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(subfonds_b + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi')))
		g.add((URIRef(subfonds_b + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		g.add((URIRef(subfonds_b + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca. Biblioteca Ezio Raimondi, Università di Bologna.')))

		# Fonds description
	
		g.add((URIRef(fonds + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding')))
		g.add((URIRef(fonds + '/object'), RDFS.label, Literal(fonds_label_it, lang='it')))
		g.add((URIRef(fonds + '/object'), RDFS.label, Literal(fonds_label_en, lang='en')))
		g.add((URIRef(fonds + '/object'), ecrm.P1_is_identified_by, URIRef(fonds + '/shelfmark')))		
		g.add((URIRef(fonds + '/object'), ecrm.P2_has_type, ficlitdlo.fonds))
		g.add((URIRef(fonds + '/object'), ecrm.P46_is_composed_of, URIRef(subfonds + '/object')))
		g.add((URIRef(fonds + '/object'), ecrm.P46_is_composed_of, URIRef(subfonds_b + '/object')))
		g.add((URIRef(fonds + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo')))
		g.add((URIRef(fonds + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc')))
		g.add((URIRef(fonds + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi')))
		g.add((URIRef(fonds + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved')))
		g.add((URIRef(fonds + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi. Biblioteca Ezio Raimondi, Università di Bologna.')))

# RDF/XML
g.serialize(destination="../output/rdf/quaderni-E78.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/quaderni-E78.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/quaderni-E78.jsonld", format='json-ld')