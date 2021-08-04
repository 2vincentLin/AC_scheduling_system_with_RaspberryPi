import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from relay_class import *
from datetime import datetime as dt
from datetime import time
from PIL import Image, ImageTk
from tkcalendar import DateEntry

class Frame2(tk.Frame):

    def __init__(self, window, board):
        super().__init__(master= window, borderwidth=15)

        self.ch = 1
        self.board = board # from relay_class
        self.relay = board.relays[0] # from relay_class
        
        self.hour_list = [i for i in range(0,24)] + [""]
        self.minute_list = [i for i in range(0,60,1)] + [""]
        
        # status frame
        self.status_text = "On" if self.relay.status else "Off"
        self.status_frame = tk.LabelFrame(master=self, relief=tk.GROOVE, borderwidth=2, text="Status")
        self.status_frame.pack(side=tk.TOP, fill= tk.BOTH)
        self.lbl_status = tk.Label(master=self.status_frame, text=f"Relay {self.ch} is {self.status_text}")
        self.lbl_status.pack()

        # frame to pack alwaysOnOff event
        self.always_frame = tk.LabelFrame(master=self, relief=tk.GROOVE, borderwidth=2, text="Always On/Off")
        self.always_frame.pack(side=tk.TOP, fill= tk.BOTH)

        # for this setting, I need 3 values, true, false and None, so I can't use BooleanVar to return
        self.statusVar = tk.StringVar(value=self.status_text)
        self.r1 = tk.Radiobutton(self.always_frame, text="Always On", variable=self.statusVar, value="On", command= self.allwaysOnOff)
        self.r2 = tk.Radiobutton(self.always_frame, text="Always Off", variable=self.statusVar, value="Off", command= self.allwaysOnOff)
        self.r3 = tk.Radiobutton(self.always_frame, text="Schedule", variable=self.statusVar, value="Schedule", command= self.allwaysOnOff)
        self.r1.pack()
        self.r2.pack()
        self.r3.pack()

        # frame to pack schedule on event
        self.schedule_on_frame = tk.LabelFrame(master=self, relief=tk.GROOVE, borderwidth=2, text="Schedule On")
        self.schedule_on_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.lbl_scheduleOn = tk.Label(master=self.schedule_on_frame, text=f"{len(self.relay.scheduleOnDTs)} schedule events")
        self.lbl_scheduleOn.grid(column=0, row=0, columnspan=6, padx=10, pady=5)

        self.lbl_scheduleOnStart = tk.Label(master=self.schedule_on_frame, text=f"Start")
        self.lbl_scheduleOnStart.grid(column=0, row=1, columnspan=3, padx=10, pady=5)

        self.lbl_scheduleOnEnd = tk.Label(master=self.schedule_on_frame, text=f"End")
        self.lbl_scheduleOnEnd.grid(column=3, row=1, columnspan=3, padx=10, pady=5)
        
        
        self.hourOnVar = tk.IntVar(master=self.schedule_on_frame)
        self.minuteOnVar = tk.IntVar(master=self.schedule_on_frame)
        self.hourOffVar = tk.IntVar(master=self.schedule_on_frame)
        self.minuteOffVar = tk.IntVar(master=self.schedule_on_frame)
        
        self.ent_scheduleOnStartDate = DateEntry(master=self.schedule_on_frame, selectmode="day")
        self.ent_scheduleOnStartDate.grid(column=0, row=2, columnspan=1, padx = 2)
        self.cb_scheduleOnStartHour = ttk.Combobox(self.schedule_on_frame, width=3)
        self.cb_scheduleOnStartHour['values'] = self.hour_list
        self.cb_scheduleOnStartHour['state'] = 'readonly'
        self.cb_scheduleOnStartHour.current(8)
        self.cb_scheduleOnStartHour.grid(column=1, row=2)        
        self.cb_scheduleOnStartMinute = ttk.Combobox(self.schedule_on_frame, width=3)
        self.cb_scheduleOnStartMinute['values'] = self.minute_list
        self.cb_scheduleOnStartMinute['state'] = 'readonly'
        self.cb_scheduleOnStartMinute.current(0)
        self.cb_scheduleOnStartMinute.grid(column=2, row=2)    
        
        self.ent_scheduleOnEndDate = DateEntry(master=self.schedule_on_frame, selectmode="day")
        self.ent_scheduleOnEndDate.grid(column=3, row=2, columnspan=1, padx=2)
        self.cb_scheduleOnEndHour = ttk.Combobox(self.schedule_on_frame, width=3)
        self.cb_scheduleOnEndHour['values'] = self.hour_list
        self.cb_scheduleOnEndHour['state'] = 'readonly'
        self.cb_scheduleOnEndHour.current(18)
        self.cb_scheduleOnEndHour.grid(column=4, row=2)        
        self.cb_scheduleOnEndMinute = ttk.Combobox(self.schedule_on_frame, width=3)
        self.cb_scheduleOnEndMinute['values'] = self.minute_list
        self.cb_scheduleOnEndMinute['state'] = 'readonly'
        self.cb_scheduleOnEndMinute.current(0)
        self.cb_scheduleOnEndMinute.grid(column=5, row=2)    

        self.btnAll = tk.Button(master=self.schedule_on_frame, text="Add to All", command=self.addScheduleOnAll)
        self.btnAll.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

        self.btnShow = tk.Button(master=self.schedule_on_frame, text="Show existing", command=self.displayScheduleOn)
        self.btnShow.grid(column=2, row=3, columnspan=2, padx=10, pady=5)

        self.btnAdd = tk.Button(master=self.schedule_on_frame, text="Add", command=self.addScheduleOn)
        self.btnAdd.grid(column=4, row=3, columnspan=2, padx=10, pady=5)


        # frame to pack schedule off event
        self.schedule_off_frame = tk.LabelFrame(master=self, relief=tk.GROOVE, borderwidth=2, text="Schedule Off")
        self.schedule_off_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.lbl_scheduleOff = tk.Label(master=self.schedule_off_frame, text=f"{len(self.relay.scheduleOffDTs)} schedule events")
        self.lbl_scheduleOff.grid(column=0, row=0, columnspan=6, padx=10, pady=5)

        self.lbl_scheduleOffStart = tk.Label(master=self.schedule_off_frame, text=f"Start")
        self.lbl_scheduleOffStart.grid(column=0, row=1, columnspan=3, padx=10, pady=5)

        self.lbl_scheduleOffEnd = tk.Label(master=self.schedule_off_frame, text=f"End")
        self.lbl_scheduleOffEnd.grid(column=3, row=1, columnspan=3, padx=10, pady=5)

        self.ent_scheduleOffStartDate = DateEntry(master=self.schedule_off_frame, selectmode="day")
        self.ent_scheduleOffStartDate.grid(column=0, row=2, columnspan=1, padx = 2)
        self.cb_scheduleOffStartHour = ttk.Combobox(self.schedule_off_frame, width=3)
        self.cb_scheduleOffStartHour['values'] = self.hour_list
        self.cb_scheduleOffStartHour['state'] = 'readonly'
        self.cb_scheduleOffStartHour.current(0)
        self.cb_scheduleOffStartHour.grid(column=1, row=2)        
        self.cb_scheduleOffStartMinute = ttk.Combobox(self.schedule_off_frame, width=3)
        self.cb_scheduleOffStartMinute['values'] = self.minute_list
        self.cb_scheduleOffStartMinute['state'] = 'readonly'
        self.cb_scheduleOffStartMinute.current(0)
        self.cb_scheduleOffStartMinute.grid(column=2, row=2)

        self.ent_scheduleOffEndDate = DateEntry(master=self.schedule_off_frame, selectmode="day")
        self.ent_scheduleOffEndDate.grid(column=3, row=2, columnspan=1, padx=2)
        self.cb_scheduleOffEndHour = ttk.Combobox(self.schedule_off_frame, width=3)
        self.cb_scheduleOffEndHour['values'] = self.hour_list
        self.cb_scheduleOffEndHour['state'] = 'readonly'
        self.cb_scheduleOffEndHour.current(23)
        self.cb_scheduleOffEndHour.grid(column=4, row=2)        
        self.cb_scheduleOffEndMinute = ttk.Combobox(self.schedule_off_frame, width=3)
        self.cb_scheduleOffEndMinute['values'] = self.minute_list
        self.cb_scheduleOffEndMinute['state'] = 'readonly'
        self.cb_scheduleOffEndMinute.current(59)
        self.cb_scheduleOffEndMinute.grid(column=5, row=2) 

        self.btnAll1 = tk.Button(master=self.schedule_off_frame, text="Add to All", command=self.addScheduleOffAll)
        self.btnAll1.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

        self.btnShow1 = tk.Button(master=self.schedule_off_frame, text="Show existing", command=self.displayScheduleOff)
        self.btnShow1.grid(column=2, row=3, columnspan=2, padx=10, pady=5)

        self.btnAdd1 = tk.Button(master=self.schedule_off_frame, text="Add", command=self.addScheduleOff)
        self.btnAdd1.grid(column=4, row=3, columnspan=2, padx=10, pady=5)

        # frame for normal schedule
        self.normal_frame = tk.LabelFrame(master=self, relief=tk.GROOVE, borderwidth=2, text="Normal schedule")
        self.normal_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.weekdayVar = []
        self.ck_list = []
        self.ck_dict = {0:"Mon",1:"Tue",2:"Wed",3:"Thr",4:"Fri",5:"Sat",6:"Sun"}
        for i in range(7):
            if i in self.relay.OffWeekdays:
                self.weekdayVar.append(tk.BooleanVar(value=True))
            else:
                self.weekdayVar.append(tk.BooleanVar(value=False))
            
            self.ck_list.append(tk.Checkbutton(master=self.normal_frame, text=self.ck_dict[i],
                                               variable = self.weekdayVar[i], onvalue=True, offvalue=False))
            self.ck_list[i].grid(column=i, row=0)
                
 
        self.lbl_on = tk.Label(master=self.normal_frame, text= "On")
        self.lbl_on.grid(column=1, row=1, columnspan=1, padx=10,)
        self.lbl_off = tk.Label(master=self.normal_frame, text= "Off")
        self.lbl_off.grid(column=4, row=1, columnspan=1, padx=10)

        
        self.OnHourVar = tk.StringVar(self.normal_frame)
        self.OnHourVar.set("")
        self.OnMinuteVar = tk.StringVar(self.normal_frame)
        self.OnMinuteVar.set("")
        self.cb_OnHour = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OnHourVar)
        self.cb_OnHour['values'] = self.hour_list
        self.cb_OnHour['state'] = 'readonly'
        self.cb_OnHour.grid(column=1, row=2, padx=10, pady=5)        
        self.cb_OnMinute = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OnMinuteVar)
        self.cb_OnMinute['values'] = self.minute_list
        self.cb_OnMinute['state'] = 'readonly'
        self.cb_OnMinute.grid(column=2, row=2, padx=10, pady=5)

        self.OffHourVar = tk.StringVar(self.normal_frame)
        self.OffHourVar.set("")
        self.OffMinuteVar = tk.StringVar(self.normal_frame)
        self.OffMinuteVar.set("")
        self.cb_OffHour = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OffHourVar)
        self.cb_OffHour['values'] = self.hour_list
        self.cb_OffHour['state'] = 'readonly'
        self.cb_OffHour.grid(column=4, row=2, padx=10, pady=5)        
        self.cb_OffMinute = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OffMinuteVar)
        self.cb_OffMinute['values'] = self.minute_list
        self.cb_OffMinute['state'] = 'readonly'
        self.cb_OffMinute.grid(column=5, row=2, padx=10, pady=5)

        self.OnHourVar1 = tk.StringVar(self.normal_frame)
        self.OnHourVar1.set("")
        self.OnMinuteVar1 = tk.StringVar(self.normal_frame)
        self.OnMinuteVar1.set("")
        self.cb_OnHour1 = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OnHourVar1)
        self.cb_OnHour1['values'] = self.hour_list
        self.cb_OnHour1['state'] = 'readonly'
        self.cb_OnHour1.grid(column=1, row=3, padx=10, pady=5)        
        self.cb_OnMinute1 = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OnMinuteVar1)
        self.cb_OnMinute1['values'] = self.minute_list
        self.cb_OnMinute1['state'] = 'readonly'
        self.cb_OnMinute1.grid(column=2, row=3, padx=10, pady=5)   

        self.OffHourVar1 = tk.StringVar(self.normal_frame)
        self.OffHourVar1.set("")
        self.OffMinuteVar1 = tk.StringVar(self.normal_frame)
        self.OffMinuteVar1.set("")
        self.cb_OffHour1 = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OffHourVar1)
        self.cb_OffHour1['values'] = self.hour_list
        self.cb_OffHour1['state'] = 'readonly'
        self.cb_OffHour1.grid(column=4, row=3, padx=10, pady=5)        
        self.cb_OffMinute1 = ttk.Combobox(self.normal_frame, width=3, textvariable=self.OffMinuteVar1)
        self.cb_OffMinute1['values'] = self.minute_list
        self.cb_OffMinute1['state'] = 'readonly'
        self.cb_OffMinute1.grid(column=5, row=3, padx=10, pady=5)

        self.btnAll2 = tk.Button(master=self.normal_frame, text="Apply to All", command=self.setNormalScheduleAll)
        self.btnAll2.grid(column=0, row=4, columnspan=4, padx=10, pady=5)

        self.btnAdd2 = tk.Button(master=self.normal_frame, text="Apply", command=self.setNormalSchedule)
        self.btnAdd2.grid(column=4, row=4, columnspan=3, padx=10, pady=5)
        
        
        # frame for load and save setting
        self.save_load_frame = tk.LabelFrame(master=self, relief=tk.GROOVE, borderwidth=2, text="Save setting")
        self.save_load_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
