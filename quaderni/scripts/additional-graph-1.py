# coding: utf-8

""" Graph 1 (purple):
Reconstruction of the relationships between Giuseppe Raimondi's notebooks and the published versions of the notebook texts (:notebook dcterms:relation :sbnubo-permalink). Last updated: 13 July 2021. 
By: Maria Chiara Tortora, 13 July 2021.
"""

from rdflib import Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, PROV
import csv
import re

# Create an empty Dataset
d = Dataset()

efrbroo = Namespace("http://erlangen-crm.org/efrbroo/")
ficlitdl = Namespace("https://w3id.org/ficlitdl/")
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")
np = Namespace("http://www.nanopub.org/nschema#")

# Add a namespace prefix to it, just like for Graph
d.bind('dcterms', DCTERMS)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1/'))
d.bind('prov', PROV)

# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub1/')

# Declare a Graph URI to be used to identify a Graph
graph_1 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_1, to the Dataset
d.graph(identifier=graph_1)

with open('../input/raimondi_q1_54-70_13-07-21-MCT.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall("(.+?) *$", row["\ufeffInventario"])
		collocazione = 'QUADERNI.1'
		specificazione = row["Specificazione"]
		sequenza = row["Sequenza"]
		permalink = row["Permalink"]

		series = URIRef(base_uri + 'record-set' + '/' + 'notebooks')

		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '-' + specificazione)
		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '-2')
		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '-3')

		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each notebook 
		rec_object = URIRef(record + 'object')
 		
 		# Declare a URI for each notebook text
		rec_expression = URIRef(record + 'text')

		


		# Add quads to graph1

		# Nanopublication
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# Provenance of the assertions
		d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2021-07-13' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0002-2972-3152'), URIRef(nanopub + 'provenance')))

		# Publication info
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1'), PROV.generatedAtTime, Literal('2023-01-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub1'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))

		if permalink:
			d.add((rec_object, DCTERMS.relation, URIRef(permalink), graph_1))
			d.add((rec_object, DCTERMS.relation, URIRef(permalink), graph_1))

			# Declare a URI for the manifestation
			manifestation = URIRef(base_uri + 'pub/' + re.findall('resource\/(.+?)\/UBO', permalink)[0])
			
			d.add((manifestation, RDF.type, efrbroo.F3_Manifestation_Product_Type, graph_1))
			d.add((manifestation, ficlitdlo.hasSbnUboPermalink, URIRef(permalink), graph_1))

			# Declare a URI for the publication expression
			pub_expression = URIRef(base_uri + 'pub-text/' + re.findall('resource\/(.+?)\/UBO', permalink)[0])

			d.add((pub_expression, RDF.type, efrbroo.F24_Publication_Expression, graph_1))
			d.add((pub_expression, efrbroo.R4_carriers_provided_by, manifestation, graph_1))


# TriG
d.serialize(destination="../output/trig/additional-graph-1.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/additional-graph-1.nq", format='nquads')