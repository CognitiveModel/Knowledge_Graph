from neo4j import GraphDatabase
# import pandas as pd
import os
from dotenv import load_dotenv
import base64

load_dotenv()

NEO4J_URL = os.environ.get("NEO4J_URL")
NEO4J_USER = os.environ.get("NEO4J_USER")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE")


#encoding
file_path = os.environ.get("PDF_DIR")
encoded_path = base64.b64encode(file_path.encode('utf-8')).decode('utf-8')



driver = GraphDatabase.driver(NEO4J_URL, database=NEO4J_DATABASE, auth=(NEO4J_USER, NEO4J_PASSWORD))

def ingesting(indexing):
    # import cypher
    json_path = f"file:///{encoded_path}.json"
    import_cypher = f'''CALL apoc.load.json("{json_path}") YIELD value'''

    import_cypher = import_cypher + '''
    MERGE (n1:Node {content: value.node_1, embedding:value.node1_embedding})
    MERGE (n2:Node {content: value.node_2, embedding:value.node2_embedding}) 
    MERGE (n1)-[:Edge {content: value.edge, embedding: value.edge_embedding}]->(n2)
    '''
    print(import_cypher)

    #create edge vector (relationship) index
    edge_cypher = '''

    CREATE VECTOR INDEX `edge-embedding`

    FOR ()-[r:Edge]-() ON (r.embedding) 

    OPTIONS {indexConfig: { 

     `vector.dimensions`: 384, 

     `vector.similarity_function`: 'cosine'

    }}

    '''

    #create node vector index
    node_cypher = '''
    CALL db.index.vector.createNodeIndex('node-embedding', 'Node', 'embedding', 384, 'COSINE')
    '''


    # ingest

    cypher_schema = [import_cypher, edge_cypher, node_cypher]



    with driver.session() as session:
        session.run(cypher_schema[0])
        if indexing:
            session.run(cypher_schema[1])
            session.run(cypher_schema[2])
        session.close()

    driver.close()


def database_creation(indexing):

    cypher_schema = ["SHOW DATABASE", f"CREATE DATABASE {NEO4J_DATABASE} IF NOT EXISTS"]

    driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # ingest_cypher = '''
    # SHOW DATABASE
    # '''
    

    # ingest

    with driver.session() as session:
        current_db = session.run(cypher_schema[0]).value()
        current_db = list(current_db)
        print("Current Database Names: ", current_db)
        
        session.run(cypher_schema[1])
        print(type(current_db))
        
        if NEO4J_DATABASE in current_db:
            print("Database already exist")
            indexing=False
        else:
            updated_db = session.run(cypher_schema[0])
            print("Updated Database Names: ", updated_db.value())

        session.close()



    driver.close()

    return indexing
