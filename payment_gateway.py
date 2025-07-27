
from datetime import datetime
import json
import secrets
import hashlib

class PaymentGateway:
    def __init__(self):
        self.payments = {}
        self.supported_methods = ['stripe', 'paypal', 'zaad', 'edahab', 'sahal']
    
    def generate_transaction_id(self):
        return f"TXN_{secrets.token_hex(8)}_{int(datetime.now().timestamp())}"
    
    def process_stripe_payment(self, amount, currency='USD'):
        # Simulate Stripe payment
        transaction_id = self.generate_transaction_id()
        return {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'currency': currency,
            'method': 'stripe',
            'status': 'completed'
        }
    
    def process_paypal_payment(self, amount, currency='USD'):
        # Simulate PayPal payment
        transaction_id = self.generate_transaction_id()
        return {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'currency': currency,
            'method': 'paypal',
            'status': 'completed'
        }
    
    def process_mobile_money(self, amount, phone, method='zaad'):
        # Simulate Somali mobile money payment
        transaction_id = self.generate_transaction_id()
        return {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'phone': phone,
            'method': method,
            'status': 'completed'
        }
    
    def verify_payment(self, transaction_id):
        # In real implementation, this would check with payment provider
        return transaction_id.startswith('TXN_')
    
    def get_payment_plans(self):
        return {
            'basic': {
                'name': 'Basic Plan',
                'price': 15,
                'currency': 'USD',
                'features': ['Acess to earning methods', 'Basic support']
            },
            'premium': {
                'name': 'Premium Plan', 
                'price': 30,
                'currency': 'USD',
                'features': ['All earning methods', 'Priority support', 'Advanced tutorials']
            },
            'vip': {
                'name': 'VIP Plan',
                'price': 50,
                'currency': 'USD',
                'features': ['Everything included', '1-on-1 mentoring', 'Exclusive opportunities']
            }
        }

# Global payment gateway instance
payment_gateway = PaymentGateway()

# Flask integration
try:
    from flask import Flask, request, jsonify
    from database import db
    
    app = Flask(__name__)
    
    @app.route('/api/process-payment', methods=['POST'])
    def process_payment():
        data = request.json
        method = data.get('method')
        amount = data.get('amount')
        plan = data.get('plan')
        user_email = data.get('email')
        
        if method == 'stripe':
            result = payment_gateway.process_stripe_payment(amount)
        elif method == 'paypal':
            result = payment_gateway.process_paypal_payment(amount)
        elif method in ['zaad', 'edahab', 'sahal']:
            phone = data.get('phone')
            result = payment_gateway.process_mobile_money(amount, phone, method)
        else:
            return jsonify({'success': False, 'error': 'Unsupported payment method'})
        
        if result['success']:
            # Record payment in database
            db.record_payment(user_email, amount, plan, method)
            
        return jsonify(result)
    
    @app.route('/api/payment-plans', methods=['GET'])
    def get_payment_plans():
        return jsonify(payment_gateway.get_payment_plans())
    
except ImportError:
    print("Flask not available for payment gateway")

if __name__ == '__main__':
    print("Payment Gateway initialized!")
