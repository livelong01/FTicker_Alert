import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_FROM = "jonathakister@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")


def send_price_alert(data, old_price):
    subject = f"🔔 Preço caiu! {data['route']}"

    body = f"""
✈️ ALERTA DE PREÇO

Rota: {data['route']}
Datas: {data['departure_date']} → {data['return_date']}
Companhia: {data['airline']}
Perfil: {data['profile']}

💰 Preço anterior: {old_price}
🔥 Novo preço: {data['price_current']}

Paradas: {data['stops']}

Hora da verificação: {data['last_seen']}
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
