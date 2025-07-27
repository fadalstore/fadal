
import hashlib
import secrets
from datetime import datetime, timedelta

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("JWT not available, using basic auth")

class SecurityManager:
    def __init__(self):
        self.secret_key = secrets.token_hex(32)
        self.failed_attempts = {}
        self.admin_users = {
            'admin': self.hash_password('FadalRewards2025!'),
            'manager': self.hash_password('Manager123!')
        }
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed_password):
        return self.hash_password(password) == hashed_password
    
    def generate_token(self, user_email):
        if not JWT_AVAILABLE:
            return f"basic_{user_email}_{secrets.token_hex(16)}"
        
        payload = {
            'email': user_email,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        if not JWT_AVAILABLE:
            if token.startswith("basic_"):
                return token.split("_")[1]
            return None
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['email']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def rate_limit_check(self, ip_address):
        current_time = datetime.now()
        if ip_address in self.failed_attempts:
            attempts = self.failed_attempts[ip_address]
            # Keep only attempts from last 15 minutes
            recent_attempts = [t for t in attempts if current_time - t < timedelta(minutes=15)]
            self.failed_attempts[ip_address] = recent_attempts
            
            if len(recent_attempts) >= 5:
                return False
        return True
    
    def log_failed_attempt(self, ip_address):
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = []
        self.failed_attempts[ip_address].append(datetime.now())
    
    def authenticate_admin(self, username, password):
        if username in self.admin_users:
            return self.verify_password(password, self.admin_users[username])
        return False
    
    def sanitize_input(self, user_input):
        # Basic input sanitization
        if not user_input:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript']
        sanitized = str(user_input)
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()

# Global security manager instance
security_manager = SecurityManager()

# Flask integration
try:
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/api/admin-login', methods=['POST'])
    def admin_login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if security_manager.authenticate_admin(username, password):
            token = security_manager.generate_token(username)
            return jsonify({'success': True, 'token': token})
        else:
            # Log failed attempt
            ip_address = request.remote_addr
            security_manager.log_failed_attempt(ip_address)
            return jsonify({'success': False, 'error': 'Invalid credentials'})
    
    @app.route('/api/verify-token', methods=['POST'])
    def verify_token():
        data = request.json
        token = data.get('token')
        
        user = security_manager.verify_token(token)
        if user:
            return jsonify({'valid': True, 'user': user})
        else:
            return jsonify({'valid': False})
            
except ImportError:
    print("Flask not available for security system")

if __name__ == '__main__':
    print("Security system initialized!")
