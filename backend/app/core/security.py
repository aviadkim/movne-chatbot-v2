from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import secrets
import logging

logger = logging.getLogger(__name__)

# הגדרות הצפנה
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """יצירת טוקן גישה"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """אימות טוקן"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None

def generate_session_id() -> str:
    """יצירת מזהה סשן ייחודי"""
    return secrets.token_urlsafe(32)

class SecurityManager:
    def __init__(self):
        self.rate_limits = {}
        self.blocked_ips = set()
        
    def check_rate_limit(self, client_ip: str) -> bool:
        """בדיקת מגבלת קצב לכתובת IP"""
        now = datetime.utcnow()
        if client_ip in self.rate_limits:
            last_request, count = self.rate_limits[client_ip]
            if (now - last_request).seconds < 60:  # חלון זמן של דקה
                if count >= settings.RATE_LIMIT_PER_MINUTE:
                    return False
                self.rate_limits[client_ip] = (last_request, count + 1)
            else:
                self.rate_limits[client_ip] = (now, 1)
        else:
            self.rate_limits[client_ip] = (now, 1)
        return True
    
    def block_ip(self, client_ip: str):
        """חסימת כתובת IP"""
        self.blocked_ips.add(client_ip)
        logger.warning(f"Blocked IP address: {client_ip}")
    
    def is_ip_blocked(self, client_ip: str) -> bool:
        """בדיקה האם כתובת IP חסומה"""
        return client_ip in self.blocked_ips

# יצירת מופע יחיד של מנהל האבטחה
security_manager = SecurityManager()
