from rasa_sdk import Action, Tracker, FormValidationAction
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

# =========================
# FUNCIONES DE SUBMENÚS
# =========================

# Submenú: Problemas con mi servicio
# Opción: No tengo señal en ningún dispositivo
# - Generar script para buscar el ping y si no responde el problema es general, no aislado
# - Generar clase aparte que se invoque para buscar ping
# - Generar función para buscar bases de datos pagos rezagados
def submenu_problemas_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("1.- Verificar que el modem esté prendido\n2.- Reiniciar modem\n3.- Verificar que estén todos los cables bien conectados")
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir:
        return pedir
    return [SlotSet("solucion_branch", "problemas_1")]

# Opción: Está muy lento e intermitente
# - Generar script para buscar el ping y que el problema no sea local
# - Generar función para buscar en la base de datos pagos rezagados
def submenu_problemas_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("1.- Verificar que el modem esté prendido\n2.- Reiniciar modem\n3.- Verificar que estén todos los cables bien conectados")
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir: 
        return pedir
    return [SlotSet("solucion_branch", "problemas_2")]

# Opción: Ya pagué pero sigue sin servicios
# - Generar script de ping para buscar que el problema no sea local
# - Buscar en la base de datos el pago actualizado
def submenu_problemas_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir:
        return pedir
    return [SlotSet("solucion_branch", "problemas_3"), SlotSet("esperando_numero_cuenta", None)]

# Opción: Vino el técnico pero no quedó bien
# - Generar nuevo reporte para el sistema, que no quedó bien la visita
def submenu_problemas_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir: 
        return pedir
    dispatcher.utter_message("Revisaremos la visita técnica anterior.")
    return [SlotSet("solucion_branch", "problemas_4")]

# =========================
# SUBMENÚ: PAGOS
# =========================

# Opción: Validar que ya se recibió el pago
# - Invocar función que reciba el número de cuenta y lo busque en la base de datos
# - Si el saldo pendiente es > 0 no hay ningún pago recibido
# - Si el saldo pendiente es = 0, ya se reflejó, generar script de pago ya recibido
def submenu_pagos_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir:
        return pedir
    dispatcher.utter_message("Validando si tu pago ha sido recibido...")
    return [SlotSet("solucion_branch", "pagos_1")]

# Opción: Consultar deuda
# - Invocar función de estado de cuenta
# - Imprimir el saldo a deber
def submenu_pagos_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir: 
        return pedir
    dispatcher.utter_message("Consultando tu deuda actual...")
    return [SlotSet("solucion_branch", "pagos_2")]

# Opción: Solicitar código o forma de pago
# - Invocar función para generar forma de pago, ya sea número de cuenta o QR
def submenu_pagos_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Generando forma de pago...")
    return [SlotSet("solucion_branch", "pagos_3")]

# Opción: Reactivar servicio
# - Generar forma de pago
# - Al realizar el pago generar ticket para visita de técnico
def submenu_pagos_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir: 
        return pedir
    dispatcher.utter_message("Número de cuenta utilizado en el anterior servicio")
    return [SlotSet("solucion_branch", "pagos_4")]

# =========================
# SUBMENÚ: AGENDAR
# =========================

# Opción: Agendar visita técnica
# - Generar script para agendar cita, pedir domicilio y dar horario
def submenu_agendar_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Agendando visita técnica...")
    return [SlotSet("solucion_branch", "agendar_1")]

# Opción: Cambiar de domicilio
# - Buscar el número de cuenta en la base de datos y cambiar la dirección
def submenu_agendar_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir: 
        return pedir
    dispatcher.utter_message("Procesando cambio de domicilio...")   
    return [SlotSet("solucion_branch", "agendar_2")]

# Opción: Cancelar visita
# - Buscar folio de visita
# - Eliminarlo de la base de datos
def submenu_agendar_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir:
        return pedir
    dispatcher.utter_message("Cancelando visita")
    return [SlotSet("solucion_branch", "agendar_3")]

# Opción: Confirmar cita
# - Buscar folio en la base de datos
# - Mandar mensaje de confirmación
def submenu_agendar_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir:
        return pedir
    dispatcher.utter_message("Confirmando cita...")
    return [SlotSet("solucion_branch", "agendar_4")]

# =========================
# SUBMENÚ: CELULAR Y ENERGÍA
# =========================

# Opción: Quiero contratar un plan celular
# - Imprimir planes celulares
def submenu_celular_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Te comparto planes de celular disponibles.")
    return [SlotSet("solucion_branch", "celular_1")]

