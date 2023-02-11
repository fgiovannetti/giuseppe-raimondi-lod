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

with open('../../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:

		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione']
		sequenza = row['Sequenza']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd']
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])
		
		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# physical notebook URI

		rec_object = URIRef(record + 'object')
 		
 		# expression URI

		rec_expression = URIRef(record + 'text')

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

		d.add((URIRef(person + 'giuseppe-raimondi'), RDF.type, ecrm.E21_Person, graph_base))
		d.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi' , lang='it'), graph_base))
		d.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi' , lang='en'), graph_base))
		d.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('http://viaf.org/viaf/7457679'), graph_base))
		d.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('https://www.worldcat.org/identities/lccn-n79021749'), graph_base))
		d.add((URIRef(person + 'giuseppe-raimondi'), OWL.sameAs, URIRef('https://www.wikidata.org/wiki/Q3771293'), graph_base))
		d.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef(rec_expression + '/author'), graph_base))


# persone menzionate nella descrizione isbd (persone menzionate nel testo TODO con trascrizioni)

my_dict = {}

with open('../../input/quaderni_ner_person.tsv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter='\t')
	for row in csv_reader:

		inventario = row["inventario"].lower().replace(' ', '')
		wd = row["wikidata"]
		wd_code = row["wikidata_code"]

		my_dict[inventario] = list()
		my_dict[inventario].append((wd, wd_code))

		record = URIRef(base_uri + 'notebook/' + inventario + '/')

 		# expression URI
		rec_expression = URIRef(record + 'text')

		# person URI
		person = URIRef('https://w3id.org/ficlitdl/' + 'person/')

		for item in my_dict[inventario]:
			mentioned_person = URIRef(person + item[0].lower().replace(' ', '-').replace('.', '').replace(',', '').replace('è', 'e').replace('é', 'e').replace('à', 'a').replace('á', 'a').replace('ö', 'o').replace('ç', 'c'))
			d.add((mentioned_person, RDF.type, ecrm.E21_Person, graph_base))
			d.add((mentioned_person, RDFS.label, Literal(item[0], lang='it'), graph_base))
			d.add((mentioned_person, RDFS.label, Literal(item[0], lang='en'), graph_base))
			if 'Q' in item[1]:
				d.add((mentioned_person, OWL.sameAs, URIRef('https://www.wikidata.org/wiki/' + item[1]), graph_base))
			elif 'viaf' in item[1]:
				d.add((mentioned_person, OWL.sameAs, URIRef(item[1]), graph_base))





# TriG
d.serialize(destination="../../dataset/trig/quaderni_base-graph-E21.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/quaderni_base-graph-E21.nq", format='nquads')