#         self.btnLoad = tk.Button(master=self.save_load_frame, text="Load setting", command=self.load_setting)
#         self.btnLoad.grid(column=0, row=0, columnspan=3, padx=10, pady=5)
        
        self.btnSave = tk.Button(master=self.save_load_frame, text="Save setting", command=self.save_setting)
        self.btnSave.grid(column=0, row=0, columnspan=1, padx=10, pady=5)
        
        self.load(self.board, self.relay)
    
    def load_setting(self):
        self.board = helper.load(self.board.n)
    
    def save_setting(self):
        helper.save(self.board, self.board.n)
    
    def OnOffEvent(self, On):
        self.status_text = "On" if On else "Off"
        self.lbl_status.config(text=f"Relay {self.ch} is {self.status_text}")

    def allwaysOnOff(self):
        # gui alwaysOnOff handler
        
        status_text = self.statusVar.get()
        if status_text == "On":
            self.relay.setAlwaysOn(True)
        elif status_text == "Off":
            self.relay.setAlwaysOn(False)
        else:
            self.relay.setAlwaysOn(None)
            
        self.update_status()

    def addScheduleOnAll(self):
        # add scheduleOn to all relays
        OnDate = self.ent_scheduleOnStartDate.get_date()
        OnHour = int(self.cb_scheduleOnStartHour.get())
        OnMinute = int(self.cb_scheduleOnStartMinute.get())
        OnTime = time(OnHour,OnMinute)
        OnDT = dt.combine(OnDate,OnTime)
              
        OffDate = self.ent_scheduleOnEndDate.get_date()
        OffHour = int(self.cb_scheduleOnEndHour.get())
        OffMinute = int(self.cb_scheduleOnEndMinute.get())
        OffTime = time(OffHour,OffMinute)
        OffDT = dt.combine(OffDate,OffTime)
        
        self.board.addScheduleOnDT([[OnDT,OffDT]])
        self.lbl_scheduleOn.config(text=f"{len(self.relay.scheduleOnDTs)} schedule events") 

    def addScheduleOn(self):
        # add scheduleOn to one relay

        OnDate = self.ent_scheduleOnStartDate.get_date()
        OnHour = int(self.cb_scheduleOnStartHour.get())
        OnMinute = int(self.cb_scheduleOnStartMinute.get())
        OnTime = time(OnHour,OnMinute)
        OnDT = dt.combine(OnDate,OnTime)
              
        OffDate = self.ent_scheduleOnEndDate.get_date()
        OffHour = int(self.cb_scheduleOnEndHour.get())
        OffMinute = int(self.cb_scheduleOnEndMinute.get())
        OffTime = time(OffHour,OffMinute)
        OffDT = dt.combine(OffDate,OffTime)

        self.relay.addScheduleOnDT([[OnDT,OffDT]])
        self.lbl_scheduleOn.config(text=f"{len(self.relay.scheduleOnDTs)} schedule events") 

    def displayScheduleOn(self):
        # display scheduleOn of one relay
        self.displaySchedule(True)   
        
    def addScheduleOffAll(self):
        # add scheduleOn to all relays
        OffDate = self.ent_scheduleOffStartDate.get_date()
        OffHour = int(self.cb_scheduleOffStartHour.get())
        OffMinute = int(self.cb_scheduleOffStartMinute.get())
        OffTime = time(OffHour,OffMinute)
        OffDT = dt.combine(OffDate,OffTime)
              
        OnDate = self.ent_scheduleOffEndDate.get_date()
        OnHour = int(self.cb_scheduleOffEndHour.get())
        OnMinute = int(self.cb_scheduleOffEndMinute.get())
        OnTime = time(OnHour,OnMinute)
        OnDT = dt.combine(OnDate,OnTime)
        
        self.board.addScheduleOffDT([[OffDT, OnDT]])
        self.lbl_scheduleOff.config(text=f"{len(self.relay.scheduleOffDTs)} schedule events") 

    def addScheduleOff(self):
        # add scheduleOn to one relay
        OffDate = self.ent_scheduleOffStartDate.get_date()
        OffHour = int(self.cb_scheduleOffStartHour.get())
        OffMinute = int(self.cb_scheduleOffStartMinute.get())
        OffTime = time(OffHour,OffMinute)
        OffDT = dt.combine(OffDate,OffTime)
              
        OnDate = self.ent_scheduleOffEndDate.get_date()
        OnHour = int(self.cb_scheduleOffEndHour.get())
        OnMinute = int(self.cb_scheduleOffEndMinute.get())
        OnTime = time(OnHour,OnMinute)
        OnDT = dt.combine(OnDate,OnTime)
        
        self.relay.addScheduleOffDT([[OffDT, OnDT]])
        self.lbl_scheduleOff.config(text=f"{len(self.relay.scheduleOffDTs)} schedule events")
 
  
    def displayScheduleOff(self):
        # display scheduleOff of one relay
        self.displaySchedule(False)

    def displaySchedule(self, On):
        # displacy scheduleOn/Off event for one relay
        
        OnOff = "On" if On else "Off"
        
        scheduleWindow = tk.Tk()
        scheduleWindow.title(f"Schedule {OnOff} Event")
        scheduleWindow.geometry("400x500")
        
        lbl_test = tk.Label(master=scheduleWindow, text=f"Schedule {OnOff} event of relay {self.ch}")
        lbl_test.pack()
        
        DTlistBox = tk.Listbox(master=scheduleWindow)
        DTlistBox.pack(fill=tk.BOTH, expand=True)

        if On:
            DTlist = self.relay.scheduleOnDTs
            for item in DTlist:
                item = "On: " + str(item[0]) + "   Off: " + str(item[1]) 
                DTlistBox.insert(tk.END, item) 
        else:
            DTlist = self.relay.scheduleOffDTs
            for item in DTlist:
                item = "Off: " + str(item[0]) + "   On: " + str(item[1])
                DTlistBox.insert(tk.END, item) 
            
        def delete():
            # curselection return (selected_id,) by zero index method
            idx = DTlistBox.curselection()[0] # get the id
            DTlistBox.delete(tk.ANCHOR)
            if On:
                self.relay.removeScheduleOnDT(idx)
            else:
                self.relay.removeScheduleOffDT(idx)
            self.update_status()
            
        def deleteForAllRelays():
            idx = DTlistBox.curselection()[0] # get the id

            DTlistBox.delete(tk.ANCHOR)
            if On:
                DTs = [self.relay.scheduleOnDTs[idx]]
                self.board.removecheduleOnDTAll(DTs)
            else:
                DTs = [self.relay.scheduleOffDTs[idx]]
                self.board.removecheduleOffDTAll(DTs)
            self.update_status()
            
        btn_delete = tk.Button(master=scheduleWindow, text="delete", command=delete)
        btn_delete.pack(side=tk.RIGHT)
        btn_delete = tk.Button(master=scheduleWindow, text="delete for all relays", command=deleteForAllRelays)
        btn_delete.pack(side=tk.LEFT)
        
        scheduleWindow.mainloop()       

    def setNormalScheduleAll(self):
        OnOffTime = [time(int(self.OnHourVar.get()), int(self.OnMinuteVar.get())),
                     time(int(self.OffHourVar.get()), int(self.OffMinuteVar.get()))]
        
        OffWeekdays = []
        for i in range(7):
            if self.weekdayVar[i].get():
                OffWeekdays.append(i)
                
        self.board.setOffWeekdaysAll(OffWeekdays)
        
        try:
            if(self.OnHourVar1.get()) != "":
                OnOffTime1 = [time(int(self.OnHourVar1.get()), int(self.OnMinuteVar1.get())),
                             time(int(self.OffHourVar1.get()), int(self.OffMinuteVar1.get()))]
                self.board.setOnOffTime([OnOffTime,OnOffTime1])
            else:
                self.board.setOnOffTime([OnOffTime])
        except ValueError:
            print("fail to set normal schedule")
            return 


    def setNormalSchedule(self):
                
        OnOffTime = [time(int(self.OnHourVar.get()), int(self.OnMinuteVar.get())),
                     time(int(self.OffHourVar.get()), int(self.OffMinuteVar.get()))]
        
        OffWeekdays = []
        for i in range(7):
            if self.weekdayVar[i].get():
                OffWeekdays.append(i)
                
        self.relay.setOffWeekdays(OffWeekdays)

        try:
            if(self.OnHourVar1.get()) != "":
                OnOffTime1 = [time(int(self.OnHourVar1.get()), int(self.OnMinuteVar1.get())),
                             time(int(self.OffHourVar1.get()), int(self.OffMinuteVar1.get()))]
                self.relay.setOnOffTime([OnOffTime, OnOffTime1])
            else:
                self.relay.setOnOffTime([OnOffTime])

        except ValueError:
            print("fail to set normal schedule")
            return 

    def load(self, board, relay):
        # load relay setting
        self.ch = relay.ch
        self.board = board
        self.relay = relay
        
        if self.relay.alwaysOnOff == True:
            self.OnOffEvent(True)
            self.r1.select()
        elif self.relay.alwaysOnOff == False:
            self.OnOffEvent(False)
            self.r2.select()
        else:
            self.r3.select()
            if relay.status == True:
                self.OnOffEvent(True)
            else:
                self.OnOffEvent(False)

        self.lbl_scheduleOn.config(text=f"{len(self.relay.scheduleOnDTs)} schedule events")
        self.lbl_scheduleOff.config(text=f"{len(self.relay.scheduleOffDTs)} schedule events")
         
        # normal schedule
        for i in range(7):
            if i in self.relay.OffWeekdays:
                self.weekdayVar[i].set(True)
                self.ck_list[i].select()
            else:
                self.ck_list[i].deselect()
  
        OnHour = str(self.relay.OnOffTime[0][0])[:2]
        OnMinute = str(self.relay.OnOffTime[0][0])[3:5]
        self.OnHourVar.set(int(OnHour))
        self.OnMinuteVar.set(int(OnMinute))
        OffHour = str(self.relay.OnOffTime[0][1])[:2]
        OffMinute = str(self.relay.OnOffTime[0][1])[3:5]
        self.OffHourVar.set(int(OffHour))
        self.OffMinuteVar.set(int(OffMinute)) 

       
        if len(self.relay.OnOffTime) > 1:      
            OnHour = str(self.relay.OnOffTime[1][0])[:2]
            OnMinute = str(self.relay.OnOffTime[1][0])[3:5]
            self.OnHourVar1.set(int(OnHour))
            self.OnMinuteVar1.set(int(OnMinute))
            OffHour = str(self.relay.OnOffTime[1][1])[:2]
            OffMinute = str(self.relay.OnOffTime[1][1])[3:5]
            self.OffHourVar1.set(int(OffHour))
            self.OffMinuteVar1.set(int(OffMinute))
        else:
            self.OnHourVar1.set("")
            self.OnMinuteVar1.set("")
            self.OffHourVar1.set("")
            self.OffMinuteVar1.set("")
            
    def update_status(self):
        # call this function with relay.schedule to update

        self.OnOffEvent(self.relay.status)
        self.lbl_scheduleOn.config(text=f"{len(self.relay.scheduleOnDTs)} schedule events")
        self.lbl_scheduleOff.config(text=f"{len(self.relay.scheduleOffDTs)} schedule events")


