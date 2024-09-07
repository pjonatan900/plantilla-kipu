!pip install pdfkit jinja2
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

# Configuración para wkhtmltopdf
PDF_CONFIG = pdfkit.configuration(wkhtmltopdf='/ruta/a/tu/wkhtmltopdf')

def generate_ticket_from_html(flight_details, output_pdf_path, template_path="templates/ticket_template.html"):
    """
    Genera un boleto PDF desde una plantilla HTML con detalles del vuelo.
    """
    # Configurar Jinja2 para cargar plantillas HTML
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Rellenar la plantilla con los detalles del vuelo
    html_content = template.render(flight_details=flight_details)

    # Generar el PDF desde el HTML usando pdfkit
    pdfkit.from_string(html_content, output_pdf_path, configuration=PDF_CONFIG)
    print(f"Boleto generado en: {output_pdf_path}")
