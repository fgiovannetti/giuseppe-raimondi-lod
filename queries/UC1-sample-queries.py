import csv
import rdflib
from rdflib import Graph, Dataset, URIRef, Literal, Namespace, ConjunctiveGraph
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, PROV

d = rdflib.ConjunctiveGraph()
d.parse("../quaderni/output/trig/base-graph-E10.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E13.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E21.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E22.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E30.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E35.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E40.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E42.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E45.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E52.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E53.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E54.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E78.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-E89.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-F22.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-F28.trig" , format="trig")
d.parse("../quaderni/output/trig/base-graph-RIT.trig" , format="trig")
d.parse("../enrichment/output/trig/additional-graph-1.trig" , format="trig")
d.parse("../enrichment/output/trig/additional-graph-2.trig" , format="trig")
d.parse("../enrichment/output/trig/additional-graph-3.trig" , format="trig")

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



# Q1 All notebooks, with titles and page count
query_1 = """
SELECT DISTINCT ?notebook ?title ?extent
    WHERE {
        ?notebook ecrm:P2_has_type ficlitdlo:notebook ;
            ecrm:P43_has_dimension ?dimension .
        ?dimension ecrm:P91_has_unit ficlitdlo:leaf ;
            rdfs:label ?extent .
        ?notebook ecrm:P128_carries ?txt .
        ?txt ecrm:P102_has_title ?title_uri .
        ?title_uri rdf:value ?title . FILTER (lang(?extent) = 'it')           
    }
"""

# Print results to CSV file
with open('results/Q1-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Notebook', 'Title', 'Page count'])
    for notebook, title, extent in d.query(query_1):
        my_writer.writerow([notebook, title, extent])




# Q2 All notebooks that contain multiple texts
query_2 = """
SELECT DISTINCT ?notebook (COUNT(?txt) as ?total) ?label
    WHERE {
        ?notebook ecrm:P2_has_type ficlitdlo:notebook .
        ?notebook rdfs:label ?label . FILTER (lang(?label) = 'it') 
        ?notebook ecrm:P128_carries ?full_txt .
        ?full_txt ecrm:P165_incorporates ?txt .
    } GROUP BY ?notebook
"""

# Print results to CSV file
with open('results/Q2-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Notebook', 'Text count', 'Description'])
    for notebook, total, label in d.query(query_2):
        my_writer.writerow([notebook, total, label])


# Q3 Texts contained in a specific notebook (RDq 303) with their titles and dates of creation
query_3 = """
SELECT DISTINCT ?txt ?title ?created
    WHERE {
        ?notebook ecrm:P2_has_type ficlitdlo:notebook .
        ?notebook ecrm:P1_is_identified_by ?identifier . 
        ?identifier rdfs:label ?label . FILTER (?label="RDq 303"^^xsd:string)
        ?notebook ecrm:P128_carries ?full_txt .
        ?full_txt ecrm:P165_incorporates ?txt .
        ?txt ecrm:P102_has_title ?title_uri .
        ?title_uri rdfs:label ?title .
        ?creation efrbroo:R17_created ?txt .
        OPTIONAL {?creation ecrm:P4_has_time-span ?timespan .
             ?timespan rdfs:label ?created . }
        } GROUP BY ?txt
"""

# Print results to CSV file
with open('results/Q3-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text', 'Title' , 'Date of creation'])
    for txt, title, created in d.query(query_3):
        my_writer.writerow([txt, title, created])



# Q4 Authors of the texts and, for attributed authors, agent responsible for authorship attribution
query_4 = """
SELECT DISTINCT ?txt ?author ?respagent
    WHERE {
      ?creation rdf:type efrbroo:F28_Expression_Creation ;
        efrbroo:R17_created ?txt ;
        ecrm:P14_carried_out_by ?author .
        OPTIONAL {?attribution ecrm:P140_assigned_attribute_to ?author . 
            ?attribution ecrm:P14_carried_out_by ?respagent .
        }
    } GROUP BY ?txt
"""

# Print results to CSV file
with open('results/Q4-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text', 'Author' , 'Authorship attributed by'])
    for txt, author, respagent in d.query(query_4):
        my_writer.writerow([txt, author, respagent])


