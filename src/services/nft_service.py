from src.models.token_nft import TokenNFT
from src.patterns.observer import Observer

class NFTService(Observer):
    def __init__(self, repo):
        self.repo = repo

    def mint_token(self, username, poll_id, option):
        token = TokenNFT(username, poll_id, option)
        self.repo.guardar(token)
        return token

    def get_tokens(self, username):
        return self.repo.obtener_por_usuario(username)

    def transfer_token(self, token_id, current_owner, new_owner):
        tokens = self.repo.obtener_por_usuario(current_owner)
        if any(t.token_id == token_id for t in tokens):
            self.repo.transferir(token_id, new_owner)
        else:
            raise Exception("Token no pertenece al usuario actual")

    def update(self, poll):
        print(f"[NFTService] Encuesta {poll.id} cerrada. Se pueden emitir NFTs por participación.")