class Frame1(tk.Frame):
    def __init__(self, window, board, frame2):
        super().__init__(master= window)
        
        self.board = board
        self.frame2 = frame2
        self.btn_list = []
        
        # using canvas and set background
        path = "ac_static/background.JPG"
        canvas = tk.Canvas(master=self, width= 1500, height= 950)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open(path).resize((1500,900), Image.ANTIALIAS))
        canvas.background = img
        canvas.create_image(0,0, anchor=tk.NW, image = img)


        for i in range(self.board.n):
            color = "green" if self.board.relays[i].status else "grey"
            text = f"relay {i+1}"
            # must use lambda i=i, or i will be 16 in this case
#             self.btn_list.append(tk.Button(master=self,relief=tk.FLAT, bg=color ,text=text,
#                                command=lambda i=i: self.frame2.load(self.board, self.board.relays[i])))
#             
#             self.btn_list[i].pack()
            self.btn_list.append(tk.Button(master=self,relief=tk.FLAT, bg=color ,text=text,
                               command=lambda i=i: self.frame2.load(self.board, self.board.relays[i])))
            #
        canvas.create_window(270,800, anchor=tk.NW, window=self.btn_list[0])
        canvas.create_window(360,800, anchor=tk.NW, window=self.btn_list[1])
        canvas.create_window(450,800, anchor=tk.NW, window=self.btn_list[2])
        canvas.create_window(540,800, anchor=tk.NW, window=self.btn_list[3])
        canvas.create_window(660,800, anchor=tk.NW, window=self.btn_list[4])
        canvas.create_window(800,800, anchor=tk.NW, window=self.btn_list[5])
        canvas.create_window(1120,800, anchor=tk.NW, window=self.btn_list[6])
        canvas.create_window(1120,700, anchor=tk.NW, window=self.btn_list[7])
        canvas.create_window(660,480, anchor=tk.NW, window=self.btn_list[8]) # FCU26
        canvas.create_window(1000,800, anchor=tk.NW, window=self.btn_list[9])
        canvas.create_window(1120,550, anchor=tk.NW, window=self.btn_list[10])
        canvas.create_window(1120,460, anchor=tk.NW, window=self.btn_list[11])
        canvas.create_window(1120,350, anchor=tk.NW, window=self.btn_list[12])
        canvas.create_window(1000,300, anchor=tk.NW, window=self.btn_list[13])
        canvas.create_window(890,300, anchor=tk.NW, window=self.btn_list[14])
        canvas.create_window(770,300, anchor=tk.NW, window=self.btn_list[15])
        canvas.create_window(650,300, anchor=tk.NW, window=self.btn_list[16])
        canvas.create_window(545,300, anchor=tk.NW, window=self.btn_list[17])
        canvas.create_window(460,300, anchor=tk.NW, window=self.btn_list[18])
        canvas.create_window(375,300, anchor=tk.NW, window=self.btn_list[19])
        canvas.create_window(290,300, anchor=tk.NW, window=self.btn_list[20])
        canvas.create_window(180,300, anchor=tk.NW, window=self.btn_list[21])
        canvas.create_window(300,480, anchor=tk.NW, window=self.btn_list[22])
        canvas.create_window(180,400, anchor=tk.NW, window=self.btn_list[23])
        canvas.create_window(300,690, anchor=tk.NW, window=self.btn_list[24])
        
        

    def update_status(self):
        
        for i in range(self.board.n):
            color = "green" if self.board.relays[i].status else "grey"
            self.btn_list[i].config(bg=color)
        
     


