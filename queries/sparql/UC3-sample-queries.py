import csv
import rdflib
from rdflib import Graph, Dataset, URIRef, Literal, Namespace, ConjunctiveGraph
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, PROV





 



d = rdflib.ConjunctiveGraph()
# d.parse("../../dataset/trig/quaderni_base-graph-E10.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E13.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E21.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E22.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E30.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E35.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E40.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E42.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E45.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E52.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E53.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E54.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E78.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E89.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-F22.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-F28.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-RIT.trig" , format="trig")
# d.parse("../../dataset/trig/additional-graph-1.trig" , format="trig")
# d.parse("../../dataset/trig/additional-graph-2.trig" , format="trig")
# d.parse("../../dataset/trig/additional-graph-3.trig" , format="trig")
# d.parse("../../dataset/trig/additional-graph-4.trig" , format="trig")
d.parse("../../dataset/trig/additional-graph-5.trig" , format="trig")
d.parse("../../dataset/trig/additional-graph-6.trig" , format="trig")
# d.parse("../../dataset/trig/libri_base-graph-F24.trig" , format="trig")
# d.parse("../../dataset/trig/libri_base-graph-E22.trig" , format="trig")
# d.parse("../../dataset/trig/libri_base-graph-E35.trig" , format="trig")
# d.parse("../../dataset/trig/libri_base-graph-E42.trig" , format="trig")


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
oa = Namespace("http://www.w3.org/ns/oa#")

d.bind('dcterms', DCTERMS)
d.bind('ecrm', ecrm)
d.bind("efrbroo", efrbroo)
d.bind('ficlitdl', ficlitdl)
d.bind('ficlitdlo', ficlitdlo)
d.bind('np', np)
d.bind('ficlitdl-np', URIRef('https://w3id.org/ficlitdl/nanopub/nanopub-base/'))
d.bind('grl-np', URIRef('https://w3id.org/giuseppe-raimondi-lod/nanopub/nanopub-base/'))
d.bind("owl", OWL)
d.bind('prov', PROV)
d.bind("pro", pro)
d.bind('rdfs', RDFS)
d.bind('prism', prism)
d.bind('seq', seq)
d.bind('ti', ti)
d.bind('tvc', tvc)
d.bind('oa', oa)


# Q1 All texts that influenced Giuseppe Raimondi's work
query_1 = """
SELECT DISTINCT ?influencingtxt
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/giuseppe-raimondi> AS ?graimondi)
        ?creation efrbroo:R17_created ?influencedtxt ;
            ecrm:P15_was_influenced_by ?influencingtxt . 
        ?graimondi pro:holdsRoleInTime ?rit .
        ?rit pro:relatesToEntity ?influencedtxt .    
    }
"""

# Print results to CSV file
with open('../results/UC3_Q1-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Texts that influenced Giuseppe Raimondi\'s work'])
    for influencingtxt in d.query(query_1):
        my_writer.writerow(influencingtxt)


# Q2 Texts that influenced specific texts by Giuseppe Raimondi
query_2 = """
SELECT DISTINCT ?influencedtxt ?influencingtxt
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/giuseppe-raimondi> AS ?graimondi)
        ?creation efrbroo:R17_created ?influencedtxt ;
            ecrm:P15_was_influenced_by ?influencingtxt . 
        ?graimondi pro:holdsRoleInTime ?rit .
        ?rit pro:relatesToEntity ?influencedtxt .    
    }
"""

# Print results to CSV file
with open('../results/UC3_Q2-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Influenced Text by Giuseppe Raimondi' , 'Influencing Text'])
    for influencedtxt , influencingtxt in d.query(query_2):
        my_writer.writerow([influencedtxt , influencingtxt])


# Q3 Works by or about Paul Valéry that Raimondi read before writing a specific text
query_3 = """
SELECT DISTINCT ?influencedtxt ?influencingtxt
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/giuseppe-raimondi> AS ?graimondi)
        BIND(<https://w3id.org/ficlitdl/person/paul-valery> AS ?pvalery)
        ?readingact ficlitdlo:relatesToText ?influencingtxt ;
            ecrm:P14_carried_out_by ?graimondi .
        ?creation efrbroo:R17_created ?influencedtxt ;
            ecrm:P15_was_influenced_by ?influencingtxt .  
    }
"""

# Print results to CSV file
with open('../results/UC3_Q3-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text by Giuseppe Raimondi' , 'Text read by Giuseppe Raimondi'])
    for influencedtxt , influencingtxt in d.query(query_3):
        my_writer.writerow([influencedtxt , influencingtxt])



