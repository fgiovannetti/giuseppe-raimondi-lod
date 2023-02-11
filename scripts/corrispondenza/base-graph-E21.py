# coding: utf-8

""" Base graph :
FICLITDL, E21 Person
"""

from rdflib import Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, PROV
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
pro = Namespace("http://purl.org/spar/pro/")
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
d.bind('ficlitdl-np', URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base/'))
d.bind("owl", OWL)
d.bind('prov', PROV)
d.bind("pro", pro)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('seq', seq)
d.bind('ti', ti)
d.bind('tvc', tvc)


# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'

# Declare a URI for the nanopub
nanopub = URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base/')

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

		
		# Ruolo di sender/recipient attribuito a GR o ai vari corrispondenti == arricchimento, non è possibile estrarlo automaticamente per il singolo documento

		# Descrizione dei corrispondenti 
		correspondent = re.findall("\/ (.+?)\. [\-\|[?]", descrizione_isbd)
		if correspondent:
			correspondent_id = correspondent[0].lower().replace(' ', '-')
			d.add((URIRef(person + correspondent_id), RDF.type, ecrm.E21_Person, graph_base))
			d.add((URIRef(person + correspondent_id), RDFS.label, Literal(correspondent[0], lang='it'), graph_base))
			d.add((URIRef(person + correspondent_id), RDFS.label, Literal(correspondent[0], lang='en'), graph_base))
			# Da disambiguare OpenRefine
			# d.add((URIRef(person + correspondent_id), OWL.sameAs, URIRef('')))



# Add quads to base-graph

		# # Nanopublication
		# d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
		# d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

		# # Provenance of the assertions
		# d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('1993-03' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
		# d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://w3id.org/ficlitdl/org/sab-ero'), URIRef(nanopub + 'provenance')))

		# # Publication info
		# d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), PROV.generatedAtTime, Literal('2022-02-28' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
		# d.add((URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))




# TriG
d.serialize(destination="../../dataset/trig/corrispondenza_base-graph-E21.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/corrispondenza_base-graph-E21.nq", format='nquads')