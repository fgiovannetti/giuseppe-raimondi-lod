# coding: utf-8

""" Base graph :
Corrispondenza, E54 Dimension
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
		if correspondent:
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence between Giuseppe Raimondi and ' + correspondent[0]
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza fra Giuseppe Raimondi e ' + correspondent[0]
		elif re.search('[p|P]artecipazione di nozze', descrizione_isbd):
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence, Wedding participation addressed to Giuseppe Raimondi'
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza, Partecipazione di nozze indirizzata a Giuseppe Raimondi'
		elif re.search('[r|R]icordo funebre', descrizione_isbd):
			file_label_en = 'Giuseppe Raimondi Fonds, Archive, Correspondence, Funeral card addressed to Giuseppe Raimondi'
			file_label_it = 'Fondo Giuseppe Raimondi, Archivio, Corrispondenza, Ricordo funebre indirizzato a Giuseppe Raimondi'

 		# Add quads to base-graph

		# Dimensioni
		dimensions =  re.findall("(\d+) x (\d+) mm", descrizione_isbd)
		for x in range(len(dimensions)):

			d.add((URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), RDF.type, ecrm.E54_Dimension, graph_base))
			d.add((URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), RDFS.label, Literal('Altezza ' + dimensions[x][1] + ' mm', lang='it'), graph_base))
			d.add((URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), RDFS.label, Literal('Height ' + dimensions[x][1] + ' mm' , lang='en'), graph_base))
			d.add((URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), ecrm.P91_has_unit, ficlitdlo.millimetre, graph_base))
			d.add((URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), ecrm.P90_has_value, Literal(dimensions[x][1], datatype=XSD.integer), graph_base))
			d.add((URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), ecrm.P2_has_type, ficlitdlo.height, graph_base))
			
			d.add((URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), RDF.type, ecrm.E54_Dimension, graph_base))
			d.add((URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), RDFS.label, Literal('Base ' + dimensions[x][0] + ' mm', lang='it'), graph_base))
			d.add((URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), RDFS.label, Literal('Width ' + dimensions[x][0] + ' mm' , lang='en'), graph_base))
			d.add((URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), ecrm.P91_has_unit, ficlitdlo.millimetre, graph_base))
			d.add((URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), ecrm.P90_has_value, Literal(dimensions[x][0], datatype=XSD.integer), graph_base))
			d.add((URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), ecrm.P2_has_type, ficlitdlo.width, graph_base))



# TriG
d.serialize(destination="../../dataset/trig/corrispondenza_base-graph-E54.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/corrispondenza_base-graph-E54.nq", format='nquads')