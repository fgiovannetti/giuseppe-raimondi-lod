# coding: utf-8

""" Graph 6:
Representation of influence of Paul Valery's ouvre on Giuseppe Raimondi's production, Part 2
By: Francesca Giovannetti, 7 April 2023 (after Rossi, Federica, and Alina Wenzlawski. 2020. ‘Nello scrittoio di Giuseppe Raimondi: carte e libri di un letterato bolognese su Paul Valéry’. In Il privilegio della parola scritta: gestione, conservazione e valorizzazione di carte e libri di persona, edited by Giovanni Di Domenico and Fiammetta Sabba, 177–94. Roma: Associazione italiana biblioteche).
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
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub6/'))
d.bind("pro", pro)
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('oa', oa)
d.bind('seq', seq)

# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'
person = 'https://w3id.org/ficlitdl/person/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub6/')

# Declare a Graph URI to be used to identify a Graph
graph_6 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_6, to the Dataset
d.graph(identifier=graph_6)

		

# Nanopublication
d.add((URIRef(base_uri + 'nanopub/nanopub6'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
d.add((URIRef(base_uri + 'nanopub/nanopub6'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
d.add((URIRef(base_uri + 'nanopub/nanopub6'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
d.add((URIRef(base_uri + 'nanopub/nanopub6'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

# Provenance of the assertions
d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2023-04-07' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'provenance')))

# Publication info
d.add((URIRef(base_uri + 'nanopub/nanopub6'), PROV.generatedAtTime, Literal('2023-04-07' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
d.add((URIRef(base_uri + 'nanopub/nanopub6'), PROV.wasDerivedFrom, URIRef('https://doi.org/10.1400/276891'), URIRef(nanopub + 'pubinfo')))
d.add((URIRef(base_uri + 'nanopub/nanopub6'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))



# Add quads to graph6
# Queries: Giuseppe Raimondi read which works by or about Paul Valéry before writing a specific text? Which of these works is represented by a copy in Giuseppe Raimondi's library?

# G.R. annotating his copy of P.V.'s Préface.

annotext1 = BNode()
annotext2 = BNode()
annotext3 = BNode()

d.add((URIRef(base_uri + 'annotation/preface-1925/anno1') , RDF.type , oa.Annotation, graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1') , prism.hasStartingPage , Literal('100', datatype=XSD.integer), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1') , prism.hasEndingPage , Literal('100', datatype=XSD.integer), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1') , DCTERMS.creator , URIRef(person + 'giuseppe-raimondi'), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1') , oa.hasBody , annotext1, graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1') , oa.hasTarget , URIRef(base_uri + 'pub-text/preface-1925'), graph_6))
d.add((annotext1 , RDF.type , oa.TextualBody, graph_6))
d.add((annotext1 , RDF.value , Literal("Mostri, prodotti dei pensieri", datatype=XSD.string), graph_6))

d.add((URIRef(base_uri + 'annotation/preface-1925/anno2') , RDF.type , oa.Annotation, graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno2') , prism.hasStartingPage , Literal('100', datatype=XSD.integer), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno2') , prism.hasEndingPage , Literal('100', datatype=XSD.integer), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno2') , DCTERMS.creator , URIRef(person + 'giuseppe-raimondi'), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno2') , oa.hasBody , annotext2, graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno2') , oa.hasTarget , URIRef(base_uri + 'pub-text/preface-1925'), graph_6))
d.add((annotext2 , RDF.type , oa.TextualBody, graph_6))
d.add((annotext2 , RDF.value , Literal("Idee mostri", datatype=XSD.string), graph_6))

d.add((URIRef(base_uri + 'pub-text/preface-1925/page100') , RDF.value , Literal('100', datatype=XSD.integer), graph_6))


# Creation of G.R.'s article 'Mostro a due Teste' influenced by P.V.'s Préface.

d.add((URIRef(base_uri + 'pub-text/mostro-a-due-teste-1971/creation') , ecrm.P15_was_influenced_by , URIRef(base_uri + 'pub-text/preface-1925'), graph_6))

# G.R.'s article 'Mostro a due Teste' possibly reusing the author's handnotes from his personal copy of P.V.'s Préface (scholarly note).

d.add((URIRef(base_uri + 'pub-text/mostro-a-due-teste-1971/creation') , ecrm.P3_has_note , Literal("The newspaper article 'Mostro a due Teste' by Giuseppe Raimondi (in «Corriere della Sera», 28 ottobre 1971), was influence by Paul Valéry's 'Préface pour une nouvelle traduction de La Soiréè avec M. Teste' (in «Commerce», 1925, n. 4). Supporting evidence for this connection is provided by the presence of handwritten annotations by Giuseppe Raimondi on his copy of the 'Préface' (BIFICLIT, FR PER COMMER 1925, p. 100). Such annotations read 'Mostri, prodotti dei pensieri' and 'Idee mostri'. The article title 'Mostro a due Teste' is a possible reworking of these notes.", datatype=XSD.string), graph_6))


# Creation of the annotation 

d.add((URIRef(base_uri + 'annotation/preface-1925/anno1-anno2/creation') , ecrm.P94_has_created , URIRef(base_uri + 'annotation/preface-1925/anno1'), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1-anno2/creation') , ecrm.P94_has_created , URIRef(base_uri + 'annotation/preface-1925/anno2'), graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1-anno2/creation') , ecrm.P125_used_object_of_type , ficlitdlo.pencil, graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1-anno2/creation') , ecrm.P32_used_general_technique , ficlitdlo.handwriting, graph_6))
d.add((URIRef(base_uri + 'annotation/preface-1925/anno1-anno2/creation') , URIRef('http://erlangen-crm.org/current/P4_has_time-span') , URIRef(base_uri + 'time-span/1925-01-01_1925-03-30'), graph_6))





# TriG
d.serialize(destination="../../dataset/trig/additional-graph-6.trig", format='trig')

# N-Quads
d.serialize(destination="../../dataset/nquads/additional-graph-6.nq", format='nquads')