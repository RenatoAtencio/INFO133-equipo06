import random
from requests_html import HTMLSession
import w3lib.html
import html
import mariadb
import sys
import time
#! scraping.py tomas los links de las noticias recopilados en crawling.py y luego extrae los titulos y fecha de cada noticia
#! usando los xpath correspondientes. Tambien la base de datos tiene un xpath para el contenido asi que seria posible tomar tambien el contenido de las noticias 

session = HTMLSession()
USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {'user-agent':random.choice(USER_AGENT_LIST) }

try:
    conn = mariadb.connect(
        user="root",
        password="pegasus",
        host="localhost",
        port=3306,
        database="Medios_Prensa"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

#* Se toman 2 arreglos Links y xpaths, para los links de las noticias y los respectivos xpaths para tomar el titulo y fecha
cur = conn.cursor()
cur.execute("select s.LinkSitioWeb,LinkNoticia from noticia n join pagina p on n.linkpagina=p.linkpagina join sitioweb s on p.linksitioweb=s.linksitioweb order by nombremedioprensa")
Links = cur.fetchall()
# for l in Links:
#     print(l)
#     print("####")
cur.execute("select xpathtitulo,xpathfecha,xpathcontenido from noticia n join pagina p on n.linkpagina=p.linkpagina join sitioweb s on p.linksitioweb=s.linksitioweb order by nombremedioprensa")
xpaths=cur.fetchall()

#* se toman los link del sitio web y se concatena con el resto del link de la noticia, el [-1] quita el ultimo \ del link del sitio web
#* esto se hace ya que al recopilar los links de las noticias nos daban el link completo con un \ al comienzo, asi que se quita uno para que no nos queden links con \\

for link,xpath in zip(Links,xpaths):
    URL_Seed = link[0][:-1] + link[1]
    response = session.get("{}".format(URL_Seed),headers=headers)
    #Estos xpath deberian devolver 1 valor solamente
    titulos = response.html.xpath(xpath[0])
    fechas = response.html.xpath(xpath[1])
    #Verificar que existan elementos
    if len(titulos) > 0:
        titulo = titulos[0].text
    else:
        titulo = "No Encontrado"
    if len(fechas) > 0:
        fecha = fechas[0].text
    else:
        fecha = "No Encontrado"
    # Agrega los titulos y fechas a la tabla noticia
    query = "UPDATE Noticia SET Titulo=%s, Fecha=%s WHERE LinkNoticia=%s"
    cur.execute(query, (titulo, fecha, link[1]))
conn.commit()
conn.close()