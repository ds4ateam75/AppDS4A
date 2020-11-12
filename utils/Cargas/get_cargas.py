from scipy import spatial
import pandas as pd
import psycopg2 as psc
from datetime import datetime, timedelta


def delta_secrec(data, minval=5):

    """
    **** (1) AQUI JULIAN: TRADUCIR AL INGLES
    # Esta funcion sirve para eliminar los viajes que
    # tienen menos de 5 registros para evitar un uso de
    # memoria mayor, todas las limpiezas deberian hacer
    # sobre el mismo objeto usando el drop.

    Parameters:

    -data: AQUI JULIAN: DESCRIBIR VARIABLES
    -minval: AQUI JULIAN: DESCRIBIR VARIABLES

    """

    aggreg = {'id_vehiculo': "count"}
    filt_reg = data.copy().groupby("secuencia_recorrido").agg(aggreg)
    filt_reg.rename(columns={'id_vehiculo': "n"}, inplace=True)
    filt_reg.reset_index(inplace=True)

    rec_fil = list(filt_reg[filt_reg["n"] < minval]["secuencia_recorrido"].unique())
    index_to_drop = data[data["secuencia_recorrido"].isin(rec_fil)].index
    data.drop(index=index_to_drop, axis=0, inplace=True)


def limit_cap(df,var_list=['subendelantera','subentrasera', 'bajandelantera', 'bajantrasera'],maxVal=["CAPPASAJEROS"]):
    """
    **** (2) AQUI JULIAN: DESCRIPCION DE FUNCIONE EN INGLES

    Parameters:

    -df: AQUI JULIAN: DESCRIBIR VARIABLES
    -var_list: AQUI JULIAN: DESCRIBIR VARIABLES
    -maxVal: AQUI JULIAN: DESCRIBIR VARIABLES
    """

    for var in var_list:
        df[var].where(df[var]<df[maxVal], df[maxVal], inplace=True)
    return


def assign_link(df_Medicion, df_Arcos):

    """
    **** (3) AQUI JULIAN: DESCRIPCION DE FUNCIONE EN INGLES

    Parameters:

    -df_Medicion: AQUI JULIAN: DESCRIBIR VARIABLES
    -df_Arcos: AQUI JULIAN: DESCRIBIR VARIABLES

    (SI TIENES DUDAS PREGUNTALE A JOSE EL HIZO LA FUNCION)
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
    **** (4) AQUI JULIAN: DESCRIPCION DE FUNCIONE EN INGLES

    Parameters:

    -df: AQUI JULIAN: DESCRIBIR VARIABLES
    """

    """difference between passengers who get on and off"""
    df.sort_values(by=["secuencia_recorrido","fecha_registro"],inplace=True,ascending=True)
    df['delta_q'] = df['subendelantera']+df['subentrasera']-df['bajandelantera']-df['bajantrasera']


    """Group by Arco date and hour"""
    df['fecha'] = df['fecha_registro'].apply(lambda x: x.date())
    df["carga"] = df.groupby(by=['secuencia_recorrido', 'fecha'])['delta_q'].cumsum()
    df.reset_index(inplace=True)

    """Set to zero negative values"""
    df.loc[df['carga'] < 0, 'carga'] = 0

    df = df.groupby(by=['arco', pd.Grouper(key='fecha_registro', freq='H')]).sum()
    df.reset_index(inplace=True)

    """Set some columns like fecha, hora and dia"""
    df['fecha'] = df['fecha_registro'].apply(lambda x: x.date())
    df['hora'] = df['fecha_registro'].dt.hour
    df['dia'] = df['fecha_registro'].apply(lambda x: x.strftime("%A"))
    df.to_csv('data_.csv')

    """Drop unnecessary columns"""
    df.drop(columns=['id_general', 'index', 'delta_q', 'secuencia_recorrido', 'id_ruta',
                     'id_vehiculo', 'latitud', 'longitud', 'latitud_corr',
                     'longitud_corr', 'subendelantera', 'subentrasera',
                     'bajandelantera', 'bajantrasera', 'fecha_registro'],
            inplace=True)

    """Set to zero negatives loads"""
    return df


if __name__ == "__main__":

    """Stting up database connection"""
    conn = psc.connect(user='team75',
                    password='*VamosPorLaFoto*',
                    host='amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',
                    port=5432,
                    database='postgres')

    """datetime object containing current date and time"""
    now_Time = datetime.now()

    ### ESTO NO JULIAN
    ### ADD: FROM CONSULTA GET MOST RECENT TIMESTAP
    ### lastUpdate_Time
    lastUpdate_Time = now_Time - timedelta(days=365)

    """Get Table measurements"""
    df_Medicion = pd.read_sql("""SELECT *
                             FROM GENERAL WHERE FECHA_REGISTRO
                             BETWEEN '{}' AND '{}'
                             LIMIT 30000""".format(lastUpdate_Time, now_Time),
                             conn)

    """Get Table vehicles"""
    df_Vehiculos = pd.read_sql("""SELECT *
                               FROM VEHICULOS""",
                               conn)

    df_Vehiculos.to_csv("vehiculos.csv")
    """Get Arco data"""
    df_Arcos = pd.read_sql('SELECT * FROM ARCOS', conn)
    df_Arcos = df_Arcos.groupby(["arco"],
                            as_index=False).median().drop('id_registro',
                                                            axis=1)

    """Remove no finished paths"""
    index_no_finalizados = df_Medicion[df_Medicion["recorrido_finalizado"] == 'N'].index
    df_Medicion.drop(index=index_no_finalizados, axis=0, inplace=True)

    """Set to Zero measurements greater of bus passengers capacity"""
    ### AQUI JULIAN USAR FUNCION limit_cap
    # FUNCION VIEJA: limit_cap(df,var_list=['subendelantera','subentrasera', 'bajandelantera', 'bajantrasera'],maxVal=["CAPPASAJEROS"])

    """Remove no finished paths"""
    delta_secrec(df_Medicion, minval=5)

    """assign links to the measurements"""
    df_Medicion = assign_link(df_Medicion, df_Arcos)

    """clean and organize data"""
    df_Medicion = carga(df_Medicion)
    df_Medicion.to_csv("tabla_consulta.csv")
