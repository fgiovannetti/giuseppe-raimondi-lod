# coding: utf-8

""" Base graph :
Articoli, E22 Human-Made Object
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

with open('../../input/articoli.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=';')
	for row in csv_reader:
		inventario =  re.findall('(.+?) *$', row['\ufeffInventario'])
		sezione = row['Sezione']
		collocazione = row['Collocazione']
		specificazione = row['Specificazione'] #?1954
		sequenza = row['Sequenza'] #00.00
		data_inv = row['Data inv.']
		identificativo = row['Id.']
		descrizione_isbd = row['Descrizione isbd'].replace('*', '')
		legami = re.findall("(.+?) *$", row["Legami con titoli superiori o supplementi"]) # HA PER ALTRO TITOLO

		series = URIRef(base_uri + 'record-set' + '/' + 'articles')

		if collocazione == 'ARTICOLI1':
			subseries = URIRef(series + '-1')
			file = URIRef(subseries + '/' + specificazione)
		elif collocazione == 'ARTICOLI2':
			subseries = URIRef(series + '-2')

		# Declare a URI for each record
		record = URIRef(base_uri + 'article/' + inventario[0].lower().replace(' ', '') + '/')

		# Declare a URI for each physical article
		rec_object = URIRef(record + 'object')
 		
		# Declare a URI for each article text
		rec_expression = URIRef(record + 'text')
		
	
		rec_label = re.findall('^(.+?) \/', descrizione_isbd)[0]

		




 		# Dimensions of physical object (height in cm, extent in number of pages and number of leaves)
		height = re.findall("; (\d+) cm.", row["Descrizione isbd"])
		extent_leaves = re.findall("\[?(\d+)\]? c\.", row["Descrizione isbd"])
		extent_leaves = [ int(x) for x in extent_leaves ] # from string to int
		extent_leaves = sum(extent_leaves)
		extent_pages = re.findall("\[?(\d+)\]? p\.", row["Descrizione isbd"])



		# Add quads to base-graph

		# # Nanopublication
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# # Provenance of the assertions
		# d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('1993-03' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		# d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), URIRef(nanopub + 'provenance')))

		# # Publication info
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), PROV.generatedAtTime, Literal('2022-02-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		# d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))


		########################
		#                      #
		# Article description  #
		#                      #
		########################

		d.add((rec_object, RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_base))
		
		# Label (it, en)
		d.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Articolo manoscritto, "' + rec_label + '"' , lang='it'), graph_base))
		d.add((rec_object, RDFS.label, Literal('Raimondi, Giuseppe. Manuscript article, "' + rec_label + '"' , lang='en'), graph_base))
		
		# Inventory number and shelfmark
		d.add((rec_object, ecrm.P1_is_identified_by, URIRef(record + 'inventory-number'), graph_base))
		d.add((rec_object, ecrm.P1_is_identified_by, URIRef(record + 'shelfmark'), graph_base))

		# Document type
		d.add((rec_object, ecrm.P2_has_type, ficlitdlo.article, graph_base))
		
		# Descrizione isbd
		d.add((rec_object, ecrm.P3_has_note, Literal(descrizione_isbd , lang='it'), graph_base))
		
		# Dimensioni (h, pagine manoscritte, carte)
		d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'height/' + height[0] + 'cm'), graph_base))
		d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'extent/' + str(extent_leaves) + 'c'), graph_base))
		if extent_pages:
			d.add((rec_object, ecrm.P43_has_dimension, URIRef(base_uri + 'extent/' + extent_pages[0] + 'p'), graph_base)) 


		# Fa parte di
		if collocazione == 'ARTICOLI1': # Fascicolo per anno
			d.add((rec_object, ecrm.P46i_forms_part_of, URIRef(file + '/object'), graph_base))
			d.add((rec_object, ficlitdlo.formsConceptuallyPartOf, URIRef(file), graph_base))
		else:
			d.add((rec_object, ecrm.P46i_forms_part_of, URIRef(subseries + '/object'), graph_base))
			d.add((rec_object, ficlitdlo.formsConceptuallyPartOf, URIRef(subseries), graph_base))

		# # Sequenza
		# if collocazione == 'QUADERNI.1':
		# 	if inventario[0] == 'RDq 84':
		# 		d.add((rec_object, seq.follows, URIRef(file + '/rdq83' + '/object'), graph_base))
		# 		d.add((rec_object, seq.precedes, URIRef(file + '/rdq85' + '/object'), graph_base))

		# 	elif inventario[0] == 'RDq 85':
		# 		d.add((rec_object, seq.follows, URIRef(file + '/rdq84' + '/object'), graph_base))
		# 		d.add((rec_object, seq.precedes, URIRef(file + '/rdq86' + '/object'), graph_base))

		# 	else: # RDq5, RDq 303-307 : mancano oggetti in sequenza ancora in mano agli eredi. Se il numero di sequenza precedente o successivo non esiste, la relazione non viene generata
		# 		seqn_prev = int(seqn) - 1
		# 		seqn_next = int(seqn) + 1
		# 		if str(seqn_prev) in invn_by_seqn[specificazione]:
		# 			d.add((rec_object, seq.follows, URIRef(base_uri + 'notebook/rdq' + invn_by_seqn[specificazione][str(seqn_prev)] + '/object'), graph_base))
		# 		if str(seqn_next) in invn_by_seqn[specificazione]:
		# 			d.add((rec_object, seq.precedes, URIRef(base_uri + 'notebook/rdq' + invn_by_seqn[specificazione][str(seqn_next)] + '/object'), graph_base))

		# if collocazione == 'QUADERNI.2':
		# 	if int(specificazione) > 1 :
		# 		spec_prev = int(specificazione) - 1
		# 		d.add((rec_object, seq.follows, URIRef(subseries + '/rdq' + invn_by_spec[str(spec_prev)] + '/object'), graph_base))
		# 	if int(specificazione) < 140 :
		# 		spec_next = int(specificazione) + 1
		# 		d.add((rec_object, seq.precedes, URIRef(subseries + '/rdq' + invn_by_spec[str(spec_next)] + '/object'), graph_base))			

		# Keeper, owner, location, and rights
		d.add((rec_object, ecrm.P50_has_current_keeper, URIRef('https://w3id.org/ficlitdl/org/unibo'), graph_base))
		d.add((rec_object, ecrm.P52_has_current_owner, URIRef('https://w3id.org/ficlitdl/org/ibc'), graph_base))
		d.add((rec_object, ecrm.P55_has_current_location, URIRef('https://w3id.org/ficlitdl/place/biblioteca-ezio-raimondi'), graph_base))
		d.add((rec_object, ecrm.P104_is_subject_to, URIRef('https://w3id.org/ficlitdl/right/' + 'all-rights-reserved'), graph_base))
		# Link to expression
		d.add((rec_object, ecrm.P128_carries, rec_expression, graph_base))

		# How to cite
		if sequenza == '00.00':
			d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + specificazione + '. Articolo manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione + '.'), graph_base))
		else:
			d.add((rec_object, DCTERMS.bibliographicCitation, Literal('Raimondi, Giuseppe. ' + specificazione + '. Articolo manoscritto. ' + 'Fondo Giuseppe Raimondi, Biblioteca Ezio Raimondi, Università di Bologna. ' + inventario[0] + ', ' + sezione + ' ' + collocazione + ' ' + specificazione + ' ' + sequenza + '.'), graph_base))




# TriG
d.serialize(destination="../../dataset/trig/articoli_base-graph-E22.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/articoli_base-graph-E22.nq", format='nquads')