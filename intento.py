import datetime
import sqlite3
import tkinter as tk

# Crear conexión con la base de datos
conn = sqlite3.connect('database.bd')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
    cliente TEXT,
    mes INTEGER,
    anio INTEGER,
    monto REAL,
    tipo_moneda TEXT,
    fecha_venta TEXT,
    PRIMARY KEY (cliente, mes, anio)
)''')
conn.commit()

def obtener_tipo_cambio(fecha):
    # Implementar lógica para obtener el tipo de cambio según la fecha en tu base de datos real
    return 20.0

def crear_instancia():
    global nombre_cliente  # Declarar como variable global

    cliente = nombre_cliente.get()
    mes = int(mes_entry.get())
    anio = int(anio_entry.get())
    monto = float(monto_entry.get())
    tipo_moneda = tipo_moneda_var.get()

    if tipo_moneda == "Dolar":
        fecha_venta = fecha_entry.get()
        tipo_cambio = obtener_tipo_cambio(fecha_venta)
        monto = monto * tipo_cambio

    cursor.execute("SELECT * FROM ventas WHERE cliente = ? AND mes = ? AND anio = ?", (cliente, mes, anio))
    row = cursor.fetchone()

    if row:
        nuevo_monto = row[3] + monto
        cursor.execute("UPDATE ventas SET monto = ? WHERE cliente = ? AND mes = ? AND anio = ?", (nuevo_monto, cliente, mes, anio))
        conn.commit()
        print(f"Se actualizó el monto de la instancia existente: {cliente} - {mes}/{anio}")
    else:
        cursor.execute("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?)", (cliente, mes, anio, monto, tipo_moneda, fecha_venta))
        conn.commit()
        print("Se creó una nueva instancia.")

def ver_info():
    cursor.execute("SELECT * FROM ventas")
    rows = cursor.fetchall()
    if len(rows) > 0:
        print("Informacion de las ventas registradas")
        for row in rows:
            cliente, mes, anio, monto, tipo_moneda, fecha_venta = row
            print(f"Cliente: {cliente} | Mes: {mes} | Año: {anio} | Monto: {monto} | Moneda: {tipo_moneda} | Fecha: {fecha_venta}")
    else:
        print("No hay informacion registrada")

def main():
    ventana = tk.Tk()
    ventana.title("Registro de Ventas")

    # Etiquetas
    tk.Label(ventana, text="Nombre del cliente:").grid(row=0, column=0)
    tk.Label(ventana, text="Mes:").grid(row=1, column=0)
    tk.Label(ventana, text="Año:").grid(row=2, column=0)
    tk.Label(ventana, text="Monto").grid(row=3, column=0)
    tk.Label(ventana, text="Tipo de moneda:").grid(row=4, column=0)
    tk.Label(ventana, text="Fecha de PO").grid(row=5, column=0)

    # Campos de entrada
    nombre_cliente = tk.StringVar()
    nombre_entry = tk.Entry(ventana, textvariable=nombre_cliente)
    nombre_entry.grid(row=0,column=1)

    mes_entry = tk.Entry(ventana)
    mes_entry.grid(row=1,column=1)

    anio_entry = tk.Entry(ventana)
    anio_entry.grid(row=2, column=1)

    monto_entry = tk.Entry(ventana)
    monto_entry.grid(row=3, column=1)

    tipo_moneda_var = tk.StringVar()
    tipo_moneda_combobox = tk.OptionMenu(ventana, tipo_moneda_var, "Dolar", "MXN")
    tipo_moneda_combobox.grid(row=4, column=1)

    fecha_entry = tk.Entry(ventana)
    fecha_entry.grid(row=5, column=1)

    # Botones
    boton_ingresar = tk.Button(ventana, text="Ingresar", command=crear_instancia)
    boton_ingresar.grid(row=6, column=0)

    boton_ver_info = tk.Button(ventana, text="Ver informacion", command=ver_info)
    boton_ver_info.grid(row=6, column=1)

    boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit)
    boton_salir.grid(row=6, column=2)

    ventana.mainloop()
    print("Programa finalizado.")

if __name__ == "__main__":
    main()
