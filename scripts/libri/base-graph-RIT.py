# coding: utf-8

""" Base graph :
Libri, Role In Time
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
pro = Namespace("http://purl.org/spar/pro/")
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
d.bind("pro", pro)
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





		# Add quads to base-graph

		d.add((URIRef(pub_text + '/author'), RDF.type, pro.RoleInTime, graph_base))
		d.add((URIRef(pub_text + '/author'), pro.withRole, pro.author, graph_base))
		d.add((URIRef(pub_text + '/author'), RDFS.label, Literal('Giuseppe Raimondi, autore di  ' + '"' + rec_label + '"', lang='it'), graph_base))
		d.add((URIRef(pub_text + '/author'), RDFS.label, Literal('Giuseppe Raimondi, author of  ' + '"' + rec_label + '"', lang='en'), graph_base))
		d.add((URIRef(pub_text + '/author'), pro.relatesToEntity, pub_text, graph_base))



# TriG
d.serialize(destination="../../dataset/trig/libri_base-graph-RIT.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/libri_base-graph-RIT.nq", format='nquads')