from src.databases.neo4j_connection import Neo4jConnection

neo4j = Neo4jConnection()

def registrar_voto_en_grafo(username, poll_id, opcion):
    query = """
    MERGE (u:Usuario {username: $username})
    MERGE (p:Encuesta {id: $poll_id})
    MERGE (u)-[:VOTO {opcion: $opcion}]->(p)
    """
    neo4j.query(query, {
        "username": username,
        "poll_id": poll_id,
        "opcion": opcion
    })
