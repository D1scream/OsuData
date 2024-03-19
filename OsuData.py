from ossapi import *
import random
import sqlite3
from datetime import datetime
class OsuData:
    def __init__(self, client_id,client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api = Ossapi(client_id, client_secret)

    def executeQuery(self, query,vars=None):
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
            #print("Ошибка при работе с СУБД ", error,vars)
            pass
        
        finally:
            if connection:
                cursor.close()
                connection.close()

    def GetUserInfo(self,id):
            try:
                user = self.executeQuery("SELECT * FROM users WHERE id = @id",{"id" : id})
                #If user Not Empty
                try:
                    
                    l=user[0][3]
                    return user[0]
                except:
                    try:
                        user = self.api.user(id, key=UserLookupKey.ID)
                    except:
                        return None
                
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

    def WriteUserToDB(self,user):
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
        try:
            self.executeQuery(query,{
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
        except Exception as error:
            print(error)

    def ReCreateTable(self):
        drop_table = "DROP TABLE users"
        self.executeQuery(drop_table)
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
        self.executeQuery(create_table_query)

    def Start(self):
        random.seed(datetime.now().timestamp()+1)
        GeneralSovSize=40000000
        mask = [0]*GeneralSovSize
        j=10
        print("start")
        while(j!=0):
                ran = random.randint(0,GeneralSovSize-1)
                mask[ran]
                user = self.GetUserInfo(ran)
                if(not user is None):
                    #print(user)
                    self.WriteUserToDB(user) #Добавить user с рандомным id в базу
                mask[ran] = 1
        print("end")

client_id = 30992
client_secret = "Qy1ezYjsN0VdPHla2uPuCwwEQ79E58m5RNplrSqj"
osudata = OsuData(client_id,client_secret)
osudata.Start()