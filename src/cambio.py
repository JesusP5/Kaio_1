import sqlite3
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

# Crear conexión con la base de datos
conn = sqlite3.connect('indicadores.bd')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute(''' CREATE TABLE IF NOT EXISTS sales (
    cliente TEXT,
    mes INTEGER, 
    anio INTEGER,
    monto REAL, 
    tipo_moneda TEXT,
    tipo_cambio REAL
)''')
conn.commit()
    
# Establecer el formato de dinero con dos decimales
pd.options.display.float_format = '${:,.2f}'.format
#Esta funcion permite ver la graficas en comparacion del añop 2022 y 2023
def ver_graficas_anio():
    # Consulta SQL para obtener los montos de ventas por mes y año
    query = "SELECT anio, mes, SUM(monto) as monto_total FROM sales GROUP BY anio, mes ORDER BY mes"

    # Ejecutar la consulta y obtener los resultados
    cursor.execute(query)
    rows = cursor.fetchall()

    # Crear listas para almacenar los datos del gráfico
    meses_anio = []
    montos_anio = []

    # Filtrar los datos para incluir solo los años 2022 y 2023
    for anio, mes, monto in rows:
        if anio in (2022, 2023):
            meses_anio.append(f"{mes}/{anio}")
            montos_anio.append(monto)

    # Crear una gráfica de barras para comparar los montos de ventas por mes y año
    plt.figure(figsize=(10, 6))

    # Ajustar el ancho de las barras para que ocupen menos espacio
    width = 0.35
    plt.bar(meses_anio, montos_anio, width=width)

    plt.xlabel('Mes/Año')
    plt.ylabel('Monto de Ventas')
    plt.title('Monto de Ventas por Mes/Año (2022 y 2023)')
    plt.xticks(rotation=45, ha='right')

    # Ajustar la ubicación de las etiquetas del eje X
    xticks_pos = [i + width / 2 for i in range(len(meses_anio))]
    plt.xticks(xticks_pos, meses_anio)

    plt.tight_layout()

    # Mostrar la gráfica sin bloquear la ejecución del programa
    plt.show(block=False)

#Esta funcion permite ver la grafica ordenada por cliente ordenado de forma descenciente
def ver_graficas_cliente():
    cursor.execute("SELECT cliente, anio, SUM(monto) FROM sales GROUP BY cliente, anio ORDER BY SUM(monto) DESC")
    rows = cursor.fetchall()
    clientes = []
    montos = []
    for row in rows:
        cliente, anio, monto = row
        if anio == 2023:  # Filtrar por el año 2023
            clientes.append(cliente)
            montos.append(monto)

    plt.figure(figsize=(8, 5))
    plt.bar(clientes, montos)
    plt.xlabel('Cliente')
    plt.ylabel('Monto')
    plt.title('Monto de ventas por Cliente (Año 2023)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrar la gráfica sin bloquear la ejecución del programa
    plt.show(block=False)
def crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio):
   
    #Si todos los datos son valido entonces ingresar la informacion
    cursor.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)", (cliente, mes, anio, monto, tipo_moneda, tipo_cambio))
    conn.commit()
    sg.popup('Se ha creado la instancia correctamente')
    
