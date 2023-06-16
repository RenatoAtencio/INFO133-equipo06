import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="pegasus",
        host="127.0.0.1",
        port=3306
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

#Crea la BD Informacion_Territorial (la elimina al comienzo y quizas de error, comentar el drop si ese es el caso)

cur = conn.cursor()
cur.execute("DROP database Informacion_Territorial")
query_create = "CREATE DATABASE Informacion_Territorial"
cur.execute(query_create)
cur.execute("USE Informacion_Territorial")
cur.execute("CREATE TABLE Pais (NombrePais VARCHAR(225), PRIMARY KEY(NombrePais))")
cur.execute("CREATE TABLE Region (NombreRegion VARCHAR(225), NombrePais VARCHAR(225),PRIMARY KEY(NombreRegion),FOREIGN KEY (NombrePais) REFERENCES Pais(NombrePais))")
cur.execute("CREATE TABLE Comuna (ComunaID VARCHAR(225),NombreComuna VARCHAR(225), NombreRegion VARCHAR(225),PRIMARY KEY (ComunaID),FOREIGN KEY(NombreRegion) REFERENCES Region(NombreRegion))")
cur.execute("CREATE TABLE Tipo(TipoID VARCHAR(225), Descripcion VARCHAR(225), PRIMARY KEY(TipoID))")
cur.execute("CREATE TABLE Establecimiento (EstablecimientoID VARCHAR(225),NombreEstablecimiento VARCHAR(225),ComunaID VARCHAR(225),TipoID VARCHAR(225), PRIMARY KEY(EstablecimientoID),FOREIGN KEY(ComunaID) REFERENCES Comuna(ComunaID),FOREIGN KEY(TipoID) REFERENCES Tipo(TipoID))")
conn.commit() 
conn.close()