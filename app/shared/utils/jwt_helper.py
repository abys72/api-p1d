from typing import Dict
import base64
from datetime import datetime, timedelta, timezone
from jwt import JWT, jwk_from_dict, AbstractJWKBase


class JWTHelper:
    _jwt = JWT()

    @classmethod
    def create_access_token(cls, identity: str, secret_key: str) -> Dict[str, str | int]:
        if not secret_key:
            raise RuntimeError("SECRET_KEY No esta presente")
        encoded_key = base64.urlsafe_b64encode(secret_key.encode()).decode().rstrip("=")
        key: AbstractJWKBase = jwk_from_dict({"k": encoded_key, "kty": "oct"})
        now = datetime.now(timezone.utc)
        exp = int((now + timedelta(hours=1)).timestamp())
        payload: Dict[str, int | str] = {
            "sub": identity,
            "iat": int(now.timestamp()),
            "exp": exp
        }
        token: str = cls._jwt.encode(payload, key, alg="HS256")
        return {
            "access_token": token,
            "expires_at": exp
        }

    @classmethod
    def decode_access_token(cls, token: str, secret_key: str) -> Dict:
        secret_key: str | None = secret_key
        if not secret_key:
            raise RuntimeError("SECRET_KEY No esta presente")
        encoded_key = base64.urlsafe_b64encode(secret_key.encode()).decode().rstrip("=")
        key = jwk_from_dict({"k": encoded_key, "kty": "oct"})
        return cls._jwt.decode(token, key, do_verify=True)
