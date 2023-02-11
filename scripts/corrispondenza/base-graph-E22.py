# coding: utf-8

""" Base graph :
Corrispondenza, E22 Human-Made Object
Fascicoli (Record): 829 cartelline ordinate alfabeticamente per corrispondente
Unità documentarie: non inventariate, utilizziamo il campo 'Precisazione' per creare permalink dei singoli items (es. lettera, cartolina, biglietto, etc.)
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


		########################
		#                      #
		# File description     #
		#                      #
		########################

		d.add((file_object, RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
		
		# Label (it, en)
		d.add((file_object, RDFS.label, Literal(file_label_it , lang='it'), graph_base))
		d.add((file_object, RDFS.label, Literal(file_label_en , lang='en'), graph_base))
		
		# Inventory number and shelfmark
		d.add((file_object, ecrm.P1_is_identified_by, URIRef(file + '/inventory-number'), graph_base))
		d.add((file_object, ecrm.P1_is_identified_by, URIRef(file + '/shelfmark'), graph_base))

		# Document type
		d.add((file_object, ecrm.P2_has_type, ficlitdlo.file, graph_base))
		
		# Descrizione isbd
		d.add((file_object, ecrm.P3_has_note, Literal(descrizione_isbd , lang='it'), graph_base))

		# Dimensioni
		dimensions =  re.findall("(\d+) x (\d+) mm", descrizione_isbd)
		for x in range(len(dimensions)):
			d.add((file_object, ecrm.P43_has_dimension, URIRef(base_uri + 'width/' + dimensions[x][0] + 'mm'), graph_base))
			d.add((file_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + dimensions[x][1] + 'mm'), graph_base))

		# Fa parte di
		d.add((file_object, ecrm.P46i_forms_part_of, URIRef(series + '/object'), graph_base))
		d.add((file_object, ficlitdlo.formsConceptuallyPartOf, URIRef(series), graph_base))

		# Keeper, owner, location, and rights
		d.add((file_object, ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((file_object, ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((file_object, ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((file_object, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/' + 'all-rights-reserved'), graph_base))

		# How to cite
		if correspondent:
			d.add((file_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. Corrispondenza con ' + correspondent[0] + '. Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + specificazione + '.'), graph_base))
		else:
			d.add((file_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. Corrispondenza. Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + specificazione + '.'), graph_base))

		##########################################
		#                                        #
		#    Single document description         #
		#                                        #
		##########################################

		if precisazione:
			d.add((file_object, ecrm.P3_has_note, Literal(precisazione), graph_base))


			file_content = re.findall(" ?(.+?)\,", precisazione)
			for item in file_content:
				item_num = re.findall("(\d+)" , item)
				c = 1
				while c < int(item_num[0]):
					d.add((URIRef(file_object + '/' + str(c)), RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
					d.add((URIRef(file_object + '/' + str(c)), ecrm.P46i_forms_part_of, file_object, graph_base))
					d.add((URIRef(file_object + '/' + str(c)), ecrm.P128_carries, URIRef(file + '/text/' + str(c)), graph_base))
					if 'L' in item:
						d.add((URIRef(file_object + '/'+ str(c)), ecrm.P2_has_type, ficlitdlo.letter, graph_base))

					if 'C ' in item:
						d.add((URIRef(file_object + '/'+ str(c)), ecrm.P2_has_type, ficlitdlo.postcard, graph_base))

					if 'CI' in item:
						d.add((URIRef(file_object + '/'+ str(c)), ecrm.P2_has_type, URIRef('https://w3id.org/ficlitdl/ontology/illustrated-postcard'), graph_base))

					# other document types

					c +=1


		# Fascicoli di un unico documento
		else:
			d.add((URIRef(file_object + '/1'), RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
			d.add((URIRef(file_object + '/1'), ecrm.P46i_forms_part_of, file_object, graph_base))
			d.add((URIRef(file_object + '/1'), ecrm.P128_carries, URIRef(file + '/text/1'), graph_base))

			# type
			if re.search('\[\*[l|L]etter', descrizione_isbd) or re.search('[l|L]ettre', descrizione_isbd):
				d.add((file_object, ecrm.P3_has_note, Literal('L 1'), graph_base))
				d.add((URIRef(file_object + '/1'), ecrm.P2_has_type, ficlitdlo.letter, graph_base))

			if re.search('\[\*[c|C]artolin', descrizione_isbd):
				d.add((file_object, ecrm.P3_has_note, Literal('C 1'), graph_base))
				d.add((URIRef(file_object + '/1'), ecrm.P2_has_type, ficlitdlo.postcard, graph_base))

			if re.search('\[\*[b|B]igliett', descrizione_isbd):
				d.add((file_object, ecrm.P3_has_note, Literal('B 1'), graph_base))
				d.add((URIRef(file_object + '/1'), ecrm.P2_has_type, ficlitdlo.card, graph_base))

			if re.search('\[\*[t|T]elegramm', descrizione_isbd):
				d.add((file_object, ecrm.P3_has_note, Literal('T 1'), graph_base))
				d.add((URIRef(file_object + '/1'), ecrm.P2_has_type, ficlitdlo.telegram, graph_base))

			if re.search('\[[i|I]nvit', descrizione_isbd) or re.search('[p|P]artecipazione di nozze', descrizione_isbd):
				d.add((file_object, ecrm.P3_has_note, Literal('I 1'), graph_base))
				d.add((URIRef(file_object + '/1'), ecrm.P2_has_type, ficlitdlo.card, graph_base))

			if re.search('\[[r|R]icordo funebre', descrizione_isbd):
				d.add((file_object, ecrm.P3_has_note, Literal('RF 1'), graph_base))
				d.add((URIRef(file_object + '/1'), ecrm.P2_has_type, ficlitdlo.card, graph_base))
			
		

# TriG
d.serialize(destination="../../dataset/trig/corrispondenza_base-graph-E22.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/corrispondenza_base-graph-E22.nq", format='nquads')