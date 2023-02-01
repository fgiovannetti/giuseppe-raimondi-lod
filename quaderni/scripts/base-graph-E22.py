# coding: utf-8

""" Base graph :
Quaderni, E22 Human-Made Object
N.B. Inseriti all'interno dei quaderni: carte ds./ms., fotografie, illustrazioni, volantini pubblicitari, biglietti di ingresso a mostre, ritagli di giornale, foglietti ms., ricevute di raccomandate, segnalibri
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
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd']
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"])

		series = URIRef(base_uri + 'record-set' + '/' + 'notebooks')

		if collocazione == 'QUADERNI.1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '-' + specificazione)
		elif collocazione == 'QUADERNI.2':
			subseries = URIRef(series + '-2')
		elif collocazione == 'QUADERNI.3':
			subseries = URIRef(series + '-3')

		# Declare a URI for each record
		record = URIRef(base_uri + 'notebook/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical notebook
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each notebook text
		rec_expression = URIRef(record + 'text')
		
		rec_label = re.findall('^(.+?) \/? \[?G(iuseppe)?\.? Raimondi', descrizione_isbd)[0]






 		# Dimensions of physical object (height in cm, extent in number of pages and number of leaves)
		height = re.findall("; +(\d+) cm.", row["Descrizione isbd"])
		extent_leaves = re.findall("su (\d+) +c+.", row["Descrizione isbd"])
		extent_pages = re.findall("(\d+) +p.", row["Descrizione isbd"])

		


		# Add quads to base-graph

		# Nanopublication
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# Provenance of the assertions
		d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('1993-03' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), URIRef(nanopub + 'provenance')))

		# Publication info
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), PROV.generatedAtTime, Literal('2022-02-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))


		########################
		#                      #
		# Notebook description #
		#                      #
		########################

		d.add((rec_object, RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
		
		# Label (it, en)
		# E.g.: Raimondi, Giuseppe. Quaderno manoscritto, "Sotto Villa Aldini. (Agosto 1958) ; I viaggi di Brandi. (8.9.58)"
		d.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Quaderno manoscritto, "' + rec_label[0].replace('*', '') + '"' , lang='it'), graph_base))
		d.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript notebook, "' + rec_label[0].replace('*', '') + '"' , lang='en'), graph_base))
		
		# Inventory number and shelfmark
		d.add((rec_object, ecrm.P1_is_identified_by, URIRef(record + 'inventory-number'), graph_base))
		d.add((rec_object, ecrm.P1_is_identified_by, URIRef(record + 'shelfmark'), graph_base))

		# Document type (notebooks are regarded both as items and files)
		d.add((rec_object, ecrm.P2_has_type, ficlitdlo.notebook, graph_base))
		# d.add((rec_object, ecrm.P2_has_type, ficlitdlo.file, graph_base))
		
		# Descrizione isbd
		d.add((rec_object, ecrm.P3_has_note, Literal(descrizione_isbd.replace('*', '') , lang='it'), graph_base))
		
		# Dimensioni (h, pagine manoscritte, carte)
		if '449' in inventario[0]: 
			d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + '10-19' + 'cm'), graph_base))
		else:
			d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + height[0] + 'cm'), graph_base))
			d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), graph_base)) 
			d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'extent/' + extent_leaves[0] + 'c'), graph_base))

		# Fa parte di
		if collocazione == 'QUADERNI.1':
			d.add((rec_object, ecrm.P46i_forms_part_of, URIRef(file + '/object'), graph_base))
			d.add((rec_object, ficlitdlo.formsConceptuallyPartOf, URIRef(file), graph_base))
		else:
			d.add((rec_object, ecrm.P46i_forms_part_of, URIRef(subseries + '/object'), graph_base))
			d.add((rec_object, ficlitdlo.formsConceptuallyPartOf, URIRef(subseries), graph_base))

		# Sequenza
		if collocazione == 'QUADERNI.1':
			if inventario[0] == 'RDq 84':
				d.add((rec_object, seq.follows, URIRef(file + '/rdq83' + '/object'), graph_base))
				d.add((rec_object, seq.precedes, URIRef(file + '/rdq85' + '/object'), graph_base))

			elif inventario[0] == 'RDq 85':
				d.add((rec_object, seq.follows, URIRef(file + '/rdq84' + '/object'), graph_base))
				d.add((rec_object, seq.precedes, URIRef(file + '/rdq86' + '/object'), graph_base))

			else: # RDq5, RDq 303-307 : mancano oggetti in sequenza ancora in mano agli eredi. Se il numero di sequenza precedente o successivo non esiste, la relazione non viene generata
				seqn_prev = int(seqn) - 1
				seqn_next = int(seqn) + 1
				if str(seqn_prev) in invn_by_seqn[specificazione]:
					d.add((rec_object, seq.follows, URIRef(base_uri + 'notebook/rdq' + invn_by_seqn[specificazione][str(seqn_prev)] + '/object'), graph_base))
				if str(seqn_next) in invn_by_seqn[specificazione]:
					d.add((rec_object, seq.precedes, URIRef(base_uri + 'notebook/rdq' + invn_by_seqn[specificazione][str(seqn_next)] + '/object'), graph_base))

		if collocazione == 'QUADERNI.2':
			if int(specificazione) > 1 :
				spec_prev = int(specificazione) - 1
				d.add((rec_object, seq.follows, URIRef(subseries + '/rdq' + invn_by_spec[str(spec_prev)] + '/object'), graph_base))
			if int(specificazione) < 140 :
				spec_next = int(specificazione) + 1
				d.add((rec_object, seq.precedes, URIRef(subseries + '/rdq' + invn_by_spec[str(spec_next)] + '/object'), graph_base))			

		# Keeper, owner, location, and rights
		d.add((rec_object, ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((rec_object, ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), graph_base))
		d.add((rec_object, ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((rec_object, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/' + 'all-rights-reserved'), graph_base))
		# Link to overall expression
		d.add((rec_object, ecrm.P128_carries, rec_expression, graph_base))
		# Link to single expressions
		if ' ; ' in rec_label[0]:
			rec_label = rec_label[0].split(' ; ')
			i = 1
			for title in rec_label:
				# Declare a URI for each notebook subtext
				rec_subexpression = URIRef(rec_expression + '/' + str(i))
				d.add((rec_object, ecrm.P128_carries, rec_subexpression, graph_base))

		# How to cite
		if collocazione == 'QUADERNI.1':
			d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + specificazione.replace('[', '').replace(']', '') + '. Quaderno manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + ' ' + sequenza + '.'), graph_base))
		elif collocazione == 'QUADERNI.2':
			d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + '. Quaderno manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione.replace('[', '').replace(']', '') + '.'), graph_base))
		elif '449' in inventario[0]:
			d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + '. Taccuini. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + '.'), graph_base))
		else:
			d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + '. Quaderno manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + '.'), graph_base))
		




# TriG
d.serialize(destination="../output/trig/base-graph-E22.trig", format='trig')

# N-Quads
d.serialize(destination="../output/nquads/base-graph-E22.nq", format='nquads')