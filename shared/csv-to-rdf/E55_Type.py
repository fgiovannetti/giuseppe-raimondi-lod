# coding: utf-8

# type

import csv
import re
import rdflib_jsonld
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL, SKOS

ecrm = Namespace("http://erlangen-crm.org/current/")

g = Graph()

g.bind("ecrm", ecrm)
g.bind("dcterms", DCTERMS)
g.bind("owl", OWL)
g.bind("skos", SKOS)

base_uri = 'https://w3id.org/ficlitdlo/'

# Document type (attributed to Physical Object and Expression, it is both physical and intellectual)

g.add((URIRef(base_uri + 'document-type/notebook'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/notebook'), RDFS.label, Literal('quaderno', lang='it')))
g.add((URIRef(base_uri + 'document-type/notebook'), RDFS.label, Literal('notebook', lang='en')))
g.add((URIRef(base_uri + 'document-type/notebook'), SKOS.relatedMatch, URIRef('http://vocab.getty.edu/aat/300027200')))

		# g.add((URIRef(base_uri + 'document-type/article'), RDF.type, ecrm.E55_Type))
		# g.add((URIRef(base_uri + 'document-type/article'), RDFS.label, Literal('articolo', lang='it')))
		# g.add((URIRef(base_uri + 'document-type/article'), RDFS.label, Literal('article', lang='en')))
		# g.add((URIRef(base_uri + 'document-type/article'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300048715')))

		# g.add((URIRef(base_uri + 'document-type/newspaper-clipping'), RDF.type, ecrm.E55_Type))
		# g.add((URIRef(base_uri + 'document-type/newspaper-clipping'), RDFS.label, Literal('ritaglio di giornale', lang='it')))
		# g.add((URIRef(base_uri + 'document-type/newspaper-clipping'), RDFS.label, Literal('newspaper clipping', lang='en')))
		# g.add((URIRef(base_uri + 'document-type/newspaper-clipping'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/page/300429554')))

g.add((URIRef(base_uri + 'document-type/letter'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/letter'), RDFS.label, Literal('lettera', lang='it')))
g.add((URIRef(base_uri + 'document-type/letter'), RDFS.label, Literal('letter', lang='en')))
g.add((URIRef(base_uri + 'document-type/letter'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300026879')))

g.add((URIRef(base_uri + 'document-type/postcard'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/postcard'), RDFS.label, Literal('cartolina', lang='it')))
g.add((URIRef(base_uri + 'document-type/postcard'), RDFS.label, Literal('postcard', lang='en')))
g.add((URIRef(base_uri + 'document-type/postcard'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300026816')))

g.add((URIRef(base_uri + 'document-type/note'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/note'), RDFS.label, Literal('biglietto', lang='it')))
g.add((URIRef(base_uri + 'document-type/note'), RDFS.label, Literal('note', lang='en')))
g.add((URIRef(base_uri + 'document-type/note'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300027200')))

g.add((URIRef(base_uri + 'document-type/telegram'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/telegram'), RDFS.label, Literal('telegramma', lang='it')))
g.add((URIRef(base_uri + 'document-type/telegram'), RDFS.label, Literal('telegram', lang='en')))
g.add((URIRef(base_uri + 'document-type/telegram'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300026909')))

g.add((URIRef(base_uri + 'document-type/invitation'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/invitation'), RDFS.label, Literal('invito', lang='it')))
g.add((URIRef(base_uri + 'document-type/invitation'), RDFS.label, Literal('invitation', lang='en')))
g.add((URIRef(base_uri + 'document-type/invitation'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/300027083')))

g.add((URIRef(base_uri + 'document-type/funeral-card'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'document-type/funeral-card'), RDFS.label, Literal('ricordo funebre', lang='it')))
g.add((URIRef(base_uri + 'document-type/funeral-card'), RDFS.label, Literal('funeral card', lang='en')))
g.add((URIRef(base_uri + 'document-type/funeral-card'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300026812')))

		# g.add((URIRef(base_uri + 'document-type/typescript'), RDF.type, ecrm.E55_Type))
		# g.add((URIRef(base_uri + 'document-type/typescript'), RDFS.label, Literal('dattiloscritto', lang='it')))
		# g.add((URIRef(base_uri + 'document-type/typescript'), RDFS.label, Literal('typescript', lang='en')))
		# g.add((URIRef(base_uri + 'document-type/typescript'), SKOS.closeMatch, URIRef(' http://vocab.getty.edu/aat/300028577')))
		# g.add((URIRef(base_uri + 'document-type/typescript'), DCTERMS.identifier, URIRef(base_uri + 'document-type/typescript')))

# Narrative form type

g.add((URIRef(base_uri + 'narrative-form-type/short-story'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'narrative-form-type/short-story'), RDFS.label, Literal('short story', lang='en')))
g.add((URIRef(base_uri + 'narrative-form-type/short-story'), RDFS.label, Literal('racconto', lang='it')))
g.add((URIRef(base_uri + 'narrative-form-type/short-story'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300202607')))
		
g.add((URIRef(base_uri + 'narrative-form-type/notes'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'narrative-form-type/notes'), RDFS.label, Literal('notes', lang='en')))
g.add((URIRef(base_uri + 'narrative-form-type/notes'), RDFS.label, Literal('appunti', lang='it')))
g.add((URIRef(base_uri + 'narrative-form-type/notes'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300027200')))
	
g.add((URIRef(base_uri + 'narrative-form-type/article'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'narrative-form-type/article'), RDFS.label, Literal('article', lang='en')))
g.add((URIRef(base_uri + 'narrative-form-type/article'), RDFS.label, Literal('articolo', lang='it')))
g.add((URIRef(base_uri + 'narrative-form-type/article'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300048715')))

# Production technique

g.add((URIRef(base_uri + 'technique-type/handwriting'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'technique-type/handwriting'), RDFS.label, Literal('manuscript (handwriting)', lang='en')))
g.add((URIRef(base_uri + 'technique-type/handwriting'), RDFS.label, Literal('manoscritto (scrittura a mano)', lang='it')))
g.add((URIRef(base_uri + 'technique-type/handwriting'), SKOS.relatedMatch, URIRef('http://vocab.getty.edu/aat/300252927')))

		
g.add((URIRef(base_uri + 'technique-type/typewriting'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'technique-type/typewriting'), RDFS.label, Literal('typescript (typewriting)', lang='en')))
g.add((URIRef(base_uri + 'technique-type/typewriting'), RDFS.label, Literal('dattiloscritto (scrittura a macchina)', lang='it')))
g.add((URIRef(base_uri + 'technique-type/typewriting'), SKOS.relatedMatch, URIRef('http://vocab.getty.edu/aat/300247929')))

# Identifier type

g.add((URIRef(base_uri + 'identifier-type/inventory-number'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'identifier-type/inventory-number'), RDFS.label, Literal('inventory number', lang='en')))
g.add((URIRef(base_uri + 'identifier-type/inventory-number'), RDFS.label, Literal('numero di inventario', lang='it')))

g.add((URIRef(base_uri + 'identifier-type/shelfmark'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'identifier-type/shelfmark'), RDFS.label, Literal('shelfmark', lang='en')))
g.add((URIRef(base_uri + 'identifier-type/shelfmark'), RDFS.label, Literal('collocazione', lang='it')))

# Archival unit type

g.add((URIRef(base_uri + 'archival-unit-type/file'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'archival-unit-type/file'), RDFS.label, Literal('file', lang='en')))
g.add((URIRef(base_uri + 'archival-unit-type/file'), RDFS.label, Literal('fascicolo', lang='it')))
g.add((URIRef(base_uri + 'archival-unit-type/file'), OWL.sameAs, URIRef('http://lod.xdams.org/reload/oad/levelOfDescription/file')))

g.add((URIRef(base_uri + 'archival-unit-type/series'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'archival-unit-type/series'), RDFS.label, Literal('series', lang='en')))
g.add((URIRef(base_uri + 'archival-unit-type/series'), RDFS.label, Literal('serie', lang='it')))
g.add((URIRef(base_uri + 'archival-unit-type/series'), OWL.sameAs, URIRef('http://lod.xdams.org/reload/oad/levelOfDescription/series')))
 		
g.add((URIRef(base_uri + 'archival-unit-type/fonds'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'archival-unit-type/fonds'), RDFS.label, Literal('fonds', lang='en')))
g.add((URIRef(base_uri + 'archival-unit-type/fonds'), RDFS.label, Literal('fondo', lang='it')))
g.add((URIRef(base_uri + 'archival-unit-type/fonds'), OWL.sameAs, URIRef('http://lod.xdams.org/reload/oad/levelOfDescription/fonds')))

# Title type

g.add((URIRef(base_uri + 'title-type/attributed'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'title-type/attributed'), RDFS.label, Literal('attributed title', lang='en')))
g.add((URIRef(base_uri + 'title-type/attributed'), RDFS.label, Literal('titolo attribuito', lang='it')))

g.add((URIRef(base_uri + 'title-type/proper'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'title-type/proper'), RDFS.label, Literal('title proper', lang='en')))
g.add((URIRef(base_uri + 'title-type/proper'), RDFS.label, Literal('titolo proprio', lang='it')))

# Dimension type
g.add((URIRef(base_uri + 'dimension-type/height'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'dimension-type/height'), RDFS.label, Literal('height', lang='en')))
g.add((URIRef(base_uri + 'dimension-type/height'), RDFS.label, Literal('altezza', lang='it')))
g.add((URIRef(base_uri + 'dimension-type/height'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/aat/300055644')))

g.add((URIRef(base_uri + 'dimension-type/extent'), RDF.type, ecrm.E55_Type))
g.add((URIRef(base_uri + 'dimension-type/extent'), RDFS.label, Literal('extent', lang='en')))
g.add((URIRef(base_uri + 'dimension-type/extent'), RDFS.label, Literal('consistenza', lang='it')))
g.add((URIRef(base_uri + 'dimension-type/extent'), SKOS.closeMatch, URIRef('http://vocab.getty.edu/page/aat/300404433')))

# RDF/XML
g.serialize(destination="../output/rdf/E55.rdf", format='xml')

# Turtle
g.serialize(destination="../output/ttl/E55.ttl", format='ttl')

# JSON-LD
g.serialize(destination="../output/jsonld/E55.jsonld", format='json-ld')