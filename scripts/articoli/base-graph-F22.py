# coding: utf-8

""" Base graph :
Articoli, F22 Self-Contained Expression
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

		if collocazione == 'ARTICOLI1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '/' + specificazione)
		elif collocazione == 'ARTICOLI2':
			subseries = URIRef(series + '-2')

		# Declare a URI for each record
		record = URIRef(base_uri + 'article/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each article text
		rec_expression = URIRef(record + 'text')
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]

	

		# Add quads to base-graph


		######################
		#                    #
		# Text description   #
		#                    #
		######################

		d.add((rec_expression, RDF.type, URIRef('http://erlangen-crm.org/efrbroo/F22_Self-Contained_Expression'), graph_base))

		# Label (it, en)
		d.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label + '"' , lang='it'), graph_base))
		d.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + rec_label + '"' , lang='en'), graph_base))
		
		# Language		
		d.add((rec_expression, ecrm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita'), graph_base))

		# Expression creation
		d.add((rec_expression, efrbroo.R17i_was_created_by, URIRef(rec_expression + '/creation'), graph_base))

		
		# Main title
		d.add((rec_expression, ecrm.P102_has_title, URIRef(rec_expression + '/title'), graph_base))
		
		# Rights
		d.add((rec_expression, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/all-rights-reserved'), graph_base))
		
		# Link to physical carrier
		d.add((rec_expression, ecrm.P128i_is_carried_by, rec_object, graph_base))

		if 'saggio' in rec_label:
			d.add((rec_expression, ecrm.P2_has_type, ficlitdlo.essay, graph_base))
		elif 'articolo' in rec_label:
			d.add((rec_expression, ecrm.P2_has_type, ficlitdlo.article, graph_base))			

		# Expression realises Work
		s = rec_label.replace(' ', 'x').replace("'", "x")
		w = ''.join(ch for ch in s if ch.isalpha())
		rec_work = URIRef(base_uri + 'work/' + w.lower().replace('x' , '-'))
		d.add((rec_work, efrbroo.R3_is_realised_in, rec_expression, graph_base))
		d.add((rec_work, RDF.type, efrbroo.F1_Work, graph_base))


		# Description of published version
		pubinfo = re.findall('(Il resto del carlino|Il giorno|La nazione|Corriere della sera|Il mondo) (\d+)\.\[?(\d+)\]?\.(\d+)', descrizione_isbd)
		for item in pubinfo:
			if int(item[2]) < 10:
				mm = '0' + item[2]
			else:
				mm = item[2]
			if int(item[1]) < 10:
				dd = '0' + item[1]
			else:
				dd = item[1]
			publisher_label = item[0]
			publisher = publisher_label.replace(' ', 'x')
			publisher = ''.join(ch for ch in publisher if ch.isalpha())
			pubtext = URIRef(base_uri + 'pub-text/' + w.lower().replace('x' , '-') + '-' + item[3] + mm + dd)
			d.add((pubtext, RDF.type, efrbroo.F24_Publication_Expression, graph_base))
			d.add((pubtext, ficlitdlo.isPublishedVersionOf, rec_expression, graph_base))
			d.add((pubtext, DCTERMS.publisher, URIRef('https://w3id.org/ficlitdl/' + publisher.lower().replace('x' , '-')), graph_base))
			d.add((URIRef('https://w3id.org/ficlitdl/' + publisher.lower().replace('x' , '-')), RDF.type, ecrm.E40_Legal_Body, graph_base))
			d.add((URIRef('https://w3id.org/ficlitdl/' + publisher.lower().replace('x' , '-')), RDFS.label, Literal(publisher_label), graph_base))
			d.add((pubtext, prism.publicationDate, Literal(item[3] + '-' + mm + '-' + dd, datatype=XSD.date), graph_base))
			d.add((pubtext, ecrm.P102_has_title, URIRef(pubtext + '/title'), graph_base))
			d.add((URIRef(pubtext + '/title'), RDF.type , ecrm.E35_Title, graph_base))





# TriG
d.serialize(destination="../../dataset/trig/base-graph-F22_art.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/base-graph-F22_art.nq", format='nquads')