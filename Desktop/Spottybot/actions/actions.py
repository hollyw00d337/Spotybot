from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import List, Dict, Any, Text
# Funciones que definen las opciones de cada submenú
# Submenu: Problemas con mi servicio
#Opcion no tengo señal en ningun dispositivo
#Generar script para buscar el ping y si no responde el problema es general no aislado
#generar clase a parte que se invoque para buscar ping
#genera funcion para buscar bases de datos pagos rezagados
def submenu_problemas_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("1.- Verificar que el modem esté prendido\n2.- Reiniciar modem\n3.- Verificar que estén todos los cables bien conectados")
    return [SlotSet("solucion_branch", "problemas_1")]
#Opcion esta muy lento e intermitente
#generar script para buscar el ping y que el problema no sea local
#generar funcion para buscar en la base de datos pagos rezagados
def submenu_problemas_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("1.- Verificar que el modem esté prendido\n2.- Reiniciar modem\n3.- Verificar que estén todos los cables bien conectados")
    return [SlotSet("solucion_branch", "problemas_2")]
#opcion ya pague pero sigue sin servicios
#generar script de ping para buscar que el problema no sea local
# buscar en la base de datos el pago actualizado
def submenu_problemas_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Verificando tu pago...")
    return [SlotSet("solucion_branch", "problemas_3")]
#Vino el tecnico pero no quedo bien
#Aun a planear esta subopcion
def submenu_problemas_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Revisaremos la visita técnica anterior.")
    return [SlotSet("solucion_branch", "problemas_4")]
#Submenu pagos
#opcion validar que ya se recibio pago
#invocar funcion que reciba el numero de cuenta y lo busque en la base de datos
#if si el saldo pendeiente es > 0 no hay ningun pago recibido
#si el saldo pendiente es = 0, ya se reflejo, generar script de pago ya recibido
def submenu_pagos_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Validando si tu pago ha sido recibido...")
    return [SlotSet("solucion_branch", "pagos_1")]
#opcion consultar deuda
#invocar funcion de estado de cuenta
#imprimir el saldo a deber
def submenu_pagos_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Consultando tu deuda actual...")
    return [SlotSet("solucion_branch", "pagos_2")]
#opcion solicitar codigo o forma de pago
#invocar funcion para generar forma de pago ya sea numero de cuenta o QR
def submenu_pagos_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Generando forma de pago...")
    return [SlotSet("solucion_branch", "pagos_3")]
#opcion reactivar servicio
#generar forma de pago
#Al realizar el pago generar ticket para visita de tecnico
def submenu_pagos_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Número de cuenta utilizado en el anterior servicio")
    return [SlotSet("solucion_branch", "pagos_4")]
#submenu agendar
#Agendar visita tecnica
#generar script para agendar cita, pedir domicilio y dar horario
def submenu_agendar_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Agendando visita técnica...")
    return [SlotSet("solucion_branch", "agendar_1")]
#opcion cambiar de domicilio
#buscar el numero de cuenta en la base de datos y agregar cambiar la direccion
def submenu_agendar_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Ingresar número de cuenta")
    return [SlotSet("solucion_branch", "agendar_2")]
#opcion cancelar visita
#buscar folio de visita
# eliminarlo de la base de datos
def submenu_agendar_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Cancelando visita")
    return [SlotSet("solucion_branch", "agendar_3")]
#confirmar cita
# buscr folio en la base de datops
# mandar mensaje de confirmacion

def submenu_agendar_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Confirmando cita...")
    return [SlotSet("solucion_branch", "agendar_4")]
#aun en desarrollo...
#submenu celular y energia
# opcion quiero contratar un plan celular
# imprimir planes celulares
def submenu_celular_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Te comparto planes de celular disponibles.")
    return [SlotSet("solucion_branch", "celular_1")]
