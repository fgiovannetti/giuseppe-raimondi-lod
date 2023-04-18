# coding: utf-8

""" Base graph :
FICLITDL, E21 Person
"""

from rdflib import Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, PROV
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
d.bind('ficlitdl-np', URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base/'))
d.bind("owl", OWL)
d.bind('prov', PROV)
d.bind("pro", pro)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('seq', seq)
d.bind('ti', ti)
d.bind('tvc', tvc)


# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base/')

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

		series = URIRef(base_uri + 'record-set' + '/' + 'printed-volumes')
		subseries = URIRef(base_uri + 'record-set' + '/' + 'printed-volumes/archivio')
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
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]

		rec_label_short = rec_label.split(' :')[0]
		
	

		s = rec_label_short.replace(' ', 'x').replace("'", "x")
		w = ''.join(ch for ch in s if ch.isalnum())
		w = w.replace('x' , '-')
		w = w.replace('--' , '-')
		rec_work = URIRef(base_uri + 'work/' + w.lower())
		pub_text = URIRef(base_uri + 'pub-text/' + w.lower().replace('x' , '-') + '-' + pubdate[0].replace('[', '').replace(']', ''))

	
		pub = publisher[0].replace(' ', 'x').replace("'", "x")
		pub_id = ''.join(ch for ch in pub if ch.isalpha())


		# person URI

		person = URIRef('https://w3id.org/ficlitdl/' + 'person/') 



		# Add quads to base-graph

		# Nanopublication
		d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# Provenance of the assertions
		d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('1993-03' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), URIRef(nanopub + 'provenance')))

		# Publication info
		d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), PROV.generatedAtTime, Literal('2022-02-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))


		###########################
		#                         #
		# Giuseppe Raimondi       #
		#                         #
		###########################

		d.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef(pub_text + '/author'), graph_base))




# TriG
d.serialize(destination="../../dataset/trig/libri_base-graph-E21.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/libri_base-graph-E21.nq", format='nquads')