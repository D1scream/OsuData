from decimal import Decimal
from ossapi import *
import random
import sqlite3
from datetime import datetime
from DbController import DbController
from OsuUser import OsuUser

class OsuData:
    api = Ossapi(OsuUser.client_id, OsuUser.client_secret)
    def __init__(self):        
        self.db=DbController('OsuData.db')

    def GetCountDB(self):
        return self.db.ExecuteQuery("SELECT COUNT(*) FROM users")[0][0]

    def ReCreateTable(self):
        self.db.ExecuteQuery("DROP TABLE users")
        self.db.ExecuteQuery(OsuUser.SQLCREATETABLE)
    
    def CheckUser(self,user:OsuUser)->bool:
        if(user.global_rank and user.global_rank>1000000):
            return False
        if(user.is_active==False):
            return False
        if(user.play_time<6000):
            return False
        return True

    def GetListUsers(self,userIds:list[int])->list[OsuUser]:
        users:list[OsuUser]=[]
        for userCompact in self.api.users(userIds):
            try:
                user = OsuUser(userCompact.id)#LazyLoad OsuUser
                #print(user.Info(), "Huinfo")
                
                users.append(user) 
            except Exception as e:
                print(e)
        return users
            

    def Start(self):
        #self.ReCreateTable()

        #print("\n")
        random.seed(datetime.now().timestamp())
        maxId=40000000
        mask:list[int]=[0]*maxId

        while(True):
                ran = random.randint(0,maxId-1)
                if(mask[ran]==0):
                    mask[ran] = -1
                    try:
                        user = OsuUser(ran)
                        
                        if(self.CheckUser(user)):
                            user.Save()
                            print(user.Info())
                            mask[ran] = 1
                        else:
                            # print("ifs")
                            pass

                    except Exception as e:
                        #print("MainErr ",e)
                        pass
            
osudata = OsuData()
osudata.Start()