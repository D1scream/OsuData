from ossapi import *
import datetime
import sys
import sqlite3
client_id = 30992
client_secret = "Qy1ezYjsN0VdPHla2uPuCwwEQ79E58m5RNplrSqj"
api = Ossapi(client_id, client_secret)

def GetUserInfo(id,Key=UserLookupKey.ID):
        try:
            if(Key==UserLookupKey.ID):
                user = executeQuery("SELECT * FROM users WHERE id = @id",{"id" : id})
                try:
                     l=user[0][3]
                     
                     return user[0]
                except:
                    pass
            
            elif(Key==UserLookupKey.USERNAME):
                user = executeQuery("SELECT * FROM users WHERE username = @id",{"id" : id})
                try:
                     l=user[0][3]
                     return user[0]
                except:
                    pass
            else:
                 print("fuck")
                 return None
            
            user = api.user(id, key=Key)
            if(user.is_bot==True):
                  return None
            if(user.statistics.play_time<6000):
                  return None
            if(not user.is_active):
                 return None
            info=[str(user.id),user.username,str(user.country.name),str(user.statistics.global_rank),str(user.statistics.country_rank),str(user.statistics.hit_accuracy)\
            ,str(user.statistics.play_count),str(user.statistics.play_time),str(user.playstyle),str(user.is_active)]
            print("Added")
            print(info)
            return info
        except Exception as error:
               print(str(id)+str(error)+" error")
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

        list = []
        for i in cursor.fetchall():
             list.append(i)
        #print(list)
        connection.commit()
        return list
        
    except Exception as error:
         pass
        #print("Ошибка при работе с СУБД", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
EmptyAns=executeQuery("SELECT * FROM users WHERE id = 0")
def CreateTable():
    drop_table = "DROP TABLE users"
    #executeQuery(drop_table)
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
def WriteUserToDB(user):

    if(user is None):
         
         return
    try:
         l = int(user[8])
    except:
         user[8]=0
    try:
         l = int(user[3])
    except:
         print(user[1]," No pp")
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
nicks = [
        "GodRoPoNiKa",
        "katalashka boy",
        "HandsomeMe",
        "azaz08967565",
        "Ben_Kir",
        "skill_issue",
        "Ahrome",
        "Ravexi",
        "mewea",
        "Shootnik",
        "YungVenuz",
        "_kurayami",
        "katalashka",
        "Lyeli",
        "VLADYUSHYA",
        "Haena-",
        "Mihlo",
        "KeS_Play",
        "AntoN",
        "BeHot",
        "pr0xladno",
        "Yukarle",
        "silversnax",
        "Ice Shark",
        "6adf0X",
        "Cangrani",
        "FlyingShark",
        "boganetdoma",
        "navkid",
        "ti2mu2r1",
        "kokoya",
        "eruhar",
        "C_helove_k",
        "Creppy_",
        "-RedSky-",
        "shimaii",
        "KrestanSXXX",
        "exp1rian",
        "sanacura",
        "ZonnYT",
        "FedRONI",
        "Nqo_love",
        "NeKiTnIkE",
        "TATAPCTAH",
        "owoPeef",
        "MaksatR",
        "k0_0dama",
        "tortik122421",
        "Naabway",
        "Shui",
        "_Kaibi_",
        "Ruslanmasterpro",
        "Y0kuH",
        "Reguxo",
        "gerDen",
        "N3K4",
        "M13er",
        "D1scream",
        "BaconCat",
        "RamkaSMEN",
        "KROKSMAN"

]

for nick in nicks:
     WriteUserToDB( GetUserInfo(nick,UserLookupKey.USERNAME))
    