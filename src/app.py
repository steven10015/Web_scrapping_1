import pandas as pd
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import time
from urllib.request import Request, urlopen
import lxml
import html5lib
import sqlite3


#Hacemos el request para acceder a la informacion y filtramos las tablas
req = Request('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue', headers={'User-Agent': 'XYZ/3.0'})
webpage = urlopen(req, timeout=10).read()
soup = BeautifulSoup(webpage, 'html.parser')
tablas = soup.find_all('table')


#Ubicamos la tabla que nos interesa en este caso 
for indice, tabla in enumerate(tablas):
    if ("Tesla Quarterly Revenue" in str(tablas)):
        tablas.index = indice
        break

#Leemos la tabla que nos interesa e indicamos que renombre las columnas
resultado = pd.read_html(str(tablas))[1]
tabladf =pd.DataFrame(resultado)
tabladf = tabladf.rename(columns={"Tesla Quarterly Revenue(Millions of US $)": "Fecha", "Tesla Quarterly Revenue(Millions of US $).1": "Monto"})
tabladf.replace('\$', '', regex=True, inplace=True)
tabladf.head()

#Validamos que no tenga valores vacios 
tabladf.fillna(0, inplace=True)

#Conectamos con sqlite
connection = sqlite3.connect("tablatesla.db")

#Creamos la Tabla
cursor = connection.cursor()
cursor.execute("""CREATE TABLE revenue (Fecha, Monto)""")

#Transformamos los valores a tuplas 
Tabla_tp = list(tabladf.to_records(index = False))
Tabla_tp[:5]

#Insertamos los Valores 
cursor.executemany("INSERT INTO revenue VALUES (?,?)", Tabla_tp)
connection.commit()

#Cerramos Conexion
connection.close()


#Graficamos los valores

