# coding: utf-8

""" Base graph :
Articoli, E42 Identifier
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


		# Declare a URI for each record
		record = URIRef(base_uri + 'article/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each article text
		rec_expression = URIRef(record + 'text')
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]



		# Add quads to base-graph

		d.add((URIRef(record + 'inventory-number'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(record + 'inventory-number'), RDFS.label, Literal(inventario[0]), graph_base))
		d.add((URIRef(record + 'inventory-number'), ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/inventory-number'), graph_base))

		d.add((URIRef(record + 'shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(record + 'shelfmark'), RDFS.label, Literal(sezione + ' ' + collocazione + ' ' + specificazione + ' ' + sequenza), graph_base))
		d.add((URIRef(record + 'shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))
	
		# File
		if collocazione == 'ARTICOLI1':
			d.add((URIRef(file + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
			d.add((URIRef(file + '/shelfmark'), RDFS.label, Literal(sezione + ' ' + collocazione + ' ' + specificazione), graph_base))
			d.add((URIRef(file + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		# Subseries

		d.add((URIRef(subseries + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(subseries + '/shelfmark'), RDFS.label, Literal(sezione + ' ' + collocazione), graph_base))
		d.add((URIRef(subseries + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))

		# Series

		d.add((URIRef(series + '/shelfmark'), RDF.type, ecrm.E42_Identifier, graph_base))
		d.add((URIRef(series + '/shelfmark'), RDFS.label, Literal(sezione + ' ARTICOLI'), graph_base))
		d.add((URIRef(series + '/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_base))




# TriG
d.serialize(destination="../../dataset/trig/articoli_base-graph-E42.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/articoli_base-graph-E42.nq", format='nquads')