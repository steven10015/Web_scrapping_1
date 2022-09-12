# Web scraping problem

En este proyecto, vamos a raspar los datos de ingresos de Tesla, almacenarlos en un marco de datos, y también en una base de datos sqlite.

Para saber si un sitio web permite el web scraping (raspado web) o no, puedes consultar el archivo "robots.txt" del sitio web. Puedes encontrar este archivo agregando `/robots.txt` a la URL que deseas raspar.

## Paso 1: Configuración e instalación

Asegúrate de tener instalados sqlite3 y pandas.

En caso de que no estén instalados, puedes usar el siguiente comando en la terminal:

```py
pip install pandas sqlite3 requests
```

Nota: esto instalará bibliotecas y bibliotecas.

## Paso 2: Crear app.py

Abre la carpeta `./src` y crea un nuevo archivo app.py, agrégale el siguiente contenido:

```py
print("Hello world")
```

Ejecuta el archivo usando el comando `python ./src/app.py`.

### Paso 3: Descargar los datos usando la biblioteca de solicitudes

Usa la [biblioteca de solicitudes](https://requests.readthedocs.io/en/latest/user/quickstart/) para descargar los datos.

El siguiente sitio web contiene los datos de ingresos de Tesla de los últimos años:
https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue

Guarda el texto de la respuesta como una variable denominada html_data.

### Paso 4: Analizar los datos html usando beautiful_soup

Crea una nueva instancia de BeautifulSoup con html_data.

Utiliza beautiful soup o la función read_html para extraer la tabla con los ingresos trimestrales de Tesla y almacenarla en un marco de datos denominado tesla_revenue. El marco de datos debe tener columnas Fecha e Ingresos. Asegúrate de eliminar la coma y el signo de dólar de la columna Ingresos. Inspecciona el código html para saber qué partes de la tabla se deben encontrar.

1. Encontrar todas las tablas.
2. Encontrar una tabla con los ingresos trimestrales de Tesla.
3. Crear el marco de datos.
4. Iterar sobre las filas de la tabla para obtener los valores y eliminar el `$` y la `coma`.

## Paso 5: Filas limpias

Elimina las filas en el marco de datos que son cadenas vacías o son `NaN` en la columna Ingresos.

Imprime todo el marco de datos `tesla_revenue` para ver si tienes alguno.

### Paso 6: Insertar los datos en sqlite3

Asegúrate de que tesla_revenue siga siendo un marco de datos.

Inserta los datos en sqlite3 convirtiendo el marco de datos en una lista de tuplas.

### Paso 7: Conectar a SQLite

Ahora vamos a crear una base de datos SQLite3. Utiliza la función connect() de sqlite3 para crear una base de datos. Creará un objeto de conexión. En caso de que la base de datos no exista, la creará.

Utiliza la función `sqlite3.connect()` de sqlite3 para crear una base de datos. Creará un objeto de conexión.

### Paso 8: Vamos a crear una tabla en nuestra base de datos para almacenar nuestros valores de ingresos:

1. Crear tabla.
2. Insertar los valores.
3. Guardar (commit) los cambios.

### Paso 9: Ahora recupera los datos de la base de datos.

El nombre de nuestra base de datos es "Tesla.db". Guardamos la conexión al objeto de conexión.

La próxima vez que ejecutemos este archivo, simplemente se conectará a la base de datos y, si la base de datos no está allí, creará una.

### Paso 10: Finalmente crea un gráfico para visualizar los datos

¿Qué tipo de visualizaciones muestran que hacemos?

Fuente:

https://github.com/bhavyaramgiri/Web-Scraping-and-sqlite3/blob/master/week%209-%20web%20scraping%20sqlite.ipynb

https://coderspacket.com/scraping-the-web-page-and-storing-it-in-a-sqlite3-database

https://gist.github.com/elifum/09dcaecfbc6c6e047222db3fcfe5f3b8