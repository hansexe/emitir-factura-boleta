
from datetime import datetime, timedelta
from boleta import Boleta
from factura import Factura
import threading
from pytz import timezone
import time

start_time = time.time()

def listar_boletas():
    result = Boleta().listar_boletas(1632882050, 1664418050, True)
    data = result['data']
    for index, boleta in enumerate(data):
        if index == 0:
            print(boleta['id'])
            body = Boleta().get_body_boleta(boleta)
            threading.Thread(target=Boleta().emitir_boleta, args=[boleta['id'], body]).start()
            return

def listar_facturas():
    result = Factura().listar_facturas(1632882050, 1664418050, True)
    data = result['data']
    for index, factura in enumerate(data):
        if index == 0:
            body = Factura().get_body_factura(factura)
            threading.Thread(target=Factura().emitir_factura, args=[factura['id'],body]).start()
            return


# listar_boletas()
# listar_facturas()


# fecha_inicio = datetime.timestamp( datetime.now() + timedelta(days=-3))
# fecha_fin = datetime.now() 


print("--- %s segundos ---" % (time.time() - start_time))