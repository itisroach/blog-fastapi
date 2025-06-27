import jwt
from datetime import datetime, timedelta, timezone
from settings import ALGORITHM, SECRET
from schema.output import JWTOutput


class JWTHandler:

    @staticmethod
    def generate(username: str, exp_time: datetime = None) -> JWTOutput:

        exp_time = exp_time if exp_time else datetime.now() + timedelta(days=1)

        exp_time = exp_time.timestamp()

        payload = {
            "exp": exp_time,
            "username": username
        }

        access_token = jwt.encode(payload, key=SECRET, algorithm=ALGORITHM)

    
        refresh_token = JWTHandler.generate_referesh_token(username)
        

        return JWTOutput(access=access_token, refresh=refresh_token)


    @staticmethod
    def generate_referesh_token(username: str):
        exp_time = datetime.now() + timedelta(days=2)
        
        payload = {
            "exp": exp_time.timestamp(),
            "username": username
        }

        refresh_token = jwt.encode(payload, key=SECRET, algorithm=ALGORITHM)

        return refresh_token