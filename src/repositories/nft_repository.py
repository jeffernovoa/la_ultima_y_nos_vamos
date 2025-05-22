from src.models.token_nft import TokenNFT
from firebase_admin import db
from pymongo import MongoClient

class NFTRepository:
    def __init__(self, mongo_uri=None, firebase_root="nfts"):
        self.firebase_ref = db.reference(firebase_root)
        if mongo_uri:
            self.mongo_client = MongoClient(mongo_uri)
            self.mongo_db = self.mongo_client["voting_app"]
            self.mongo_nfts = self.mongo_db["nfts"]
        else:
            self.mongo_client = None

    def save(self, token: TokenNFT):
        # Guardar en Firebase
        self.firebase_ref.child(str(token.token_id)).set(token.to_dict())
        # Guardar en MongoDB
        if self.mongo_client:
            self.mongo_nfts.update_one(
                {"token_id": str(token.token_id)},
                {"$set": token.to_dict()},
                upsert=True
            )

    def get_by_id(self, token_id: str) -> TokenNFT | None:
        data = self.firebase_ref.child(token_id).get()
        if data:
            return TokenNFT.from_dict(data)
        if self.mongo_client:
            data = self.mongo_nfts.find_one({"token_id": token_id})
            if data:
                return TokenNFT.from_dict(data)
        return None

    def list_by_owner(self, owner: str) -> list[TokenNFT]:
        nfts = []
        all_nfts = self.firebase_ref.get() or {}
        for nft in all_nfts.values():
            if nft["owner"] == owner:
                nfts.append(TokenNFT.from_dict(nft))
        return nfts

    def transfer(self, token_id: str, new_owner: str) -> bool:
        token = self.get_by_id(token_id)
        if not token:
            return False
        token.owner = new_owner
        self.save(token)
        return True
