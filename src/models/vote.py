from datetime import datetime
from uuid import uuid4

class Vote:
    def __init__(self, vote_id: str = None, poll_id: str = None, username: str = None, option: str = None, timestamp: datetime = None):
        self.vote_id = vote_id or str(uuid4())
        self.poll_id = poll_id
        self.username = username
        self.option = option
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            "vote_id": self.vote_id,
            "poll_id": self.poll_id,
            "username": self.username,
            "option": self.option,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict):
        from datetime import datetime
        return Vote(
            vote_id=data["vote_id"],
            poll_id=data["poll_id"],
            username=data["username"],
            option=data["option"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
