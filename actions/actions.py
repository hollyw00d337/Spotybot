# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# This is a simple example for a custom action which utters "Hello World!"
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import EventType
from typing import List, Dict, Any, Text
from rasa_sdk.types import DomainDict
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image
import os

#  Submenú: Problemas con mi servicio
# Opcion no tengo señal en ningun dispositivo
# generar script para buscar el ping y si no responde el problema es general no aislado
# generar clase a parte que se invoque para buscar ping
# genera funcion para buscar bases de datos pagos rezagados
def submenu_problemas_1(dispatcher: CollectingDispatcher, tracker: Tracker):
    #en caso de que el problema sea local generar este script
    dispatcher.utter_message("1.- Verificar que el modem este prendido\n "
                             "2.- Reiniciar Modem\n"
                             "3.- Verificar que esten todos los cables bien conectados")
# opcion esta muy lento e intermitente
# generar script para buscar el ping y que el problema no sea local
# generar funcion para buscar en la base de datos pagos rezagados
def submenu_problemas_2(dispatcher: CollectingDispatcher, tracker: Tracker):
    #en caso de que el problema sea local generar este script
    dispatcher.utter_message("1.- Verificar que el modem este prendido\n "
                             "2.- Reiniciar Modem\n"
                             "3.- Verificar que esten todos los cables bien conectados")
#opcion ya pague pero sigue sin servicio
#generar script de ping para buscar que el problema no sea local
# buscar en la base de datos el pago actualizado
def submenu_problemas_3(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Verificando tu pago...")
#opcion vino el tecnico pero no quedo bien
#generar nuevo reporte para el sistema, que no quedo bien la visita
def submenu_problemas_4(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Revisaremos la visita técnica anterior.")

#  Submenú: Pagos
#opcion validar que ya se recibio el pago
# invocar funcion que reciba el numero de cuenta y lo busque en la base de datos
#if el pago es > 0 no hay ningun pago recibido
# else si el pago = 0, ya se reflejo
def submenu_pagos_1(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Validando si tu pago ha sido recibido...")
#opcion consultar deuda
# invocar funcion de estado de cuenta
#imprimir el saldo a deber
def submenu_pagos_2(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Consultando tu deuda actual...")
#opcion solicitar codigo o forma de pago
# invocar funcion para generar forma de pago, ya sea numero de cuenta o QR
def submenu_pagos_3(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Generando forma de pago...")

#opcion reactivar servicio
# generar forma de pago
#Al realizar el pago generar ticket para visita de tecnico
def submenu_pagos_4(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Numero de cuenta utilizado en el anterior servicio")
# 🛠 Submenú: Agendar
def submenu_agendar_1(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Agendando visita técnica...")
#opcion cambiar de domicilio
# buscar el numero de cuenta en la base de datos y agregar el proximo
# domicilio
def submenu_agendar_2(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Ingresar numero de cuenta")
#Opcion cancelar visita
# buscar folio de visita
# eliminarlo base de datos
def submenu_agendar_3(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Cancelando visita")
# Confirmar cita
# buscar folio en la base de datos
# mandar mensaje de confirmacion
def submenu_agendar_4(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Confirmando cita...")
# Aun en desarrollo
#  Submenú: Celular y energía
# opcion Quiero contratar un plan celular
#imprimir planes celulares
def submenu_celular_1(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Te comparto planes de celular disponibles.")
# me interesa ahorrar luz con spot Energy
# imprimir planes de luz disponibles
def submenu_celular_2(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Te comparto planes de luz disponibles")
# Tengo dudas sobre estos servicios
# imprimir script sobre los servicios que tenemos a disposicion de luz y telefonia
def submenu_celular_3(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("En que consisten estos servicios y como puedes obtenerlos")
# Cliente que necesita soporte
def submenu_celular_4(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Cual es el error que presentas?")
# 🗣 Submenú: Otros
#opcion cancelar mi servicio
# consultar numero de cuenta, mandar reporte de cancelacion
def submenu_otros_1(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Estamos procesando tu solicitud de cancelación.")
#opcion quejarme del servicio
# el mensaje que mande el cliente, imprimirlo como queja
def submenu_otros_2(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Dime la queja")
# opcion saber mas sobre spotuno
# mandar mensaje de informacion sobre la empresa
def submenu_otros_3(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Mensaje de informacion sobre la empresa")
# opcion dejar un comentario o sugerencia
def submenu_otros_4(dispatcher: CollectingDispatcher, tracker: Tracker):
    dispatcher.utter_message("Deja aqui tu queja")
#  Diccionario de modulos
MENU_HANDLERS = {
    "submenu_problemas": {
        "1": submenu_problemas_1,
        "2": submenu_problemas_2,
        "3": submenu_problemas_3,
        "4": submenu_problemas_4,
        "5": lambda d, t: volver_menu_principal(d)
    },
    "submenu_pagos": {
        "1": submenu_pagos_1,
        "2": submenu_pagos_2,
        "3": submenu_pagos_3,
        "4": submenu_pagos_4,
        "5": lambda d, t: volver_menu_principal(d)
    },
    "submenu_agendar": {
        "1": submenu_agendar_1,
        "2": submenu_agendar_2,
        "3": submenu_agendar_3,
        "4": submenu_agendar_4,
        "5": lambda d, t: volver_menu_principal(d)
    },
    "submenu_celular": {
        "1": submenu_celular_1,
        "2": submenu_celular_2,
        "3": submenu_celular_3,
        "4": submenu_celular_4,
        "5": lambda d, t: volver_menu_principal(d)
    },
    "submenu_otros": {
        "1": submenu_otros_1,
        "2": submenu_otros_2,
        "3": submenu_otros_3,
        "4": submenu_otros_4,
        "5": lambda d, t: volver_menu_principal(d)
    },
}
def volver_menu_principal(dispatcher: CollectingDispatcher) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Menú Principal:\n"
                             "1. Tengo un problema con mi servicio\n"
                             "2. Pagos y facturación\n"
                             "3. Agendar o cambiar visita\n"
                             "4. Celular o energía\n"
                             "5. Otro asunto")
    return [SlotSet("estado_menu", "menu_principal")]

class ActionElegirOpcion(Action):
    def name(self) -> Text:
        return "action_elegir_opcion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        estado = tracker.get_slot("estado_menu") or "menu_principal"
        numero_opcion = next(tracker.get_latest_entity_values("numero_opcion"), None)

        if not numero_opcion or estado not in MENU_HANDLERS:
            dispatcher.utter_message("No entendí la opción. Por favor, elige un número del 1 al 5.")
            return []

        if estado == "menu_principal":
            return self.handle_main_menu(dispatcher, numero_opcion)

        return self.handle_submenu(dispatcher, tracker, estado, numero_opcion)

    def handle_main_menu(self, dispatcher: CollectingDispatcher, numero_opcion: Text) -> List[Dict[Text, Any]]:
        opciones = {
            "1": ("Tengo un problema con mi servicio", "submenu_problemas"),
            "2": ("Pagos y facturación", "submenu_pagos"),
            "3": ("Agendar o cambiar visita", "submenu_agendar"),
            "4": ("Celular o energía", "submenu_celular"),
            "5": ("Otro asunto", "submenu_otros")
        }

        if numero_opcion in opciones:
            mensaje, nuevo_estado = opciones[numero_opcion]
            dispatcher.utter_message(text=mensaje)
            return [SlotSet("estado_menu", nuevo_estado)]
        else:
            dispatcher.utter_message("Opción inválida. Elige del 1 al 5.")
            return []

    def handle_submenu(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                       estado_menu: Text, numero_opcion: Text) -> List[Dict[Text, Any]]:
        if numero_opcion in MENU_HANDLERS[estado_menu]:
            handler = MENU_HANDLERS[estado_menu][numero_opcion]
            handler(dispatcher, tracker)
            if numero_opcion == "5":
                return [SlotSet("estado_menu", "menu_principal")]
            return []
        else:
            dispatcher.utter_message("Opción inválida. Intenta de nuevo.")
            return []
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