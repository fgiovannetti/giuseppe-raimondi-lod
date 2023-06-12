# coding: utf-8

""" Graph 7:
Letters sent by Paul Valéry to Giuseppe Raimondi
By: Francesca Giovannetti, 09 June 2023 (after Rossi, Federica, and Alina Wenzlawski. 2020. ‘Nello scrittoio di Giuseppe Raimondi: carte e libri di un letterato bolognese su Paul Valéry’. In Il privilegio della parola scritta: gestione, conservazione e valorizzazione di carte e libri di persona, edited by Giovanni Di Domenico and Fiammetta Sabba, 177–94. Roma: Associazione italiana biblioteche).
"""

from rdflib import Dataset, URIRef, Literal, Namespace, BNode
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
pro = Namespace("http://purl.org/spar/pro/")
oa = Namespace('http://www.w3.org/ns/oa#')
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')

# Add a namespace prefix to it, just like for Graph
d.bind('dcterms', DCTERMS)
d.bind('ecrm', ecrm)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub7/'))
d.bind("pro", pro)
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('oa', oa)
d.bind('seq', seq)

# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'
person = 'https://w3id.org/ficlitdl/person/'
place = 'https://w3id.org/ficlitdl/place/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub7/')

# Declare a Graph URI to be used to identify a Graph
graph_7 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_7, to the Dataset
d.graph(identifier=graph_7)

		

# Nanopublication
d.add((URIRef(base_uri + 'nanopub/nanopub7'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
d.add((URIRef(base_uri + 'nanopub/nanopub7'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
d.add((URIRef(base_uri + 'nanopub/nanopub7'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
d.add((URIRef(base_uri + 'nanopub/nanopub7'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

# Provenance of the assertions
d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2023-06-09' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'provenance')))

# Publication info
d.add((URIRef(base_uri + 'nanopub/nanopub7'), PROV.generatedAtTime, Literal('2023-06-09' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
d.add((URIRef(base_uri + 'nanopub/nanopub7'), PROV.wasDerivedFrom, URIRef('https://doi.org/10.1400/276891'), URIRef(nanopub + 'pubinfo')))
d.add((URIRef(base_uri + 'nanopub/nanopub7'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))



# Add quads to graph_7

# Letter 1

d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , RDF.type , ficlitdlo.CorrespondenceActivity, graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , ficlitdlo.hadSender , URIRef(person + 'paul-valery'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , ficlitdlo.hadReceiver , URIRef(person + 'giuseppe-raimondi'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , ficlitdlo.hadDateOfDispatch , Literal('1925-05-17' , datatype=XSD.date), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , ficlitdlo.hadPlaceOfOrigin , URIRef(place + 'paris'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , ficlitdlo.hadPlaceOfDestination , URIRef(place + 'bologna'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/1') , ficlitdlo.sent , URIRef(base_uri + 'letter/rdm831/object/1'), graph_7))


d.add((URIRef(base_uri + 'letter/rdm831/object/1') , ecrm.P128_carries , URIRef(base_uri + 'letter/rdm831/text/1'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/object/1') , ecrm.P46i_forms_part_of , URIRef(base_uri + 'record-set/album-valery/rdm831/object'), graph_7))


d.add((URIRef(base_uri + 'letter/rdm831/text/1') , ecrm.P72_has_language , URIRef('http://id.loc.gov/vocabulary/iso639-2/ita'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/1') , ficlitdlo.hasTrascription , URIRef(base_uri + 'letter/rdm831/text/1/xml-tei'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/1') , ficlitdlo.hasPublishedVersion , URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955/lettera-di-paul-valery-19250517'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/1') , ecrm.P67_refers_to , URIRef(base_uri + 'pub-text/divagazioni-intorno-a-paul-valery-1925'), graph_7))

d.add((URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955'), ecrm.P148_has_component , URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955/lettera-di-paul-valery-19250517'), graph_7))







# Letter 2

d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , RDF.type , ficlitdlo.CorrespondenceActivity, graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , ficlitdlo.hadSender , URIRef(person + 'paul-valery'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , ficlitdlo.hadReceiver , URIRef(person + 'giuseppe-raimondi'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , ficlitdlo.hadDateOfDispatch , Literal('1925-10-06' , datatype=XSD.date), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , ficlitdlo.hadPlaceOfOrigin , URIRef(place + 'paris'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , ficlitdlo.hadPlaceOfDestination , URIRef(place + 'bologna'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/2') , ficlitdlo.sent , URIRef(base_uri + 'letter/rdm831/object/2'), graph_7))


d.add((URIRef(base_uri + 'letter/rdm831/object/2') , ecrm.P128_carries , URIRef(base_uri + 'letter/rdm831/text/2'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/object/2') , ecrm.P46i_forms_part_of , URIRef(base_uri + 'record-set/album-valery/rdm831/object'), graph_7))


d.add((URIRef(base_uri + 'letter/rdm831/text/2') , ecrm.P72_has_language , URIRef('http://id.loc.gov/vocabulary/iso639-2/ita'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/2') , ficlitdlo.hasTrascription , URIRef(base_uri + 'letter/rdm831/text/3/xml-tei'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/2') , ficlitdlo.hasPublishedVersion , URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955/lettera-di-paul-valery-19251006'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/2') , ecrm.P67_refers_to , URIRef(base_uri + 'pub-text/ringraziamento-a-commerce-1925'), graph_7))

d.add((URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955'), ecrm.P148_has_component , URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955/lettera-di-paul-valery-19251006'), graph_7))






# Letter 3

d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , RDF.type , ficlitdlo.CorrespondenceActivity, graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , ficlitdlo.hadSender , URIRef(person + 'paul-valery'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , ficlitdlo.hadReceiver , URIRef(person + 'giuseppe-raimondi'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , ficlitdlo.hadDateOfDispatch , Literal('1928-06-03' , datatype=XSD.date), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , ficlitdlo.hadPlaceOfOrigin , URIRef(place + 'paris'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , ficlitdlo.hadPlaceOfDestination , URIRef(place + 'bologna'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/corresp-act/3') , ficlitdlo.sent , URIRef(base_uri + 'letter/rdm831/object/3'), graph_7))


d.add((URIRef(base_uri + 'letter/rdm831/object/3') , ecrm.P128_carries , URIRef(base_uri + 'letter/rdm831/text/3'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/object/3') , ecrm.P46i_forms_part_of , URIRef(base_uri + 'record-set/album-valery/rdm831/object'), graph_7))


d.add((URIRef(base_uri + 'letter/rdm831/text/3') , ecrm.P72_has_language , URIRef('http://id.loc.gov/vocabulary/iso639-2/ita'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/3') , ficlitdlo.hasTrascription , URIRef(base_uri + 'letter/rdm831/text/3/xml-tei'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/3') , ficlitdlo.hasPublishedVersion , URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955/lettera-di-paul-valery-19280603'), graph_7))
d.add((URIRef(base_uri + 'letter/rdm831/text/3') , ecrm.P67_refers_to , URIRef(base_uri + 'pub-text/il-cartesiano-signor-teste-1928'), graph_7))

d.add((URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955'), ecrm.P148_has_component , URIRef(base_uri + 'pub-text/la-valigia-delle-indie-1955/lettera-di-paul-valery-19280603'), graph_7))







# TriG
d.serialize(destination="../../dataset/trig/additional-graph-7.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/additional-graph-7.nq", format='nquads')