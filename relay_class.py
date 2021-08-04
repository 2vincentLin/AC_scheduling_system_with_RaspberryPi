from datetime import datetime as dt
from datetime import date
from datetime import time
from datetime import timedelta
import time as t
import RPi.GPIO as gp
import pickle
import random


class helper:
    @staticmethod
    def load(n):
        try:
            with open('ac_static/{}setting.pkl'.format(n), 'rb') as f:
                obj = pickle.load(f)
            return obj
        except Exception as e:
            print("unable to load setting.pkl")
            raise e
    @staticmethod
    def save(obj,n):
        try:
            with open('ac_static/{}setting.pkl'.format(n), 'wb') as f:
                pickle.dump(obj, f)
        except Exception as e:
            print("unable to save setting.pkl")
            raise e


class relay:
    def __init__(self, channel, pin):
        self.ch = channel # 1st one is 1
        self.pin = pin
        
        # [[dt,dt],[dt,dt]...]
        self.OnOffTime = list()
        
        self.status = None # True is on
        self.alwaysOnOff = None # if it's true, this relay always On
        
        # [[dt,dt],[dt,dt]...]
        self.scheduleOnDTs = list()
        self.scheduleOffDTs = list()
        
        # 5 is Saturday, 6 is Sunday
        self.OffWeekdays = [5,6]
        
        # set pin to OUT, this will activate relay immediately
        # if end the program without calling gp.cleanup(), it won't change current status
        gp.setup(self.pin, gp.OUT)
        #gp.output(self.pin, gp.HIGH)
        
        
    def setAlwaysOn(self, On):
        if On:
            self.alwaysOnOff = True
        elif On == False:
            self.alwaysOnOff = False
        else:
            self.alwaysOnOff = None
            
    def setOnOffTime(self, OnOffTime):
        # OnOffTime is [[time, time],[time,time],...]
        ori_OnOffTime = self.OnOffTime
        try:
            for On, Off in OnOffTime:
                if type(On) != type(dt.today().time()) and type(Off) != type(dt.today().time()):
                    raise Exception("unable to setOnOffTime, please input datetime.time object")
            self.OnOffTime = OnOffTime
        except Exception as e:
            self.OnOffTime = ori_OnOffTime
            raise e
    
    def getOnOffTime(self):
        #return [self.OnTime.strftime("%H%M"), self.OffTime.strftime("%H%M")]
        return self.OnOffTime
    
    def setOffWeekdays(self, OffWeekdays):
        self.OffWeekdays = OffWeekdays
        
    def relayOn(self, log=False):
        # check the actual pin status, 0 here is ON
        #if gp.input(self.pin) == 0 and self.status == True:
        if gp.input(self.pin) == 0:
            return
        gp.output(self.pin, gp.LOW)
        if log:
            print("relay{} is On at {}".format(self.ch, dt.today()))
        self.status = True
        
    def relayOff(self, log=False):
        # check the actual pin status, 1 is here OFF
        #if gp.input(self.pin) == 1 and self.status == False:
        if gp.input(self.pin) == 1:
            return
        gp.output(self.pin, gp.HIGH)
        if log:
            print("relay{} is Off at {}".format(self.ch, dt.today()))
        self.status = False
                
    def addScheduleOnDT(self, OnOffDTs):
        # OnOffDTs is [[dt, dt],[dt,dt]...]
        for OnOffDT in OnOffDTs:
            self.scheduleOnDTs.append(OnOffDT)
        # you need it sorted in case user add the date randomly
        self.scheduleOnDTs = sorted(self.scheduleOnDTs)
            
    def removeScheduleOnDT(self, index):
        if index >= len(self.scheduleOnDTs):
            return
        self.scheduleOnDTs.pop(index)

    def removeScheduleOnDTbyDT(self, OnOffDT):
        # OnOffDT = [[dt,dt]]
        index = 0
        for On, Off in self.scheduleOnDTs:
            if On==OnOffDT[0] and Off==OnOffDT[1]:
                self.removeScheduleOnDT(index)
                return
            index+=1
          
    def addScheduleOffDT(self, OffOnDTs):
        # OnOffDTs is [[dt, dt],[dt,dt]...]
        for OffOnDT in OffOnDTs:
            self.scheduleOffDTs.append(OffOnDT)
        # you need it sorted in case user add the date randomly
        self.scheduleOffDTs = sorted(self.scheduleOffDTs)
            
    def removeScheduleOffDT(self, index):
        if index >= len(self.scheduleOffDTs):
            return
        self.scheduleOffDTs.pop(index)

    def removeScheduleOffDTbyDT(self, OffOnDT):
        # OffOnDT = [[dt,dt]]
        index = 0
        for Off, On in self.scheduleOffDTs:
            if Off==OffOnDT[0] and On==OffOnDT[1]:
                self.removeScheduleOffDT(index)
                return
            index+=1

    def schedule(self,log=False):
        # 1. check alwayOnOff
        # 2. check scheduleOn 
        # 3. check normal schedule (weekend, holiday and On Off time)
        if self.alwaysOnOff == True:
            self.relayOn(log)
            return
        elif self.alwaysOnOff == False:
            self.relayOff(log)
            return
        
        # scheduleOn event
        now = dt.today()
        if len(self.scheduleOnDTs) > 0:
            # make sure 1st item is the earlist
            OnDT, OffDT = self.scheduleOnDTs[0]
            if OnDT <= now and OffDT >= now:
                self.relayOn(log)
                return
            if OffDT < now:
                self.scheduleOnDTs.pop(0)
                
        if len(self.scheduleOffDTs) > 0:
            # make sure 1st item is the earlist
            OffDT, OnDT = self.scheduleOffDTs[0]
            if OffDT <= now and OnDT >= now:
                self.relayOff(log)
                return
            if OnDT < now:
                self.scheduleOffDTs.pop(0)
        
        # normal schedule
        if now.weekday() in self.OffWeekdays:
            # OffWeekdays or holiday, don't turn on this relay
            self.relayOff(log)
        else:
            time_now = now.time()
            On_already = False
            
            # run through all OnOffTime and check does it need to be On
            for OnTime, OffTime in self.OnOffTime:
                if OnTime <= time_now and OffTime >= time_now:
                    #print("relay{} is On".format(self.relay))
                    self.relayOn(log)
                    On_already = True
                    
            # if no need to be On, then Off
            if On_already == False:
                #print("relay{} is Off".format(self.relay))
                self.relayOff(log)
            

        
