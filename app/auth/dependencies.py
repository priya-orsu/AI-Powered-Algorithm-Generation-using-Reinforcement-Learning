from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

print(">>> dependencies.py LOADED <<<")

SECRET_KEY = "algorithm_generator_backend_secret"
ALGORITHM = "HS256"

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    print("verify_token() CALLED")
    print("Credentials:", credentials)

    token = credentials.credentials

    print("TOKEN:", token)
    print("SECRET:", SECRET_KEY)

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("TOKEN VERIFIED")
        print(payload)

        return payload

    except JWTError as e:

        print("JWT ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )