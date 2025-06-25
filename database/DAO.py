from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYear():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                        SELECT DISTINCT s.`year`
                        FROM seasons s 
                        ORDER BY s.`year` """
            cursor.execute(query)
            result = []
            for row in cursor.fetchall():
                result.append(row['year'])
            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getAllDriversByYear(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                        SELECT DISTINCT d.driverId, d.driverRef, d.number, d.code, 
                                        d.forename, d.surname, d.dob, d.nationality, d.url
                        FROM drivers d, races r, results res
                        WHERE r.year = %s
                            AND res.driverId = d.driverId
                            AND res.raceId = r.raceId
                            AND res.position IS NOT NULL"""
            cursor.execute(query, (year, ))
            result = []
            for row in cursor.fetchall():
                result.append(Driver(**row))
            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def getAllResultsByYear(year, idMap): # da qui ottengo delle tuple (posizione, id_gara, id_pilota)
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                        select r1.driverId as d1, r2.driverId as d2, count(*) as cnt
				        from results as r1, results as r2, races
				        where r1.raceId = r2.raceId
                            and races.raceId = r1.raceId
                            and races.year = %s
                            and r1.position is not null
                            and r2.position is not null 
                            and r1.position < r2.position 
				        group by d1, d2"""

            cursor.execute(query, (year, ))
            result = []
            for row in cursor.fetchall():
                result.append((row['d1'], row['d2'], row['cnt']))
            return result
        finally:
            cursor.close()
            conn.close()