import jwt

from fastapi import HTTPException
from starlette.requests import Request as StarletteRequest
from config import settings

def validate(req: StarletteRequest):
   auth0_issuer_url: str = f"https://{settings.auth0_domain}/"
   auth0_audience: str = settings.auth0_audience
   algorithm: str = "RS256"
   jwks_uri: str = f"{auth0_issuer_url}.well-known/jwks.json"
   authorization_header = req.headers.get("Authorization")
   
   if authorization_header:
      try:
         authorization_scheme, bearer_token = authorization_header.split()
      except ValueError:
         raise HTTPException(401, "bad credentials")
      
      valid = authorization_scheme.lower() == "bearer" and bool(bearer_token.strip())
      if valid:
         try:
            jwks_client = jwt.PyJWKClient(jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
               bearer_token
            ).key
            payload = jwt.decode(
               bearer_token,
               jwt_signing_key,
               algorithms=algorithm,
               audience=auth0_audience,
               issuer=auth0_issuer_url
            )
         except jwt.exceptions.PyJWKClientError:
            raise HTTPException(500, "unable to verify credentials")
         except jwt.exceptions.InvalidTokenError:
            raise HTTPException(401, "bad credentials")
         yield payload
   else:
      raise HTTPException(401, "bad credentials")