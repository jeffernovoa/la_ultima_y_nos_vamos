import uuid
from datetime import datetime
from src.repositories.utils.neo4j_utils import driver

class NFTService:
    def __init__(self):
        self.driver = driver

    def mint_token(self, owner, poll_id, option):
        token_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        with self.driver.session() as session:
            session.run("""
                MERGE (u:User {username: $owner})
                CREATE (t:Token {
                    token_id: $token_id,
                    poll_id: $poll_id,
                    option: $option,
                    issued_at: $timestamp
                })
                CREATE (u)-[:OWNS]->(t)
            """, owner=owner, token_id=token_id, poll_id=poll_id,
                 option=option, timestamp=timestamp)

        return token_id

    def transfer_token(self, token_id, from_user, to_user):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (from:User {username: $from_user})-[:OWNS]->(t:Token {token_id: $token_id})
                MATCH (to:User {username: $to_user})
                DELETE r = (from)-[:OWNS]->(t)
                CREATE (to)-[:OWNS]->(t)
                RETURN t
            """, from_user=from_user, to_user=to_user, token_id=token_id)
            if result.single() is None:
                raise Exception("Transferencia inválida o token no encontrado")

    def get_tokens_by_user(self, username):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {username: $username})-[:OWNS]->(t:Token)
                RETURN t.token_id AS id, t.poll_id AS poll_id, t.option AS option, t.issued_at AS issued_at
            """, username=username)

            return [record.data() for record in result]
