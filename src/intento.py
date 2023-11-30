import sqlite3
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

# Crear conexión con la base de datos
conn = sqlite3.connect('indicadores.bd')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute(''' CREATE TABLE IF NOT EXISTS pruebaventas (
    cliente TEXT,
    mes INTEGER, 
    anio INTEGER,
    monto REAL, 
    tipo_moneda TEXT,
    tipo_cambio REAL
)''')
conn.commit()

def ver_graficas_anio():
    # Consulta SQL para obtener los montos de ventas por mes y año
    query = "SELECT anio, mes, SUM(monto) as monto_total FROM pruebaventas GROUP BY anio, mes"

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql_query(query, conn)

    # Crear una columna en el DataFrame que combine el mes y el año
    df['Mes_Año'] = df['mes'].astype(str) + '/' + df['anio'].astype(str)

    # Filtrar los datos para incluir solo los años 2022 y 2023
    df = df[(df['anio'] == 2022) | (df['anio'] == 2023)]

    # Ordenar los datos por la columna "Mes_Año"
    df = df.sort_values('Mes_Año')

    # Crear una gráfica de barras para comparar los montos de ventas por mes y año
    plt.figure(figsize=(10, 6))

    # Ajustar el ancho de las barras para que ocupen menos espacio
    width = 0.35
    plt.bar(df['Mes_Año'], df['monto_total'], width=width)

    plt.xlabel('Mes/Año')
    plt.ylabel('Monto de Ventas')
    plt.title('Monto de Ventas por Mes/Año (2022 y 2023)')
    plt.xticks(rotation=45, ha='right')

    # Ajustar la ubicación de las etiquetas del eje X
    xticks_pos = [i + width / 2 for i in range(len(df['Mes_Año']))]
    plt.xticks(xticks_pos, df['Mes_Año'])

    plt.tight_layout()

    # Mostrar la gráfica sin bloquear la ejecución del programa
    plt.show(block=False)

def ver_graficas_cliente():
    cursor.execute("SELECT cliente, anio, SUM(monto) FROM pruebaventas GROUP BY cliente, anio ORDER BY SUM(monto) DESC")
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

def crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio=None):
    cursor.execute("INSERT INTO pruebaventas VALUES (?, ?, ?, ?, ?, ?)", (cliente, mes, anio, monto, tipo_moneda, tipo_cambio))
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
        [sg.Button('Eliminar', size=(10, 1))]]),
        sg.VSeparator(),
            sg.Column([
                [sg.Text("Informacion de las ventas", font=('Arial', 16))],
                [sg.Button('Act')],
                [sg.Table(values=[],
                          headings=['Cliente', 'Mes', 'Año', 'Monto'],
                          justification='left', font=('Arial', 12),
                          num_rows=20,
                          col_widths=[15, 5, 5, 25],  # Ajustar el ancho de la columna "monto"
                          auto_size_columns=False,
                          key='-TABLE-')],
            ], size=(550, 470))
        ]
    ]

    window = sg.Window('Eliminar información', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        cliente = values['-CLIENTE-']
        mes = int(values['-MES-'])
        anio = int(values['-ANIO-'])
        monto = float(values['-MONTO-'])
        tipo_cambio = float(values['-TIPO_CAMBIO-'])
        monto = monto * tipo_cambio
        
        # Convertir los montos a formato de dinero con dos decimales
        rows_formatted = [(cliente, mes, anio, f"${monto:.2f}") for cliente, mes, anio, monto in rows]

        window['-TABLE-'].update(values=rows_formatted)
        
        cursor.execute("SELECT * FROM pruebaventas WHERE cliente = ? AND mes = ? AND anio = ? AND monto = ?", (cliente, mes, anio, monto))
        row = cursor.fetchone()

        if row:
            cursor.execute("DELETE FROM pruebaventas WHERE cliente = ? AND mes = ? AND anio = ? AND monto = ?", (cliente, mes, anio, monto))
            conn.commit()
            print("Se eliminó la información del cliente.")
        else:
            print("No existe un cliente con esos datos.")
        # Update the table with the latest data after each event
        cursor.execute("SELECT cliente, mes, anio, monto FROM pruebaventas GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
        rows = cursor.fetchall()

    window.close()

def layout_principal():
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    divisas = ['Dolar', 'MXN']

    layout = [
        [
            sg.Column([
                [sg.Image(filename=str(Path('C:/Users/jesus/OneDrive/Documentos/Proyectos_propios/Kaio_1/CBH-Logo.png')), expand_x=True, expand_y=True)],
                [sg.Text("Nombre del cliente:")],
                [sg.Input(key='-CLIENTE-')],
                [sg.Text("Mes de las ventas:")],
                [sg.Combo(meses, key='-MES-', size=(45, 1))],
                [sg.Text("Año de las ventas:")],
                [sg.Input(key='-ANIO-')],
                [sg.Text("Monto:")],
                [sg.Input(key='-MONTO-')],
                [sg.Text("Tipo de moneda (Dolar o MXN):")],
                [sg.Combo(divisas, key='-TIPO_MONEDA-', size=(45, 1))],
                [sg.Text("Tipo de cambio de ese día (si aplica):")],
                [sg.Input(key='-TIPO_CAMBIO-')],
                [sg.Button('Agregar')]
            ]),
            sg.VSeparator(),
            sg.Column([
                [sg.Text("Informacion de las ventas", font=('Arial', 16))],
                [sg.Table(values=[],
                          headings=['Cliente', 'Mes', 'Año', 'Monto'],
                          justification='left', font=('Arial', 12),
                          num_rows=20,
                          col_widths=[15, 5, 5, 25],  # Ajustar el ancho de la columna "monto"
                          auto_size_columns=False,
                          key='-TABLE-')],
                [sg.Button('Act', size=(5, 2)), sg.Button('Borrar informacion', size=(15, 2)),
                 sg.Button('Grafica Año Pasado/Año Actual', size=(18, 2), key='Graf Anio'),
                 sg.Button('Grafica por cliente año actual', key='Graf Cliente', size=(18, 2))]
            ], size=(550, 470))  # Added the key '-TABLE-' to the Column element containing the table
        ]
    ]

    return layout

def main():
    sg.theme('DarkBlue2')
    window = sg.Window('Ventana principal', layout_principal(), finalize=True)
 
    while True:
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
                monto = monto * tipo_cambio
                crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio)
            else:
                crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio=None)
        elif event == 'Borrar informacion':
            eliminar_info()
        elif event == 'Graf Anio':
            ver_graficas_anio()
        elif event == 'Graf Cliente':
            ver_graficas_cliente()

        # Update the table with the latest data after each event
        cursor.execute("SELECT cliente, mes, anio, SUM(monto) FROM pruebaventas GROUP BY cliente, mes, anio ORDER BY anio DESC, mes DESC")
        rows = cursor.fetchall()

        # Convertir los montos a formato de dinero con dos decimales
        rows_formatted = [(cliente, mes, anio, f"${monto:.2f}") for cliente, mes, anio, monto in rows]

        window['-TABLE-'].update(values=rows_formatted)

    window.close()

if __name__ == "__main__":
    main()