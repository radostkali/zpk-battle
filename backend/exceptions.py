class LoginException(Exception):
    def __init__(self, message: str):
        self.message = message


class SubmitTrackException(Exception):
    def __init__(self, message: str):
        self.message = message
