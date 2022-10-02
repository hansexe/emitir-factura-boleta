from environment import Environment
import requests
import xmltodict
import threading
import json
from datetime import datetime
from pytz import timezone

class Factura:
    
    def __init__(self):
        return
    
    def listar_facturas(self, fecha_inicio, fecha_fin, estado) -> dict:
        endpoint = Environment.url_oea + "facturacion/listar/facturas/estado/"
        headers = {'content-type': 'application/json'}
        body ={
            "fecha_inicio" : fecha_inicio,
            "fecha_fin" : fecha_fin,
            "estado" : estado
        }
        response = requests.post(endpoint, data=json.dumps(body), headers=headers)
        # if response.status_code == 200:
        #     print('hola')
        result = json.loads(response.text)
        return result

    def actualizar_factura(self, id, fact_response) -> None:

        endpoint = Environment.url_oea + "facturacion/actualizar/factura/"
        headers = {'content-type': 'application/json'}
        body ={
            "id" : id,
            "fact_response" : fact_response,
        }
        response = requests.patch(endpoint, data=json.dumps(body), headers=headers)
        result = json.loads(response.text)
        print(result)
        return

    def get_body_factura(self, data) -> dict :
        # now_peru = datetime.now(timezone('UTC')).astimezone(timezone('America/Lima'))
        datetimes = datetime.now().strftime('%Y-%m-%d')
        now_peru = f'{datetimes}T0:00:00-05:00'

        jsonload = data['fact_response']
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
          "tipoOperacion": data['fact_tipo_operacion'],
          "tipoDoc": "01",
          "serie": data['fact_serie'],
          "correlativo": data['fact_correlativo'],
          "fechaEmision": str(now_peru),
          "formaPago": {
            "moneda": "PEN",
            "tipo": 'Contado'
          },
          "tipoMoneda": "PEN",
          "client": {
            "tipoDoc": tipo_doc,
            "numDoc": numDoc,
            "rznSocial": nombres,
            "address": {
                    "ubigueo": "",
                    "distrito": "Sin dirección",
                    "direccion": "Sin dirección",
                    "provincia": "Sin dirección",
                    "departamento": "Sin dirección"
                }
            },
          "mtoOperGravadas": float(sutotal),
          "mtoOperExoneradas": 0,
          "mtoIGV": float(igv),
          "mtoISC": 0,
          "totalImpuestos": float(igv),
          "valorVenta": float(sutotal),
          "subTotal": float(total),
          "mtoImpVenta": float(total),
          "details": [
              {
              "codProducto": str(course_code),
              "descripcion": str(descripcion),
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


    def emitir_factura(self, id, body) -> None:
        response = requests.post(Environment().get_url_sunat() + 'send', data=json.dumps(body), headers={
            "Content-type": "application/json",
            "Authorization": 'Bearer ' + str(Environment().get_token())
        })

        # * actualizar
        result = json.loads(response.text)
        if not result.get("sunatResponse"):
            return
        print(result)
        threading.Thread(target=self.actualizar_factura, args=[id,result]).start()
        return