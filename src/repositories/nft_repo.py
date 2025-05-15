from src.models.token_nft import TokenNFT

class NFTRepository:
    def __init__(self):
        self.tokens = {}

    def guardar(self, token: TokenNFT):
        self.tokens[token.token_id] = token

    def obtener_por_usuario(self, username):
        return [t for t in self.tokens.values() if t.owner == username]

    def transferir(self, token_id, nuevo_owner):
        token = self.tokens.get(token_id)
        if token:
            token.owner = nuevo_owner