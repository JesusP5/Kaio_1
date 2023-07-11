import requests

def obtener_tipo_cambio_historico(base, objetivo, fecha, access_key):
    url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={base}&to_symbol={objetivo}&apikey=VHN39N3M3QJ0GLVV"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        time_series_key = next(iter(data['Time Series FX (Daily)']))
        tipo_cambio = data['Time Series FX (Daily)'][time_series_key]['4. close']
        return tipo_cambio
    else:
        print(f"Error al obtener el tipo de cambio. Código de respuesta: {response.status_code}")
        return None

# Ejemplo de uso
access_key = 'TU_API_KEY'
base = 'USD'
objetivo = 'MXN'
fecha = '2022-07-13'

tipo_cambio = obtener_tipo_cambio_historico(base, objetivo, fecha, access_key)
if tipo_cambio is not None:
    print(f"El tipo de cambio el {fecha} entre {base} y {objetivo} fue: {tipo_cambio}")

    

		