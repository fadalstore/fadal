
from datetime import datetime
import json
import secrets

class PaymentGateway:
    def __init__(self):
        self.transactions = {}
    
    def process_stripe_payment(self, amount, email, plan):
        # Simulate Stripe payment
        transaction_id = f"stripe_{secrets.token_hex(8)}"
        result = {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'stripe',
            'timestamp': datetime.now().isoformat()
        }
        self.transactions[transaction_id] = result
        return result
    
    def process_paypal_payment(self, amount, email, plan):
        # Simulate PayPal payment
        transaction_id = f"paypal_{secrets.token_hex(8)}"
        result = {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'paypal',
            'timestamp': datetime.now().isoformat()
        }
        self.transactions[transaction_id] = result
        return result
    
    def process_mobile_money(self, amount, phone, plan):
        # Simulate Mobile Money payment
        transaction_id = f"mobile_{secrets.token_hex(8)}"
        result = {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'method': 'mobile_money',
            'timestamp': datetime.now().isoformat()
        }
        self.transactions[transaction_id] = result
        return result
    
    def verify_payment(self, transaction_id):
        return self.transactions.get(transaction_id)

# Global payment gateway instance
payment_gateway = PaymentGateway()
