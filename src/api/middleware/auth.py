from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class AuthConfig:
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        """Create JWT token"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
            return jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)
        except Exception as e:
            logger.error(f"Error creating token: {e}")
            raise

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decode JWT token"""
        try:
            payload = jwt.decode(token, AuthConfig.SECRET_KEY, algorithms=[AuthConfig.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            raise HTTPException(status_code=401, detail="Invalid token")

class User(BaseModel):
    username: str
    password: str

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        payload = AuthConfig.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

if __name__ == "__main__":
    # Example usage
    token = AuthConfig.create_access_token({"sub": "testuser"})
    print(f"Generated token: {token}")
    decoded = AuthConfig.decode_token(token)
    print(f"Decoded token: {decoded}")