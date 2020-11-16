# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 14:23:39 2020

@author: juanp
"""

import pandas as pd
import psycopg2 as psc
import pandas.io.sql as sql
import json
import datetime as dt
import sklearn as skt
from sklearn.neighbors import NearestNeighbors
import numpy as np
from tensorflow.python.keras import backend as K
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import psycopg2 as psc
from tensorflow.keras.models import load_model
import json

####################################################################################

def binary_encoder(value):
    """
    Function to codify the categories of criticity into binary vector.
    This function is done to the neuronal network last layer
    """
    if value == 'baja':
        return [1,0,0,0,0]
    elif value == 'media_baja':
        return [0,1,0,0,0]
    elif value == 'media':
        return [0,0,1,0,0]
    elif value == 'media_alta':
        return [0,0,0,1,0]
    else :
        return[0,0,0,0,1]
        
def binary_decoder(prediction):
    """
    Function to decodify the categories of criticity into labels.
    This function is done to the decodify the prediction of the neuronal network
    """

    prediction = np.argmax(prediction)
    if prediction == 0:
        return 'baja'
    elif prediction == 1:
        return 'media_baja'
    elif prediction == 2:
        return 'media'
    elif prediction == 3:
        return 'media_alta'
    else:
        return 'alta'

#################################################################################
"""
Connection with the database to extract the information of the required tables.
"""

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

#################################################################################

"""
After obtain the tables that are required for the model, 
we standarize the latitude and the longitude of the observation to
taking out all the geographical outlier information.
"""


consulta = pd.read_sql('SELECT * FROM CONSULTA', conn)
arco = pd.read_sql('SELECT ARCO, AVG(LATITUD) AS LATITUD, AVG(LONGITUD) AS LONGITUD FROM ARCOS WHERE LATITUD IS NOT NULL GROUP BY ARCO', conn)

arco['latitud_stand'] = (arco['latitud'] - arco['latitud'].mean())/arco['latitud'].std()

arco['longitud_stand'] = (arco['longitud'] - arco['longitud'].mean())/arco['longitud'].std()

consulta = consulta[consulta['arco'].isin(arco['arco'][(arco['latitud_stand']>3) | (arco['latitud_stand']<-3)].tolist()) == False]
arco = arco[arco['arco'].isin(arco['arco'][(arco['latitud_stand']>3) | (arco['latitud_stand']<-3)].tolist()) == False]

arco['latitud_stand'] = (arco['latitud'] - arco['latitud'].mean())/arco['latitud'].std()

arco['longitud_stand'] = (arco['longitud'] - arco['longitud'].mean())/arco['longitud'].std()

###################################################################################

"""
Mergin the information of latitude and longitude of the archs 
with the information of days, hours and charge of passengers

"""


data = consulta.merge(arco,on ='arco', how='left')
del(arco)
del(consulta)
###################################################################################


"""
define a log scale for charge of passenger. this procedure is made to reduce the 
dispersion and to change the distribution of the information. At the end,
the result is a nolmal distributed

"""

data['log_carga'] = np.log(data['carga'] +1) 


data.loc[data['log_carga'] <= data['log_carga'].quantile(0.2) ,'cluster'] = 'baja'
data.loc[(data['log_carga'] > data['log_carga'].quantile(0.2)) & (data['log_carga']<= data['log_carga'].quantile(0.4)),'cluster'] = 'media_baja'
data.loc[(data['log_carga'] > data['log_carga'].quantile(0.4)) & (data['log_carga']<= data['log_carga'].quantile(0.6)),'cluster'] = 'media'
data.loc[(data['log_carga'] > data['log_carga'].quantile(0.6)) & (data['log_carga']<= data['log_carga'].quantile(0.8)),'cluster'] = 'media_alta'
data.loc[data['log_carga'] > data['log_carga'].quantile(0.8),'cluster'] = 'alta'

###################################################################################

"""
make cross and level dummy variables of archs, days and hours.
The idea behind is to have independent neurons that just been activate when it look 
for an specific space of the city, and specific moment in time 
"""


y = data['cluster']
data = data[['dia','hora','arco']]
    
data['hora_dia'] = data['hora'].astype('str') + '_' + data['dia'].astype('str')


x =  pd.get_dummies(data[['arco','hora_dia','hora']], columns=['arco','hora_dia','hora'],drop_first = True)

del(data)

y = np.array([binary_encoder(category) for category in y ])

###################################################################################

"""
split the variables into test and train datasets
"""
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.7)
del(y)

#############################################################################

"""
Define the neuronal network model and save it afeter been excecuted
"""

K.clear_session()
model = tf.keras.Sequential()

model.add(tf.keras.layers.Dense(120, input_dim=x_train.shape[1], activation='tanh'))
model.add(tf.keras.layers.Dense(50, activation='tanh'))
model.add(tf.keras.layers.Dense(20, activation='tanh'))
model.add(tf.keras.layers.Dense(5,activation='softmax'))

model.compile(loss='categorical_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])

model.fit(x_train,
          y_train,
          validation_data=(x_test, y_test),
          batch_size = 200,
          epochs = 10)


model.save('C:/Users/juanp/OneDrive/Escritorio/aburrappmodel_structure.h5')
model.save_weights('C:/Users/juanp/OneDrive/Escritorio/aburrappmodel_weights.h5')
del(
    x_test,
    x_train,
    y_test,
    y_train
    )
#model = load_model('C:/Users/juanp/OneDrive/Escritorio/aburrappmodel_structure.h5')
#model .load_weights('C:/Users/juanp/OneDrive/Escritorio/aburrappmodel_weights.h5')


###############################################################################
"""
Make the prediction of actual data,
it could be new data if the advance architecture where implemented

