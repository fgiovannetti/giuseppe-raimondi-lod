# coding: utf-8

""" Base graph :
Corrispondenza, F28 Expression Creation
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

with open('../../input/corrispondenza.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] 
		data_inv = row['Data inv.']
		identificativo = row['Id.']
		precisazione = row['Precisazione inventario']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"]) # HA PER ALTRO TITOLO

		# N.B. Riconciliazione dei corrispondenti via OpenRefine
		correspondent = re.findall("\/ (.+?)\. [\-\|[?]", descrizione_isbd)

		# URI Serie Corrispondenza
		series = URIRef(base_uri + 'record-set' + '/' + 'correspondence')
		series_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence'
		series_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza'

		# URI Fascicolo per corrispondente
		specificazione = specificazione.replace('[', '').replace(']', '').replace('?', '')
		file = URIRef(base_uri + 'record-set/corresp-' + specificazione.lower() + '/' + inventario[0].lower().replace(' ', ''))
		file_object = URIRef(file + '/object')
		file_text = URIRef(file + '/text')
		if correspondent:
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence between Giuseppe Raimondi and ' + correspondent[0]
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza fra Giuseppe Raimondi e ' + correspondent[0]
		elif re.search('[p|P]artecipazione di nozze', descrizione_isbd):
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence, Wedding participation addressed to Giuseppe Raimondi'
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza, Partecipazione di nozze indirizzata a Giuseppe Raimondi'
		elif re.search('[r|R]icordo funebre', descrizione_isbd):
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence, Funeral card addressed to Giuseppe Raimondi'
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza, Ricordo funebre indirizzato a Giuseppe Raimondi'

		timespan = re.findall('\. \- (\[?\d.+?)\. \-', descrizione_isbd)
		
		person = URIRef('https://w3id.org/ficlitdl/person/')


		# Add quads to base-graph

		if precisazione:
			file_content = re.findall(" ?(.+?)\,", precisazione)
			for item in file_content:
				item_num = re.findall("(\d+)" , item)
				c = 1
				while c < int(item_num[0]):
					d.add((URIRef(file_text + '/' + str(c) + '/creation'), RDF.type, efrbroo.F28_Expression_Creation, graph_base))
					d.add((URIRef(file_text + '/' + str(c) + '/creation'), efrbroo.R17_created, URIRef(file_text + '/' + str(c)), graph_base))
					d.add((URIRef(file_text + '/' + str(c) + '/creation'), efrbroo.R18_created, URIRef(file_object + '/' + str(c)), graph_base))
					d.add((URIRef(file_text + '/' + str(c) + '/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + timespan[0]), graph_base))
					if correspondent:
						correspondent_id = correspondent[0].lower().replace(' ', '-')
						d.add((URIRef(file_text + '/' + str(c) + '/creation'), ecrm.P14_carried_out_by, URIRef(person + correspondent_id), graph_base))
					elif 'R ' in item:
						d.add((URIRef(file_text + '/' + str(c) + '/creation'), ecrm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi'), graph_base))

					c +=1


		# Fascicoli di un unico documento
		else:
			d.add((URIRef(file_text + '/1' + '/creation'), RDF.type, efrbroo.F28_Expression_Creation, graph_base))
			d.add((URIRef(file_text + '/1' + '/creation'), efrbroo.R17_created, URIRef(file_text + '/1'), graph_base))
			d.add((URIRef(file_text + '/1' + '/creation'), efrbroo.R18_created, URIRef(file_object + '/1'), graph_base))
			d.add((URIRef(file_text + '/1' + '/creation'), URIRef('http://erlangen-crm.org/current/P4_has_time-span'), URIRef(base_uri + 'time-span/' + timespan[0]), graph_base))
			if correspondent:
				correspondent_id = correspondent[0].lower().replace(' ', '-')
				d.add((URIRef(file_text + '/1' + '/creation'), ecrm.P14_carried_out_by, URIRef(person + correspondent_id), graph_base))



	


# TriG
d.serialize(destination="../../dataset/trig/corrispondenza_base-graph-F28.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/corrispondenza_base-graph-F28.nq", format='nquads')