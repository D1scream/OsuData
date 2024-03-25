
import ossapi
from DbController import DbController
from ossapi import *
class OsuUser:
    SQLINSERTQUERY="INSERT INTO users (id, username, country, rank, country_rank, accuracy, playcount, playtime,pp, playstyle, isactive) \
        VALUES (@id, @username, @country, @rank, @country_rank, @accuracy, @playcount, @playtime, @pp, @playstyle, @isactive);"
    SQLCREATETABLE= '''         CREATE TABLE users
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
    client_id = 30992
    client_secret = "Qy1ezYjsN0VdPHla2uPuCwwEQ79E58m5RNplrSqj"
    def __init__(self, id:int):
        self.db=DbController('OsuData.db')
        self.api = Ossapi(self.client_id, self.client_secret)
        self.user = self.db.ExecuteQuery("SELECT * FROM users WHERE id = @id",{"id" : id})
        if(len(self.user)==1):
            self.user=self.user[0]
            self.id:int=self.user[0]
            self.username:str=self.user[1]
            self.country_name:str=self.user[2]
            self.global_rank:int=self.user[3]
            self.country_rank:int=self.user[4]
            self.hit_accuracy:float=self.user[5]
            self.play_count:int=self.user[6]
            self.play_time:int=self.user[7]
            self.pp:float=self.user[8]
            self.playstyle:int=self.user[9]
            self.is_active:bool=self.user[10]
        else:
            self.user:User = self.api.user(id, key=UserLookupKey.ID,mode=GameMode.OSU)
            self.id=self.user.id
            self.username=self.user.username
            self.country_name=self.user.country.name
            self.global_rank=self.user.statistics.global_rank
            self.country_rank=self.user.statistics.country_rank
            self.hit_accuracy=self.user.statistics.hit_accuracy
            self.play_count=self.user.statistics.play_count
            self.play_time=self.user.statistics.play_time
            self.pp=self.user.statistics.pp
            if(self.user.playstyle):
                self.playstyle=self.user.playstyle
            else:
                self.playstyle=0
            self.is_active=self.user.is_active
    
    def Save(self):
        self.db.ExecuteQuery(self.SQLINSERTQUERY,{
                "id":self.id,
                "username":self.username,
                "country":self.country_name,
                "rank":self.global_rank,
                "country_rank":self.country_rank,
                "accuracy":self.hit_accuracy,
                "playcount":self.play_count,
                "playtime":self.play_time,
                "pp":self.pp,
                "playstyle":self.playstyle,
                "isactive":self.is_active}
                )
    def Info(self):
        return ("id:{}, username:{}, country:{}, rank:{}, country_rank:{}, accuracy:{}, playcount:{}, playtime:{}, pp:{}, playstyle:{}, isactive:{}"
              .format(self.id,self.username,self.country_name,self.global_rank,self.country_rank,self.hit_accuracy,self.play_count,self.play_time,self.pp,self.playstyle,self.is_active))
    
            
                        
