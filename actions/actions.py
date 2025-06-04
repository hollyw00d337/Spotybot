from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image
import os

ALLOWED_PIZZA_SIZES = ["small", "medium", "large", "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_PIZZA_TYPES = ["mozzarella", "fungi", "veggie", "pepperoni", "hawaii"]

class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_nombre_usuario(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `nombre_usuario` value."""

        """if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"nombre_usuario": None}"""
        dispatcher.utter_message(text=f"OK! Tu nombre es {slot_value} .")
        return {"nombre_usuario": slot_value}

    def validate_num_servicio(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `num_servicio` value."""

        """if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}.")
            return {"num_servicio": None}
            """
        dispatcher.utter_message(text=f"OK! Tu numero de servicio es {slot_value} .")
        return {"num_servicio": slot_value}
    
class ActionSavePizzaToPDF(Action):
    def name(self) -> Text:
        return "action_save_pizza_to_pdf"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        nombre_imagen = os.path.join(os.path.dirname(__file__), "person.png")

        # Función para convertir PNG con transparencia a imagen con fondo blanco
        def convertir_imagen_sin_transparencia(imagen_path):
            img = Image.open(imagen_path).convert("RGBA")
            fondo_blanco = Image.new("RGBA", img.size, (255, 255, 255, 255))  # blanco opaco
            fondo_blanco.paste(img, mask=img.split()[3])  # pegar usando canal alpha como máscara
            # Guardar temporal sin transparencia
            temporal_path = "temp_no_transparencia.png"
            fondo_blanco.convert("RGB").save(temporal_path, "PNG")
            return temporal_path

        nombre_usuario = tracker.get_slot("nombre_usuario")
        num_servicio = tracker.get_slot("num_servicio")

        if not nombre_usuario or not num_servicio:
            dispatcher.utter_message(text="Error: missing pizza information.")
            return []

        # Crear nombre de archivo con fecha y hora
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
        filepath = os.path.join("pdf_outputs", filename)

        # Crear carpeta si no existe
        os.makedirs("pdf_outputs", exist_ok=True)

        # Crear PDF
        c = canvas.Canvas(filepath)
        ancho, alto = A4
        titulo = "SpotUno"
        subtitulo = "Disfruta de navegar con la mejor velocidad"
        contenido1 = f"A nombre de {nombre_usuario}"
        contenido2 = f"Con numero de servicio: {num_servicio}"
        contenido3 = "Cita agendada para el dia Lunes 25 de Mayo a las 10:25 a.m."
        despedida = "Encantados de atenderte. ¡Hasta pronto!"

        y = alto - 2*cm
        
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(ancho / 2, y, titulo)

        y -= 1.5*cm
        c.setFont("Helvetica", 14)
        c.drawCentredString(ancho / 2, y, subtitulo)
        y -= 2*cm
        c.setFont("Helvetica", 12)
        c.drawString(2*cm, y, contenido1)

        y -= 1.5*cm
        c.drawString(2*cm, y, contenido2)

        y -= 1.5*cm
        c.drawString(2*cm, y, contenido3)

        y -= 3*cm
        c.setFont("Helvetica-Oblique", 12)
        c.drawCentredString(ancho / 2, y, despedida)

        # Convertir imagen para quitar transparencia
        imagen_sin_transparencia = convertir_imagen_sin_transparencia(nombre_imagen)

        # Cargar imagen para dimensiones
        img = Image.open(imagen_sin_transparencia)
        ancho_img, alto_img = img.size

        ancho_deseado = 10 * cm
        alto_deseado = (ancho_deseado / ancho_img) * alto_img

        x_imagen = (ancho - ancho_deseado) / 2
        y_imagen = 1.5 * cm

        c.drawImage(imagen_sin_transparencia, x_imagen, y_imagen, ancho_deseado, alto_deseado)

      #  c.drawString(100, 750, f"Cita programada")
      #  c.drawString(100, 730, f"A nombre de: {nombre_usuario}")
      #  c.drawString(100, 710, f"Con numero de servicio: {num_servicio}")
        c.save()
        if os.path.exists(imagen_sin_transparencia):
            os.remove(imagen_sin_transparencia)

        dispatcher.utter_message(text=f"Recoge aqui el ticket de tu cita {filename}.")

        return []
