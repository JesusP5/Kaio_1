#Se importan las librerias necesarias para ejecutar el programa
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import PySimpleGUI as sg

#Creacion de la base de datos
conn = sqlite3.connect('kaio_db.bd')

#Definir las funciones que se utilizaran en el programa
def creacion_database(conn):
    #Se crea la base de datos
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Ventas (
        
        cliente TEXT,
        mes INTEGER, 
        anio INTEGER,
        monto REAL, 
        tipo_moneda TEXT,
        tipo_cambio REAL
    
    )''')
    conn.commit()
    
def importar_csv_to_sqlite(conn, csv_file_path, table_name, separador):
    #Se importan los datos del csv a la base de datos
    df = pd.read_csv(csv_file_path, sep=separador)
    df.to_sql(table_name, conn, if_exists='append', index=False)