def eliminar_info():
    
    layout = [
        [
     sg.Column([
                [sg.Text("Nombre del cliente registrado:")],
                [sg.Input(key='-CLIENTE-', size=(20, 1))],
                [sg.Text("Mes:")],
                [sg.Input(key='-MES-', size=(20, 1))],
                [sg.Text("Año:")],
                [sg.Input(key='-ANIO-', size=(20, 1))],
                [sg.Text("Monto")],
                [sg.Input(key='-MONTO-', size=(20, 1))],
                [sg.Text('Introduce el tipo de cambio que ingresaste si fue en MXN introduce un 1', size=(20, 2))],
                [sg.Input(key='-TIPO_CAMBIO-', size=(20, 1))],
                [sg.Button('Eliminar', size=(10, 1))]
                ]),
                sg.VSeparator(),
                sg.Column([
                    [sg.Input(key = 'Buscar', enable_events=True, size=(30, 1)), sg.Button('Busqueda')],
                    [sg.Table(values=[], headings=['Cliente', 'Mes', 'Año', 'Monto', 'Tipo Cambio'],
                        display_row_numbers=False,
                        auto_size_columns=False,
                        num_rows=20,
                        col_widths=[15, 5, 5, 20],
                        key='-TABLE-')],
                    [sg.Button('Actualizar', size=(10, 1))],
                ])
        ]
    ]
    
    window = sg.Window('Eliminar información', layout)

    while True:
         # Update the table with the latest data after each event
        cursor.execute("SELECT cliente, mes, anio, monto/tipo_cambio, tipo_cambio FROM sales GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
        rows = cursor.fetchall()

        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Eliminar':
            cliente = values['-CLIENTE-']
            mes = int(values['-MES-'])
            anio = int(values['-ANIO-'])
            monto = float(values['-MONTO-'])
            tipo_cambio = float(values['-TIPO_CAMBIO-'])
            monto=monto*tipo_cambio
            
            cursor.execute("SELECT * FROM sales WHERE cliente = ? AND mes = ? AND anio = ? AND monto = ?", (cliente, mes, anio, monto))
            row = cursor.fetchone()

            if row:
                cursor.execute("DELETE FROM sales WHERE  cliente = ? AND mes = ? AND anio = ? AND monto = ?", (cliente, mes, anio, monto))
                conn.commit()
                sg.popup("Se eliminó la información del cliente.")
            else:
                sg.popup("No existe un cliente con esos datos.")
        elif event == 'Actualizar':
            
            cursor.execute("SELECT cliente, mes, anio, monto/tipo_cambio, tipo_cambio FROM sales GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
            rows = cursor.fetchall()
           
            window['-TABLE-'].update(values=rows)
        # Evento para capturar el texto ingresado en el input 'Buscar'
        elif event == 'Busqueda':
            texto_buscar = values['Buscar'].strip().lower()  # Obtener el texto y eliminar espacios y convertir a minúsculas

            # Obtener todos los datos de la tabla
            cursor.execute("SELECT cliente, mes, anio, monto/tipo_cambio, tipo_cambio FROM sales GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
            rows = cursor.fetchall()

            # Filtrar los datos según el texto ingresado en 'Buscar'
            rows_filtrados = [row for row in rows if texto_buscar in str(row).lower()]

            # Convertir los montos a formato de dinero con dos decimales
            rows_formatted = [(cliente, mes, anio, f"${monto:.2f}", tipo_cambio) for cliente, mes, anio, monto, tipo_cambio in rows_filtrados]

            window['-TABLE-'].update(values=rows_formatted)
   
    window.close()

def layout_principal():
    meses = [1,2,3,4,5,6,7,8,9,10,11,12]
    divisas = ['Dolar', 'MXN']
    
    layout = [
        [          
            sg.Column([
                [sg.Image(filename=str(Path('C:/Users/jesus/OneDrive/Documentos/Proyectos_propios/Kaio_1/CBH-Logo.png')), expand_x=True, expand_y=True )],
                [sg.Text("Nombre del cliente:")],
                [sg.Input(key='-CLIENTE-')],
                [sg.Text("Mes de las ventas:")],
                [sg.Combo(meses, key='-MES-', size=(45,1))],
                [sg.Text("Año de las ventas:")],
                [sg.Input(key='-ANIO-')],
                [sg.Text("Monto:")],
                [sg.Input(key='-MONTO-')],
                [sg.Text("Tipo de moneda (Dolar o MXN):")],
                [sg.Combo(divisas, key='-TIPO_MONEDA-', size = (45,1))],
                [sg.Text("Tipo de cambio de ese día (si aplica):")],
                [sg.Input(key='-TIPO_CAMBIO-')],
                [sg.Button('Agregar')]
            ]),
            sg.VSeparator(),
            sg.Column([
                [sg.Text("Informacion de las ventas", font=('Arial', 16), )],
                [sg.Input(key = 'Buscar', enable_events=True, size=(30, 1)), sg.Button('Busqueda')],
                [sg.Table(values=[], 
                          headings=['Cliente', 'Mes', 'Año', 'Monto'], 
                          justification='left', font=('Arial', 12), 
                          num_rows=17, 
                          col_widths=[15,5 , 5, 20], 
                          auto_size_columns=False,
                          key='-TABLE-')],
                [sg.Button('Act', size = (5,2)), sg.Button('Borrar informacion', size=(15, 2)), sg.Button('Grafica Año Pasado/Año Actual', size=(18, 2), key='Graf Anio'), sg.Button('Grafica por cliente año actual',key='Graf Cliente' ,size=(18, 2))]
            ], size=(550,470))  # Added the key '-TABLE-' to the Column element containing the table
        ]
    ]
    
    return layout

def main():
    sg.theme('DarkBlue2')
    window = sg.Window('Ventana principal', layout_principal(), finalize=True)
   
    while True:
         # Update the table with the latest data after each event
        cursor.execute("SELECT cliente, mes, anio, SUM(monto) FROM sales GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
        rows = cursor.fetchall()
        event, values = window.read()
      
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Agregar':
            cliente = values['-CLIENTE-']
            mes = int(values['-MES-'])
            anio = int(values['-ANIO-'])
            monto = float(values['-MONTO-'])
            tipo_moneda = values['-TIPO_MONEDA-']
            
            if tipo_moneda == "Dolar":
                tipo_cambio = float(values['-TIPO_CAMBIO-']) 
                monto = monto*tipo_cambio
                crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio)
            else:
                
                crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio=1)
        elif event == 'Borrar informacion':
            eliminar_info()
        elif event == 'Graf Anio':
            ver_graficas_anio()
        elif event == 'Graf Cliente':
            ver_graficas_cliente()
        elif event == 'Busqueda':
            texto_buscar = values['Buscar'].strip().lower()  # Obtener el texto y eliminar espacios y convertir a minúsculas

            # Obtener todos los datos de la tabla
            cursor.execute("SELECT cliente, mes, anio, SUM(monto) FROM sales GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
            rows = cursor.fetchall()

            # Filtrar los datos según el texto ingresado en 'Buscar'
            rows_filtrados = [row for row in rows if texto_buscar in str(row).lower()]

            # Convertir los montos a formato de dinero con dos decimales
            rows_formatted = [(cliente, mes, anio, f"${monto:.2f}") for cliente, mes, anio, monto in rows_filtrados]

            window['-TABLE-'].update(values=rows_formatted)
        elif event == 'Act':
            None
        
    window.close()
    
if __name__ == "__main__":
    main()