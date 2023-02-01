# coding: utf-8

""" Base graph :
Quaderni, F22 Self-Contained Expression
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

with open('../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:

		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione']
		sequenza = row['Sequenza']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		yyyy = re.findall("(.+?) *$", descrizione_isbd[0])
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		# Declare a URI for each record
		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical notebook
		rec_object = URIRef(record + 'object')
 		
 		# Declare a URI for each notebook text
		rec_expression = URIRef(record + 'text')

		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]


		# Add quads to base-graph


		######################
		#                    #
		# Text description   #
		#                    #
		######################

		d.add((rec_expression, RDF.type, URIRef('http://erlangen-crm.org/efrbroo/F22_Self-Contained_Expression'), graph_base))

		# Label (it, en)
		# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		d.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + rec_label[0].replace('*', '') + '"' , lang='it'), graph_base))
		d.add((rec_expression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + rec_label[0].replace('*', '') + '"' , lang='en'), graph_base))
		
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


		################################
		#                              #
		# Description of single texts  #
		#                              #
		################################

		# Subexpressions (as per descrizione_isbd, separated by ';')
		# The relation 'CONTIENE ANCHE' features this same information
		if ' ; ' in rec_label[0]:
			rec_label = rec_label[0].split(' ; ')
			i = 1
			for title in rec_label:
				
				# URI Subexpression
				rec_subexpression = URIRef(rec_expression + '/' + str(i))

				d.add((rec_subexpression, RDF.type, URIRef('http://erlangen-crm.org/efrbroo/F22_Self-Contained_Expression'), graph_base))

				# Link to overall expression (whole text in notebook)
				d.add((rec_expression, ecrm.P165_incorporates, rec_subexpression, graph_base))
				
				# Label (it, en)
				# E.g.: Raimondi, Giuseppe. Testo manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
				d.add((rec_subexpression, RDFS.label, Literal('Raimondi, Giuseppe. Testo manoscritto, "' + title + '"' , lang='it'), graph_base))
				d.add((rec_subexpression, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript text, "' + title + '"' , lang='en'), graph_base))

				# # Narrative form type (if available)
				if 'racconto' in title:
					d.add((rec_subexpression, ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/short-story'), graph_base))
				elif 'appunti' in title:
					d.add((rec_subexpression, ecrm.P2_has_type, ficlitdlo.notes, graph_base))
				elif 'articolo' in title:
					d.add((rec_subexpression, ecrm.P2_has_type, ficlitdlo.article, graph_base))			
				
				# Language		
				d.add((rec_subexpression, ecrm.P72_has_language, URIRef('http://id.loc.gov/vocabulary/iso639-2/ita'), graph_base))		
				
				# Main title
				subrec = URIRef(record + str(i))
				d.add((rec_subexpression, ecrm.P102_has_title, URIRef(rec_subexpression + '/title'), graph_base))

				# Link to physical carrier
				d.add((rec_subexpression, ecrm.P128i_is_carried_by, rec_object, graph_base))

				# Link to overall expression
				d.add((rec_subexpression, ecrm.P165i_is_incorporated_in, rec_expression, graph_base))
				
				# Subexpression creation
				d.add((rec_subexpression, efrbroo.R17i_was_created_by, URIRef(rec_subexpression + '/creation'), graph_base))
				d.add((URIRef(rec_subexpression + '/creation'), RDF.type, efrbroo.F28_Expression_Creation, graph_base))
				d.add((URIRef(rec_subexpression + '/creation'), ecrm.P14_carried_out_by, URIRef('https://w3id.org/ficlitdl/person/giuseppe-raimondi'), graph_base))
				d.add((URIRef(rec_subexpression + '/creation'), ecrm.P32_used_general_technique, ficlitdlo.handwriting, graph_base))
				d.add((URIRef(rec_subexpression + '/creation'), efrbroo.R17_created, URIRef(rec_subexpression), graph_base))
				d.add((URIRef(rec_expression + '/creation'), ecrm.P9_consists_of, URIRef(rec_subexpression + '/creation'), graph_base))

				i += 1

		# Expression realises Work
				s = title.replace(' ', 'x')
				w = ''.join(ch for ch in s if ch.isalpha())
				rec_work = URIRef(base_uri + 'work/' + w.lower().replace('x' , '-'))
				d.add((rec_work, efrbroo.R3_is_realised_in, rec_expression, graph_base))
				d.add((rec_work, RDF.type, efrbroo.F1_Work, graph_base))
		else:
			s = rec_label[0].replace(' ', 'x')
			w = ''.join(ch for ch in s if ch.isalpha())
			rec_work = URIRef(base_uri + 'work/' + w.lower().replace('x' , '-'))
			d.add((rec_work, efrbroo.R3_is_realised_in, rec_expression, graph_base))
			d.add((rec_work, RDF.type, efrbroo.F1_Work, graph_base))

# TriG
d.serialize(destination="../output/trig/base-graph-F22.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-F22.nq", format='nquads')