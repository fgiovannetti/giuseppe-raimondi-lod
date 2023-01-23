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

crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')

g = Graph()

g.bind('crm', crm)
g.bind('dcterms', DCTERMS)
g.bind('seq', seq)

# base_uri = 'https://w3id.org/ficlitdl/' # da eliminare
# base_uri_grf = base_uri + 'giuseppe-raimondi-fonds/a/'
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/' # da eliminare
base_uri_grf = base_uri

# Sequenza QUADERNI.1 (specificata in Sequenza)
invn_by_seqn = {}
# {'anno': {'sequenza' : 'invn', 'sequenza' : 'invn', ...}, 'anno' : {...}}
# {'1954': {'1': '1', '2': '2', '3': '3', '4': '4', '6': '5', '7': '6', '8': '7', '9': '8', '10': '9', '11': '10', '12': '11', '13': '12', '14': '13', '15': '14', '16': '15'}, '1955': {'1': '16', '2': '17', '3': '18', '4': '19', '5': '20', '6': '21', '7': '22', '8': '23', '9': '24', '10': '25', '11': '26', '12': '27', '13': '28', '14': '29', '15': '30', '16': '31', '17': '32'}, '1956': {'1': '33', '2': '34', '3': '35', '4': '36', '5': '37', '6': '38', '7': '39', '8': '40', '9': '41', '10': '42', '11': '43', '12': '44', '13': '45', '14': '46', '15': '47', '16': '48', '17': '49', '18': '50'}, '1957': {'1': '51', '2': '52', '3': '53', '4': '54', '5': '55', '6': '56', '7': '57', '8': '58', '9': '59', '10': '60', '11': '61', '12': '62', '13': '63', '14': '64', '15': '65', '16': '66', '17': '67', '18': '68', '19': '69'}, '1958': {'1': '70', '2': '71', '3': '72', '4': '73', '5': '74', '6': '75', '7': '76', '8': '77', '9': '78', '10': '79', '11': '80', '12': '81', '13': '82', '14': '83', '15': '85', '16': '86', '17': '87', '18': '88', '19': '89', '20': '90', '21': '91', '22': '92'}, '1959': {'1': '93', '2': '94', '3': '95', '4': '96', '5': '97', '6': '98', '7': '99', '8': '100', '9': '101', '10': '102', '11': '103', '12': '104', '13': '105', '14': '106', '15': '107', '16': '108', '17': '109', '19': '110', '20': '111', '21': '112', '18': '135'}, '1960': {'1': '113', '2': '114', '3': '115', '4': '116', '5': '117', '6': '118', '7': '119', '8': '120', '9': '121', '10': '122', '11': '123', '12': '124', '13': '125', '14': '126', '16': '127', '15': '128', '17': '129', '18': '130'}, '1961': {'1': '131', '2': '132', '3': '133', '4': '134', '5': '136', '6': '137', '7': '138', '8': '139', '9': '140', '10': '141', '11': '142', '12': '143', '13': '144', '14': '145', '16': '146', '17': '147', '18': '148', '19': '149', '20': '150', '21': '151', '15': '162'}, '1962': {'1': '152', '2': '153', '3': '154', '4': '155', '5': '156', '6': '157', '7': '158', '8': '159', '9': '160', '10': '161', '11': '163', '12': '164', '13': '165', '14': '166', '15': '167', '16': '168', '17': '169', '18': '170'}, '1963': {'1': '171', '2': '172', '3': '173', '4': '174', '5': '175', '6': '176', '8': '177', '9': '178', '10': '179', '11': '180', '13': '181', '7': '182', '14': '183', '15': '184', '16': '185', '17': '186', '18': '187', '19': '188', '21': '189', '20': '190'}, '1964': {'1': '191', '2': '192', '3': '193', '4': '194', '5': '195', '6': '196', '7': '197', '8': '198', '9': '199', '10': '200', '11': '201'}, '1965': {'1': '202', '2': '203', '3': '204', '4': '205', '5': '206', '6': '207', '7': '208', '8': '209', '9': '210', '10': '211', '11': '212', '12': '213', '13': '214', '14': '215'}, '1966': {'1': '216', '2': '217', '3': '218', '4': '219', '5': '220', '6': '221', '7': '222', '8': '223', '9': '224', '10': '225', '11': '226'}, '1967': {'1': '227', '2': '228', '3': '229', '4': '230', '5': '231', '6': '232', '7': '233', '8': '234', '9': '235', '10': '236'}, '1968': {'1': '237', '4': '238', '5': '239', '6': '240', '2': '241', '3': '242', '7': '243', '8': '244', '9': '245', '10': '246', '11': '247', '12': '248'}, '1969': {'1': '249', '2': '250', '3': '251', '4': '252', '5': '253', '6': '254', '7': '255', '8': '256', '9': '257', '10': '258'}, '1970': {'1': '259', '2': '260', '3': '261', '4': '262', '5': '263', '6': '264'}, '1971': {'1': '265', '2': '266', '3': '267', '4': '268', '5': '269', '6': '270', '7': '271'}, '1972': {'15': '272', '14': '273', '1': '274', '2': '275', '3': '276', '4': '277', '5': '278', '6': '279', '7': '280', '8': '281', '9': '282', '10': '283', '11': '284', '12': '285', '13': '286'}, '1973': {'1': '287', '2': '288', '3': '289', '4': '290', '5': '291', '6': '292', '7': '293'}, '1974': {'1': '294', '2': '295', '3': '296'}, '1975': {'1': '297', '2': '298', '3': '299', '4': '300', '5': '308'}, '1976': {'1': '301', '2': '302', '3': '303', '7': '304', '8': '305', '9': '306', '6': '307'}}

