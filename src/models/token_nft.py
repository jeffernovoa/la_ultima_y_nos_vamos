class TokenNFT:
    def __init__(self, token_id, owner, poll_id, option, issued_at):
        self.token_id = token_id
        self.owner = owner
        self.poll_id = poll_id
        self.option = option
        self.issued_at = issued_at

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "owner": self.owner,
            "poll_id": self.poll_id,
            "option": self.option,
            "issued_at": self.issued_at.isoformat(),
            "tipo": self.__class__.__name__
        }


class StandardToken(TokenNFT):
    def __init__(self, token_id, owner, poll_id, option, issued_at):
        super().__init__(token_id, owner, poll_id, option, issued_at)


class LimitedEditionToken(TokenNFT):
    def __init__(self, token_id, owner, poll_id, option, issued_at):
        super().__init__(token_id, owner, poll_id, option, issued_at)
        self.edicion_limitada = True

    def to_dict(self):
        data = super().to_dict()
        data["edicion_limitada"] = True
        return data
