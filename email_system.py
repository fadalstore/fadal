
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSystem:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = os.getenv('SMTP_EMAIL')
        self.password = os.getenv('SMTP_PASSWORD')
    
    def send_welcome_email(self, user_email, user_name, plan):
        subject = f"Ku soo dhawoow Fadal Rewards - {plan} Plan!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🎉 Mahadsanid {user_name}!</h2>
            <p>Waxaad si guul leh ugu biirisay Fadal Rewards {plan} plan!</p>
            
            <h3>Waxaad hadda heli kartaa:</h3>
            <ul>
                <li>✅ Premium money-making links</li>
                <li>✅ Tilmaamo sir ah</li>
                <li>✅ 24/7 Support</li>
                <li>✅ WhatsApp VIP group</li>
            </ul>
            
            <a href="https://your-repl-url.replit.app/payment.html" 
               style="background: #28a745; color: white; padding: 15px 30px; 
               text-decoration: none; border-radius: 5px; display: inline-block;">
               🚀 Access Your Premium Content
            </a>
            
            <p>Haddii aad qabto su'aalo, nala soo xiriir: support@fadalrewards.com</p>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_email(self, to_email, subject, html_content):
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