# Q5 Notebook texts that mentions one or more persons
query_5 = """
SELECT DISTINCT ?person ?persname ?txt
       WHERE {
            ?notebook ecrm:P2_has_type ficlitdlo:notebook ;
                ecrm:P128_carries ?txt . 
            ?txt ecrm:P67_refers_to ?person .
            ?person rdf:type ecrm:E21_Person ;
                rdfs:label ?persname .FILTER (lang(?persname) = 'it')
       } GROUP BY ?person
"""

with open('results/Q5-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Person', 'Person name', 'Mentioned in'])
    for person, persname, txt in d.query(query_5):
        my_writer.writerow([person, persname, txt])



# Q6 Any known variants of the notebook text "Una forca per il poeta François Villon" contained in the archive
query_6 = """
SELECT DISTINCT ?variant ?title ?item 
       WHERE {
            ?notebook ecrm:P2_has_type ficlitdlo:notebook ;
                ecrm:P128_carries ?txt .
            ?txt ecrm:P102_has_title ?title_uri .
            ?title_uri rdf:value ?title . FILTER( regex(?title, "Una forca per il poeta François Villon" ))
            ?txt ficlitdlo:hasVariantVersion ?variant .
            ?item ecrm:P128_carries ?variant .
       } 
"""

with open('results/Q6-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Variant text' , 'Title', 'Document'])
    for variant , title , item in d.query(query_6):
        my_writer.writerow([variant , title, item])


# Q7 All archival documents that mention François Villon
query_7 = """
SELECT DISTINCT ?item ?doctype ?label
    WHERE {
        ?txt ecrm:P67_refers_to ?person . FILTER( regex(str(?person), "villon" ))
        ?item ecrm:P128_carries ?txt ;
            ecrm:P2_has_type ?doctype ;
            ecrm:P1_is_identified_by ?shelfmark .
        ?shelfmark ecrm:P2_has_type ficlitdlo:shelfmark ; 
            rdfs:label ?label .
    } GROUP BY ?item
"""

with open('results/Q7-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Document', 'Document type', 'Document shelfmark'])
    for item, doctype, label in d.query(query_7):
        my_writer.writerow([item, doctype, label])

# Q8 All published versions of the notebook text "Una forca per il poeta François Villon" (RDq 303)
query_8 = """
SELECT DISTINCT ?txt ?pubtxt
    WHERE {
        ?notebook ecrm:P128_carries ?txt ;
            ecrm:P2_has_type ficlitdlo:notebook .
        ?txt ecrm:P102_has_title ?title_uri .
        ?title_uri rdf:value ?title . FILTER( regex(?title, "Una forca per il poeta François Villon" ))   
        ?pubtxt ficlitdlo:isPublishedVersionOf ?txt .
    }
"""

with open('results/Q8-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text', 'Published version'])
    for txt , pubtxt in d.query(query_8):
        my_writer.writerow([txt , pubtxt])

# Q9 Relationships involving the notebook text “Una forca per il poeta François Villon”, as reconstructed by a named researcher.
query_9 = """
SELECT DISTINCT ?s ?p ?o ?respagent
    WHERE {
        GRAPH ?g {
            BIND(<https://w3id.org/giuseppe-raimondi-lod/notebook/rdq303/text/1> AS ?o)
            ?s ?p ?o.
        }
        GRAPH ?h {?np np:hasAssertion ?g ;
            np:hasProvenance ?prov .
        }
         GRAPH ?prov {?g prov:wasAttributedTo ?respagent .
        }

    }
"""

with open('results/Q9-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Entity' , 'Relation' , 'Notebook text', 'Responsible agent'])
    for s , p , o , respagent in d.query(query_9):
        my_writer.writerow([s , p , o , respagent])

# Q10 Texts that mention works of art.
query_10 = """
SELECT DISTINCT ?txt ?artwork
    WHERE {
        ?txt ecrm:P67_refers_to ?artwork .
        ?artwork ecrm:P2_has_type ficlitdlo:painting .
    }
"""

with open('results/Q10-result.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    my_writer.writerow(['Text' , 'Artwork'])
    for txt , artwork in d.query(query_10):
        my_writer.writerow([txt , artwork])