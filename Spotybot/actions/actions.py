from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormValidationAction
from typing import List, Dict, Any, Text
from rasa_sdk.types import DomainDict
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image
import os

MENU_DEFS = {
    "menu_principal": {
        "message": "🧩 1. Problema con mi servicio\n💸 2. Pagos y facturación\n🛠 3. Agendar o cambiar visita\n📱 4. Celular o energía\n 🎁 5. Conoce nuestros planes\n🗣 6. Otro asunto",
        "options": {
            "1": ("submenu_problemas", "utter_opcion_problemas"),
            "2": ("submenu_pagos", "utter_opcion_pagos"),
            "3": ("submenu_agendar", "utter_opcion_agendar"),
            "4": ("submenu_celular", "utter_opcion_celular"),
            "6": ("submenu_otros", "utter_opcion_otros"),
            "5": ("submenu_planes", "utter_seleccion_planes")
        },
        "keywords": {
            "problema": "1", "soporte": "1",
            "pago": "2", "factura": "2", "deuda": "2",
            "agendar": "3", "cita": "3", "visita": "3",
            "celular": "4", "energía": "4", "luz": "4",
            "otro": "5", "queja": "5", "cancelar": "5", "comentario": "5", "sugerencia": "5", "saber más": "5"
        }
    },
    "submenu_problemas": {
        "message": "🧩 1. Sin señal\n2. Intermitente\n3. Ya pagué pero sigo sin servicio\n4. Técnico no dejó bien\n5. Regresar al menú principal",
        "options": {
            "1": ("problemas_1", "utter_solucion_problemas_1"),
            "2": ("problemas_2", "utter_solucion_problemas_2"),
            "3": ("problemas_3", "utter_solucion_problemas_3"),
            "4": ("problemas_4", "utter_solucion_problemas_4"),
            "5": ("menu_principal", "utter_menu_principal"),
        },
        "keywords": {
            "sin señal": "1", "no tengo señal": "1",
            "intermitente": "2", "lento": "2",
            "ya pagué": "3", "sin servicio": "3", "pagué": "3",
            "técnico": "4", "no quedó bien": "4",
            "volver": "5", "regresar": "5", "menú principal": "5"
        }
    },
    "submenu_pagos": {
        "message": "💸 1. Validar pago\n2. Consultar deuda\n3. Solicitar forma de pago\n4. Reactivar servicio\n5. Regresar al menú principal",
        "options": {
            "1": ("pagos_1", "utter_solucion_pagos_1"),
            "2": ("pagos_2", "utter_solucion_pagos_2"),
            "3": ("pagos_3", "utter_solucion_pagos_3"),
            "4": ("pagos_4", "utter_solucion_pagos_4"),
            "5": ("menu_principal", "utter_menu_principal"),
        },
        "keywords": {
            "validar pago": "1", "validar": "1", "pago recibido": "1",
            "deuda": "2", "consultar deuda": "2",
            "forma de pago": "3", "código": "3", "qr": "3",
            "reactivar": "4", "servicio": "4",
            "volver": "5", "regresar": "5", "menú principal": "5"
        }
    },
    "submenu_agendar": {
        "message": "🛠 1. Agendar visita\n2. Cambiar domicilio\n3. Cancelar visita\n4. Confirmar cita\n5. Regresar al menú principal",
        "options": {
            "1": ("agendar_1", "utter_solucion_agendar_1"),
            "2": ("agendar_2", "utter_solucion_agendar_2"),
            "3": ("agendar_3", "utter_solucion_agendar_3"),
            "4": ("agendar_4", "utter_solucion_agendar_4"),
            "5": ("menu_principal", "utter_menu_principal"),
        },
        "keywords": {
            "agendar visita": "1", "agendar": "1",
            "cambiar domicilio": "2", "cambiar dirección": "2",
            "cancelar visita": "3", "cancelar": "3",
            "confirmar cita": "4", "confirmar": "4",
            "volver": "5", "regresar": "5", "menú principal": "5"
        }
    },
    "submenu_celular": {
        "message": "📱 1. Contratar plan celular\n2. Ahorrar luz\n3. Dudas servicios\n4. Soporte\n5. Regresar al menú principal",
        "options": {
            "1": ("celular_1", "utter_solucion_celular_1"),
            "2": ("celular_2", "utter_solucion_celular_2"),
            "3": ("celular_3", "utter_solucion_celular_3"),
            "4": ("celular_4", "utter_solucion_celular_4"),
            "5": ("menu_principal", "utter_menu_principal"),
        },
        "keywords": {
            "contratar plan": "1", "plan celular": "1",
            "ahorrar luz": "2", "plan luz": "2",
            "dudas servicios": "3", "dudas": "3",
            "soporte": "4",
            "volver": "5", "regresar": "5", "menú principal": "5"
        }
    },
    "submenu_otros": {
        "message": "🗣 1. Cancelar servicio\n2. Quejarme\n3. Saber más\n4. Comentario o sugerencia\n5. Regresar al menú principal",
        "options": {
            "1": ("otros_1", "utter_solucion_otros_1"),
            "2": ("otros_2", "utter_solucion_otros_2"),
            "3": ("otros_3", "utter_solucion_otros_3"),
            "4": ("otros_4", "utter_solucion_otros_4"),
            "5": ("menu_principal", "utter_menu_principal"),
        },
        "keywords": {
            "cancelar servicio": "1", "cancelar": "1",
            "quejarme": "2", "queja": "2",
            "saber más": "3", "información": "3",
            "comentario": "4", "sugerencia": "4",
            "volver": "5", "regresar": "5", "menú principal": "5"
        }
    },#Planes
    "submenu_planes": {
        "message": "FUERA SE SERVICIO",
        "options": {
            "1": ("menu_principal", "utter_menu_principal")
        },
        "keywords": {
            "volver": "1", "regresar": "1", "menú principal": "1"
        }
    }
}

