from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="test"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
