from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(start, end):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.constructorId, c.constructorRef, c.name ,c.nationality
                    from constructors c, results r, races r2 
                    where r.position is not null and r2.`year` >=%s and r2.`year` <=%s
                    and c.constructorId =r.constructorId and r2.raceId =r.raceId """

        cursor.execute(query,(start,end))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(start, end):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.constructorid as id1, t2.constructorid as id2, count(distinct t1.driverid) as peso
                    from (select r2.constructorId , r2.driverId 
                    from races r,results r2 
                    where r.raceId =r2.raceId and r.`year`>=%s and r.`year` <=%s and r2.position is not null) t1,
                    (select  r2.constructorId , r2.driverId 
                    from races r,results r2 
                    where r.raceId =r2.raceId and r.`year`>=%s and r.`year` <=%s and r2.position is not null) t2
                    where t1.driverid =t2.driverid and t1.constructorid <t2.constructorid 
                    group by id1 ,id2"""

        cursor.execute(query, (start, end, start, end))

        for row in cursor:
            results.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOld(start, end):
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """select r.constructorId, min(d.dob ) as oldest
                    from results r, drivers d, races r2 
                    where r2.`year`>=%s and r2.`year` <=%s
                    and r.driverId =d.driverId and r2.raceId=r.raceId 
                    group by r.constructorId"""

        cursor.execute(query, (start, end))

        for row in cursor:
            results[row["constructorId"]] = row["oldest"]

        cursor.close()
        conn.close()
        return results