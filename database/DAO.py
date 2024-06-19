from database.DB_connect import DBConnect
from model.squadra import Squadra


class DAO:
    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct YEAR 
from teams
where year >= 1980"""
            cursor.execute(query)
            for row in cursor:
                result.append(row['YEAR'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_teams(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
from teams
where year = %s"""
            cursor.execute(query, (year,))
            for row in cursor:
                result.append(Squadra(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_weights(year, idMap):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select sum(s.salary) as salario , t.ID 
from salaries s , appearances a , teams t 
where s.playerID = a.playerID and t.ID = a.teamID and t.`year` = a.`year` and a.`year` = s.`year` and t.`year` = %s
GROUP by t.ID 
order by t.ID  """
            cursor.execute(query, (year,))
            for row in cursor:
                result[idMap[row['ID']]] = row['salario']
            cursor.close()
            cnx.close()
        return result

