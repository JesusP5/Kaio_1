import pandas as pd

# Ruta al archivo de Excel
ruta_archivo_excel = 'C:/Users/jesus/OneDrive/Documentos/Proyectos propios/Kaio_1/Ventas2022tablaexcel.xlsx'

# Leer el archivo de Excel en un DataFrame de pandas
df = pd.read_excel(ruta_archivo_excel)

# Mostrar los primeros 5 registros del DataFrame
print(df.head())
