from datetime import datetime
import tinytuya
import logging
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'test')
sys.path.append( mymodule_dir )
import pvpc_script

ip = "***.***.***.***"
id = "***************"
key = "**************"

logging.basicConfig(filename='logs_domoticController.log', encoding='utf-8', level=logging.INFO, force=True)
logging.info(str(datetime.now()) + " - Comienza el proceso")

def minimoRango(inicio, fin):
    logging.info(str(datetime.now()) + " - Entra en minimoRango")
    precios_rango = {}
    precios_dia = pvpc_script.getDatos()
    for i in range(inicio, fin+1):
        precios_rango[i] = precios_dia[i]

    precios_ordenados = [(hora, precio) for hora, precio in {hora: precio for hora, precio in sorted(precios_rango.items(), key=lambda item: item[1])}.items()]
    logging.info(str(datetime.now()) + " - Mejor hora tras ordenar: " + str(precios_ordenados[0][0]))

    if precios_ordenados[0][0] == 6:
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, precios_ordenados[0][0], 45)
    elif precios_ordenados[0][0] == 7:
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, precios_ordenados[0][0], 00)
    elif precios_ordenados[0][0] == 8:
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, precios_ordenados[0][0], 00)

def enchufe(hora):

    # Connect to Device - pytuya Method
    d = tinytuya.OutletDevice(id, ip, key)
    d.set_version(3.3)

    # Get Status
    data = d.status()

    # Show status and state of first controlled switch on device
    logging.info(str(datetime.now()) + " - Status previo: " + str(data['dps']['1']))

    # Toggle switch state
    if str(datetime.now().time())[0:5] == str(hora.time())[0:5]:
        logging.info(str(datetime.now()) + "Son las " + str(hora.time())[0:5] + "!!")
        switch_state = data['dps']['1']
        data = d.set_status(not switch_state)  # This requires a valid key
        if data:
            logging.info(str(datetime.now()) + " - Status final: " + str(data))

enchufe(minimoRango(6, 8))
