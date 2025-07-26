
import hashlib
import jwt
import secrets
from datetime import datetime, timedelta
import ratelimit
from functools import wraps

class SecurityManager:
    def __init__(self):
        self.secret_key = secrets.token_hex(32)
        self.failed_attempts = {}
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_token(self, user_email):
        payload = {
            'email': user_email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['email']
        except:
            return None
    
    def rate_limit_check(self, ip_address):
        # Implement rate limiting
        current_time = datetime.now()
        if ip_address in self.failed_attempts:
            attempts = self.failed_attempts[ip_address]
            recent_attempts = [t for t in attempts if current_time - t < timedelta(minutes=15)]
            if len(recent_attempts) >= 5:
                return False
        return True
    
    def log_failed_attempt(self, ip_address):
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = []
        self.failed_attempts[ip_address].append(datetime.now())

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token required'}), 401
        
        user_email = security.verify_token(token.replace('Bearer ', ''))
        if not user_email:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(user_email, *args, **kwargs)
    return decorated
