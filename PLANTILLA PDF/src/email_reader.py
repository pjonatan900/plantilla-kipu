import sys
import os

# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(".."))

# Ahora deberías poder importar config.settings sin problemas
from config import settings

import imaplib
import email
from email.header import decode_header


# Conectar a Gmail usando IMAP
def connect_to_gmail():
    try:
        # Crear conexión IMAP con Gmail
        mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER, settings.IMAP_PORT)
        # Autenticarse con la dirección de correo y la contraseña de aplicación
        mail.login(settings.EMAIL_ADDRESS, settings.APP_PASSWORD)
        print("Conexión exitosa con Gmail")
        return mail
    except Exception as e:
        print(f"Error al conectarse a Gmail: {str(e)}")
        return None

# Buscar correos electrónicos en la bandeja de entrada por asunto
def search_emails_by_subject(subject_keyword):
    mail = connect_to_gmail()
    if not mail:
        return []

    try:
        # Seleccionar la bandeja de entrada (INBOX)
        mail.select("inbox")

        # Buscar correos electrónicos por asunto que contengan el 'subject_keyword'
        status, messages = mail.search(None, f'(SUBJECT "{subject_keyword}")')

        if status != "OK":
            print("No se encontraron correos electrónicos")
            return []

        email_ids = messages[0].split()

        # Almacenar los correos que coincidan
        emails = []
        for email_id in email_ids:
            # Obtener el correo por ID
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            if status != "OK":
                print(f"Error al obtener el correo con ID {email_id}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parsear el mensaje con el paquete `email`
                    msg = email.message_from_bytes(response_part[1])
                    emails.append(msg)

        return emails
    except Exception as e:
        print(f"Error al buscar correos: {str(e)}")
        return []
    finally:
        mail.logout()

# Extraer contenido de un correo electrónico
def extract_email_content(msg):
    try:
        # Decodificar el asunto del correo
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        print(f"Subject: {subject}")

        # Obtener el remitente
        from_ = msg.get("From")
        print(f"From: {from_}")

        # Procesar el contenido del correo
        if msg.is_multipart():
            # Iterar sobre las partes del mensaje
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if content_type == "text/plain" or content_type == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            return payload.decode("utf-8")
        else:
            # El correo no tiene partes múltiples
            payload = msg.get_payload(decode=True)
            return payload.decode("utf-8")
    except Exception as e:
        print(f"Error al extraer el contenido del correo: {str(e)}")
        return None