# Q4 Which of these works has a copy in Giuseppe Raimondi's library?
query_4 = """
SELECT DISTINCT ?influencingtxt ?colloc
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/giuseppe-raimondi> AS ?graimondi)
        BIND(<https://w3id.org/ficlitdl/person/paul-valery> AS ?pvalery)
        ?creation efrbroo:R17_created ?influencedtxt ;
            ecrm:P15_was_influenced_by ?influencingtxt . 
        ?graimondi pro:holdsRoleInTime ?rit .
        ?rit pro:relatesToEntity ?influencedtxt .
        ?influencingtxt ecrm:P165i_is_incorporated_in ?periodical .
        ?periodical ecrm:P128i_is_carried_by ?exemplar .
        ?exemplar ecrm:P1_is_identified_by ?shelfmark .
        ?shelfmark rdfs:label ?colloc .
    }
"""

# Print results to CSV file
with open('../results/UC3_Q4-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text by Giuseppe Raimondi' , 'Exemplar of the published text in Giuseppe Raimondi\'s library'])
    for influencingtxt , colloc in d.query(query_4):
        my_writer.writerow([influencingtxt , colloc])



# Q5 Date on which Raimondi is most likely to have read a specific text
query_5 = """
SELECT DISTINCT ?influencingtxt ?readingdate
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/giuseppe-raimondi> AS ?graimondi)
        BIND(<https://w3id.org/ficlitdl/person/paul-valery> AS ?pvalery)
        ?readingact ficlitdlo:relatesToText ?influencingtxt ;
            ecrm:P14_carried_out_by ?graimondi ;
            <http://erlangen-crm.org/current/P4_has_time-span> ?readingdate .
        ?creation efrbroo:R17_created ?influencedtxt ;
            ecrm:P15_was_influenced_by ?influencingtxt .  
    }
"""

# Print results to CSV file
with open('../results/UC3_Q5-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text read by Giuseppe Raimondi' , 'When they were read'])
    for influencingtxt , readingdate in d.query(query_5):
        my_writer.writerow([influencingtxt , readingdate])




# Q6 All annotations on a specific copy of a publication
query_6 = """
SELECT DISTINCT ?pubtxt ?annotxt
    WHERE {
        ?anno rdf:type oa:Annotation;
            oa:hasBody [rdf:value ?annotxt] ;
            oa:hasTarget ?pubtxt .  
    }
"""

# Print results to CSV file
with open('../results/UC3_Q6-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Annotated text' , 'Annotation'])
    for pubtxt , annotxt in d.query(query_6):
        my_writer.writerow([pubtxt , annotxt])



# Q7 Locations of the annotations
query_7 = """
SELECT DISTINCT ?pubtxt ?annotxt ?page
    WHERE {
        ?anno rdf:type oa:Annotation;
            oa:hasBody [rdf:value ?annotxt] ;
            oa:hasTarget ?pubtxt ;
            prism:hasEndingPage ?page ;
    }
"""

# Print results to CSV file
with open('../results/UC3_Q7-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Annotated text' , 'Annotation' , 'Page'])
    for pubtxt , annotxt, page in d.query(query_7):
        my_writer.writerow([pubtxt , annotxt, page])


# Q8 Type of annotations
query_8 = """
SELECT DISTINCT ?pubtxt ?annotxt ?annotype
    WHERE {
        ?anno rdf:type oa:Annotation;
            oa:hasBody [rdf:value ?annotxt] ;
            oa:hasTarget ?pubtxt .
        ?creation ecrm:P94_has_created ?anno ;
            ecrm:P32_used_general_technique ?annotype . 
    }
"""

# Print results to CSV file
with open('../results/UC3_Q8-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Annotated text' , 'Annotation' , 'Type'])
    for pubtxt , annotxt, annotype in d.query(query_8):
        my_writer.writerow([pubtxt , annotxt, annotype])



# Q9 When were the annotations probably added to the text?
query_9 = """
SELECT DISTINCT ?pubtxt ?annotxt ?annodate
    WHERE {
        ?anno rdf:type oa:Annotation;
            oa:hasBody [rdf:value ?annotxt] ;
            oa:hasTarget ?pubtxt .
        ?creation ecrm:P94_has_created ?anno ;
            <http://erlangen-crm.org/current/P4_has_time-span> ?annodate . 
    }
"""

# Print results to CSV file
with open('../results/UC3_Q9-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Annotated text' , 'Annotation' , 'Date'])
    for pubtxt , annotxt, annodate in d.query(query_9):
        my_writer.writerow([pubtxt , annotxt, annodate])


