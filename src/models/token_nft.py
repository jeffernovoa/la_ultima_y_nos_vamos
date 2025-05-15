import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, owner, poll_id, option):
        self.token_id = str(uuid.uuid4())
        self.owner = owner
        self.poll_id = poll_id
        self.option = option
        self.issued_at = datetime.now()