import pandas as pd
import psycopg2 as psc


class Sql:

    def __init__(self):
        self.conn = psc.connect(user='team75',
                    password='*VamosPorLaFoto*',
                    host='amvappdb.cqxpk4qplvq9.us-east-2.rds.amazonaws.com',
                    port=5432,
                    database='postgres')

    def request(self, query):
        return pd.read_sql(query, self.conn)


class Carga_query:

    def __init__(self, update_map=True, agr='SUM'):
        self.agr = agr
        self.update_map = update_map
        if self.update_map is True:
            self.query = "SELECT ARCO, {}(CARGA) AS CARGA FROM CONSULTA ".format(self.agr)
        else:
            self.query = "SELECT HORA, {}(CARGA) AS CARGA FROM CONSULTA ".format(self.agr)
        self.number_filters = 0

    def add_date_range(self, start_date, end_date):
        if self.number_filters == 0:
            self.query += 'WHERE '
            self.query += 'FECHA BETWEEN \'{}\' AND \'{}\' '.format(start_date, end_date)
        else:
            self.query += 'AND '
            self.query += 'FECHA BETWEEN \'{}\' AND \'{}\' '.format(start_date, end_date)
        self.number_filters += 1

    def add_hour_filter(self, hour=None):
        if self.number_filters == 0 and (hour is not None and hour != []):
            self.query += 'WHERE '
            self.query += 'HORA IN {} '.format(str(hour).replace("[", "(").replace("]", ")"))
        elif hour is not None and hour != []:
            self.query += 'AND '
            self.query += 'HORA IN {} '.format(str(hour).replace("[", "(").replace("]", ")"))
        self.number_filters += 1

    def add_day_filter(self, dia=None):
        if self.number_filters == 0 and (dia is not None and dia != []):
            self.query += 'WHERE '
            self.query += 'DIA IN {} '.format(str(dia).replace("[", "('").replace("]", "')"))
        elif dia is not None and dia != []:
            self.query += 'AND '
            self.query += 'DIA IN {} '.format(str(dia).replace("[", "('").replace("]", "')"))
        self.number_filters += 1

    def restart_query(self, update_map=True, agr='SUM'):
        self.agr = agr
        self.update_map = update_map
        if self.update_map is True:
            self.query = "SELECT ARCO, {}(CARGA) AS CARGA FROM CONSULTA ".format(self.agr)
        else:
            self.query = "SELECT HORA, {}(CARGA) AS CARGA FROM CONSULTA ".format(self.agr)
        self.number_filters = 0

    def last_add(self):
        if self.update_map is True:
            self.query += "GROUP BY ARCO;"
        else:
            self.query += "GROUP BY HORA;"


class Arco_query:

    def get_arco_query(self):
        query = '''SELECT * FROM ARCOS'''
        return query
