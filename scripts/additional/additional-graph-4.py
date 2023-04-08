# coding: utf-8

""" Graph 4 (red):
Representation of author's revision of short story title "Dei colombi in una facciata"
By: Francesca Giovannetti, 8 February 2023.
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
oa = Namespace('http://www.w3.org/ns/oa#')
seq = Namespace('http://www.ontologydesignpatterns.org/cp/owl/sequence.owl#')

# Add a namespace prefix to it, just like for Graph
d.bind('dcterms', DCTERMS)
d.bind('ecrm', ecrm)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4/'))
d.bind('prov', PROV)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('oa', oa)
d.bind('seq', seq)

# Declare a base URI for the Giuseppe Raimondi Fonds 
base_uri = 'https://w3id.org/giuseppe-raimondi-lod/'
person = 'https://w3id.org/ficlitdl/person/'

# Declare a URI for the nanopub
nanopub = URIRef(base_uri + 'nanopub/nanopub4/')

# Declare a Graph URI to be used to identify a Graph
graph_4 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_3, to the Dataset
d.graph(identifier=graph_4)

		

# Nanopublication
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

# Provenance of the assertions
d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2023-02-08' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'provenance')))

# Publication info
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4'), PROV.generatedAtTime, Literal('2023-02-08' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub4'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))



# Add quads to graph3

# Description of three alternative titles of short story as witnessed by the notebook
# E35 Title specialises E90 Symbolic Object

d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , RDF.type , URIRef('http://erlangen-crm.org/efrbroo/F22_Self-Contained_Expression'), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , DCTERMS.identifier , URIRef(base_uri + 'notebook/rdq2' + '/text/2'), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ecrm.P2_has_type , URIRef('https://w3id.org/ficlitdl/ontology/short-story'), graph_4)) 
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ecrm.P165i_is_incorporated_in , URIRef(base_uri + 'notebook/rdq2' + '/text'), graph_4)) 
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ecrm.P102_has_title, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1'), graph_4)) 
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ecrm.P102_has_title, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2'), graph_4)) 
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ecrm.P102_has_title, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3'), graph_4)) 
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ficlitdlo.hasPublishedVersion , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata'), graph_4)) 
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2') , ficlitdlo.hasPublishedVersion , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata'), graph_4)) 

d.add((URIRef(base_uri + 'notebook/rdq2' + '/text') , ficlitdlo.hasTrascription, URIRef(base_uri + 'notebook/rdq2' + '/text/xml-tei'), graph_4))


# Titles/Variants description
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1') , RDF.value, Literal("L'anno '43"), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1') , RDF.type, ecrm.E35_Title, graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1') , RDF.type, ecrm.E90_Symbolic_Object, graph_4))

# Locating the variant within the text
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1') , ecrm.P106i_forms_part_of, URIRef(base_uri + 'notebook/rdq2' + '/text/2'), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1') , oa.hasSource, URIRef(base_uri + 'notebook/rdq2' + '/text/xml-tei'), graph_4))
var1_selector = BNode()
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1') , oa.hasSelector, var1_selector, graph_4))
d.add((var1_selector , RDF.type, oa.XPathSelector, graph_4))
d.add((var1_selector , RDF.value, Literal('//line[@xml:id="ln-227"]'), graph_4))




d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2') , RDF.value, Literal("I piccioni di Santa Lucia"), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2') , RDF.type, ecrm.E35_Title, graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2') , RDF.type, ecrm.E90_Symbolic_Object, graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2') , ecrm.P106i_forms_part_of, URIRef(base_uri + 'notebook/rdq2' + '/text/2'), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2') , oa.hasSource, URIRef(base_uri + 'notebook/rdq2' + '/text/xml-tei'), graph_4))
var2_selector = BNode()
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2') , oa.hasSelector, var2_selector, graph_4))
d.add((var2_selector , RDF.type, oa.XPathSelector, graph_4))
d.add((var2_selector , RDF.value, Literal('//line[@xml:id="ln-6"]'), graph_4))

d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , RDF.value, Literal("Dei colombi in una facciata"), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , RDF.type, ecrm.E35_Title, graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , RDF.type, ecrm.E90_Symbolic_Object, graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , ecrm.P2_has_note, Literal("Tit. a c. [9]."), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , ecrm.P106i_forms_part_of, URIRef(base_uri + 'notebook/rdq2' + '/text/2'), graph_4))
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , oa.hasSource, URIRef(base_uri + 'notebook/rdq2' + '/text/xml-tei'), graph_4))
var3_selector = BNode()
d.add((URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3') , oa.hasSelector, var3_selector, graph_4))
d.add((var3_selector , RDF.type, oa.XPathSelector, graph_4))
d.add((var3_selector , RDF.value, Literal('//line[@xml:id="ln-226"]'), graph_4))


# Representing textual variation (= annotation on text transcription)

d.add((URIRef(base_uri + 'textvar-1') , RDF.type, ficlitdlo.TextualVariation, graph_4))
d.add((URIRef(base_uri + 'textvar-1') , ficlitdlo.hasVariantReading, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1'), graph_4))
d.add((URIRef(base_uri + 'textvar-1') , ficlitdlo.hasVariantReading, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2'), graph_4))
d.add((URIRef(base_uri + 'textvar-1') , ficlitdlo.hasVariantReading, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3'), graph_4))

# Textual variation as a result of authorial revision	

d.add((URIRef(base_uri + 'textrev-1') , RDF.type, ficlitdlo.TextRevision, graph_4))
d.add((URIRef(base_uri + 'textrev-1') , ecrm.P2_has_type, ficlitdlo.deletion, graph_4))
d.add((URIRef(base_uri + 'textrev-1') , ecrm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi'), graph_4))
d.add((URIRef(base_uri + 'textrev-1') , ficlitdlo.deleted, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/1'), graph_4))
d.add((URIRef(base_uri + 'textrev-1') , ficlitdlo.resultedIn, URIRef(base_uri + 'textvar-1'), graph_4))


d.add((URIRef(base_uri + 'textrev-2') , RDF.type, ficlitdlo.TextRevision, graph_4))
d.add((URIRef(base_uri + 'textrev-2') , ecrm.P2_has_type, ficlitdlo.addition, graph_4))
d.add((URIRef(base_uri + 'textrev-2') , ecrm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi'), graph_4))
d.add((URIRef(base_uri + 'textrev-2') , ficlitdlo.added, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/2'), graph_4))
d.add((URIRef(base_uri + 'textrev-2') , ficlitdlo.resultedIn, URIRef(base_uri + 'textvar-1'), graph_4))


d.add((URIRef(base_uri + 'textrev-3') , RDF.type, ficlitdlo.TextRevision, graph_4))
d.add((URIRef(base_uri + 'textrev-3') , ecrm.P2_has_type, ficlitdlo.addition, graph_4))
d.add((URIRef(base_uri + 'textrev-3') , ecrm.P14_carried_out_by, URIRef(person + 'giuseppe-raimondi'), graph_4))
d.add((URIRef(base_uri + 'textrev-3') , ficlitdlo.added, URIRef(base_uri + 'notebook/rdq2' + '/text/2/title/3'), graph_4))
d.add((URIRef(base_uri + 'textrev-3') , ficlitdlo.resultedIn, URIRef(base_uri + 'textvar-1'), graph_4))


d.add((URIRef(base_uri + 'textrev-1') , seq.precedes, URIRef(base_uri + 'textrev-2'), graph_4))
d.add((URIRef(base_uri + 'textrev-2') , seq.precedes, URIRef(base_uri + 'textrev-3'), graph_4))
d.add((URIRef(base_uri + 'textrev-3') , seq.follows, URIRef(base_uri + 'textrev-2'), graph_4))
d.add((URIRef(base_uri + 'textrev-2') , seq.follows, URIRef(base_uri + 'textrev-1'), graph_4))


# Description of published versions (Comunità 1954 and Mignon 1955)

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata') , RDF.type , efrbroo.E24_Publication_Expression, graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata/title'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata') , DCTERMS.identifier , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata'), graph_4))


d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata/title') , RDF.type , ecrm.E35_Title, graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/dei-colombi-in-una-facciata/title') , RDF.value , Literal('Dei colombi in una facciata'), graph_4))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25') , prism.publicationDate , Literal('1954-06', datatype=XSD.date), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25') , DCTERMS.publisher , URIRef('https://w3id.org/ficlitdl/edizioni-di-comunita'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/title'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25') , ecrm.P128i_is_carried_by , URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl6683/object'), graph_4))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl6683/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl6683/object'), ecrm.P1_is_identified_by, URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl6683/shelfmark'), graph_4))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl6683/shelfmark'), RDFS.label, Literal('FR PER COMUNI 1954'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl6683/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_4))


d.add((URIRef('https://w3id.org/ficlitdl/edizioni-di-comunita'), RDF.type, ecrm.E40_Legal_Body, graph_4))
d.add((URIRef('https://w3id.org/ficlitdl/edizioni-di-comunita'), RDFS.label, Literal('Edizioni di comunità'), graph_4))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/title'), RDF.type, ecrm.E35_Title, graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/comunita-1954-25/title'), RDF.value, Literal('Comunità: rivista mensile del Movimento Comunità'), graph_4))


d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata') , RDF.type , efrbroo.E24_Publication_Expression, graph_4)) 
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955'), graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata/title'), graph_4))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata/title') , RDF.type , ecrm.E35_Title, graph_4))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mignon-racconti-1955/dei-colombi-in-una-facciata/title') , RDF.value , Literal('Dei colombi in una facciata'), graph_4))



# TriG
d.serialize(destination="../../dataset/trig/additional-graph-4.trig", format='trig')


# N-Quads
#d.serialize(destination="../../dataset/nquads/additional-graph-4.nq", format='nquads')