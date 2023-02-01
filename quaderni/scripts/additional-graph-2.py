# coding: utf-8

""" Graph 2 (green):
Reconstruction of the network of relationships that characterises the notebook "Una forca per il poeta François Villon" (RDq 303). 
By: Francesca Giovannetti, 30 January 2023.
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
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2/'))
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)

# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub2/')

# Declare a Graph URI to be used to identify a Graph
graph_2 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_2, to the Dataset
d.graph(identifier=graph_2)

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

		# Add quads to graph2

		# Nanopublication
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# Provenance of the assertions
		d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2023-01-30' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'provenance')))

		# Publication info
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2'), PROV.generatedAtTime, Literal('2023-01-30' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub2'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))

		# Declare a base URI for works
		work = URIRef(base_uri + 'work/')

		# Declare a base URI for publication expressions
		pub_text = URIRef(base_uri + 'pub-text/')

		# Date the notebook texts
		d.add((URIRef(base_uri + 'notebook/rdq303/text/1/creation'), efrbroo.R17_created, URIRef(base_uri + 'notebook/rdq303/text/1'), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/text/1/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/1976-05-24'), graph_2))
		d.add((URIRef(base_uri + 'time-span/1976-05-24'), RDFS.label, Literal('1976-05-24', datatype=XSD.date), graph_2))


		d.add((URIRef(base_uri + 'notebook/rdq303/text/2/creation'), efrbroo.R17_created, URIRef(base_uri + 'notebook/rdq303/text/2'), graph_2))	
		d.add((URIRef(base_uri + 'notebook/rdq303/text/2/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/1976-07-03'), graph_2))
		d.add((URIRef(base_uri + 'time-span/1976-07-03'), RDFS.label, Literal('1976-07-03', datatype=XSD.date), graph_2))


		d.add((URIRef(base_uri + 'notebook/rdq303/text/creation'), ecrm.P9_consists_of, URIRef(base_uri + 'notebook/rdq303/text/1/creation'), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/text/creation'), ecrm.P9_consists_of, URIRef(base_uri + 'notebook/rdq303/text/2/creation'), graph_2))


		# Declare the texts contained in the notebook
		d.add((URIRef(base_uri + 'notebook/rdq303/text'), ecrm.P165_incorporates, URIRef(base_uri + 'notebook/rdq303/text/1'), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/text'), ecrm.P165_incorporates, URIRef(base_uri + 'notebook/rdq303/text/2'), graph_2))

		d.add((URIRef(base_uri + 'notebook/rdq303/object'), ecrm.P128_carries, URIRef(base_uri + 'notebook/rdq303/text/1'), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/object'), ecrm.P128_carries, URIRef(base_uri + 'notebook/rdq303/text/2'), graph_2))

		d.add((URIRef(base_uri + 'notebook/rdq303/text/1'), ecrm.P102_has_title, URIRef(base_uri + 'notebook/rdq303/text/1/title'), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/text/2'), ecrm.P102_has_title, URIRef(base_uri + 'notebook/rdq303/text/2/title'), graph_2))

		d.add((URIRef(base_uri + 'notebook/rdq303/text/1/title'), RDF.value, Literal('Una forca per il poeta François Villon', lang="it"), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/text/2/title'), RDF.value, Literal('A proposito di tegole, di tetti e di fantasmi', lang="it"), graph_2))


		# Link the variant expressions to the work they realise
		d.add((URIRef(work + 'una-forca-per-il-poeta-francois-villon'), efrbroo.R3_realised_in, URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), graph_2))
		d.add((URIRef(work + 'una-forca-per-il-poeta-francois-villon'), efrbroo.R3_realised_in, URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), graph_2))

		d.add((URIRef(base_uri + 'notebook/rdq303/text/1'), ficlitdlo.hasVariantVersion, URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), graph_2))
		d.add((URIRef(base_uri + 'notebook/rdq303/text/1'), ficlitdlo.hasVariantVersion, URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), graph_2))


		# Relationships between different expressions of the same work
		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), RDF.type, efrbroo:F24_Publication_Expression, graph_2))
		d.add((URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), RDF.type, efrbroo:F24_Publication_Expression, graph_2))
		
		d.add((URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), ecrm.P148i_is_component_of, URIRef(pub_text + 'i-tetti-sulla-citta-19731976'), graph_2))
		d.add((URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), ficlitdlo.isPublishedVersionOf, URIRef(base_uri + 'notebook/rdq303/text/1'), graph_2))
		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), ficlitdlo.isPublishedVersionOf, URIRef(base_uri + 'notebook/rdq303/text/1'), graph_2))

		d.add((URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), ecrm.P102_has_title, URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon/title'), graph_2))
		d.add((URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon/title'), RDF.type, ecrm.E35_Title, graph_2))
		d.add((URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon/title'), RDF.value, Literal('Una forca per il poeta François Villon') , graph_2))


		# Relationships between different carriers of the variant expressions of the same work
		d.add((URIRef(base_uri + 'printed-volume/rl7137/object'), DCTERMS.relation, URIRef(base_uri + 'notebook/rdq303/object'), graph_2))
		d.add((URIRef(base_uri + 'printed-volume/rai5105/object'), DCTERMS.relation, URIRef(base_uri + 'notebook/rdq303/object'), graph_2))
		d.add((URIRef(base_uri + 'printed-volume/mc0571/object'), DCTERMS.relation, URIRef(base_uri + 'notebook/rdq303/object'), graph_2))

		# Relationships between carriers of the same publication expression
		d.add((URIRef(base_uri + 'printed-volume/rl7137/object'), ecrm.P128_carries, URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), graph_2))
		d.add((URIRef(base_uri + 'printed-volume/rai5105/object'), ecrm.P128_carries, URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), graph_2))
		d.add((URIRef(base_uri + 'printed-volume/mc0571/object'), ecrm.P128_carries, URIRef(pub_text + 'i-tetti-sulla-citta-19731976/una-forca-per-il-poeta-francois-villon'), graph_2))

		# Description of the published text "Gelo invernale e nostalgia di legna accesa", a variant version of "Una forca per il poeta François Villon" published in Il Giorno, 7 June 1976. 
		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), prism.publicationDate, Literal('1976-06-07', datatype=XSD.date), graph_2))
		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), DCTERMS.publisher, URIRef('https://w3id.org/ficlitdl/org/il-giorno'), graph_2))
		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607'), ecrm.P102_has_title, URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607/title'), graph_2))

		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607/title'), RDF.type, ecrm.E35_Title, graph_2))
		d.add((URIRef(pub_text + 'gelo-invernale-e-nostalgia-di-legna-accesa-19760607/title'), RDF.value, Literal('Gelo invernale e nostalgia di legna accesa') , graph_2))

		
		d.add((URIRef('https://w3id.org/ficlitdl/org/il-giorno'), RDF.type, ecrm.E40_Legal_Body, graph_2))
		d.add((URIRef('https://w3id.org/ficlitdl/org/il-giorno'), RDFS.label, Literal('Il Giorno'), graph_2))

		# Link another notebook carrying a text about Villon to the work of art it mentions (archive-museum interchange)
		d.add((URIRef(base_uri + 'notebook/rdq230/text'), ecrm.P67_refers_to, URIRef('https://collections.louvre.fr/ark:/53355/cl010066409'), graph_2))


# TriG
d.serialize(destination="../output/trig/additional-graph-2.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/additional-graph-2.nq", format='nquads')