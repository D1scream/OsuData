
import sqlite3

class DbController:
    def __init__(self,dbName:str):
        self.dbName:str = dbName
        
    def ExecuteQuery(self, query,vars:list=None)->list:
        connection:sqlite3.Connection = sqlite3.connect(self.dbName)
        cursor:sqlite3.Connection = connection.cursor()
        try:
            if(vars is None):
                cursor.execute(query)
            else:
                cursor.execute(query,vars)
            glist:list = []
            for i in cursor.fetchall():
                glist.append(i)
            connection.commit()
            return glist
        except Exception as error:
            print("Ошибка при работе с СУБД ",query, error,vars)
            pass
        
        finally:
            if connection:
                cursor.close()
                connection.close()
    
