# coding: utf-8

""" Base graph :
Libri, E54 Dimension
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

with open('../input/libri.csv', mode='r') as csv_file:
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
		pubdate = re.findall(', (\[?\d+\]?)\.', descrizione_isbd)
		publisher = re.findall('\. - .+? : (.+?),', descrizione_isbd)
		pubplace = re.findall('\. - (\[?\S+?\]?) : .+?,', descrizione_isbd)

		
	


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


 		# Dimensions of physical object (height in cm, extent in number of pages and number of leaves)
		height = re.findall(" (\d+) cm\.", row["Descrizione isbd"])
		extent_pages = re.findall("(\d+) p\.", row["Descrizione isbd"])

		# Add quads to base-graph

		# Dimensioni (h, pagine manoscritte, carte)

		d.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), RDF.type, ecrm.E54_Dimension, graph_base))
		d.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), RDFS.label, Literal('Altezza ' + height[0] + ' cm', lang='it'), graph_base))
		d.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), RDFS.label, Literal('Height ' + height[0] + ' cm' , lang='en'), graph_base))
		d.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), ecrm.P91_has_unit, ficlitdlo.centimetre, graph_base))
		d.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), ecrm.P90_has_value, Literal(height[0], datatype=XSD.integer), graph_base))
		d.add((URIRef(base_uri + 'height/' + height[0] + 'cm'), ecrm.P2_has_type, ficlitdlo.height, graph_base))
		
	
		d.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), RDF.type, ecrm.E54_Dimension, graph_base))
		d.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), RDFS.label, Literal(extent_pages[0] + ' pagine', lang='it'), graph_base))
		d.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), RDFS.label, Literal(extent_pages[0] + ' pages', lang='en'), graph_base))
		d.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), ecrm.P91_has_unit, ficlitdlo.page, graph_base))
		d.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), ecrm.P90_has_value, Literal(extent_pages[0], datatype=XSD.integer), graph_base))
		d.add((URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), ecrm.P2_has_type, ficlitdlo.extent, graph_base))




# TriG
d.serialize(destination="../output/trig/base-graph-E54.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E54.nq", format='nquads')