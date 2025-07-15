from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormValidationAction
from typing import List, Dict, Any, Text
from rasa_sdk.types import DomainDict
from datetime import datetime
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
#from reportlab.lib.units import cm
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
        "message": "📱 1. Ver planes de celular\n2. Generar código QR de pago\n3. Dudas servicios\n4. Soporte\n5. Regresar al menú principal",
        "options": {
            "1": ("submenu_celular", "utter_planes_celular"),
            "2": ("capturar_datos_qr", "utter_solicitar_datos_qr"),
            "3": ("celular_3", "utter_solucion_celular_3"),
            "4": ("celular_4", "utter_solucion_celular_4"),
            "5": ("menu_principal", "utter_menu_principal"),
        },
        "keywords": {
            "planes": "1", "plan celular": "1", "celular": "1",
            "pago": "2", "qr": "2", "código": "2", "forma de pago": "2",
            "dudas servicios": "3", "dudas": "3", "información": "3",
            "soporte": "4", "ayuda": "4",
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

class ActionMostrarPlanesCelular(Action):
    def name(self) -> Text:
        return "action_mostrar_planes_celular"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        # Mostrar los planes celulares
        dispatcher.utter_message(response="utter_planes_celular")
        
        # Mantener el estado en el submenú celular para permitir navegación
        return [SlotSet("estado_menu", "submenu_celular")]

class ActionGenerarQrPago(Action):
    def name(self) -> Text:
        return "action_generar_qr_pago"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        # Solicitar datos necesarios para generar el QR
        dispatcher.utter_message(response="utter_solicitar_datos_qr")
        
        # Cambiar el estado del menú para capturar los datos
        return [SlotSet("estado_menu", "capturar_datos_qr")]

class ActionProcesarDatosQr(Action):
    def name(self) -> Text:
        return "action_procesar_datos_qr"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        import requests
        import json
        
        # Obtener el texto del usuario (debería contener los datos)
        user_message = tracker.latest_message.get('text', '')
        
        try:
            # Parsear los datos del usuario
            # Formato esperado: "Nombre|Monto|Concepto"
            datos = user_message.split('|')
            
            if len(datos) >= 3:
                nombre = datos[0].strip()
                monto = datos[1].strip()
                concepto = datos[2].strip()
                
                # Preparar payload para tu API
                payload = {
                    "nombre": nombre,
                    "monto": float(monto),
                    "concepto": concepto,
                    "empresa": "SpotUno Telecomunicaciones"
                }
                
                # Hacer petición a tu microservicio
                response = requests.post(
                    "https://apps-ws.spot1.mx/reference-codi",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    qr_data = response.json()
                    # El microservicio debe devolver un link
                    qr_link = qr_data.get('link', qr_data.get('url', qr_data.get('qr_url', 'No disponible')))
                    
                    dispatcher.utter_message(
                        text=f"✅ ¡Código QR generado exitosamente!\n\n"
                             f"📱 **Tu código QR personalizado está listo**\n"
                             f"💰 Monto: ${monto}\n"
                             f"� Beneficiario: {nombre}\n"
                             f"📝 Concepto: {concepto}\n\n"
                             f"🔗 **Link del código QR:**\n{qr_link}\n\n"
                             f"📱 Puedes abrir este link desde tu celular para ver el código QR\n"
                             f"💳 O escanearlo con cualquier app bancaria\n\n"
                             f"⚠️ **IMPORTANTE:**\n"
                             f"• Guarda este link y tu comprobante de pago\n"
                             f"• El servicio se activa en 24-48 hrs\n"
                             f"• Para dudas: 📞 614 399 00 92"
                    )
                else:
                    dispatcher.utter_message(
                        text=f"❌ Error al generar el código QR (Código: {response.status_code})\n"
                             f"Por favor intenta nuevamente o contacta soporte: 614 399 00 92"
                    )
            else:
                dispatcher.utter_message(response="utter_formato_datos_incorrecto")
                
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(
                text="❌ Error de conexión con el servicio de códigos QR.\n"
                     "Por favor intenta más tarde o contacta soporte: 📞 614 399 00 92"
            )
        except ValueError:
            dispatcher.utter_message(
                text="❌ El monto debe ser un número válido.\n"
                     "Ejemplo: Juan Pérez|500|Pago internet enero"
            )
        except Exception as e:
            dispatcher.utter_message(
                text="❌ Error al procesar los datos.\n"
                     "Verifica el formato: NombreCompleto|Monto|Concepto"
            )
        
        # Regresar al menú de celular
        return [SlotSet("estado_menu", "submenu_celular")]

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
            
            # Caso especial: acciones personalizadas para celular
            if estado == "submenu_celular" and numero_opcion == "1":
                # Ejecutar action_mostrar_planes_celular
                from rasa_sdk.executor import CollectingDispatcher
                action_mostrar_planes = ActionMostrarPlanesCelular()
                action_mostrar_planes.run(dispatcher, tracker, domain)
                return [SlotSet("estado_menu", next_state)]
            elif estado == "submenu_celular" and numero_opcion == "2":
                # Ejecutar action_generar_qr_pago
                action_generar_qr = ActionGenerarQrPago()
                action_generar_qr.run(dispatcher, tracker, domain)
                return [SlotSet("estado_menu", next_state)]
            
            # Para el resto de casos, usar utterance normal
            dispatcher.utter_message(response=utterance)
            return [SlotSet("estado_menu", next_state)]

        # Si estamos en estado de capturar datos QR, procesar los datos
        elif estado == "capturar_datos_qr":
            # Si el texto contiene el formato de datos (nombre|monto|concepto)
            if "|" in texto and len(texto.split("|")) >= 3:
                action_procesar_qr = ActionProcesarDatosQr()
                action_procesar_qr.run(dispatcher, tracker, domain)
                return []
            else:
                # Formato incorrecto, mostrar instrucciones nuevamente
                dispatcher.utter_message(response="utter_formato_datos_incorrecto")
                return []

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
        # Fallback mejorado para cuando el usuario se pierde
        estado = tracker.get_slot("estado_menu") or "menu_principal"
        
        # Contar cuántas veces seguidas ha caído en fallback
        eventos_recientes = [evento for evento in tracker.events[-5:] if evento.get("name") == "action_fallback"]
        num_fallbacks_consecutivos = len(eventos_recientes)
        
        if num_fallbacks_consecutivos >= 2:
            # Si ya ha fallado varias veces, ofrecer volver al menú principal
            dispatcher.utter_message(text="Veo que te has perdido un poco. Te llevo de vuelta al menú principal para que puedas empezar de nuevo.")
            dispatcher.utter_message(response="utter_menu_principal")
            return [SlotSet("estado_menu", "menu_principal")]
        else:
            # Primer fallback: dar ayuda específica según el estado actual
            dispatcher.utter_message(response="utter_fallback_custom")
            
            if estado in MENU_DEFS:
                dispatcher.utter_message(text=f"Estás en: {MENU_DEFS[estado].get('name', 'un submenú')}.")
                dispatcher.utter_message(text="Puedes escribir el número de la opción que te interesa, o decir 'volver al menú' para regresar al inicio.")
                dispatcher.utter_message(text=MENU_DEFS[estado]["message"])
            else:
                dispatcher.utter_message(text="Puedes escribir 'menú' para ver las opciones principales.")
                dispatcher.utter_message(response="utter_menu_principal")
                return [SlotSet("estado_menu", "menu_principal")]
        
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

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        # Saludo automático al iniciar una nueva sesión
        dispatcher.utter_message(response="utter_saludar")
        dispatcher.utter_message(response="utter_menu_principal")
        
        # Establecer el estado inicial del menú
        return [SlotSet("estado_menu", "menu_principal")]
