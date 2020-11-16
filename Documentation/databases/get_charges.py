from scipy import spatial
import pandas as pd
import psycopg2 as psc
from datetime import datetime, timedelta
import json
import logging


def delta_secrec(data, minval=5):

    """
    ****
    Description:

     # This function is used to eliminate the trips that
     # have less than 5 registers to avoid a use of
     # higher memory, all cleaning is done
     # on the same object using the drop function.

    Parameters:

    -data:It is the table that emerges from the SQL query. Its name in this script is df_Medicion.
     It is the table with which the information for the DS4A challenge was provided. 
     It contains the following columns:"secuenciarecorrido","recorridofinalizado","idvehiculo",
     "codigoruta","fecharegistro","latitud","longitud",
     "subendelantera","subentrasera","bajandelantera","bajantrasera"
    -minval: It a integer, it is the minimum value of stops valid for a trip. The default values is: 5
    ****
    """

    """Count the amount of records per travel"""
    aggreg = {'id_vehiculo': "count"}
    filt_reg = data.copy().groupby("secuencia_recorrido").agg(aggreg)
    filt_reg.rename(columns={'id_vehiculo': "n"}, inplace=True)
    filt_reg.reset_index(inplace=True)

    """Drop the travels"""
    rec_fil = list(filt_reg[filt_reg["n"] < minval]["secuencia_recorrido"].unique())
    index_to_drop = data[data["secuencia_recorrido"].isin(rec_fil)].index
    data.drop(index=index_to_drop, axis=0, inplace=True)


def limit_cap(df,var_list=['subendelantera','subentrasera', 'bajandelantera', 'bajantrasera'],maxVal='cappasajeros'):
    """
    ****
    Description:

    # The limit_cap function is used to limit the values of the up and down streams to the capacity of the bus.
    # It uses the information contained in the tables of measurements and vehicles.

    Parameters:

    -df: It is a dataframe. It is the result of the merge between df_Medicion and df_Vehiculos.
     It contains the following columns:"secuenciarecorrido","recorridofinalizado","idvehiculo",
     "codigoruta","fecharegistro","latitud","longitud",
     "subendelantera","subentrasera","bajandelantera","bajantrasera", "placavehiculo",
     "modelo", "cappasajeros", "cappasajerospie", "cappasajerossentados",
     "idempresa" and "nombres"
    -var_list: It is a list with the names of the upstream and downstream flows in the df table. 
     The default values are: ['subendelantera','subentrasera', 'bajandelantera', 'bajantrasera']
    -maxVal: It is a string with the name of the bus capacity in table df. The default values is: "cappasajeros"
    ****
    """
    for var in var_list:
        df[var].where(df[var]<df[maxVal], df[maxVal], inplace=True)
    return


def assign_link(df_Medicion, df_Arcos):

    """
    ****
    Description:
    # This function assigns the arcs to each point of the DataFrame df_Medicion.
    # It requires the library spatial from scipy to perform the calculations

    Parameters:

    -df_Medicion: It is a DataFrame that emerges from the SQL query. Its name in this script is df_Medicion.
     The format is the same of the information provided for the DS4A challenge. 
     It contains the following columns:"secuenciarecorrido","recorridofinalizado","idvehiculo",
     "codigoruta","fecharegistro","latitud","longitud",
     "subendelantera","subentrasera","bajandelantera","bajantrasera"
    -df_Arcos: It is a DataFrame, each record contains an arch id and its location (latitude and longitude) 
     from Medellin road network.
    ****
    """

    """Selecting the data"""
    data_tuple = list(zip(df_Medicion['latitud_corr'],
                        df_Medicion['longitud_corr']))

    """Giving specified format to arc data
        according to the spatial.KDTree function"""
    df_Arcos['Coordinates'] = list(zip(df_Arcos['latitud'], df_Arcos['longitud']))
    arc_coordinates = df_Arcos['Coordinates']
    arc_coordinates_list = arc_coordinates.tolist()
    arc_coord_df = pd.DataFrame(arc_coordinates)

    """Aplying the function. It queries the route
        coordinate that is closest to each tuple in data tuple"""
    tree = spatial.KDTree(arc_coordinates_list)
    coord_index = tree.query([data_tuple])[1][0]

    """Generating a new coordinates list that
        is going to be added to the dataframe"""
    arc_list = []
    for i in coord_index:
        arc_list.append(df_Arcos[df_Arcos.index==i]['arco'].iloc[0])

    """Adding the new coordinates list to the dataframe"""
    df_Medicion.loc[:, 'arco'] = pd.Series(arc_list)

    return df_Medicion


