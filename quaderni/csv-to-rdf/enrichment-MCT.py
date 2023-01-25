# coding: utf-8

# notebooks as human-made (physical) objects

# Fondo: Giuseppe Raimondi
	# Subfondo: Archivio
		# Serie: Quaderni
			# Sottoserie 1: Quaderni manoscritti 1954-1976
				# Fascicoli: dal 1954 al 1976
					# Quaderni: da RDq1 a RDq308
			# Sottoserie 2: Quaderni manoscritti 1915-1981
					# Quaderni: da RDq309 a RDq448
			# Sottoserie 3
					# Quaderni (anche'essi fascicoli e, dunque, a livello teorico, individui della classe E78 Curated Holding): da RDq449 (16 taccuini) a RDq460

# N.B. Inserti all'interno dei quaderni NON ESTRATTI per Omeka (parte dell'arricchimeno): carte ds./ms., fotografie, illustrazioni, volantini pubblicitari, biglietti di ingresso a mostre, ritagli di giornale, foglietti ms., ricevute di raccomandate, segnalibri

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

ecrm = Namespace("http://erlangen-crm.org/current/")
ficlitdlo = Namespace("https://w3id.org/ficlitdl/ontology/")
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')

g = Graph()

g.bind('ecrm', ecrm)
g.bind('dcterms', DCTERMS)
g.bind('ficlitdlo' , ficlitdlo)
g.bind('seq', seq)

base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Arricchimento WIP di Maria Chiara Tortora (relazione fra quaderni e schede OPAC delle pubblicazioni corrispondenti), aggiornato al 13 luglio 2021

with open('../input/raimondi_q1_54-70_13-07-21-MCT.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall("(.+?) *$", row["\ufeffInventario"])
		collocazione = 'QUADERNI.1'
		specificazione = row["Specificazione"]
		sequenza = row["Sequenza"]
		permalink = row["Permalink"]

		series = URIRef(base_uri + 'notebooks/')
		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '1/')
			file = URIRef(subseries + specificazione)
			record = URIRef(file + '/' + inventario[0].lower().replace(' ', '') + '/')
		# elif collocazione == 'QUADERNI.2':
		# 	subseries = URIRef(series + '2')
		# 	record = URIRef(subseries + '/' + inventario[0].lower().replace(' ', '') + '/')
		# elif collocazione == 'QUADERNI.3':
		# 	subseries = URIRef(series + '3')
		# 	record = URIRef(subseries + '/' + inventario[0].lower().replace(' ', '') + '/')

		# physical notebook URI
		rec_object = URIRef(record + 'object')

		if permalink:
			g.add((rec_object, DCTERMS.relation, URIRef(permalink)))

# RDF/XML
g.serialize(destination="../output/rdf/enrichment-MCT.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/enrichment-MCT.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/enrichment-MCT.jsonld", format='json-ld')