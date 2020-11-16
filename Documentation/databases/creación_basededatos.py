# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 21:14:03 2020

@author: juanp
"""
import pandas as pd
import psycopg2 as psc
import pandas.io.sql as sql
import json
import datetime as dt

##############################################################################
"""
Import of the infromation required

"""

data = pd.read_csv(r'C:/Users/juanp/Downloads/base.csv')
#data['latitud_corr'] = data['nuevas coordenadas'].apply(lambda x:float(x[1:-1].split(',')[0]))
#data['longitud_corr'] = data['nuevas coordenadas'].apply(lambda x:float(x[1:-1].split(',')[1]))
#data = data[data.columns[1:]]
#data.to_csv(r'C:/Users/juanp/Downloads/base.csv', index = False)
data['FECHAREGISTRO'] = data['FECHAREGISTRO'].astype('int64')
data['FECHAREGISTRO'] = data['FECHAREGISTRO'].apply(lambda x: dt.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

#############################################################################
"""
Creation of the general table
"""

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

cur = conn.cursor()
cur.execute('''CREATE TABLE GENERAL(
    ID_GENERAL serial PRIMARY KEY,
    SECUENCIA_RECORRIDO int, 
    RECORRIDO_FINALIZADO char(1), 
    ID_VEHICULO int,
    ID_RUTA int,
    FECHA_REGISTRO timestamp,
    LATITUD float,
    LONGITUD float,
    LATITUD_CORR float,
    LONGITUD_CORR float,
    SUBENDELANTERA smallint,
    SUBENTRASERA smallint,
    BAJANDELANTERA smallint,
    BAJANTRASERA smallint
    );''')
conn.commit()

if cur:
    cur.close()
##################################################################################
"""
Pushing the information to the general table
"""

def querysfun(rango_inicio,rango_fin):
    query = '''INSERT INTO GENERAL ( SECUENCIA_RECORRIDO, RECORRIDO_FINALIZADO, ID_VEHICULO,
    ID_RUTA, FECHA_REGISTRO, LATITUD, LONGITUD, LATITUD_CORR, LONGITUD_CORR, SUBENDELANTERA,
    SUBENTRASERA, BAJANDELANTERA, BAJANTRASERA) VALUES '''
    
    values_query = json.dumps(list(zip(
        data['SECUENCIARECORRIDO'].tolist()[rango_inicio : rango_fin],
        data['RECORRIDOFINALIZADO'].tolist()[rango_inicio : rango_fin],
        data['IDVEHICULO'].tolist()[rango_inicio : rango_fin],
        data['CODIGORUTA'].tolist()[rango_inicio : rango_fin],
        data['FECHAREGISTRO'].tolist()[rango_inicio : rango_fin],
        data['LATITUD'].tolist()[rango_inicio : rango_fin],
        data['LONGITUD'].tolist()[rango_inicio : rango_fin],
        data['latitud_corr'].tolist()[rango_inicio : rango_fin],
        data['longitud_corr'].tolist()[rango_inicio : rango_fin],
        data['SUBENDELANTERA'].tolist()[rango_inicio : rango_fin],
        data['SUBENTRASERA'].tolist()[rango_inicio : rango_fin],
        data['BAJANDELANTERA'].tolist()[rango_inicio : rango_fin],
        data['BAJANTRASERA'].tolist()[rango_inicio : rango_fin]
        )))
    
    values_query = values_query[1:-1].replace('[', '(').replace(']', ')').replace('"',"'")
    
    
    query = query+ values_query +';'

    return query

"""
pushing block of information of 250000 rows to the database
"""

querys = [querysfun(250000*i, 250000*(i+1)) for i in range(88)]+[querysfun(22000000, 22261826)]
for query,iteration in list(zip(querys,range(int(len(querys)))))[73:]:
    conn = psc.connect(user = 'team75',
                       password = '*VamosPorLaFoto*',
                       host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                       port = 5432,
                       database = 'postgres')
    
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    
    if cur:
        cur.close()
    print(iteration)
############################################################################
"""
Creation of frontend consume table
"""
conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

cur = conn.cursor()
cur.execute('''CREATE TABLE CONSULTA(
    ID_CONSULTA serial PRIMARY KEY,
    ARCO varchar(25), 
    CARGA int, 
    FECHA timestamp,
    HORA smallint,
    DIA varchar(20)
    );''')
conn.commit()

if cur:
    cur.close()



#######################################################################
"""
Creation of the archs table

"""

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

cur = conn.cursor()
cur.execute('''CREATE TABLE ARCOS(
    ID serial PRIMARY KEY,
    ARCO varchar(25), 
    LATITUD float, 
    LONGITUD float,
    );''')
conn.commit()

if cur:
    cur.close()

###################################################################

"""
Creation of the route table

"""

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

cur = conn.cursor()
cur.execute('''CREATE TABLE RUTAS(
    ID_CONSULTA serial PRIMARY KEY,
    NOMBRE varchar(200), 
    );''')
conn.commit()

if cur:
    cur.close()


#########################################################################

"""
Creation of the KMLS table

"""

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

cur = conn.cursor()
cur.execute('''CREATE TABLE KMLS(
    ID serial PRIMARY KEY,
    LATITUDE float,
    LONGITUDE float,
    ID_RUTA int
    );''')
conn.commit()

if cur:
    cur.close()

###############################################################################


"""
Creation of the VEHICULOS table

"""

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

cur = conn.cursor()
cur.execute('''CREATE TABLE VEHICULOS(
    ID serial PRIMARY KEY,
    PLACE varchar(20),
    MODELO int,
    CAPACIDAD int,
    CAPACIDADDEPIE int,
    CAPACIDADDESENTADOS int,
    ID_EMPRESA int,
    NOMVRE_EMPRESA varchar(150),
    ID_OPERADOR int
    );''')
conn.commit()

if cur:
    cur.close()

###########################################################################
"""
validation of tables
"""

data = pd.read_sql('SELECT * FROM GENERAL LIMIT 1', conn)
data = pd.read_sql('SELECT * FROM KMLS LIMIT 1', conn)
data = pd.read_sql('SELECT * FROM RUTAS  LIMIT 1', conn)
data = pd.read_sql('SELECT * FROM ARCOS  LIMIT 1', conn)
data = pd.read_sql('SELECT * FROM VEHICULOS  LIMIT 1', conn)
data = pd.read_sql('SELECT * FROM CONSULTA  LIMIT 1', conn)


















