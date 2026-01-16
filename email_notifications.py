import os
import smtplib
from dotenv import load_dotenv 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_reservation_email(user_data):

    sender_email = os.getenv('MAIL_USERNAME')
    sender_password = os.getenv('MAIL_PASSWORD')
    
    recipient_email = user_data.get('email')
    
    if not recipient_email or not sender_email or not sender_password:
        print("BŁĄD: Brakuje danych email (sprawdź plik .env lub sesję użytkownika)")
        return False


    first_name = user_data.get('first_name', 'Gościu')
    last_name = user_data.get('last_name', '')
    date = user_data.get('date', 'Nieznana data')
    start_time = user_data.get('start_time', '--:--')
    

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Restauracja XYZ: Potwierdzenie rezerwacji - {date}"

    html_body = f"""
    <html>
      <body>
        <h3>Dzień dobry, {first_name} {last_name}!</h3>
        <p>Twoja rezerwacja została potwierdzona.</p>
        <p><strong>Szczegóły:</strong><br>
           Data: {date}<br>
           Godzina: {start_time}
        </p>
        <p>Pozdrawiamy,<br>Zespół Restauracji XYZ</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))


    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Sukces: Mail wysłany do {recipient_email}")
            return True
    except smtplib.SMTPAuthenticationError:
        print("Błąd logowania do Gmaila! Sprawdź MAIL_USERNAME i hasło aplikacji w .env")
        return False
    except Exception as e:
        print(f"Inny błąd wysyłki: {e}")
        return False