import random
from requests_html import HTMLSession
import w3lib.html
import html
import mariadb
import sys
import time
#! crawling.py toma los links de los sitios web y sus categorias y recorre esas paginas en busca de los links para las noticias
#! luego inserta esos links en la tabla noticia

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

#* LinkPaginas toma los links de las paginas por categoria, XPATHs toma los xpaths para tomar los links a las noticias 
cur = conn.cursor()
cur.execute("SELECT LinkPagina FROM Pagina")
LinkPaginas = cur.fetchall()
cur.execute("SELECT XPATHLinksNoticias FROM Pagina")
XPATHs=cur.fetchall()

#* Toma el link de una pagina con su respectivo xpath para tomas los links de las noticias
for i in range(0,len(LinkPaginas)):
    URL_Seed = LinkPaginas[i][0]
    response = session.get("{}".format(URL_Seed),headers=headers)
    xpath = XPATHs[i][0].replace("`","'")
    linkNoticias = response.html.xpath(xpath)
    for linkN in linkNoticias:
        cur.execute(f"INSERT IGNORE INTO Noticia(LinkNoticia,LinkPagina) VALUES ('{linkN}','{URL_Seed}')")

#! no olvidar los commit, esto actualiza la base de datos (en mariadb), sin esto no te aparecen los datos ingresados en el codigo en la base de datos
conn.commit()
conn.close()