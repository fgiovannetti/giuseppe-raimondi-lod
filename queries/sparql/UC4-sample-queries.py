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
d.parse("../../dataset/trig/additional-graph-7.trig" , format="trig")
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


# Q1 All correspondence between Paul Valéry and Giuseppe Raimondi 
query_1 = """
SELECT DISTINCT ?corresp ?mail
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/paul-valery> AS ?pvalery)
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail .   
    }
"""

# Print results to CSV file
with open('../results/UC4_Q1-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Correspondence Activity between G. Raimondi and P. Valéry' , 'Mail'])
    for corresp , mail in d.query(query_1):
        my_writer.writerow([corresp , mail])


# Q2 Correspondence between G. Raimondi and P. Valéry, ordered by date.
query_2 = """
SELECT DISTINCT ?corresp ?mail
    WHERE {
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail ;
            ficlitdlo:hadDateOfDispatch ?dispatch .
    }
    ORDER BY DESC(?dispatch) 
"""

with open('../results/UC4_Q2-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Correspondence Activity between G. Raimondi and P. Valéry' , 'Mail'])
    for corresp , mail in d.query(query_2):
        my_writer.writerow([corresp , mail])


# Q3 Date of dispatch of the letters
query_3 = """
SELECT DISTINCT ?mail ?dispatch
    WHERE {
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail ;
            ficlitdlo:hadDateOfDispatch ?dispatch .
    }
"""

# Print results to CSV file
with open('../results/UC4_Q3-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Mail', 'Date of Dispatch'])
    for mail , dispatch in d.query(query_3):
        my_writer.writerow([mail , dispatch])



# Q4 Language of the letters
query_4 = """
SELECT DISTINCT ?mail ?lang
    WHERE {
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail .
            ?mail ecrm:P128_carries ?txt .
            ?txt ecrm:P72_has_language ?lang .
    }
"""

# Print results to CSV file
with open('../results/UC4_Q4-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Mail', 'Language'])
    for mail , lang in d.query(query_4):
        my_writer.writerow([mail , lang])



# Q5 Works by Raimondi mentioned in the letters
query_5 = """
SELECT DISTINCT ?mail ?work
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/giuseppe-raimondi> AS ?graimondi)
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail .
            ?mail ecrm:P128_carries ?txt .
            ?graimondi pro:holdsRoleInTime ?rit .
            ?rit pro:relatesToEntity ?work .
            ?txt ecrm:P67_refers_to ?work .

    }
"""

# Print results to CSV file
with open('../results/UC4_Q5-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Mail' , 'Mentioned Work'])
    for mail , work in d.query(query_5):
        my_writer.writerow([mail , work])



# Q6 Places of origin of the letters
query_6 = """
SELECT DISTINCT ?mail ?origin
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/paul-valery> AS ?pvalery)
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail ;
            ficlitdlo:hadPlaceOfOrigin ?origin . 
    }
"""

# Print results to CSV file
with open('../results/UC4_Q6-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Mail', 'Origin'])
    for mail , origin in d.query(query_6):
        my_writer.writerow([mail , origin])



# Q7 Venues of publication of the letters (if any)
query_7 = """
SELECT DISTINCT ?mail ?pub
    WHERE {
        BIND(<https://w3id.org/ficlitdl/person/paul-valery> AS ?pvalery)
        ?corresp rdf:type ficlitdlo:CorrespondenceActivity ;
            ficlitdlo:hadSender | ficlitdlo:hadReceiver ?pvalery ;
            ficlitdlo:sent ?mail .
            ?mail ecrm:P128_carries ?txt .
            OPTIONAL {?txt ficlitdlo:hasPublishedVersion ?pubtxt .
                ?pub ecrm:P148_has_component ?pubtxt . } 
    }
"""

# Print results to CSV file
with open('../results/UC4_Q7-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Mail', 'Published in'])
    for mail , pub in d.query(query_7):
        my_writer.writerow([mail , pub])
