import pdfplumber
import re

def extract_flight_details_from_pdf(pdf_filepath):
    """
    Extrae los detalles del vuelo desde un archivo PDF.
    """
    flight_details = {
        "codigo_reserva": None,
        "nombre_pasajero": None,
        "fecha_salida": None,
        "fecha_llegada": None
    }

    with pdfplumber.open(pdf_filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Aquí podemos usar expresiones regulares o buscar palabras clave
            codigo_reserva = re.search(r'Código de reserva:\s*(\w+)', text)
            nombre_pasajero = re.search(r'Pasajero:\s*([\w\s]+)', text)
            fecha_salida = re.search(r'Fecha de salida:\s*([\w\s,]+)', text)
            fecha_llegada = re.search(r'Fecha de llegada:\s*([\w\s,]+)', text)

            # Guardamos los resultados si los encontramos
            if codigo_reserva:
                flight_details["codigo_reserva"] = codigo_reserva.group(1)
            if nombre_pasajero:
                flight_details["nombre_pasajero"] = nombre_pasajero.group(1)
            if fecha_salida:
                flight_details["fecha_salida"] = fecha_salida.group(1)
            if fecha_llegada:
                flight_details["fecha_llegada"] = fecha_llegada.group(1)

    return flight_details

def process_all_pdfs_in_folder(folder_path):
    """
    Procesa todos los archivos PDF en una carpeta y extrae detalles del vuelo.
    """
    flight_details_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_filepath = os.path.join(folder_path, filename)
            print(f"Procesando PDF: {pdf_filepath}")
            flight_details = extract_flight_details_from_pdf(pdf_filepath)
            flight_details_list.append(flight_details)

    return flight_details_list
