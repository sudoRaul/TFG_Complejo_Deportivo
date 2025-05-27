import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import current_app
from email.header import make_header

def enviar_correo(destinatario, asunto, cuerpo):
    try:
        msg = MIMEText(cuerpo, 'html', 'utf-8')
        msg['Subject'] = str(make_header([(asunto, 'utf-8')]))
        msg['From'] = current_app.config['EMAIL_FROM']
        msg['To'] = destinatario

        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD'])
            server.sendmail(msg['From'], [msg['To']], msg.as_string())

        return True
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        return False