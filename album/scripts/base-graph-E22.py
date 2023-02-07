# coding: utf-8

""" Base graph :
Album, E22 Human-Made Object
Fascicoli (Record): 829 cartelline ordinate alfabeticamente per corrispondente
Unità documentarie: non inventariate, utilizziamo il campo 'Precisazione' per creare permalink dei singoli items (es. lettera, cartolina, biglietto, etc.)
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


# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub-base/')

# Declare a Graph URI to be used to identify a Graph
graph_base = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_base, to the Dataset
d.graph(identifier=graph_base)

with open('../input/album.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] 
		data_inv = row['Data inv.']
		identificativo = row['Id.']
		precisazione = row['Precisazione inventario']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"]) # HA PER ALTRO TITOLO

		# URI Serie Album
		series = URIRef(base_uri + 'record-set' + '/' + 'album')
		series_label_en = 'Giuseppe Raimondi Fonds, Archive, Album'
		series_label_it = 'Fondo Giuseppe Raimondi, Archivio, Album'

		# URI Album
		specificazione = specificazione.replace('[', '').replace(']', '').replace('?', '')
		file = URIRef(base_uri + 'record-set/album-' + specificazione.lower() + '/' + inventario[0].lower().replace(' ', ''))
		file_object = URIRef(file + '/object')
		file_expression = URIRef(file + '/text')
		label = re.findall('^(.+?)\. \-', descrizione_isbd)

		file_label_en = 'Giuseppe Raimondi Fonds, Archive, ' + label[0]
		file_label_it = 'Fondo Giuseppe Raimondi, Archivio, ' + label[0]
	
		########################
		#                      #
		# File description     #
		#                      #
		########################

		d.add((file_object, RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
		
		# Label (it, en)
		d.add((file_object, RDFS.label, Literal(file_label_it , lang='it'), graph_base))
		d.add((file_object, RDFS.label, Literal(file_label_en , lang='en'), graph_base))
		
		# Inventory number and shelfmark
		d.add((file_object, ecrm.P1_is_identified_by, URIRef(file + '/inventory-number'), graph_base))
		d.add((file_object, ecrm.P1_is_identified_by, URIRef(file + '/shelfmark'), graph_base))

		# Document type
		d.add((file_object, ecrm.P2_has_type, ficlitdlo.file, graph_base))
		d.add((file_object, ecrm.P2_has_type, ficlitdlo.album, graph_base))

		
		# Descrizione isbd
		d.add((file_object, ecrm.P3_has_note, Literal(descrizione_isbd , lang='it'), graph_base))

		# Dimensioni
		height =  re.findall("(\d+) cm", descrizione_isbd)
		d.add((file_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + height[0] + 'cm'), graph_base))

		# Fa parte di
		d.add((file_object, ecrm.P46i_forms_part_of, URIRef(series + '/object'), graph_base))
		d.add((file_object, ficlitdlo.formsConceptuallyPartOf, URIRef(series), graph_base))

		# Keeper, owner, location, and rights
		d.add((file_object, ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((file_object, ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((file_object, ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((file_object, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/' + 'all-rights-reserved'), graph_base))

		# How to cite
		if 'album' in label[0]:
			d.add((file_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + label[0] + '. Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + specificazione + '.'), graph_base))
		else:
			d.add((file_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + label[0] + '. Album. Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + specificazione + '.'), graph_base))

		d.add((file_object, ecrm.P128_carries, file_expression, graph_base))





# TriG
d.serialize(destination="../output/trig/base-graph-E22.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E22.nq", format='nquads')