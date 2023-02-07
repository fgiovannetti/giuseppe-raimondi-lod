# coding: utf-8

""" Base graph :
Libri, E22 Human-Made Object
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

		# # Nanopublication
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# # Provenance of the assertions
		# d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('1993-03' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		# d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), URIRef(nanopub + 'provenance')))

		# # Publication info
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), PROV.generatedAtTime, Literal('2022-02-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))


		########################
		#                      #
		# Volume description   #
		#                      #
		########################

		d.add((rec_object, RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
		d.add((rec_object, RDF.type, efrbroo.F5_Item, graph_base))

		# Label (it, en)
		d.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Libro moderno, "' + rec_label + '"' , lang='it'), graph_base))
		d.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Libro moderno, "' + rec_label + '"' , lang='en'), graph_base))
		
		# Inventory number and shelfmark
		d.add((rec_object, ecrm.P1_is_identified_by, URIRef(record + 'inventory-number'), graph_base))
		d.add((rec_object, ecrm.P1_is_identified_by, URIRef(record + 'shelfmark'), graph_base))

		# Document type
		d.add((rec_object, ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/printed-volume'), graph_base))
		
		# Descrizione isbd
		d.add((rec_object, ecrm.P3_has_note, Literal(descrizione_isbd , lang='it'), graph_base))
		d.add((rec_object, ecrm.P3_has_note, Literal(precisazione , lang='it'), graph_base))

		# Dimensioni (h, pagine)
		d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + height[0] + 'cm'), graph_base))
		d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), graph_base)) 

		d.add((rec_object, ecrm.P46i_forms_part_of, URIRef(series + '/object'), graph_base))
		d.add((rec_object, ficlitdlo.formsConceptuallyPartOf, URIRef(series), graph_base))

		# Keeper, owner, location, and rights
		d.add((rec_object, ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((rec_object, ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((rec_object, ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((rec_object, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/' + 'all-rights-reserved'), graph_base))
		# Link to expression
		d.add((rec_object, ecrm.P128_carries, pub_text, graph_base))

		# How to cite
		d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + pubdate[0] + '. ' + rec_label + '. ' + pubplace[0] + ': ' + publisher[0] + '. Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario + ', ' + sezione + ' ' + collocazione + '.'), graph_base))




# TriG
d.serialize(destination="../output/trig/base-graph-E22.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E22.nq", format='nquads')