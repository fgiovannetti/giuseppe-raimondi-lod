import csv
import rdflib
from rdflib import Graph, Dataset, URIRef, Literal, Namespace, ConjunctiveGraph
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, PROV

d = rdflib.ConjunctiveGraph()
# d.parse("../../dataset/trig/quaderni_base-graph-E10.trig" , format="trig")
# d.parse("../../dataset/trig/quaderni_base-graph-E13.trig" , format="trig")
d.parse("../../dataset/trig/quaderni_base-graph-E21.trig" , format="trig")
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
d.parse("../../dataset/trig/additional-graph-4.trig" , format="trig")
d.parse("../../dataset/trig/libri_base-graph-F24.trig" , format="trig")
d.parse("../../dataset/trig/libri_base-graph-E22.trig" , format="trig")
d.parse("../../dataset/trig/libri_base-graph-E35.trig" , format="trig")
d.parse("../../dataset/trig/libri_base-graph-E42.trig" , format="trig")


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


# Q1 All titles attributed to the notebook text
query_1 = """
SELECT DISTINCT ?txt ?title
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?txt ecrm:P102_has_title ?title_uri .
        ?title_uri rdf:value ?title .     
    }
"""

# Print results to CSV file
with open('../results/UC2_Q1-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Notebook text' , 'Title'])
    for txt , title in d.query(query_1):
        my_writer.writerow([txt , title])


# Q2 The published versions of the notebook text: title, date, and publisher
query_2 = """
SELECT DISTINCT ?pubtxttitle ?pubtitle ?pubdate ?publisher_label
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?txt ficlitdlo:hasPublishedVersion ?pubtxt .
        ?pubtxt ecrm:P165i_is_incorporated_in ?pub ; ecrm:P102_has_title ?pubtxttitle_uri .
        ?pubtxttitle_uri rdf:value ?pubtxttitle .      
        ?pub ecrm:P102_has_title ?pubtitle_uri ; prism:publicationDate ?pubdate ; dcterms:publisher ?publisher .
        ?pubtitle_uri rdf:value ?pubtitle .
        ?publisher rdfs:label ?publisher_label .

    } 
"""

with open('../results/UC2_Q2-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Published version', 'In', 'Publication date', 'Publisher'])
    for pubtxttitle , pubtitle , pubdate , publisher_label in d.query(query_2):
        my_writer.writerow([pubtxttitle , pubtitle , pubdate , publisher_label])


# Q3 Copies of the published versions available within the Giuseppe Raimondi Archive
query_3 = """
SELECT ?pub ?shelfmark
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?txt ficlitdlo:hasPublishedVersion ?pubtxt .
        ?pubtxt ecrm:P165i_is_incorporated_in ?pub . 
        ?pub ecrm:P128i_is_carried_by ?item .
        ?item ecrm:P1_is_identified_by ?shelfmark_uri .
        ?shelfmark_uri ecrm:P2_has_type ficlitdlo:shelfmark ; rdfs:label ?shelfmark . 
        } 
"""

# Print results to CSV file
with open('../results/UC2_Q3-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Publication', 'Carrier shelfmark'])
    for pubtxt , shelfmark in d.query(query_3):
        my_writer.writerow([pubtxt , shelfmark])



# Q4 Textual variations (either internal or external) that involve the notebook text 
query_4 = """
SELECT ?txt ?txtvar
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?txtvar rdf:type ficlitdlo:TextualVariation ;
            ficlitdlo:hasVariantReading ?varrdg .
            ?varrdg ecrm:P106i_forms_part_of ?txt .
        }
        
"""

# Print results to CSV file
with open('../results/UC2_Q4-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text' , 'Textual variation'])
    for txt , txtvar in d.query(query_4):
        my_writer.writerow([txt , txtvar])


# Q5 For each textual variation in which the notebook text is involved, return all variant readings
query_5 = """
SELECT ?txtvar ?varrdg ?varvalue
       WHERE {
            BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
            ?txtvar rdf:type ficlitdlo:TextualVariation ;
                ficlitdlo:hasVariantReading ?varrdg .
                ?varrdg ecrm:P106i_forms_part_of ?txt ; rdf:value ?varvalue .
       }
"""

with open('../results/UC2_Q5-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Variant reading', 'Textual variation'])
    for txtvar , varrdg , varvalue in d.query(query_5):
        my_writer.writerow([txtvar , varrdg , varvalue ])



