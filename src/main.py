import sqlite3
import matplotlib.pyplot as plt


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
    tipo_cambio REAL
)''')
conn.commit()


def crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio=None):
    cursor.execute("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?)", (cliente, mes, anio, monto, tipo_moneda, tipo_cambio))
    conn.commit()
    print("Se creó una nueva instancia.")


def leer_datos():
    cliente = input("Nombre del cliente: ")
    mes = int(input("Mes de las ventas: "))
    anio = int(input("Año de las ventas: "))
    monto = float(input("Monto: "))
    tipo_moneda=input("Tipo de moneda (Dolar o MXN): ")
    
    if tipo_moneda=="Dolar":
        tipo_cambio=float(input("Introduce el tipo de cambio de ese dia: "))
        monto=tipo_cambio*monto
    else:
        tipo_cambio=None
    crear_instancia(cliente, mes, anio, monto, tipo_moneda, tipo_cambio)

def ver_info():
    cursor.execute("SELECT cliente, mes, anio, SUM(monto) FROM ventas GROUP BY cliente, mes, anio")
    rows = cursor.fetchall()
    if len(rows) > 0:
        print("Informacion de las ventas registradas")
        for row in rows:
            cliente, mes, anio, monto = row
            print(f"Cliente: {cliente} | Mes: {mes} | Año: {anio} | Monto: {monto} ")  
    else:
            print("No hay informacion registrada")

def eliminar_info():
    cliente = input("Nombre del cliente registrado: ")
    mes = int(input("Introduce el mes: "))
    anio = int(input("Introudece el anio: "))
    monto = float(input("Introduce el monto:"))
    tipo_cambio =  float(input("Si fue en dolares introduce el tipo de cambio, si no ingresa 1:"))
    monto = monto * tipo_cambio
  
    cursor.execute("SELECT * FROM ventas WHERE  cliente = ? AND mes = ? AND anio = ? AND monto = ?",  (cliente, mes, anio, monto))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM ventas WHERE  cliente = ? AND mes = ? AND anio = ? AND monto = ?",  (cliente, mes, anio, monto))
        conn.commit()
        print("Informacion borrada")
    else:
        print("No existe una instancia con la informacion ingresada, verificar su informacion")
def main():
    while True:
        print("\n --- Registro de Ventas ---")
        print("1. Ingresar datos de ventas")
        print("2. Ver informacion")
        print("3. Borrar informacion")
        print("4. Salir")
        opcion = int(input("Selecciona una opción: "))
        
        if opcion == 1:
            leer_datos()
        elif opcion == 2:
            ver_info()
        elif opcion == 3:
            eliminar_info()
        elif opcion == 4:
            break
        else:
            print("Introduce una opcion valida.")
    conn.close()
    
    print("Programa finalizado.")
if __name__ == "__main__":
    main()