def carga(df):

    """
    ****
    Description:
    # This function performs the calculation of the loads for each node of the road mesh.
    # This function requires the functions limit_cap, delta_secrec, assign_link to be executed before.

    Parameters:

    -df: It's a data frame. 
    -This function must be excute after the function assign_link()
    -It is the table with which the information for the DS4A challenge was provided. 
    -It contains the following columns:"SECUENCIARECORRIDO","RECORRIDOFINALIZADO","IDVEHICULO",
    "CODIGORUTA","FECHAREGISTRO","LATITUD","LONGITUD",
    "SUBENDELANTERA","SUBENTRASERA","BAJANDELANTERA","BAJANTRASERA"
    ****
    """

    """difference between passengers who get on and off"""
    df.sort_values(by=["secuencia_recorrido","fecha_registro"],inplace=True,ascending=True)
    df['delta_q'] = df['subendelantera']+df['subentrasera']-df['bajandelantera']-df['bajantrasera']

    df['fecha'] = df['fecha_registro'].apply(lambda x: x.date())
    df["carga"] = df.groupby(by=['secuencia_recorrido', 'fecha'])['delta_q'].cumsum()
    df.reset_index(inplace=True)

    """Set to zero negative values"""
    df.loc[df['carga'] < 0, 'carga'] = 0
    """Limitar las cargas a la capacidad del bus"""
    df["carga"].where(df["carga"]<df["cappasajeros"], df["cappasajeros"], inplace=True)

    """Group by Arco date and hour"""
    df = df.groupby(by=['arco', pd.Grouper(key='fecha_registro', freq='H')]).sum()
    df.reset_index(inplace=True)

    """Set some columns like fecha, hora and dia"""
    df['fecha'] = df['fecha_registro'].apply(lambda x: x.date())
    df['hora'] = df['fecha_registro'].dt.hour
    df['dia'] = df['fecha_registro'].dt.dayofweek

    """Drop unnecessary columns"""
    df.drop(columns=['id_general', 'index', 'delta_q', 'secuencia_recorrido', 'id_ruta',
                     'id_vehiculo', 'latitud', 'longitud', 'latitud_corr',
                     'longitud_corr', 'subendelantera', 'subentrasera',
                     'bajandelantera', 'bajantrasera', 'fecha_registro',
                     'idvehiculo','modelo','cappasajeros','cappasajerospie',
                     'cappasajerossentados','idempresa','identidadopera'],
            inplace=True)

    """Set to zero negatives loads"""
    return df


def load_data(data_consulta):
    """
    Function to load the dat to the data base

    data_consulta: data that will be loaded
    """
    query = '''
    INSERT INTO CONSULTA (ARCO, CARGA, FECHA, HORA, DIA) VALUES
    '''

    data_consulta['fecha'] = pd.to_datetime(data_consulta['fecha'], format = '%Y-%m-%d')
    data_consulta['fecha'] = data_consulta['fecha'].dt.strftime('%Y-%m-%d')

    data_str = json.dumps(list(zip(
        data_consulta['arco'].tolist(),
        data_consulta['carga'].tolist(),
        data_consulta['fecha'].tolist(),
        data_consulta['hora'].tolist(),
        data_consulta['dia'].tolist()
        )))

    data_str = data_str[1:-1].replace('[', '(').replace(']', ')').replace('"',"'")

    query = query + data_str + ';'

    cur = conn.cursor()

    cur.execute(query)

    conn.commit()

    if cur:
        cur.close()


if __name__ == "__main__":

    logging.basicConfig(filename='log_load_cargas.log',level=logging.DEBUG)

    """Setting up database connection"""
    conn = psc.connect(user='team75',
                    password='*VamosPorLaFoto*',
                    host='amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',
                    port=5432,
                    database='postgres')

    """Get Table vehicles"""
    df_Vehiculos = pd.read_sql("""SELECT *
                            FROM VEHICULOS""",
                            conn)

    """Get Arco data"""
    df_Arcos = pd.read_sql('SELECT * FROM ARCOS', conn)
    df_Arcos = df_Arcos.groupby(["arco"],
                            as_index=False).median().drop('id_registro',
                                                            axis=1)

    """datetime object containing current date and time"""

    lastUpdate_Time = datetime.strptime('2020-04-25', '%Y-%m-%d').date() # START DATE 2019-11-02
    stop_date = datetime.strptime('2020-05-12', '%Y-%m-%d').date() # STOP DATE 2020-05-11
    # stop_date =  datetime.now().date()

    while stop_date != lastUpdate_Time:

        log_msg = 'Start: ' +str(lastUpdate_Time)
        logging.info(log_msg)
        day_after = lastUpdate_Time + timedelta(days=1)
        """Get Table measurements"""
        df_Medicion = pd.read_sql("""SELECT *
                                FROM GENERAL WHERE FECHA_REGISTRO
                                BETWEEN '{}' AND '{}' """.format(lastUpdate_Time, day_after),
                                conn)


        #logging.info('Removing no finished path')
        #"""Remove no finished paths"""
        #index_no_finalizados = df_Medicion[df_Medicion["recorrido_finalizado"] == 'N'].index
        #df_Medicion.drop(index=index_no_finalizados, axis=0, inplace=True)

        if len(df_Medicion) != 0:
            logging.info('limit passenger loads greater than bus capacity to bus capacity')
            """limit passenger loads greater than bus capacity to bus capacity"""
            df_Medicion = df_Medicion.merge(df_Vehiculos, left_on = 'id_vehiculo', right_on="idvehiculo", how='left')
            limit_cap(df_Medicion)

            logging.info('Remove no with 5 or less measurements')
            """Remove no with 5 or less measurements"""
            delta_secrec(df_Medicion, minval=5)

            logging.info('assign links to the measurements')
            """assign links to the measurements"""
            df_Medicion = assign_link(df_Medicion, df_Arcos)

            logging.info('Calculating transit load')
            """Calculating transit load"""
            df_Medicion = carga(df_Medicion)

            """load data to the table"""
            logging.info('Cargando...')
            load_data(df_Medicion)

            log_msg = 'Cargada:' + str(lastUpdate_Time)
            logging.info(log_msg)

            lastUpdate_Time = day_after

            logging.info('--------------------------')
