import mariadb
import sys
#! read.py permite realizar consultas a la base de datos
#! tiene un arreglo donde uno le puede poner las consultas o puede hacerse a travez de un input del usuario

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

# arreglo de consultas
Consultas = [["SELECT Linkpagina, count(*) FROM Noticia GROUP BY Linkpagina"]
            ,["SELECT xpathfecha,linksitioweb FROM pagina WHERE linksitioweb LIKE '%eldeber%' GROUP BY linksitioweb"]
            ,]

#* Hace las consultas presentes en el arreglo
cur = conn.cursor()
for consulta in Consultas:
    cur.execute(consulta[0])
    resultado = cur.fetchall()
    for elem in resultado:
        print(" | ".join(str(atrib) for atrib in elem))
    #Para diferenciar entre consultas
    print("#######################")

#* input de usuario
seguir = True
while seguir:
    consulta = input("Cual es tu consulta?: ")
    print(consulta)
    repetir = input("Es esta consulta correcta? (s/n): ")
    while repetir.lower() != "s":
        cosulta = input("Cual es tu consulta?: ")
        repetir = input("Es esta consulta correcta? (s/n): ")

    try:
        cur.execute(consulta)
        resultado = cur.fetchall()
        for elem in resultado:
            print(" | ".join(str(atrib) for atrib in elem))
    except mariadb.Error as error:
        print(f"Consulta Invalida: {error}")
        sys.exit(1)

    continuar = input("Quieres hacer otra consulta? (s/n): ")
    if continuar.lower() == "n":
        seguir = False