# Sequenza QUADERNI.2 (specificata in Specificazione)
invn_by_spec = {}

with open('../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall("(.+?) *$", row["\ufeffInventario"])
		invn = re.findall('(\d+)' , inventario[0])
		specificazione = row['Specificazione']
		if row['Collocazione'] == 'QUADERNI.1':
			invn_by_seqn[specificazione] = {}
		if row['Collocazione'] == 'QUADERNI.2':
			invn_by_spec[specificazione] = invn[0]

with open('../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		if row['Collocazione'] == 'QUADERNI.1':		
			inventario =  re.findall("(.+?) *$", row["\ufeffInventario"])
			specificazione = row["Specificazione"]
			sequenza = row['Sequenza']
			seqn = sequenza.replace('[' , '').replace(']' , '').replace('?' , '').replace(' ' , '')
			seqn = re.sub('0(\d)', r'\1', seqn)
			invn = re.findall('(\d+)' , inventario[0])
			invn_by_seqn[specificazione][seqn] = invn[0]

with open('../input/quaderni.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione']
		sequenza = row['Sequenza']
		#TODO
		#data_inv = row['Data inv.']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd']
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])

		series = URIRef(base_uri_grf + 'record-set' + '/' + 'notebooks')

		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '-' + specificazione)
		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '-2')
		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '-3')

		record = URIRef(base_uri_grf + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# physical notebook URI
		rec_object = URIRef(record + 'object')
 		
 		# expression URI
		rec_expression = URIRef(record + 'text')


		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]

 		# dimensions of physical object (height in cm, extent in number of pages and number of leaves)
		height = re.findall("; +(\d+) cm.", row["Descrizione isbd"])
		extent_leaves = re.findall("su (\d+) +c+.", row["Descrizione isbd"])
		extent_pages = re.findall("(\d+) +p.", row["Descrizione isbd"])


		########################
		#                      #
		# Notebook description #
		#                      #
		########################


		g.add((rec_object, RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/E22_Human-Made_Object')))

		# Permalink (for Omeka S)
		g.add((rec_object, DCTERMS.identifier, rec_object))
		
		# Label (it, en)
		# E.g.: Raimondi, Giuseppe. Quaderno manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		g.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Quaderno manoscritto, "' + rec_label[0].replace('*', '') + '"' , lang='it')))
		g.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript notebook, "' + rec_label[0].replace('*', '') + '"' , lang='en')))
		
		# Inventory number and shelfmark
		g.add((rec_object, crm.P1_is_identified_by, URIRef(record + 'inventory-number')))
		g.add((rec_object, crm.P1_is_identified_by, URIRef(record + 'shelfmark')))

		# Document type (notebooks are regarded both as items and files)
		g.add((rec_object, crm.P2_has_type, URIRef(base_uri + 'document-type/notebook')))
		g.add((rec_object, crm.P2_has_type, URIRef(base_uri + 'archival-unit-type/file')))
		
		# Descrizione isbd
		g.add((rec_object, crm.P3_has_note, Literal(descrizione_isbd.replace('*', '') , lang='it')))
		
		# Dimensioni (h, pagine manoscritte, carte)
		if '449' in inventario[0]: 
			g.add((rec_object, crm.P43_has_dimension, URIRef(base_uri + 'height/' + '10-19' + 'cm')))
		else:
			g.add((rec_object, crm.P43_has_dimension, URIRef(base_uri + 'height/' + height[0] + 'cm')))
			g.add((rec_object, crm.P43_has_dimension, URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'))) 
			g.add((rec_object, crm.P43_has_dimension, URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c')))

		# Fa parte di
		if collocazione == 'QUADERNI.1':
			g.add((rec_object, crm.P46i_forms_part_of, URIRef(file + '/object')))
		else:
			g.add((rec_object, crm.P46i_forms_part_of, URIRef(subseries + '/object')))

		# Sequenza
		if collocazione == 'QUADERNI.1':
			if inventario[0] == 'RDq 84':
				g.add((rec_object, seq.follows, URIRef(file + '/rdq83' + '/object')))
				g.add((rec_object, seq.precedes, URIRef(file + '/rdq85' + '/object')))

			elif inventario[0] == 'RDq 85':
				g.add((rec_object, seq.follows, URIRef(file + '/rdq84' + '/object')))
				g.add((rec_object, seq.precedes, URIRef(file + '/rdq86' + '/object')))

			else: # RDq5, RDq 303-307 : mancano oggetti in sequenza ancora in mano agli eredi. Se il numero di sequenza precedente o successivo non esiste, la relazione non viene generata
				seqn_prev = int(seqn) - 1
				seqn_next = int(seqn) + 1
				if str(seqn_prev) in invn_by_seqn[specificazione]:
					g.add((rec_object, seq.follows, URIRef(base_uri_grf + 'notebook/rdq' + invn_by_seqn[specificazione][str(seqn_prev)] + '/object')))
				if str(seqn_next) in invn_by_seqn[specificazione]:
					g.add((rec_object, seq.precedes, URIRef(base_uri_grf + 'notebook/rdq' + invn_by_seqn[specificazione][str(seqn_next)] + '/object')))

		if collocazione == 'QUADERNI.2':
			if int(specificazione) > 1 :
				spec_prev = int(specificazione) - 1
				g.add((rec_object, seq.follows, URIRef(subseries + '/rdq' + invn_by_spec[str(spec_prev)] + '/object')))
			if int(specificazione) < 140 :
				spec_next = int(specificazione) + 1
				g.add((rec_object, seq.precedes, URIRef(subseries + '/rdq' + invn_by_spec[str(spec_next)] + '/object')))			

		# Keeper, owner, location, and rights
		g.add((rec_object, crm.P50_has_current_keeper, URIRef(base_uri + 'organization/' + 'alma-mater-studiorum-university-of-bologna')))
		g.add((rec_object, crm.P52_has_current_owner, URIRef(base_uri + 'organization/' + 'istituto-per-i-beni-artistici-culturali-e-naturali')))
		g.add((rec_object, crm.P55_has_current_location, URIRef(base_uri + 'place/' + 'biblioteca-ezio-raimondi')))
		g.add((rec_object, crm.P104_is_subject_to, URIRef(base_uri + 'right/' + 'all-rights-reserved')))
		
		# Link to overall expression
		g.add((rec_object, crm.P128_carries, rec_expression))

		# How to cite
		if collocazione == 'QUADERNI.1':
			g.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + specificazione.replace('[', '').replace(']', '') + '. Quaderno manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza + '.')))
		elif collocazione == 'QUADERNI.2':
			g.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + '. Quaderno manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + '.')))
		elif '449' in inventario[0]:
			g.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + '. Taccuini. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + '.')))
		else:
			g.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + '. Quaderno manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + '.')))

# Arricchimento WIP di Maria Chiara Tortora (relazione fra quaderni e schede OPAC delle pubblicazioni corrispondenti), aggiornato al 13 luglio 2021

with open('../input/raimondi_q1_54-70_13-07-21.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall("(.+?) *$", row["\ufeffInventario"])
		collocazione = 'QUADERNI.1'
		specificazione = row["Specificazione"]
		sequenza = row["Sequenza"]
		permalink = row["Permalink"]

		series = URIRef(base_uri_grf + 'notebooks/')
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
g.serialize(destination="../output/rdf/fr-a-quaderni-E22.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/fr-a-quaderni-E22.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/fr-a-quaderni-E22.jsonld", format='json-ld')