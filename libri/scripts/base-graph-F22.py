# coding: utf-8

""" Base graph :
Libri, F24 Self-Contained Expression
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
		# https://w3id.org/giuseppe-raimondi-lod/pub-text/i-tetti-sulla-citta-19731976
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]

	

		s = rec_label.replace(' ', 'x').replace("'", "x")
		w = ''.join(ch for ch in s if ch.isalnum())
		w = w.replace('x' , '-')
		w = w.replace('--' , '-')
		rec_work = URIRef(base_uri + 'work/' + w.lower())
		pub_text = URIRef(base_uri + 'pub-text/' + w.lower().replace('x' , '-') + '-' + pubdate[0])

	
		pub = publisher[0].replace(' ', 'x').replace("'", "x")
		pub_id = ''.join(ch for ch in pub if ch.isalpha())



		# Add quads to base-graph


		######################
		#                    #
		# Pub text desc      #
		#                    #
		######################

		d.add((pub_text, RDF.type, URIRef('http://erlangen-crm.org/efrbroo/F24_Publication_Expression'), graph_base))

		d.add((pub_text, DCTERMS.publisher, URIRef('https://w3id.org/ficlitdl/' + pub_id.lower().replace('x' , '-')), graph_base))
		
		d.add((URIRef('https://w3id.org/ficlitdl/' + pub_id.lower().replace('x' , '-')), RDF.type, ecrm.E40_Legal_Body, graph_base))
		
		d.add((URIRef('https://w3id.org/ficlitdl/' + pub_id.lower().replace('x' , '-')), RDFS.label, Literal(publisher[0]), graph_base))
		
		d.add((pub_text, prism.publicationDate, Literal(pubdate[0], datatype=XSD.date), graph_base))
		
		d.add((pub_text, ecrm.P102_has_title, URIRef(pub_text + '/title'), graph_base))




		# Label (it, en)
		d.add((pub_text, RDFS.label, Literal('Raimondi, Giuseppe. Testo a stampa, "' + rec_label + '"' , lang='it'), graph_base))
		d.add((pub_text, RDFS.label, Literal('Raimondi, Giuseppe. Printed text, "' + rec_label + '"' , lang='en'), graph_base))
		
		# Language		
		d.add((pub_text, ecrm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita'), graph_base))

				
		# Link to physical carrier
		d.add((pub_text, ecrm.P128i_is_carried_by, rec_object, graph_base))


		d.add((rec_work, efrbroo.R3_is_realised_in, pub_text, graph_base))
		d.add((rec_work, RDF.type, efrbroo.F1_Work, graph_base))


		
	




# TriG
d.serialize(destination="../output/trig/base-graph-F24.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-F24.nq", format='nquads')