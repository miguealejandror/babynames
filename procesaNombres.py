from connect import connect
from tabulate import tabulate
import pandas as pd
#Conexion a la Base de Datos
conn=connect()
cur = conn.cursor()

#Importando Archivos
names2018 = pd.read_csv("names2018.txt", sep="\t")
births2018 = pd.read_csv("births2018.txt", sep="\t")

#Separando Nombres por Sexo
nameMale = pd.DataFrame(names2018[["Rank", "Male name"]])
nameFemale = pd.DataFrame(names2018[["Rank","Female name"]])

#Renombrando Columnas para ambos dataframe
nameMale = nameMale.rename(columns={"Male name":"Name"})
nameFemale = nameFemale.rename(columns={"Female name":"Name"})

#Agregamos el Genero
nameMale["Gender"] = "M"
nameFemale["Gender"] = "F"

#Agregamos la Cantidad a Cada nombre
nameMale["Number"] = births2018["Number of males"]
nameMale["Number"] = nameMale["Number"].str.replace('\,+', '')
nameFemale["Number"] = births2018["Number of females"]
nameFemale["Number"] = nameFemale["Number"].str.replace('\,+', '')



#Unimos los dataframes y cambiamos NaN por 0
Result = pd.concat([nameMale,nameFemale])
Result = Result.fillna(0)
Result.index.name ='Index'

#Exportamos Dataframe as csv
Result.to_csv('Result.csv', sep='\t')


#Creando Tabla
query ='''CREATE TABLE IF NOT EXISTS babynames(
   ID INT,
   RANGO INT,
   NOMBRE VARCHAR(50),
   SEX CHAR(1),
   CANTIDAD INT
)'''
cur.execute(query)
print("Tabla creada exitosamente")
conn.commit()

#Insertando los Datos en la tabla
with open('Result.csv','r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f,'babynames', sep='\t')
print("Datos Insertados Correctamente")
conn.commit()
#Realizando las Consultas
#Primera Consulta
print('Los 100 primeros nombres mas populares')
cur.execute("SELECT * FROM babynames ORDER BY cantidad DESC LIMIT 100")
query = cur.fetchall()
print(tabulate(query, headers=['Index', 'Rango', 'Nombre', 'Sexo', 'Cantidad'], tablefmt='psql'))
#Segunda Consulta
print('Todos los nombres que tienen 4 letras o menos y sus rangos')
cur.execute("SELECT * FROM babynames WHERE LENGTH(nombre) < 5")
query = cur.fetchall()
print(tabulate(query, headers=['Index', 'Rango', 'Nombre', 'Sexo', 'Cantidad'], tablefmt='psql'))
#Tercera Consulta
print('Imprima todos los nombres femeninos que tengan las letras ‘w’ o ‘x’ o ‘y’ o ‘z’ en ellas')
cur.execute("SELECT * FROM babynames WHERE sex = 'F' AND (nombre LIKE '%w%' OR nombre LIKE (CONCAT('%','x%')) OR nombre LIKE '%y%' OR nombre LIKE '%z%')")
query = cur.fetchall()
print(tabulate(query, headers=['Index', 'Rango', 'Nombre', 'Sexo', 'Cantidad'], tablefmt='psql'))
#Cuarta Consulta
print('Todos los nombres que tienen dos letras repetidas(aa,cc,pp)')
cur.execute("SELECT * FROM babynames WHERE nombre LIKE (CONCAT('%','aa%')) OR nombre LIKE (CONCAT('%','cc%')) OR nombre LIKE '%pp%'")
query = cur.fetchall()
print(tabulate(query, headers=['Index', 'Rango', 'Nombre', 'Sexo', 'Cantidad'], tablefmt='psql'))


#Cerrando Conexion
cur.close()
conn.commit()
conn.close()
print('Database connection closed.')
