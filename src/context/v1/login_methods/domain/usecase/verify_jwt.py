from shared.app.handlers.jwt import JWTHandler


class VerifyJWTUseCase:

    def __init__(self, jwt: str):
        self.jwt = jwt

    def execute(self):
        JWTHandler.validate_token(self.jwt)
        return True
