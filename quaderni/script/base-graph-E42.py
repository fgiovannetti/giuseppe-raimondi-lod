# coding: utf-8

""" Base graph :
Quaderni, E42 Identifier
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

		# Add quads to base-graph

		d.add((URIRef(record + 'inventory-number'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(record + 'inventory-number'), RDFS.label, Literal(inventario[0]), graph_base))
		d.add((URIRef(record + 'inventory-number'), ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/inventory-number'), graph_base))

		d.add((URIRef(record + 'shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(record + 'shelfmark'), RDFS.label, Literal(sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza), graph_base))
		d.add((URIRef(record + 'shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))
	
		# File

		d.add((URIRef(file + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(file + '/shelfmark'), RDFS.label, Literal(sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '')), graph_base))
		d.add((URIRef(file + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		# Subseries

		d.add((URIRef(subseries + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(subseries + '/shelfmark'), RDFS.label, Literal(sezione + ' ' + collocazione), graph_base))
		d.add((URIRef(subseries + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		# Series

		d.add((URIRef(series + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(series + '/shelfmark'), RDFS.label, Literal(sezione + ' QUADERNI'), graph_base))
		d.add((URIRef(series + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		# Subfonds

		d.add((URIRef(subfonds + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(subfonds + '/shelfmark'), RDFS.label, Literal(sezione), graph_base))
		d.add((URIRef(subfonds + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		d.add((URIRef(subfonds_b + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(subfonds_b + '/shelfmark'), RDFS.label, Literal(sezione), graph_base))
		d.add((URIRef(subfonds_b + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		# Fonds

		d.add((URIRef(fonds + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(fonds + '/shelfmark'), RDFS.label, Literal(sezione), graph_base))
		d.add((URIRef(fonds + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))




# TriG
d.serialize(destination="../output/trig/base-graph-E42.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E42.nq", format='nquads')