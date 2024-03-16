from ossapi import *
import datetime
import psycopg2
client_id = 30992
client_secret = "Qy1ezYjsN0VdPHla2uPuCwwEQ79E58m5RNplrSqj"
api = Ossapi(client_id, client_secret)
today = datetime.datetime
def GetUserInfo(id):
        try:
            user = api.user(id, key=UserLookupKey.ID)
            if(user.is_bot==True):
                  return None
            if(user.statistics.play_time<6000):
                  return None
            info=[str(user.id),user.username,str(user.country.name),str(user.statistics.global_rank),str(user.statistics.country_rank),str(user.statistics.hit_accuracy)\
            ,str(user.statistics.play_count),str(user.statistics.play_time),str(user.playstyle),str(user.is_active)]
            return info
        except Exception as error:
               #print(str(id)+str(error)+" error")
               return None
def WriteUserToDB(user,id):
      pass
me = GetUserInfo(34699410)

GeneralSovSize=40000000
step = round(GeneralSovSize/100)
for i in range(0,GeneralSovSize,step):
        user = GetUserInfo(i)
        if user:
            print(GetUserInfo(i))
            WriteUserToFile(GetUserInfo(i))


try:
    connection = psycopg2.connect(user="postgres",
                                  password="9132",
                                  host="localhost",
                                  port="5432",
                                  database="OsuDB")
    cursor = connection.cursor()
    create_table_query = '''  CREATE TABLE users
                              (ID INT PRIMARY KEY     NOT NULL,
                              username           TEXT    NOT NULL,
                              playtime INT REAL); '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

