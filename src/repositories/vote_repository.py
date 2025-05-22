from src.models.vote import Vote
from firebase_admin import db
from pymongo import MongoClient

class VoteRepository:
    def __init__(self, mongo_uri=None, firebase_root="votes"):
        self.firebase_ref = db.reference(firebase_root)
        if mongo_uri:
            self.mongo_client = MongoClient(mongo_uri)
            self.mongo_db = self.mongo_client["voting_app"]
            self.mongo_votes = self.mongo_db["votes"]
        else:
            self.mongo_client = None

    def save(self, vote: Vote):
        # Firebase
        self.firebase_ref.child(vote.vote_id).set(vote.to_dict())
        # MongoDB
        if self.mongo_client:
            self.mongo_votes.update_one(
                {"vote_id": vote.vote_id},
                {"$set": vote.to_dict()},
                upsert=True
            )

    def get_by_poll_and_user(self, poll_id: str, username: str) -> Vote | None:
        votes = self.firebase_ref.get() or {}
        for vote in votes.values():
            if vote["poll_id"] == poll_id and vote["username"] == username:
                return Vote.from_dict(vote)

        if self.mongo_client:
            data = self.mongo_votes.find_one({"poll_id": poll_id, "username": username})
            if data:
                return Vote.from_dict(data)
        return None

    def list_votes_by_poll(self, poll_id: str) -> list[Vote]:
        votes = []
        all_votes = self.firebase_ref.get() or {}
        for v in all_votes.values():
            if v["poll_id"] == poll_id:
                votes.append(Vote.from_dict(v))
        return votes
