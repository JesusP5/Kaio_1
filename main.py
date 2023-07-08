import datetime
import sqlite3

#Crear conexion con base de datos
conn = sqlite3.connect('database.bd')
cursor = conn.cursor()

#Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
    cliente TEXT,
    mes INTEGER,
    ANIO INTEGER,
    monto REAL,
    tipo_moneda TEXT,
    fecha_venta TEXT,
    Primary KEY (cliente, mes, anio)
)''')
conn.commit()

def obtener_tipo_cambio(fecha):
    #Implementar logica para obtener en el tipo de cambio segun la fecha en mi base de datos real
    return 20.0
def crear_instancia(cliente,mes,anio,monto,tipo_moneda,fecha_venta=None):
    #Verificar si ya existe una instancia con el mismo cliente, mes y año 
    #ESTUDIAR SINGLETON RECORDAR!!!
    cursor.execute("SELCT * FROM ventas WHERE cliente = ? AND mes = ? AND anio = ?",(cliente, mes, anio))
    row = cursor.fetchone()
    
    if row:
        #Actualizar el monto de ls instancia existente
        nuevo_monto=row[3]+monto
        cursor.execute("UPDARE entas SET monto = ? WHERE cliente = ? AND mes = ? AND anio = ?",  (nuevo_monto, cliente, mes, anio))
        conn.commit()
        print(f"Se actualizo el monto de la instancia existente: {cliente} - {mes}/{anio}")
    else:
        #Obtener el tipo de cambio si se selecciono dolar
        if tipo_moneda == "Dolar":
            tipo_cambio=obtener_tipo_cambio(fecha_venta)
            monto = monto*tipo_cambio
        #Insertar nueva instancia
        cursor.execute("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?)", (cliente, mes, anio, monto, tipo_moneda, fecha_venta))
        conn.commit()
        print("Se creó una nueva instancia.")

def leer_datos():
    cliente = input("Nombre del cliente: ")
    mes = int(input("Mes de las ventas: "))
    anio = int(input("Año de las ventas: "))
    monto = float(input("Monto: "))
    tipo_moneda=input("Tipo de moneda (Dolar o MXN): ")
    
    if tipo_moneda=="Dolar":
        fecha_venta=input("Fecha de la venta (YYYY-MM-DD):")
    else:
        fecha_venta=None
    crear_instancia(cliente, mes, anio, monto, tipo_moneda, fecha_venta)
    
def main():
    while True:
        print("\n --- Registro de Ventas ---")
        print("1. Ingresar datos de ventas")
        print("2. Salir")
        opcion = int(input("Selecciona una opción: "))
        
        if opcion == 1:
            leer_datos()
        elif opcion == 2:
            break
        else:
            print("Introduce una opcion valida.")
    conn.close()
    
    print("Programa finalizado.")
if __name__ == "__mai__":
    main()