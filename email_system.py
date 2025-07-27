
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailManager:
    def __init__(self):
        # These would be real SMTP settings in production
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = "fadal.rewards@gmail.com"
        self.password = "your_app_password"  # This should be in environment variables
        
    def send_welcome_email(self, user_email, user_name):
        subject = "Ku soo dhawoow Fadal Rewards!"
        
        body = f"""
        Salaam {user_name},
        
        Ku soo dhawoow Fadal Rewards! Waxaad hadda ku biirtay nidaamka ugu fiican lacag-helidda online.
        
        Waxa aad heli doontaa:
        - Training videos
        - Daily tasks
        - Referral bonuses
        - 24/7 Support
        
        Fadlan sii wad website-ka oo bilow lacag-helidda maanta!
        
        Mahadsanid,
        Fadal Rewards Team
        """
        
        return self._send_email(user_email, subject, body)
    
    def send_payment_confirmation(self, user_email, amount, plan):
        subject = "Lacag-bixintaada waa la aqbalay!"
        
        body = f"""
        Salaam,
        
        Lacag-bixintaada ${amount} plan-ka {plan} waa la aqbalay.
        
        Hadda waxaad heli kartaa:
        - Unlimited access
        - Premium content
        - Priority support
        
        Mahadsanid,
        Fadal Rewards Team
        """
        
        return self._send_email(user_email, subject, body)
    
    def _send_email(self, to_email, subject, body):
        try:
            # In development, just log the email
            print(f"EMAIL SENT TO: {to_email}")
            print(f"SUBJECT: {subject}")
            print(f"BODY: {body}")
            print("-" * 50)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

# Global email manager instance
email_manager = EmailManager()
