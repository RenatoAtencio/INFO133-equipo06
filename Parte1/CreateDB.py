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

cur = conn.cursor()
cur.execute("DROP database MedioPrensa")
query_create = "CREATE DATABASE MedioPrensa"
cur.execute(query_create)
cur.execute("USE MedioPrensa")
cur.execute("CREATE TABLE Ubicacion (Ciudad VARCHAR(225),Region VARCHAR(225),Pais VARCHAR(225),Continente VARCHAR(225), PRIMARY KEY(Ciudad,Region,Pais))")
cur.execute("CREATE TABLE MedioPrensa (NombreMP VARCHAR(225),AñoFundacion DATE,Cobertura VARCHAR(225), PRIMARY KEY(NombreMP),FOREING KEY(Ciudad,Region,Pais) REFERENCES Ubicacion(Ciudad,Region,Pais))")
cur.execute("CREATE TABLE RedSocial (NombreRedSocial VARCHAR(225),Seguidores INT,Link VARCHAR(225),Fecha DATE,NombreMP VARCHAR(225), PRIMARY KEY(Link),FOREIGN KEY(NombreMP) REFERENCES MedioPrensa(NombreMP))")