#opcion me interesa ahorrar luz con spot Energy
# imprimir planes de luz disponibles
def submenu_celular_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Te comparto planes de luz disponibles.")
    return [SlotSet("solucion_branch", "celular_2")]
# opcion tengo duda sobre estos servicios
# imprimir script sobre todos los servicios que tenemos a disposicion en luz y energia
def submenu_celular_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("En qué consisten estos servicios y cómo puedes obtenerlos.")
    return [SlotSet("solucion_branch", "celular_3")]
#cliente que necesita soporte
def submenu_celular_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("¿Cuál es el error que presentas?")
    return [SlotSet("solucion_branch", "celular_4")]
# submenu otros
# opcion cancelar mi servicio
# consultar numero de cuenta, mandar reporte de cancelacion
def submenu_otros_1(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Estamos procesando tu solicitud de cancelación.")
    return [SlotSet("solucion_branch", "otros_1")]
# opcion de quejarme del servicio
# el mensaje que mande el cliente, imprimirlo como queja y guardarlo
def submenu_otros_2(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Dime la queja.")
    return [SlotSet("solucion_branch", "otros_2")]
# saber mas sobre spotuno
# mandar mensaje de informacion sobre la empresa
def submenu_otros_3(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Mensaje de información sobre la empresa.")
    return [SlotSet("solucion_branch", "otros_3")]
# opcion dejar comenrario o sugerencia

def submenu_otros_4(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    dispatcher.utter_message("Deja aquí tu queja.")
    return [SlotSet("solucion_branch", "otros_4")]

# Diccionario para submenús (no se incluye el menú principal aquí)
# Menu principal esta en dominio
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
    dispatcher.utter_message("Menú Principal:\n1. Tengo un problema con mi servicio\n2. Pagos y facturación\n3. Agendar o cambiar visita\n4. Celular o energía\n5. Otro asunto")
    return [SlotSet("estado_menu", "menu_principal")]

# Accion que evalua la opción elegida y dirige el flujo
class ActionElegirOpcion(Action):
    def name(self) -> Text:
        return "action_elegir_opcion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Se intenta obtener el valor desde el slot y, si no está, de la entidad
        numero_opcion = tracker.get_slot("numero_opcion")
        if numero_opcion is None:
            numero_opcion = next(tracker.get_latest_entity_values("numero_opcion"), None)
        if numero_opcion is not None:
            numero_opcion = str(numero_opcion).strip()
            # Si aparece en formato "1.0", quita el ".0"
            if numero_opcion.endswith(".0"):
                numero_opcion = numero_opcion[:-2].strip()
            # Mapeo de sinónimos
            synonyms = {"uno": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5"}
            if numero_opcion.lower() in synonyms:
                numero_opcion = synonyms[numero_opcion.lower()]
            else:
                try:
                    numero_opcion = str(int(float(numero_opcion)))
                except Exception as e:
                    pass
        else:
            dispatcher.utter_message("No entendí la opción. Por favor, elige un número del 1 al 5.")
            return []

        # Mensaje de debug para verificar el valor
        # Este mensaje fue hecho para pruebas, borrar al terminar bot
        dispatcher.utter_message(f"DEBUG: Valor recibido: '{numero_opcion}', tipo: {type(numero_opcion).__name__}")

        estado = tracker.get_slot("estado_menu") or "menu_principal"
        if estado == "menu_principal":
            return self.handle_main_menu(dispatcher, numero_opcion)
        elif estado in MENU_HANDLERS:
            return self.handle_submenu(dispatcher, tracker, estado, numero_opcion)
        else:
            dispatcher.utter_message("Estado desconocido.")
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

# Ejemplo de accion que actúa como raiz para una solución especifica
class ActionSolucionProblemas1(Action):
    def name(self) -> Text:
        return "action_solucion_problemas_1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("solucion_branch") == "problemas_1":
            dispatcher.utter_message("Ejecutando solución para el problema 1: iniciando prueba de conexión (ping) y analizando la respuesta...")
        return []