# Q6 Location of each variant reading in the transcription of the ms. witness
query_6 = """
SELECT DISTINCT ?varvalue ?loc ?tei  
       WHERE {
            BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
            ?txt ecrm:P165i_is_incorporated_in ?nbtxt .
            ?txtvar rdf:type ficlitdlo:TextualVariation ;
                ficlitdlo:hasVariantReading ?varrdg .
                ?varrdg ecrm:P106i_forms_part_of ?txt ; rdf:value ?varvalue .
                ?nbtxt ficlitdlo:hasTrascription ?tei .
                ?varrdg oa:hasSource ?tei ; oa:hasSelector [rdf:value ?loc] .
       } 
"""

with open('../results/UC2_Q6-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Variant reading' , 'XPath selector', 'XML/TEI transcription'])
    for varvalue , loc , tei in d.query(query_6):
        my_writer.writerow([varvalue , loc , tei])


# Q7 Causes for the textual variation
query_7 = """
SELECT DISTINCT ?txtvar ?cause ?cause_type 
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?cause ficlitdlo:resultedIn ?txtvar. 
        ?txtvar rdf:type ficlitdlo:TextualVariation ; ficlitdlo:hasVariantReading ?varrdg .
        ?varrdg ecrm:P106i_forms_part_of ?txt .
        ?cause ecrm:P2_has_type ?cause_type .

    } 
"""

with open('../results/UC2_Q7-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Variant reading', 'Cause', 'Cause type'])
    for txtvar , cause , cause_type  in d.query(query_7):
        my_writer.writerow([txtvar , cause , cause_type])

# Q8 Description of each text revision act 
query_8 = """
SELECT DISTINCT ?txtrev ?p ?varrdg_value ?person
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?txtrev ficlitdlo:resultedIn ?txtvar. 
        ?txtvar rdf:type ficlitdlo:TextualVariation ; ficlitdlo:hasVariantReading ?varrdg .
        ?varrdg ecrm:P106i_forms_part_of ?txt .
        ?txtrev ?p ?varrdg ; ecrm:P14_carried_out_by ?person_uri .
        ?person_uri rdfs:label ?person . FILTER (lang(?person) = 'it') 
        ?varrdg rdf:value ?varrdg_value .
    }
"""

with open('../results/UC2_Q8-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text', 'Published version' , 'Author of the text revision'])
    for txtrev , p , varrdg_value , person in d.query(query_8):
        my_writer.writerow([txtrev , p , varrdg_value , person])


# Q9 Chronological sequence of the text revision acts
query_9 = """
SELECT DISTINCT ?txtrev_a ?p ?txtrev_b
    WHERE {
        BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
        ?txtrev_a ficlitdlo:resultedIn ?txtvar.
        ?txtrev_b ficlitdlo:resultedIn ?txtvar. 
        ?txtvar rdf:type ficlitdlo:TextualVariation ; ficlitdlo:hasVariantReading ?varrdg .
        ?varrdg ecrm:P106i_forms_part_of ?txt .
        ?txtrev_a ?p ?txtrev_b .
    }
"""

with open('../results/UC2_Q9-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text revision act', 'Relation' , 'Text revision act'])
    for txtrev_a , p , txtrev_b in d.query(query_9):
        my_writer.writerow([txtrev_a , p , txtrev_b])


# Q10 Provenance of the statements about textual variation in the notebook text.
query_10 = """
SELECT DISTINCT ?txtvar ?respagent
    WHERE {
        GRAPH ?g {
            BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq2/text/2> AS ?txt)
            ?txtrev ficlitdlo:resultedIn ?txtvar. 
            ?txtvar rdf:type ficlitdlo:TextualVariation ; ficlitdlo:hasVariantReading ?varrdg .
            ?varrdg ecrm:P106i_forms_part_of ?txt .
            ?txtvar ?p ?o.
        }
        GRAPH ?h {?np np:hasAssertion ?g ;
            np:hasProvenance ?prov .
        }
         GRAPH ?prov {?g prov:wasAttributedTo ?respagent .
        }

    }
"""

with open('../results/UC2_Q10-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Textual variation' , 'Responsible agent'])
    for txtvar , respagent in d.query(query_10):
        my_writer.writerow([txtvar , respagent])
