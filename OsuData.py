from ossapi import *
import datetime
import sys
import random
import sqlite3
client_id = 30992
client_secret = "Qy1ezYjsN0VdPHla2uPuCwwEQ79E58m5RNplrSqj"
api = Ossapi(client_id, client_secret)

def GetUserInfo(id,Key=UserLookupKey.ID):
        try:
            user = None
            if(Key==UserLookupKey.ID):
                user = executeQuery("SELECT * FROM users WHERE id = @id",{"id" : id})
                
            elif(Key==UserLookupKey.USERNAME):
                 user = executeQuery("SELECT * FROM users WHERE username = @id",{"id" : id})
            #If user Not Empty
            try:
                l=user[0][3]
                return user[0]
            except:
                user = api.user(id, key=Key)
            if(user.is_bot==True):
                  #print("Bot")
                  return None
            
            if(user.statistics.play_time<6000 and False):
                  #print("low time")
                  return None
            
            if(not user.is_active and False):
                 #print("not active")
                 return None
            if(user.statistics.global_rank>1000000):
                 #print("low rank ",user.statistics.rank)
                 return None
            info=[str(user.id),user.username,
                  str(user.country.name),
                  str(user.statistics.global_rank),
                  str(user.statistics.country_rank),
                  str(user.statistics.hit_accuracy),
                  str(user.statistics.play_count),
                  str(user.statistics.play_time),
                  str(user.statistics.pp),
                  str(user.playstyle),
                  str(user.is_active)]
            print("Added")
            print(info)
            return info
        except Exception as error:
               #print(str(id)+" "+str(error))
               return None
def executeQuery(query,vars=None):
    connection = sqlite3.connect('OsuData.db')
    cursor = connection.cursor()
    try:
        if(vars is None):
            cursor.execute(query)
        else:
            cursor.execute(query,vars)
        list = []
        for i in cursor.fetchall():
             list.append(i)
        connection.commit()
        return list
        
    except Exception as error:
         pass
        #print("Ошибка при работе с СУБД ", error)
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
                                pp REAL,
                                playstyle INTEGER,
                                isactive BOOLEAN); '''
    executeQuery(create_table_query)
def WriteUserToDB(user):
    if(user is None):
         return
    try:
         l = int(user[9])
    except:
          user[9]=0
    try:
         l = int(user[3])
    except:
         print(user[1]," No pp")
         return
    query = "INSERT INTO users (id, username, country, rank, country_rank, accuracy, playcount, playtime,pp, playstyle, isactive) \
        VALUES (@id, @username, @country, @rank, @country_rank, @accuracy, @playcount, @playtime, @pp, @playstyle, @isactive);"
    executeQuery(query,{
                 "id":int(user[0]),
                 "username":user[1],
                 "country":user[2],
                 "rank":int(user[3]),
                 "country_rank":int(user[4]),
                 "accuracy":float(user[5]),
                 "playcount":int(user[6]),
                 "playtime":int(user[7]),
                 "pp":float(user[8]),
                 "playstyle":int(user[9]),
                 "isactive":bool(user[10])}
                 )

GeneralSovSize=40000000
mask = [0]*GeneralSovSize
j=10
while(j!=0):
    ran = random.randint(0,len(mask)-1)
    if(mask[ran]==0):
          WriteUserToDB(GetUserInfo(ran)) #Добавить user с рандомным id в базу
          mask[ran]=1
          #print(ran)
    else:
         print("was") 
    