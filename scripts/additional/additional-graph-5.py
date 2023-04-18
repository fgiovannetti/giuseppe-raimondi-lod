# coding: utf-8

""" Graph 5:
Representation of influence of Paul Valery's ouvre on Giuseppe Raimondi's production, Part 1
By: Francesca Giovannetti, 8 February 2023.
"""

from rdflib import Dataset, URIRef, Literal, Namespace, BNode
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, PROV, RDFS
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
d.bind('grlod-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5/'))
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
nanopub = URIRef(base_uri + 'nanopub/nanopub5/')

# Declare a Graph URI to be used to identify a Graph
graph_5 = URIRef(nanopub + 'assertion')

# Add an empty Graph, identified by graph_5, to the Dataset
d.graph(identifier=graph_5)

		

# Nanopublication
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5'), RDF.type, np.Nanopublication, URIRef(nanopub + 'head')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5'), np.hasAssertion, URIRef(nanopub + 'assertion'), URIRef(nanopub + 'head')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5'), np.hasProvenance, URIRef(nanopub + 'provenance'), URIRef(nanopub + 'head')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5'), np.hasPublicationInfo, URIRef(nanopub + 'pubinfo'), URIRef(nanopub + 'head')))

# Provenance of the assertions
d.add((URIRef(nanopub + 'assertion'), PROV.generatedAtTime, Literal('2023-04-04' , datatype=XSD.date), URIRef(nanopub + 'provenance')))
d.add((URIRef(nanopub + 'assertion'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'provenance')))

# Publication info
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5'), PROV.generatedAtTime, Literal('2023-04-04' , datatype=XSD.date), URIRef(nanopub + 'pubinfo')))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub5'), PROV.wasAttributedTo, URIRef('https://orcid.org/0000-0001-6007-9118'), URIRef(nanopub + 'pubinfo')))



# Add quads to graph5

# Texts by Giuseppe Raimondi related to P. Valéry



# Giuseppe Raimondi, Divagazioni intorno a Paul Valéry, «Il Convegno», 2/3, 1925, p. 90-97.

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925') , prism.publicationDate , Literal('1925-03-30', datatype=XSD.date), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-convegno-1925-2-3'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925/title') , RDF.value , Literal('Divagazioni intorno a Paul Valéry'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925'), graph_5))
d.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/divagazioni-intorno-a-paul-valery-1925' + '/author'), graph_5))

d.add((URIRef(base_uri + 'pub-text/divagazioni-intorno-a-paul-valery-1925/creation') , RDF.type , efrbroo.E28_Expression_Creation, graph_5))
d.add((URIRef(base_uri + 'pub-text/divagazioni-intorno-a-paul-valery-1925/creation') , efrbroo.R17_created , URIRef(base_uri + 'pub-text/divagazioni-intorno-a-paul-valery-1925'), graph_5))



# Giuseppe Raimondi, Ringraziamento a Commerce, «Il Convegno», 9, 1925, p. 487-491.

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925') , prism.publicationDate , Literal('1925-10-30', datatype=XSD.date), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-convegno-1925-9'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925/title') , RDF.value , Literal('Ringraziamento a Commerce'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925'), graph_5))
d.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/ringraziamento-a-commerce-1925' + '/author'), graph_5))

d.add((URIRef(base_uri + 'pub-text/ringraziamento-a-commerce-1925/creation') , RDF.type , efrbroo.E28_Expression_Creation, graph_5))
d.add((URIRef(base_uri + 'pub-text/ringraziamento-a-commerce-1925/creation') , efrbroo.R17_created , URIRef(base_uri + 'pub-text/ringraziamento-a-commerce-1925'), graph_5))


# Giuseppe Raimondi, Il cartesiano signor Teste. Firenze: Edizioni di Solaria, 1928.

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928') , DCTERMS.publisher , URIRef('https://w3id.org/ficlitdl/org/edizioni-di-solaria'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928') , prism.publicationDate , Literal('1928', datatype=XSD.gYear), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928/title') , RDF.value , Literal('Il cartesiano signor Teste'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928'), graph_5))
d.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/il-cartesiano-signor-teste-1928' + '/author'), graph_5))

d.add((URIRef(base_uri + 'pub-text/il-cartesiano-signor-teste-1928/creation') , RDF.type , efrbroo.E28_Expression_Creation, graph_5))
d.add((URIRef(base_uri + 'pub-text/il-cartesiano-signor-teste-1928/creation') , efrbroo.R17_created , URIRef(base_uri + 'pub-text/il-cartesiano-signor-teste-1928'), graph_5))