class relayBoard:
    def __init__(self, n, relayList, pinList):
        self.n = n
        if (n == len(relayList) and n == len(pinList)):
            self.relayList = relayList
            self.pinList = pinList
            self.scheduleOnDTs = list() # store scheduleOnDT for all relays for deletion purpose if needed
            self.scheduleOffDTs = list() # store scheduleOffDT for all relays for deletion purpose if needed
            
            self.relays = list()
            for i in range(n):
                self.relays.append(relay(relayList[i],pinList[i]))
        else:
            raise ValueError("number of argument are different")
    
                
    def setOnOffTime(self, OnOffTime):
        for ch in self.relays:
            ch.setOnOffTime(OnOffTime)   
            
    def getOnOffTime(self):
        result = dict()
        for i in range(self.n):
            result[i] = self.relays[i].getOnOffTime()
        return result
    
    def setOffWeekdaysAll(self, OffWeekdays):
        for ch in self.relays:
            ch.setOffWeekdays(OffWeekdays)
    
    def addScheduleOnDT(self, OnOffDTs):
        # OnOffDTs is [[dt, dt],[dt,dt]...]
        self.scheduleOnDTs = OnOffDTs
        for ch in self.relays:
            ch.addScheduleOnDT(OnOffDTs)
            
    def removecheduleOnDTAll(self, OnOffDTs):
        # OnOffDTs is [[dt, dt],[dt,dt]...]
        for On, Off in OnOffDTs:
            for ch in self.relays:
                ch.removeScheduleOnDTbyDT([On,Off])
            try:
                self.scheduleOnDTs.remove([On,Off])
            except Exception as e:
                raise e
                    
            
    def addScheduleOffDT(self, OffOnDTs):
        # OffOnDTs is [[dt, dt],[dt,dt]...]
        self.scheduleOffDTs = OffOnDTs
        for ch in self.relays:
            ch.addScheduleOffDT(OffOnDTs)   

    def removecheduleOffDTAll(self, OffOnDTs):
        # OnOffDTs is [[dt, dt],[dt,dt]...]
                        
        for Off, On in OffOnDTs:
            for ch in self.relays:
                ch.removeScheduleOffDTbyDT([Off,On])
            try:
                self.scheduleOffDTs.remove([Off,On])
            except Exception as e:
                raise e


    def relayAllOn(self):
        for ch in self.relays:
            ch.relayOn()
            
    def relayAllOff(self):
        for ch in self.relays:
            ch.relayOff()
            
    def schedule(self, log=False):
        for i in range(self.n):
            self.relays[i].schedule(log)
    
    def print_all_relay(self):
        for i in range(self.n):
            print("relay{}'s pin is {}".format(self.relays[i].ch,self.relays[i].pin))
    
 
if __name__ == "__main__":
    
    gp.cleanup()
    gp.setmode(gp.BCM)
    
    #relayList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    #pinList = [10,9,11,5,6,13,19,26,21,20,16,12,7,8,25,24]
    
    relayList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    pinList = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,21,20,16,12,7,8,25,24,23,18,15]
    
    for pin in pinList:
        gp.setup(pin, gp.OUT)
    
    for pin in pinList:
        gp.output(pin, gp.LOW)
        
    print('all on')
    t.sleep(1)
    
    random.shuffle(pinList)
    print(pinList)
    
    for pin in pinList:
        t.sleep(0.3)
        gp.output(pin, gp.HIGH)
    
#     for pin in [2,3,4,17,27,22,10,9,11,5,13,19]:
#         t.sleep(0.1)
#         gp.output(pin, gp.HIGH)
    print('all off')