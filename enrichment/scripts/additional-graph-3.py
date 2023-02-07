# coding: utf-8

""" Graph 3 (blue):
References to named entities from the finding aid (this same extraction will need to be done on transcriptions once available). 
By: Francesca Giovannetti, 14 November 2022.
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

# Add a namespace prefix to it, just like for Graph
d.bind('dcterms', DCTERMS)
d.bind('ecrm', ecrm)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3/'))
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)

# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub3/')

# Declare a Graph URI to be used to identify a Graph
graph_3 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_3, to the Dataset
d.graph(identifier=graph_3)

my_dict = {}

with open('../input/ner_output_person.tsv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter='\t')
	for row in csv_reader:

		inventario = row["inventario"].lower().replace(' ', '')
		wd = row["wikidata"]
		wd_code = row["wikidata_code"]

		my_dict[inventario] = list()
		my_dict[inventario].append((wd, wd_code))

		record = URIRef(base_uri + 'notebook/' + inventario + '/')

 		# Declare a URI for each notebook text
		rec_expression = URIRef(record + 'text')

		# Declare a URI for each mentioned person
		person = URIRef('https://w3id.org/ficlitdl/' + 'person/')

		


		# Add quads to graph3

		# Nanopublication
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# Provenance of the assertions
		d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2022-11-14' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'provenance')))

		# Publication info
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3'), PROV.generatedAtTime, Literal('2023-01-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub3'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))


		for item in my_dict[inventario]:
			mentioned_person = URIRef(person + item[0].lower().replace(' ', '-').replace('.', '').replace(',', '').replace('è', 'e').replace('é', 'e').replace('à', 'a').replace('á', 'a').replace('ö', 'o').replace('ç', 'c'))
			d.add((rec_expression, ecrm.P67_refers_to, mentioned_person, graph_3))


# TriG
d.serialize(destination="../output/trig/additional-graph-3.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/additional-graph-3.nq", format='nquads')