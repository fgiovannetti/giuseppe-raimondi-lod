# coding: utf-8

""" Base graph :
Articoli, E78 Curated Holding
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

with open('../../input/articoli.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] #?1954
		sequenza = row['Sequenza'] #00.00
		data_inv = row['Data inv.']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"]) # HA PER ALTRO TITOLO

		series = URIRef(base_uri + 'record-set' + '/' + 'articles')
		series_label_en = 'Giuseppe Raimondi Fonds, Archive, Manuscripts'
		series_label_it = 'Fondo Giuseppe Raimondi, Archivio, Manoscritti'


		if collocazione == 'ARTICOLI1':
			subseries = URIRef(series + '-1')
			subseries_label_en = 'Giuseppe Raimondi Fonds, Archive, Manuscripts, Manuscripts 1960–1976'
			subseries_label_it = 'Fondo Giuseppe Raimondi, Archivio, Manoscritti, Manoscritti 1960–1976'
			subseries_note = 'Mat. document.-manoscr 3621050 [Manoscritti] / Giuseppe Raimondi. - 1960-1976. - 17 carpette ; 32 cm. ((Minute di articoli, racconti, quasi tutte su mezzi fogli protocollo, ordinate da Giuseppe Raimondi in carpette per anno, con indici. - Pubblicati su Il resto del carlino e altri periodici (cfr., anche per le date di pubblicazione, gli Indici fatti tenere dallo stesso G. R. "Arte, Letteratura, Narrativa, Poesia: articoli pubblicati dal 1955: Il mondo, Il resto del carlino, La nazione, Corriere della sera, giornali vari").'

			file = URIRef(subseries + '/' + specificazione)
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Manuscripts, Manuscripts 1960–1976, ' + specificazione
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Manoscritti, Manoscritti 1960–1976, ' + specificazione

		
		elif collocazione == 'ARTICOLI2':
			subseries = URIRef(series + '-2')
			subseries_label_en = 'Giuseppe Raimondi Fonds, Archive, Manuscripts, Manuscripts 1947–1971'
			subseries_label_it = 'Fondo Giuseppe Raimondi, Archivio, Manoscritti, Manoscritti 1947–1971'
			subseries_note = 'Mat. document.-manoscr 3621051 [Manoscritti di Prefazioni, Conferenze, Omaggi] / Giuseppe Raimondi. - 1947-1971. - 1 carpetta ; 31 cm.'

		subfonds = URIRef(base_uri + 'record-set' + '/' + 'giuseppe-raimondi-archive')

		# Declare a URI for each record
		record = URIRef(base_uri + 'article/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each article text
		rec_expression = URIRef(record + 'text')
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]




		# Add quads to base-graph

		# File description (Solo in Articoli 1, Fascicoli per anno)
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

		# How to cite
		d.add((URIRef(file + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' ' + collocazione + ' ' + specificazione + '.') , graph_base))

		# Subseries description (Articoli 1-2)

		d.add((URIRef(subseries + '/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(subseries + '/object'), RDFS.label, Literal(subseries_label_it, lang='it'), graph_base))
		d.add((URIRef(subseries + '/object'), RDFS.label, Literal(subseries_label_en, lang='en'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P1_is_identified_by, URIRef(subseries + '/shelfmark'), graph_base))		
		d.add((URIRef(subseries + '/object'), ecrm.P2_has_type, ficlitdlo.series, graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P3_has_note, Literal(subseries_note , lang='it'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P46i_forms_part_of, URIRef(series + '/object'), graph_base)) # Quaderni
		if collocazione == 'ARTICOLI1':
			d.add((URIRef(subseries + '/object'), ecrm.P46_is_composed_of, URIRef(file + '/object'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((URIRef(subseries + '/object'), ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		d.add((URIRef(subseries + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + ' ' + collocazione + '.') , graph_base))

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
		d.add((URIRef(series + '/object'), DCTERMS.bibliographicCitation, Literal('Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + sezione + '.') , graph_base))


# TriG
d.serialize(destination="../../dataset/trig/base-graph-E78_art.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-E78_art.nq", format='nquads')