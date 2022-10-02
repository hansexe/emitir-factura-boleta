from environment import Environment
import requests
import xmltodict
import json
from datetime import datetime
from pytz import timezone
import threading

class Boleta:
    
    def __init__(self):
        return

    def listar_boletas(self, fecha_inicio, fecha_fin, estado) -> dict:
        endpoint = Environment.url_oea + "facturacion/listar/boletas/estado/"
        headers = {'content-type': 'application/json'}
        body ={
            "fecha_inicio" : fecha_inicio,
            "fecha_fin" : fecha_fin,
            "estado" : estado
        }
        response = requests.post(endpoint, data=json.dumps(body), headers=headers)
        result = json.loads(response.text)
        return result
    
    def actualizar_boleta(self, id, bol_response) -> None:

        endpoint = Environment.url_oea + "facturacion/actualizar/boleta/"
        headers = {'content-type': 'application/json'}
        body ={
            "id" : id,
            "bol_response" : bol_response,
        }
        response = requests.patch(endpoint, data=json.dumps(body), headers=headers)
        result = json.loads(response.text)
        print(result)
        return

    def get_body_boleta(self, data) -> dict :
        # now_peru = datetime.now(timezone('UTC')).astimezone(timezone('America/Lima'))
        datetimes = datetime.now().strftime('%Y-%m-%d')
        now_peru = f'{datetimes}T0:00:00-05:00'
        jsonload = data['bol_response']
        dictionary = xmltodict.parse(jsonload['xml'])

        numDoc = dictionary['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
        tipo_doc = dictionary['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PartyIdentification']['cbc:ID']['@schemeID']
        nombres = dictionary['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']
        total = str(dictionary['Invoice']['cac:InvoiceLine']['cac:PricingReference']['cac:AlternativeConditionPrice']['cbc:PriceAmount']['#text'])
        total = int(total)
        sutotal = round(total / (1 + 0.18), 2)
        igv = round(total - sutotal, 2)
        sutotal = total - igv

        course_code =  dictionary['Invoice']['cac:InvoiceLine']['cac:Item']['cac:SellersItemIdentification']['cbc:ID']
        descripcion = dictionary['Invoice']['cac:InvoiceLine']['cac:Item']['cbc:Description']
        leyenda = dictionary['Invoice']['cbc:Note']['#text']

        datos = {
            "ublVersion": Environment().get_ubl_version(),
            "tipoOperacion": data['bol_tipo_operacion'],
            "tipoDoc": "03",
            "serie": data['bol_serie'],
            "correlativo": data['bol_correlativo'],
            "fechaEmision": str(now_peru),
            "formaPago": {
                "moneda": "PEN",
                "tipo": "Contado"
            },
            "tipoMoneda": "PEN",
            "client": {
                "numDoc": numDoc,
                "address": {
                    "ubigueo": "",
                    "distrito": "Sin dirección",
                    "direccion": "Sin dirección",
                    "provincia": "Sin dirección",
                    "departamento": "Sin dirección"
                },
                "tipoDoc": tipo_doc,
                "rznSocial": nombres
            },
            "mtoOperGravadas": float(sutotal),
            "mtoOperExoneradas": 0,
            "mtoIGV": float(igv),
            "valorVenta": float(sutotal),
            "totalImpuestos": float(igv),
            "subTotal": float(total),
            "mtoImpVenta": float(total),
            "details": [
                {
                    "codProducto": course_code,
                    "descripcion": descripcion,
                    "unidad": "NIU",
                    "cantidad": 1,
                    "mtoValorUnitario": float(sutotal),
                    "mtoValorVenta": float(sutotal),
                    "mtoBaseIgv": float(sutotal),
                    "porcentajeIgv": 18,
                    "igv": float(igv),
                    "tipAfeIgv": 10,
                    "totalImpuestos": float(igv),
                    "mtoPrecioUnitario": float(total)
                }
            ],
            "legends": [
                {
                    "code": "1000",
                    "value": leyenda
                }
            ]
        }
        datos["company"] = Environment().get_company()
        return datos
    
    def emitir_boleta(self, id, body) -> None:
        response = requests.post(Environment().get_url_sunat() + 'send', data=json.dumps(body), headers={
            "Content-type": "application/json",
            "Authorization": 'Bearer ' + str(Environment().get_token())
        })

        result = json.loads(response.text)
        if not result.get("sunatResponse"):
            return
        print(result)
        threading.Thread(target=self.actualizar_boleta, args=[id,result]).start()
        return