if __name__ == "__main__":
    
    gp.cleanup()
    gp.setmode(gp.BCM)
    
    #relayList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    #pinList = [10,9,11,5,6,13,19,26,21,20,16,12,7,8,25,24]
    
    relayList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    pinList = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,21,20,16,12,7,8,25,24,23,18,15]
    
    relayBoard1 = relayBoard(25, relayList,pinList)
    
    
    relayBoard1.setOnOffTime([[time(7,30),time(18,30)]])
  

    try:
        relayBoard1 = helper.load(25)
    except Exception as e:
        print(e)
    
    relayBoard1.schedule()
    
    

    window = tk.Tk()
    window.title("Flex KP 7F GPO automatic AC scheduling system")
    window.geometry("1920x1080")
    
    frame2 = Frame2(window, relayBoard1)
    frame1 = Frame1(window, relayBoard1, frame2)
    


    frame2.pack(side=tk.RIGHT, fill=tk.Y)
    frame1.pack(side=tk.LEFT, fill=tk.Y)
    
    
    

    def schedule():
        global relayBoard1
        global frame2
        global frame1
        relayBoard1.schedule(log=True)
        frame2.update_status()
        frame1.update_status()
        window.after(1000, schedule)

    window.after(1000,schedule)
    
    window.mainloop()
