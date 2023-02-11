# coding: utf-8

""" Base graph :
Articoli, E89 Propositional Object
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

with open('../../input/libri.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  row['Inventario']
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] 
		data_inv = row['\ufeffData inv.']
		precisazione = row['Precisazione inventario']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')

		series = URIRef(base_uri + 'record-set' + '/' + 'printed-volumes/archivio')
		series_label_it = 'Fondo Giuseppe Raimondi, Biblioteca , Archivio '
		series_label_en = 'Giuseppe Raimondi Fonds, Library , Archive'
		pubdate = re.findall(', (\[?\d+\]?)\.', descrizione_isbd)
		publisher = re.findall('\. - .+? : (.+?),', descrizione_isbd)
		pubplace = re.findall('\. - (\[?\S+?\]?) : .+?,', descrizione_isbd)

		
	
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

		# Declare a URI for each record
		record = URIRef(base_uri + 'printed-volume/' + inventario.lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each pub text
		rec_expression = URIRef(record + 'text')
		pub_text = URIRef(base_uri + 'pub-text/' )
		# https://w3id.org/giuseppe-raimondi-lod/pub-text/i-tetti-sulla-citta-19731976
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]

	

		s = rec_label.replace(' ', 'x').replace("'", "x")
		w = ''.join(ch for ch in s if ch.isalnum())


		w = w.replace('x' , '-')
		w = w.replace('--' , '-')
		rec_work = URIRef(base_uri + 'work/' + w.lower())
		pub_text = URIRef(base_uri + 'pub-text/' + w.lower().replace('x' , '-') + '-' + pubdate[0])


		# Add quads to base-graph

		# Series description (Serie 'Archivio' all'interno del subfondo biblioteca) 

		d.add((URIRef(series), RDF.type, URIRef('http://erlangen-crm.org/current/E78_Curated_Holding'), graph_base))
		d.add((URIRef(series), RDFS.label, Literal(series_label_it, lang='it'), graph_base))
		d.add((URIRef(series), RDFS.label, Literal(series_label_en, lang='en'), graph_base))
		d.add((URIRef(series), ecrm.P2_has_type, ficlitdlo.series, graph_base))
		d.add((URIRef(series), ficlitdlo.formsConceptuallyPartOf, URIRef(subfonds_b + '/object'), graph_base)) # Archivio (FR.A)
		d.add((URIRef(series), ficlitdlo.isConceptuallyComposedOf, URIRef(rec_object), graph_base))


# TriG
d.serialize(destination="../../dataset/trig/libri_base-graph-E89.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/libri_base-graph-E89.nq", format='nquads')