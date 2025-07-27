import sqlite3
from datetime import datetime
import json

try:
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available, running database only")

class DatabaseManager:
    def __init__(self):
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect('fadal_rewards.db')
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                registered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                has_paid BOOLEAN DEFAULT FALSE,
                plan TEXT,
                last_login TIMESTAMP
            )
        ''')

        # Payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                amount REAL NOT NULL,
                plan TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                transaction_id TEXT,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')

        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_ip TEXT,
                page_visited TEXT,
                visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                referrer TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, name, email, phone):
        conn = sqlite3.connect('fadal_rewards.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, email, phone) 
                VALUES (?, ?, ?)
            ''', (name, email, phone))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def record_payment(self, user_email, amount, plan, method):
        conn = sqlite3.connect('fadal_rewards.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (user_email, amount, plan, payment_method, status)
            VALUES (?, ?, ?, ?, 'completed')
        ''', (user_email, amount, plan, method))

        # Update user status
        cursor.execute('''
            UPDATE users SET has_paid = TRUE, plan = ? WHERE email = ?
        ''', (plan, user_email))

        conn.commit()
        conn.close()

    def get_analytics(self):
        conn = sqlite3.connect('fadal_rewards.db')
        cursor = conn.cursor()

        # Total revenue
        cursor.execute('SELECT SUM(amount) FROM payments WHERE status = "completed"')
        total_revenue = cursor.fetchone()[0] or 0

        # Active users
        cursor.execute('SELECT COUNT(*) FROM users WHERE has_paid = TRUE')
        active_users = cursor.fetchone()[0]

        # Today's income
        cursor.execute('''
            SELECT SUM(amount) FROM payments 
            WHERE DATE(payment_date) = DATE('now') AND status = 'completed'
        ''')
        today_income = cursor.fetchone()[0] or 0

        conn.close()
        return {
            'total_revenue': total_revenue,
            'active_users': active_users,
            'today_income': today_income
        }

# Initialize database
db = DatabaseManager()

# API endpoints
if FLASK_AVAILABLE:
    @app.route('/api/register', methods=['POST'])
    def register_user():
        data = request.get_json()
        email = data.get('email')
        name = data.get('name', '')
        phone = data.get('phone', '')

        success = db.add_user(name, email, phone)

        if success:
            return jsonify({'status': 'success', 'message': 'User registered successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Email already exists'}), 400

    @app.route('/api/payment', methods=['POST'])
    def process_payment():
        data = request.get_json()
        user_email = data.get('email')
        amount = data.get('amount')
        plan = data.get('plan')
        payment_method = data.get('method')

        payment_id = db.record_payment(user_email, amount, plan, payment_method)

        if payment_id:
            return jsonify({'status': 'success', 'payment_id': payment_id})
        else:
            return jsonify({'status': 'error', 'message': 'Payment failed'}), 400

    @app.route('/api/analytics', methods=['GET'])
    def get_analytics():
        stats = db.get_analytics()
        return jsonify(stats)

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'database': 'connected'})

if __name__ == "__main__":
    # Initialize database
    db = DatabaseManager()
    print("Database initialized successfully!")

    if FLASK_AVAILABLE:
        print("Starting Flask server...")
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        print("Flask not available, database running in standalone mode")
        # Keep database running
        import time
        while True:
            time.sleep(60)