# Opción: Me interesa ahorrar luz con spot Energy
# - Imprimir planes de luz disponibles
def submenu_celular_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Te comparto planes de luz disponibles.")
    return [SlotSet("solucion_branch", "celular_2")]

# Opción: Tengo dudas sobre estos servicios
# - Imprimir script sobre todos los servicios que tenemos a disposición en luz y energía
def submenu_celular_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("En qué consisten estos servicios y cómo puedes obtenerlos.")
    return [SlotSet("solucion_branch", "celular_3")]

# Cliente que necesita soporte
def submenu_celular_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("¿Cuál es el error que presentas?")
    return [SlotSet("solucion_branch", "celular_4")]

# =========================
# SUBMENÚ: OTROS
# =========================

# Opción: Cancelar mi servicio
# - Consultar número de cuenta, mandar reporte de cancelación
def submenu_otros_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    pedir = pedir_numero_cuenta_para_servicios(dispatcher, tracker)
    if pedir:
        return pedir
    dispatcher.utter_message("Estamos procesando tu solicitud de cancelación.")
    return [SlotSet("solucion_branch", "otros_1")]

# Opción: Quejarme del servicio
# - El mensaje que mande el cliente, imprimirlo como queja y guardarlo
def submenu_otros_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Dime la queja.")
    return [SlotSet("solucion_branch", "otros_2")]

# Opción: Saber más sobre spotuno
# - Mandar mensaje de información sobre la empresa
def submenu_otros_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Mensaje de información sobre la empresa.")
    return [SlotSet("solucion_branch", "otros_3")]

# Opción: Dejar comentario o sugerencia
def submenu_otros_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Deja aquí tu queja.")
    return [SlotSet("solucion_branch", "otros_4")]

# =========================
# DICCIONARIO DE SUBMENÚS
# =========================

# Diccionario para submenús (no se incluye el menú principal aquí)
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

# =========================
# MENÚ PRINCIPAL
# =========================

def volver_menu_principal(dispatcher: CollectingDispatcher) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Menú Principal:\n1. Tengo un problema con mi servicio\n2. Pagos y facturación\n3. Agendar o cambiar visita\n4. Celular o energía\n5. Otro asunto")
    return [SlotSet("estado_menu", "menu_principal")]

# =========================
# ACCIÓN PRINCIPAL DE OPCIONES
# =========================

class ActionElegirOpcion(Action):
    def name(self) -> Text:
        return "action_elegir_opcion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        numero_opcion = tracker.get_slot("numero_opcion")
        if numero_opcion is None:
            numero_opcion = next(tracker.get_latest_entity_values("numero_opcion"), None)

        if not numero_opcion:
            num_servicio = tracker.get_slot("num_servicio")
            if not num_servicio:
                num_servicio = next(tracker.get_latest_entity_values("num_servicio"), None)
            # Si el usuario escribió solo dígitos
            if num_servicio and str(num_servicio).isdigit():
                if 1 <= int(num_servicio) <= 5 and len(str(num_servicio)) == 1:
                    numero_opcion = str(num_servicio)
                elif len(str(num_servicio)) > 1:
                    # Es un número de servicio
                    dispatcher.utter_message("Recibí tu número de servicio.")
                    # Aquí puedes guardar el número o pedir más información
                    return []
    
        if numero_opcion and str(numero_opcion).isdigit() and 1 <= int(numero_opcion) <= 5:
            dispatcher.utter_message(f"DEBUG: Valor recibido: '{numero_opcion}', tipo: {type(numero_opcion).__name__}")
            estado = tracker.get_slot("estado_menu") or "menu_principal"
            if estado == "menu_principal":
                return self.handle_main_menu(dispatcher, numero_opcion)
            elif estado in MENU_HANDLERS:
                return self.handle_submenu(dispatcher, tracker, estado, numero_opcion)
            else:
                dispatcher.utter_message("Estado desconocido.")
                return []
        else:
            dispatcher.utter_message("Por favor, elige una opción del 1 al 5 o proporciona tu número de servicio.")
            return []

    def handle_main_menu(self, dispatcher: CollectingDispatcher, numero_opcion: Text) -> List[Dict[Text, Any]]:
        # Usamos un diccionario para mapear la opción a sus datos:
        opciones = {
            "1": ("Tengo un problema con mi servicio", "submenu_problemas", "utter_opcion_problemas"),
            "2": ("Pagos y facturación", "submenu_pagos", "utter_opcion_pagos"),
            "3": ("Agendar o cambiar visita", "submenu_agendar", "utter_opcion_agendar"),
            "4": ("Celular o energía", "submenu_celular", "utter_opcion_celular"),
            "5": ("Otro asunto", "submenu_otros", "utter_opcion_otros")
        }
        if numero_opcion in opciones:
            mensaje, nuevo_estado, respuesta = opciones[numero_opcion]
            dispatcher.utter_message(text=mensaje)
            # Envia la respuesta configurada en el dominio para mostrar el submenú
            dispatcher.utter_message(response=respuesta)
            return [SlotSet("estado_menu", nuevo_estado)]
        else:
            dispatcher.utter_message("Opción inválida en el menú principal. Elige entre 1 y 5.")
            return []

    def handle_submenu(self, dispatcher: CollectingDispatcher, tracker: Tracker, estado_menu: Text, numero_opcion: Text) -> List[Dict[Text, Any]]:
        if numero_opcion in MENU_HANDLERS.get(estado_menu, {}):
            events = MENU_HANDLERS[estado_menu][numero_opcion](dispatcher, tracker) or []
            # Si la opcion es "5" (regresar), actualizar el estado al menu principal.
            if numero_opcion == "5":
                events.extend([SlotSet("estado_menu", "menu_principal")])
            return events
        else:
            dispatcher.utter_message("Opción inválida en el submenú. Intenta de nuevo.")
            return []

