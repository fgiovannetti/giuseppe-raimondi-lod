# coding: utf-8

""" Base graph :
Quaderni, E78 Curated Holding
"""

from rdflib import Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, PROV
import csv
import re

# Create an empty Dataset
d = Dataset()

efrbroo = Namespace('http://erlangen-crm.org/efrbroo/')
ecrm = Namespace('http://erlangen-crm.org/current/')
ficlitdl = Namespace('https://w3id.org/ficlitdl/')
ficlitdlo = Namespace('https://w3id.org/ficlitdl/ontology/')
np = Namespace('http://www.nanopub.org/nschema#')
prism = Namespace('http://prismstandard.org/namespaces/basic/2.0/')
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')
ti = Namespace("http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#")
tvc = Namespace("http://www.essepuntato.it/2012/04/tvc/")



# Add a namespace prefix to it, just like for Graph
d.bind('dcterms', DCTERMS)
d.bind('ecrm', ecrm)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base/'))
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('seq', seq)
d.bind('ti', ti)
d.bind('tvc', tvc)


# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub-base/')

# Declare a Graph URI to be used to identify a Graph
graph_base = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_base, to the Dataset
d.graph(identifier=graph_base)

with open('../../input/quaderni.csv', mode='r') as csv_file:
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





		# Add quads to base-graph


		# File description (Solo in Quaderni 1, Fascicoli per anno)
		# Physical (E78)
		d.add((URIRef(file + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(file + '/object'), RDFS.label, Literal(file_label_it, lang='it'), graph_base))
		d.add((URIRef(file + '/object'), RDFS.label, Literal(file_label_en, lang='en'), graph_base))
		d.add((URIRef(file + '/object'), ecrm.P1_is_identified_by, URIRef(file + '/shelfmark'), graph_base))		
		d.add((URIRef(file + '/object'), ecrm.P2_has_type, ficlitdlo.file, graph_base))
		d.add((URIRef(file + '/object'), ecrm.P46i_forms_part_of, URIRef(subseries + '/object'), graph_base)) # Quaderni manoscritti 1954-1976
		d.add((URIRef(file + '/object'), ecrm.P46_is_composed_of, rec_object, graph_base))
		d.add((URIRef(file + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(file + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(file + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(file + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		
		# # Conceptual (E89)
		# d.add((file, RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		# d.add((file, RDFS.label, Literal(file_label_it, lang='it'), graph_base))
		# d.add((file, RDFS.label, Literal(file_label_en, lang='en'), graph_base))
		# d.add((file, ecrm.P1_is_identified_by, URIRef(file + '/shelfmark'), graph_base))		
		# d.add((file, ecrm.P2_has_type, ficlitdlo.file, graph_base))
		# d.add((file, ecrm:P102_has_title, URIRef(file + '/title'), graph_base))
		# d.add((file, ficlitdlo.formsConceptuallyPartOf, URIRef(subseries), graph_base)) # [Quaderni manoscritti] 1954-[1976]
		# d.add((file, ficlitdlo.isConceptuallyComposedOf, rec_object))	
		
		# How to cite
		d.add((URIRef(file + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + '.'), graph_base))

		# Subseries description (Quaderni 1-2-3)

		d.add((URIRef(subseries + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(subseries + '/object'), RDFS.label, Literal(subseries_label_it, lang='it'), graph_base))
		d.add((URIRef(subseries + '/object'), RDFS.label, Literal(subseries_label_en, lang='en'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P1_is_identified_by, URIRef(subseries + '/shelfmark'), graph_base))		
		d.add((URIRef(subseries + '/object'), ecrm.P2_has_type, ficlitdlo.series, graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P3_has_note, Literal(subseries_note , lang='it'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P46i_forms_part_of, URIRef(series + '/object'), graph_base)) # Quaderni
		if collocazione == 'QUADERNI.1':
			d.add((URIRef(subseries + '/object'), ecrm.P46_is_composed_of, URIRef(file + '/object'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		d.add((URIRef(subseries + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' ' + collocazione + '.'), graph_base))

		# Series description 

		d.add((URIRef(series + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(series + '/object'), RDFS.label, Literal(series_label_it, lang='it'), graph_base))
		d.add((URIRef(series + '/object'), RDFS.label, Literal(series_label_en, lang='en'), graph_base))
		d.add((URIRef(series + '/object'), ecrm.P1_is_identified_by, URIRef(series + '/shelfmark'), graph_base))		
		d.add((URIRef(series + '/object'), ecrm.P2_has_type, ficlitdlo.series, graph_base))
		d.add((URIRef(series + '/object'), ecrm.P46i_forms_part_of, URIRef(subfonds + '/object'), graph_base)) # Archivio (FR.A)
		d.add((URIRef(series + '/object'), ecrm.P46_is_composed_of, URIRef(subseries + '/object'), graph_base))
		d.add((URIRef(series + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(series + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(series + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(series + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		d.add((URIRef(series + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' QUADERNI.'), graph_base))

		# Subfonds description
	
		# Archive

		d.add((URIRef(subfonds + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(subfonds + '/object'), RDFS.label, Literal(subfonds_label_it, lang='it'), graph_base))
		d.add((URIRef(subfonds + '/object'), RDFS.label, Literal(subfonds_label_en, lang='en'), graph_base))
		d.add((URIRef(subfonds + '/object'), ecrm.P1_is_identified_by, URIRef(subfonds + '/shelfmark'), graph_base))		
		d.add((URIRef(subfonds + '/object'), ecrm.P2_has_type, ficlitdlo.fonds, graph_base))
		d.add((URIRef(subfonds + '/object'), ecrm.P46i_forms_part_of, URIRef(fonds + '/object'), graph_base)) # Fondo Giuseppe Raimondi (Archivio e Biblioteca)
		d.add((URIRef(subfonds + '/object'), ecrm.P46_is_composed_of, URIRef(series + '/object'), graph_base))
		d.add((URIRef(subfonds + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(subfonds + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(subfonds + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(subfonds + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		d.add((URIRef(subfonds + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Archivio. Biblioteca Ezio Raimondi, Università di Bologna.'), graph_base))

		# Library

		d.add((URIRef(subfonds_b + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), RDFS.label, Literal(subfonds_b_label_it, lang='it'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), RDFS.label, Literal(subfonds_b_label_en, lang='en'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), ecrm.P1_is_identified_by, URIRef(subfonds_b + '/shelfmark'), graph_base))		
		d.add((URIRef(subfonds_b + '/object'), ecrm.P2_has_type, ficlitdlo.fonds, graph_base))
		d.add((URIRef(subfonds_b + '/object'), ecrm.P46i_forms_part_of, URIRef(fonds + '/object'), graph_base)) # Fondo Giuseppe Raimondi (Archivio e Biblioteca)
		d.add((URIRef(subfonds_b + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		d.add((URIRef(subfonds_b + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca. Biblioteca Ezio Raimondi, Università di Bologna.'), graph_base))

		# Fonds description
	
		d.add((URIRef(fonds + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(fonds + '/object'), RDFS.label, Literal(fonds_label_it, lang='it'), graph_base))
		d.add((URIRef(fonds + '/object'), RDFS.label, Literal(fonds_label_en, lang='en'), graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P1_is_identified_by, URIRef(fonds + '/shelfmark'), graph_base))		
		d.add((URIRef(fonds + '/object'), ecrm.P2_has_type, ficlitdlo.fonds, graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P46_is_composed_of, URIRef(subfonds + '/object'), graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P46_is_composed_of, URIRef(subfonds_b + '/object'), graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(fonds + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		d.add((URIRef(fonds + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi. Biblioteca Ezio Raimondi, Università di Bologna.'), graph_base))



# TriG
d.serialize(destination="../../dataset/trig/base-graph-E78_quad.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-E78_quad.nq", format='nquads')