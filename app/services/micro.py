import requests
def procesar_dni(dni):
    url = "https://demo.mikrosystem.net/api/v1/GetClientsDetails"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "token": "Smx2SVdkbUZIdjlCUlkxdFo1cUNMQT09",
        "cedula": dni
    }
    response = requests.post("https://demo.mikrosystem.net/api/v1/GetClientsDetails", json={
        "Content-Type": "application/json"
    }, headers={
        "token": "Smx2SVdkbUZIdjlCUlkxdFo1cUNMQT09",
        "cedula": dni
    })
    response = response.json()
    if response["estado"] == "error":
        return "error"
    else: 
        if response["estado"] == "exito" and response["datos"]:
            primer_cliente = response["datos"][0]  # Accede al primer cliente
            mensaje_para_usuario = primer_cliente["nombre"]  # Extrae el nombre
        else:
            mensaje_para_usuario = "error"
    return mensaje_para_usuario
        

def enviar_ticket(nombre, dni, contenido):
    url = "https://demo.mikrosystem.net/api/v1/NewTicket"
    headers = {
        "Content-Type": "application/json"  
    }
    payload = {
        "token": "Smx2SVdkbUZIdjlCUlkxdFo1cUNMQT09",
        "solicitante": nombre,
        "cedula": dni,
        "dp": "1",
        "asunto": "Solicitud de ticket",
        "agendado": "Solicitud desde el bot de WhatsApp",
        "contenido": contenido
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json() 