# =========================
# ACCIONES DE SERVICIO Y UTILIDAD
# =========================

# Ejemplo de acción que actúa como raíz para una solución específica
class ActionSolucionProblemas1(Action):
    def name(self) -> Text:
        return "action_solucion_problemas_1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("solucion_branch") == "problemas_1":
            dispatcher.utter_message("Ejecutando solución para el problema 1: iniciando prueba de conexión (ping) y analizando la respuesta...")
        return []

# Acción de pedir el número de cuenta
class ActionPedirNumeroCuenta(Action):
    def name(self) -> Text:
        return "action_pedir_numero_cuenta"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Por favor, proporciona tu número de cuenta para continuar.")
        return [SlotSet("numero_cuenta", None)]  # Reiniciar el slot para el número de cuenta

# Función para pedir números de cuenta a los usuarios para diferentes servicios
def pedir_numero_cuenta_para_servicios(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    numero_cuenta = tracker.get_slot("numero_cuenta")
    if not numero_cuenta:
        dispatcher.utter_message("Por favor, proporciona tu número de cuenta para continuar con el servicio.")
        return [SlotSet("esperando_numero_cuenta", True)]
    return []

# Acción para generar ticket PDF de servicio
class ActionGenerarTicketPDF(Action):
    def name(self) -> Text:
        return "action_generar_ticket_pdf"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[EventType]:

        numero_cuenta = tracker.get_slot("numero_cuenta") or "Desconocido"
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        solucion = tracker.get_slot("solucion_branch") or "No especificada"

        nombre_archivo = f"ticket_{numero_cuenta}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_archivo = os.path.join("tickets", nombre_archivo)

        os.makedirs("tickets", exist_ok=True)

        c = canvas.Canvas(ruta_archivo, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica", 12)

        c.drawString(2 * cm, height - 2 * cm, "TICKET DE SERVICIO")
        c.drawString(2 * cm, height - 3 * cm, f"Número de cuenta: {numero_cuenta}")
        c.drawString(2 * cm, height - 4 * cm, f"Fecha y hora: {fecha}")
        c.drawString(2 * cm, height - 5 * cm, f"Solución aplicada: {solucion}")

        c.showPage()
        c.save()

        dispatcher.utter_message(text=f"Se ha generado tu ticket de servicio en PDF: {nombre_archivo}")
        return []

# =========================
# ACCIONES Y VALIDACIONES PARA PIZZA (EJEMPLO DE OTRO SERVICIO)
# =========================

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
        # Validar el nombre del usuario para la pizza
        dispatcher.utter_message(text=f"OK! Tu nombre es {slot_value} .")
        return {"nombre_usuario": slot_value}

    def validate_num_servicio(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validar el número de servicio para la pizza
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
        # Ruta de la imagen a incluir en el PDF
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
        img = Image.open(imagen_sin_transparencia)
        ancho_img, alto_img = img.size

        ancho_deseado = 10 * cm
        alto_deseado = (ancho_deseado / ancho_img) * alto_img

        x_imagen = (ancho - ancho_deseado) / 2
        y_imagen = 1.5 * cm

        c.drawImage(imagen_sin_transparencia, x_imagen, y_imagen, ancho_deseado, alto_deseado)
        c.save()
        if os.path.exists(imagen_sin_transparencia):
            os.remove(imagen_sin_transparencia)

        dispatcher.utter_message(text=f"Recoge aqui el ticket de tu cita {filename}.")
        return []