"""

prediction = model.predict(x)

conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')

consulta = pd.read_sql('SELECT * FROM CONSULTA', conn)
arco = pd.read_sql('SELECT ARCO, AVG(LATITUD) AS LATITUD, AVG(LONGITUD) AS LONGITUD FROM ARCOS WHERE LATITUD IS NOT NULL GROUP BY ARCO', conn)

arco['latitud_stand'] = (arco['latitud'] - arco['latitud'].mean())/arco['latitud'].std()

arco['longitud_stand'] = (arco['longitud'] - arco['longitud'].mean())/arco['longitud'].std()

consulta = consulta[consulta['arco'].isin(arco['arco'][(arco['latitud_stand']>3) | (arco['latitud_stand']<-3)].tolist()) == False]
arco = arco[arco['arco'].isin(arco['arco'][(arco['latitud_stand']>3) | (arco['latitud_stand']<-3)].tolist()) == False]

del(arco)

consulta['nivel'] = [binary_decoder(obs) for obs in prediction ] 
consulta['nivel'] = consulta['nivel'].str.replace('_',' ')

print(consulta['nivel'])
del(prediction)


############################################################################

"""
Create the table that going to contain the new prediction
"""




conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')



query = """
CREATE TABLE PREDICCION
(
ID serial PRIMARY KEY,
ARCO varchar(25),
CARGA int,
FECHA timestamp,
HORA smallint,
DIA smallint,
NIVEL varchar(25) 
)
;
"""

cur = conn.cursor()
cur.execute(query)
conn.commit()

if cur:
    cur.close()

#############################################################################
"""
Push the prediction of the model to the database in block of 250000 rows,
that was because the database daesnt suport a masive set of values.
(it is a free tier instance)
"""

query = """
INSERT INTO PREDICCION
(
ARCO,
CARGA,
FECHA,
HORA,
DIA,
NIVEL 
)
VALUES
"""
for i in range(10):
    data = list(zip(
        consulta['arco'].tolist()[i*250000:(i+1)*250000],
        consulta['carga'].tolist()[i*250000:(i+1)*250000],
        pd.to_datetime(consulta['fecha'],format = '%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d').tolist()[i*250000:(i+1)*250000],
        consulta['hora'].tolist()[i*250000:(i+1)*250000],
        consulta['dia'].astype('int').tolist()[i*250000:(i+1)*250000],
        consulta['nivel'].tolist()[i*250000:(i+1)*250000]
        ))
    data = json.dumps(data)
    data = data[1:-1]
    data = data.replace('[', '(').replace(']', ')').replace('"',"'")
    
    
    conn = psc.connect(user = 'team75',
                       password = '*VamosPorLaFoto*',
                       host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                       port = 5432,
                       database = 'postgres')
    
    
    cur = conn.cursor()
    cur.execute(query + data + ';')
    conn.commit()
    
    if cur:
        cur.close()
    print(i)

data = list(zip(
    consulta['arco'].tolist()[2500000:],
    consulta['carga'].tolist()[2500000:],
    pd.to_datetime(consulta['fecha'],format = '%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d').tolist()[2500000:],
    consulta['hora'].tolist()[2500000:],
    consulta['dia'].astype('int').tolist()[2500000:],
    consulta['nivel'].tolist()[2500000:]
    ))
data = json.dumps(data)
data = data[1:-1]
data = data.replace('[', '(').replace(']', ')').replace('"',"'")


conn = psc.connect(user = 'team75',
                   password = '*VamosPorLaFoto*',
                   host = 'amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',  
                   port = 5432,
                   database = 'postgres')


cur = conn.cursor()
cur.execute(query + data + ';')
conn.commit()

if cur:
    cur.close()
print('end')





