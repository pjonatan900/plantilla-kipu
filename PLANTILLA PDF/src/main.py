import os
from email_reader import fetch_emails
from data_parser import process_all_pdfs_in_folder
from pdf_generator import generate_ticket_from_html

# Directorios de trabajo
ATTACHMENTS_DIR = "attachments/"
GENERATED_TICKETS_DIR = "generated_tickets/"

# Crear la carpeta si no existe
if not os.path.exists(GENERATED_TICKETS_DIR):
    os.makedirs(GENERATED_TICKETS_DIR)

# Leer correos y descargar archivos adjuntos (esto ya lo tienes implementado)
fetch_emails(ATTACHMENTS_DIR)

# Procesar los PDFs descargados y extraer detalles de los vuelos
flight_details_list = process_all_pdfs_in_folder(ATTACHMENTS_DIR)

# Generar boletos para cada vuelo
for flight_details in flight_details_list:
    codigo_reserva = flight_details.get("codigo_reserva", "sin_codigo")
    output_pdf_path = os.path.join(GENERATED_TICKETS_DIR, f"{codigo_reserva}_boleto.pdf")
    
    generate_ticket_from_html(flight_details, output_pdf_path)

print("Todos los boletos han sido generados.")
