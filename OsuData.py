from ossapi import *
import datetime
import sys
import sqlite3
client_id = 30992
client_secret = "Qy1ezYjsN0VdPHla2uPuCwwEQ79E58m5RNplrSqj"
api = Ossapi(client_id, client_secret)
def GetUserInfo(id,Key=UserLookupKey.ID):
        try:
            user = api.user(id, key=Key)
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
GeneralSovSize=40000000
step = round(GeneralSovSize/100)


def executeQuery(query,vars=None):
    connection = sqlite3.connect('OsuData.db')
    cursor = connection.cursor()
    try:
        if(vars is None):
            cursor.execute(query)
        else:
             cursor.execute(query,vars)
        connection.commit()
    except Exception as error:
        print("Ошибка при работе с СУБД", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
def CreateTable():
    drop_table = "DROP TABLE users"
    executeQuery(drop_table)
    create_table_query = '''  CREATE TABLE users
                                (id INTEGER PRIMARY KEY NOT NULL,
                                username TEXT NOT NULL,
                                country TEXT,
                                rank INTEGER,
                                country_rank INTEGER,
                                accuracy REAL,
                                playcount INTEGER,
                                playtime INTEGER,
                                playstyle INTEGER,
                                isactive BOOLEAN); '''
    executeQuery(create_table_query)
    print("Таблица успешно создана в PostgreSQL")
def WriteUserToDB(user):
    if(user is None):
         return
    query = "INSERT INTO users (id, username, country, rank, country_rank, accuracy, playcount, playtime, playstyle, isactive) \
        VALUES (@id, @username, @country, @rank, @country_rank, @accuracy, @playcount, @playtime, @playstyle, @isactive);"
    executeQuery(query,{
                 "id":int(user[0]),
                 "username":user[1],
                 "country":user[2],
                 "rank":int(user[3]),
                 "country_rank":int(user[4]),
                 "accuracy":float(user[5]),
                 "playcount":int(user[6]),
                 "playtime":int(user[7]),
                 "playstyle":int(user[8]),
                 "isactive":bool(user[9])}
                 )
CreateTable()

squad = [
        GetUserInfo("GodRoPoNiKa",UserLookupKey.USERNAME),
        GetUserInfo("katalashka boy",UserLookupKey.USERNAME),
        GetUserInfo("D1scream",UserLookupKey.USERNAME),
        GetUserInfo("HandsomeMe",UserLookupKey.USERNAME),
        GetUserInfo("azaz08967565",UserLookupKey.USERNAME),
        GetUserInfo("Ben_Kir",UserLookupKey.USERNAME),
        GetUserInfo("skill_issue",UserLookupKey.USERNAME),
        GetUserInfo("Ahrome",UserLookupKey.USERNAME),
        GetUserInfo("Ravexi",UserLookupKey.USERNAME),
        GetUserInfo("mewea",UserLookupKey.USERNAME),
        GetUserInfo("Shootnik",UserLookupKey.USERNAME),
        GetUserInfo("YungVenuz",UserLookupKey.USERNAME),
        GetUserInfo("_kurayami",UserLookupKey.USERNAME),

         ]
for user in squad:
     WriteUserToDB(user)
    