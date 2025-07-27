
import sqlite3
import json
from datetime import datetime

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

# Initialize database first
db = DatabaseManager()

# API endpoints
try:
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    flask_available = True
except ImportError:
    print("Flask not available, running database only")
    flask_available = False

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    success = db.add_user(data['name'], data['email'], data['phone'])
    return jsonify({'success': success})

@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.json
    db.record_payment(data['email'], data['amount'], data['plan'], data['method'])
    return jsonify({'success': True})

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    return jsonify(db.get_analytics())

if __name__ == '__main__':
    print("Database initialized successfully!")
    if flask_available:
        print("Starting Flask API on port 5001...")
        app.run(host='0.0.0.0', port=5001)
    else:
        print("Flask not available, database running in standalone mode")
        # Keep the script running
        import time
        while True:
            time.sleep(60)