class ActionElegirOpcion(Action):
    def name(self) -> Text:
        return "action_elegir_opcion"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        estado = tracker.get_slot("estado_menu") or "menu_principal"
        texto = tracker.latest_message.get("text", "").lower().strip()
        numero_opcion = next(
            (ent.get("value") for ent in tracker.latest_message.get("entities", [])
             if ent.get("entity") == "numero_opcion"), None
        )

        # Si no es número, busca palabra clave
        if not numero_opcion and estado in MENU_DEFS:
            for palabra, opcion in MENU_DEFS[estado].get("keywords", {}).items():
                if palabra in texto:
                    numero_opcion = opcion
                    break

        # Fallback global: si el usuario quiere regresar al menú principal desde cualquier estado
        if any(x in texto for x in ["regresar", "volver", "menú principal"]):
            dispatcher.utter_message(response="utter_menu_principal")
            return [SlotSet("estado_menu", "menu_principal")]

        # Navegación normal de menú/submenú y manejo de formulario
        if estado in MENU_DEFS and numero_opcion in MENU_DEFS[estado]["options"]:
            next_state, utterance = MENU_DEFS[estado]["options"][numero_opcion]
            # Caso especial: activar formulario en submenu_agendar y opción 1
            if estado == "submenu_agendar" and numero_opcion == "1":
                dispatcher.utter_message(response=utterance)
                return [
                    SlotSet("estado_menu", next_state),
                    {"active_loop": "agendar_visita_form"}
                ]
            dispatcher.utter_message(response=utterance)
            return [SlotSet("estado_menu", next_state)]

        # Fallback personalizado
        dispatcher.utter_message(response="utter_fallback_custom")
        dispatcher.utter_message(text="No entendí tu elección. Por favor, selecciona una opción válida.")
        # Repite el menú actual
        if estado in MENU_DEFS:
            dispatcher.utter_message(text=MENU_DEFS[estado]["message"])
        else:
            dispatcher.utter_message(response="utter_menu_principal")
        return []

class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        estado = tracker.get_slot("estado_menu") or "menu_principal"
        dispatcher.utter_message(response="utter_fallback_custom")
        if estado in MENU_DEFS:
            dispatcher.utter_message(text=MENU_DEFS[estado]["message"])
        else:
            dispatcher.utter_message(response="utter_menu_principal")
        return []
class ActionGuardarCitaYGenerarTicket(Action):
    def name(self) -> Text:
        return "action_guardar_cita_y_generar_ticket"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        numero_cuenta = tracker.get_slot("numero_cuenta")
        direccion = tracker.get_slot("direccion")
        fecha_cita = tracker.get_slot("fecha_cita")
        # Aquí irá la lógica para guardar la cita en la base de datos real
        # En lo que la tenemos, simulamos el guardado
        dispatcher.utter_message(
            f"¡Listo! Tu cita está agendada para el {fecha_cita} en la dirección: {direccion}. Se ha generado tu ticket."
        )
        return []
