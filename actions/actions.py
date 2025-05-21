# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# This is a simple example for a custom action which utters "Hello World!"
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import List, Dict, Any, Text

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
