from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime
from reportlab.pdfgen import canvas
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
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, f"Cita programada")
        c.drawString(100, 730, f"A nombre de: {nombre_usuario}")
        c.drawString(100, 710, f"Con numero de servicio: {num_servicio}")
        c.save()

        dispatcher.utter_message(text=f"Your order has been saved as {filename}.")

        return []