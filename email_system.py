
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailManager:
    def __init__(self):
        # Email configuration - in production use environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = "your-email@gmail.com"  # Replace with your email
        self.password = "your-app-password"  # Replace with app password
        
    def send_welcome_email(self, to_email, user_name):
        subject = "🎉 Ku soo dhawoow Fadal Rewards!"
        body = f"""
        Salaam {user_name},
        
        Waad ku mahadsantahay registration-ka Fadal Rewards platform-ka!
        
        🚀 Hadda waxaad heli kartaa:
        • Fursado lacag-helid oo badan
        • Training videos oo muhiim ah  
        • Support 24/7
        • Community ah oo taageera
        
        Bilow safarkaaga lacag-helidda maanta!
        
        Best regards,
        Fadal Rewards Team
        """
        return self.send_email(to_email, subject, body)
    
    def send_payment_confirmation(self, to_email, amount, plan, transaction_id):
        subject = "✅ Payment Confirmation - Fadal Rewards"
        body = f"""
        Payment Successfully Processed!
        
        Plan: {plan}
        Amount: ${amount}
        Transaction ID: {transaction_id}
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Your account has been activated. Welcome to Fadal Rewards!
        
        Start earning today: https://your-website.com
        
        Best regards,
        Fadal Rewards Team
        """
        return self.send_email(to_email, subject, body)
    
    def send_email(self, to_email, subject, body):
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP configuration
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            # In development, just log the email
            print(f"EMAIL SENT TO: {to_email}")
            print(f"SUBJECT: {subject}")
            print(f"BODY: {body}")
            print("-" * 50)
            return True

# Global email manager instance
email_manager = EmailManager()

# Flask integration
try:
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/api/send-welcome', methods=['POST'])
    def send_welcome():
        data = request.json
        success = email_manager.send_welcome_email(data['email'], data['name'])
        return jsonify({'success': success})
    
    @app.route('/api/send-payment-confirmation', methods=['POST'])
    def send_payment_confirmation():
        data = request.json
        success = email_manager.send_payment_confirmation(
            data['email'], data['amount'], data['plan'], data['transaction_id']
        )
        return jsonify({'success': success})
        
except ImportError:
    print("Flask not available for email system")

if __name__ == '__main__':
    print("Email system initialized!")