# Giuseppe Raimondi, Mostro a due Teste, «Corriere della Sera», 28 ottobre 1971.

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971') , DCTERMS.publisher , URIRef('https://w3id.org/ficlitdl/org/corriere-della-sera'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971') , prism.publicationDate , Literal('1971-10-28', datatype=XSD.date), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/corriere-della-sera-1971-10-28'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971/title') , RDF.value , Literal('Mostro a due Teste'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971'), graph_5))
d.add((URIRef(person + 'giuseppe-raimondi'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/mostro-a-due-teste-1971' + '/author'), graph_5))

d.add((URIRef(base_uri + 'pub-text/mostro-a-due-teste-1971/creation') , RDF.type , efrbroo.E28_Expression_Creation, graph_5))
d.add((URIRef(base_uri + 'pub-text/mostro-a-due-teste-1971/creation') , efrbroo.R17_created , URIRef(base_uri + 'pub-text/mostro-a-due-teste-1971'), graph_5))




# Texts by or about P. Valéry (in Giuseppe Raimondi's personal archive)

# Paul Valéry, Préface pour une nouvelle traduction de La Soiréè avec M. Teste in «Commerce», 4, 1925, p. 93-102, BIFICLIT, FR PER COMMER 1925, RL 7034

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925/title'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925/title') , RDF.value , Literal('Préface pour une nouvelle traduction de La Soiréè avec M. Teste'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925'), graph_5))
d.add((URIRef(person + 'paul-valery'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/preface-1925' + '/author'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4') , prism.publicationDate , Literal('1925', datatype=XSD.gYear), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4') , ecrm.P128i_is_carried_by , URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl7034/object'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl7034/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl7034/object'), ecrm.P1_is_identified_by, URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl7034/shelfmark'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl7034/shelfmark'), RDFS.label, Literal('FR PER COMMER 1925'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl7034/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4/title'), RDF.type, ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/commerce-1925-4/title'), RDF.value, Literal('Commerce: cahiers trimestriels, 1925, 4'), graph_5))


# Paul Valéry, La Soiréè avec Monsieur Teste, «Vers et Prose», 4 (décembre 1905, janvier-février 1906), p. 69-83, BFICLIT, FR LS 2085 dic 1905, RL 4472 (Dono di Giuseppe Ungaretti a G.R.)

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906') , ecrm.P165i_is_incorporated_in , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906/title'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906/title') , RDF.value , Literal('La Soiréè avec Monsieur Teste'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906'), graph_5))
d.add((URIRef(person + 'paul-valery'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-soiréè-avec-monsieur-teste-1906' + '/author'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4') , prism.publicationDate , Literal('1906', datatype=XSD.gYear), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4') , ecrm.P128i_is_carried_by , URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl4472/object'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl4472/object'), RDF.type, URIRef('http://erlangen-crm.org/current/E22_Human-Made_Object'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl4472/object'), ecrm.P1_is_identified_by, URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl4472/shelfmark'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl4472/shelfmark'), RDFS.label, Literal('FR LS 2085 dic 1905'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/periodical/rl4472/shelfmark'), ecrm.P2_has_type, ficlitdlo.shelfmark, graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4/title'), RDF.type, ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/verse-et-prose-1906-4/title'), RDF.value, Literal('Vers et prose, décembre 1905, janvier-février 1906, 4'), graph_5))


# Jean Prévost, La pensée de Paul Valéry, Nimes: Fabre, 1926, BIFICLIT, FR LS 1872, RL 4251 (Inviato da R. Franchi a G. R.)

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926') ,DCTERMS.publisher , URIRef('https://w3id.org/ficlitdl/org/fabre'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926') , prism.publicationDate , Literal('1926', datatype=XSD.gYear), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926/title') , RDF.value , Literal('La pensée de Paul Valéry'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926'), graph_5))
d.add((URIRef(person + 'jean-prevost'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/la-pensee-de-paul-valery-1926' + '/author'), graph_5))



# Paul Valéry, Monsieur Teste, Paris: Cres, 1927, BIFICLIT, FR LS 1879, RL 4163

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927') , RDF.type , efrbroo.F24_Publication_Expression, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927') , ecrm.P102_has_title , URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927/title'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927') , DCTERMS.publisher , URIRef('https://w3id.org/ficlitdl/org/cres'), graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927') , prism.publicationDate , Literal('1927', datatype=XSD.gYear), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927/title') , RDF.type , ecrm.E35_Title, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927/title') , RDF.value , Literal('Monsieur Teste'), graph_5))

d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927' + '/author'), RDF.type, pro.RoleInTime, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927' + '/author'), pro.withRole, pro.author, graph_5))
d.add((URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927' + '/author'), pro.relatesToEntity, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927'), graph_5))
d.add((URIRef(person + 'paul-valery'), pro.holdsRoleInTime, URIRef('https://w3id.org/giuseppe-raimondi-lod/pub-text/monsieur-teste-1927' + '/author'), graph_5))


d.add((URIRef(person + 'giuseppe-raimondi'), RDFS.label, Literal('Giuseppe Raimondi'), graph_5))
d.add((URIRef(person + 'paul-valery'), RDFS.label, Literal('Paul Valéry'), graph_5))
d.add((URIRef(person + 'jean-prevost'), RDFS.label, Literal('Jean Prévost'), graph_5))






# TODO

# Aggiorna diagrammi su GraphDB sulla base delle triple effettivamente create.

# Per UC4 Crea diagramma e triple: [Raffaello Franchi sending G.R. a copy of J. Prévost's La pensée de P.V. oppure scambio GR e PV]

# Queries per verificare correttezza dati per ciascun UC (UC3 e UC4)

# Modifiche generali a dataset
# NB holds role in time per tutti gli item che non sono quaderni mi pare che manchi dal dataset generale, aggiungi
# NB manca base_uri + 'time-span/' etichetta time-span in alcuni casi, aggiungi (e usa underscore per time intervals)
# NB appunta in tesi di ricontrollare ontologia sulla base dell'UC3

# Aggiungi UC3 e UC4 a Evaluation Chapter

# Aggiorna capitolo modello










# TriG
d.serialize(destination="../../dataset/trig/additional-graph-5.trig", format='trig')


# N-Quads
d.serialize(destination="../../dataset/nquads/additional-graph-5.nq", format='nquads')