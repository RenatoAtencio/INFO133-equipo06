import mariadb
import sys
#! insert.py crea la base de datos y las tablas correspondientes, tambien agrega la informacion inicial (a travez de un arreglo o input)
#! se uso aaron-bond.better-comments extension que resalta comentarios (no afecta al codigo, solo afecta como se ven los comentarios)

#* Conecta a mariadb
try:
    conn = mariadb.connect(
        user="root",
        password="pegasus", #! Cambiar la password a la correspondiente del computador
        host="127.0.0.1",
        port=3306
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()    

#* Dropear la base de datos si existe
cur.execute("DROP DATABASE IF EXISTS Medios_Prensa")

#* Create base de datos 
cur.execute("CREATE DATABASE Medios_Prensa")
cur.execute("USE Medios_Prensa")

#* Crear las tablas (los \ permiten escribir en distintas lineas para leer mejor)
#Ubicacion(PK_(Ciudad,Region,Pais),Continente)
cur.execute("CREATE TABLE Ubicacion( \
            Ciudad VARCHAR(225), \
            Region VARCHAR(225), \
            Pais VARCHAR(225), \
            Continente VARCHAR(225), \
            PRIMARY KEY(Ciudad,Region,Pais))")
#MedioPrensa(PK_NombreMedioPrensa,AñoFundacion,Cobertura,FK_(Ciudad,Region,Pais))
cur.execute("CREATE TABLE MedioPrensa( \
            NombreMedioPrensa VARCHAR(225), \
            AñoFundacion VARCHAR(225), \
            Cobertura VARCHAR(225), \
            Ciudad VARCHAR(225), \
            Region VARCHAR(225), \
            Pais VARCHAR(225), \
            PRIMARY KEY(NombreMedioPrensa), \
            FOREIGN KEY(Ciudad, Region, Pais) REFERENCES Ubicacion(Ciudad, Region, Pais))")
#RedSocial(PK_linkRedSocial,NombreRedSocial,Seguidores,Fecha,FK_NombreMedioPrensa)
cur.execute("CREATE TABLE RedSocial( \
            LinkRedSocial VARCHAR(225), \
            NombreRedSocial VARCHAR(225), \
            Seguidores INT, \
            Fecha DATE, \
            NombreMedioPrensa VARCHAR(225), \
            PRIMARY KEY(LinkRedSocial), \
            FOREIGN KEY(NombreMedioPrensa) REFERENCES MedioPrensa(NombreMedioPrensa))")
#Fundador(PK_FundadorID,Nombre)
cur.execute("CREATE TABLE Fundador( \
            FundadorID INT, \
            NombreFundador VARCHAR(225), \
            PRIMARY KEY(FundadorID))")
#SitioWeb(PK_LinkSitioWeb,FK_NombreMedioPrensa)
cur.execute("CREATE TABLE SitioWeb( \
            LinkSitioWeb VARCHAR(225), \
            NombreMedioPrensa VARCHAR(225), \
            PRIMARY KEY(LinkSitioWeb), \
            FOREIGN KEY(NombreMedioPrensa) REFERENCES MedioPrensa(NombreMedioPrensa))")
#Pagina(PK_LinkPagina,Categoria,XPATHPagina,FK_LinkSitioWeb)
cur.execute("CREATE TABLE Pagina( \
            LinkPagina VARCHAR (225), \
            XPATHLinksNoticias VARCHAR(225), \
            XPATHFecha VARCHAR(225), \
            XPATHTitulo VARCHAR(225), \
            XPATHContenido VARCHAR(225), \
            LinkSitioWeb VARCHAR(225), \
            PRIMARY KEY(LinkPagina), \
            FOREIGN KEY(LinkSitioWeb) REFERENCES SitioWeb(LinkSitioWeb))")
#Noticia(PK_LinkNoticia,XPATHFecha,XPATHContenido,XPATHTitulo,FK_LinkPagina)
cur.execute("CREATE TABLE Noticia( \
            LinkNoticia VARCHAR(1000), \
            Fecha VARCHAR(225), \
            Titulo VARCHAR(225), \
            Contenido VARCHAR(225), \
            LinkPagina VARCHAR(225), \
            PRIMARY KEY(LinkNoticia), \
            FOREIGN KEY(LinkPagina) REFERENCES Pagina(LinkPagina))")
#Fundado(PK_(FK_NombreMedioPrensa,FK_FundadorID))
cur.execute("CREATE TABLE Fundado( \
            NombreMedioPrensa VARCHAR(225), \
            FundadorID INT, \
            PRIMARY KEY(NombreMedioPrensa,FundadorID), \
            FOREIGN KEY(NombreMedioPrensa) REFERENCES MedioPrensa(NombreMedioPrensa), \
            FOREIGN KEY(FundadorID) REFERENCES Fundador(FundadorID))")

#* Sitios web para cargar altiro en la base de datos, sigue la estructura
#  NombreSitioWeb,AñoFundacion,Cobertura,LinkSW,Categorias(dejar 3 por ahora),XPATH(LinkNoticias,Titulo,Contenido,Fecha) Cuidado con el tipo de coma `` o ""
#! Asegurarse que los xpath para titulo y fecha entregen 1 solo elemento
sitiosWeb=[["PaginaSiete","2010","Internacional","https://www.paginasiete.bo/",["nacional","seguridad","economia"],["//div[@class=`headline`]//a/@href","//div//h1","//div[@class=`paragraph texto`]//p","//div[@class=`date`]"]],
           ["ElDeber","2016","Internacional","https://eldeber.com.bo/",["pais","economia","mundo"],["//div//a[@class=`nota-link`]/@href","//div[@class=`heading heading-gallery`]//h1","//div//p","//div[@class=`dateNote`]"]]
           ]

#* Insertar los datos que esten en sitiosWeb
for SW in sitiosWeb:
    cur.execute(f"INSERT INTO MedioPrensa(NombreMedioPrensa,AñoFundacion,Cobertura) VALUES('{SW[0]}','{SW[1]}','{SW[2]}')")
    cur.execute(f"INSERT INTO SitioWeb(LinkSitioWeb,NombreMedioPrensa) VALUES('{SW[3]}','{SW[0]}')")
    for i in range(0,3):
        Link=SW[3]+SW[4][i]
        cur.execute(f"INSERT INTO Pagina(LinkPagina,XPATHLinksNoticias,XPATHTitulo,XPATHContenido,XPATHFecha,LinkSitioWeb) VALUES('{Link}','{SW[5][0]}','{SW[5][1]}','{SW[5][2]}','{SW[5][3]}','{SW[3]}')")

#* Codigo para insertar de manera manual
#! Requiere indicar NombreSitioWeb,AñoFundacion,Cobertura,LinkSitioWeb,Categorias(dejar 3 por ahora),XPATH(LinkNoticias,Titulo,Contenido,Fecha)

#NombreMedioPrensa, LinkPaginaPrincipal = input("Ingrese el Nombre y Link de la pagina del Medio de prensa(Separados por ','): ").split(",")
#print("Nombre Medio Prensa : {} ".format(NombreMedioPrensa))
#print("Link : {} ".format(LinkPaginaPrincipal))

#Nombre, Ciudad ,Region ,Pais , Continente ,Año de creacion del MP crear el elemento en la base de datos

conn.commit() 
conn.close()