import os
import json
import tkinter
from tkinter import Label, Button, Listbox, Scrollbar, messagebox
from tkinter.constants import *
import keyboard

class keyGUI():
    def __init__(self):
        try:
            self.file = open("data/keyboardData.json", "x")
            json.dump(dict(disabledKeys = []),self.file)
        except Exception as e:
            print(e)
        finally:
            self.file = open("data/keyboardData.json", "r+")
        
        if os.stat("data/keyboardData.json").st_size != 0:
            data = json.load(self.file)
            for i in data["disabledKeys"]:
                keyboard.block_key(i.strip())
        self.dKey = ""
        self.root = tkinter.Tk()
        self.root.title('App')
        self.root.resizable(False, False)
        windowWidth = 500
        windowHeight = 350
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        self.root.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        
        clickBtn = Button(self.root, text = 'Enter Key', bd = '5',command = self.getKey)
        clickBtn.grid(row = 0, column = 0, padx = 20)
        
        self.scrollbar = Scrollbar(self.root)
        self.printKey = Label(self.root, text = "Key", font=("Arial", 20))
        self.printKey.grid(row = 1, column = 0)
        
        self.disableBtn = Button(self.root, text = 'Disable Key', bd = '5',command = self.disableKey, state = DISABLED)
        self.disableBtn.grid(row = 2, column = 0)
        
        self.printBlocked = Label(self.root, text = "Blocked Keys", font=("Arial", 20))
        self.printBlocked.grid(row = 0, column = 1)
        
        self.Lb = Listbox(self.root, yscrollcommand = self.scrollbar.set, font=("Helvetica", 20),
                          bg = "white", activestyle = 'dotbox', fg = "black", selectforeground="pink",
                          selectbackground="grey")
        self.Lb.grid(row = 1, rowspan = 2, column = 1, padx = 50, pady = 5)
        self.Lb.bind('<Double-1>', self.unBlock)
        
        self.file.seek(0)
        data = json.load(self.file)
        for i in data["disabledKeys"]:
            if os.stat("data/keyboardData.json").st_size != 0:
                self.Lb.insert(self.Lb.size()+1,i)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
    
    def on_closing(self):
        self.root.destroy()
    
    def unBlock(self,event):
        cs = self.Lb.curselection()
        self.Lb.configure(state=DISABLED)
        res = messagebox.askokcancel("Unblock Key \""+self.Lb.get(cs).strip()+"\"", "Are you sure?")
        self.Lb.configure(state=NORMAL)
        if res is True:
            removeKey = self.Lb.get(cs).strip()
            keyboard.unhook_key(removeKey)
            self.Lb.delete(cs)
            self.file.seek(0)
            data = json.load(self.file)
            data["disabledKeys"].remove(removeKey)
            self.file.seek(0)
            self.file.truncate()
            json.dump(data,self.file)
    
    def getKey(self):
        self.dKey = keyboard.read_key()
        self.printKey.configure(text = self.dKey)
        self.disableBtn.configure(state = NORMAL)
    
    def disableKey(self):
        keyboard.block_key(self.dKey)
        self.Lb.insert(self.Lb.size()+1,self.dKey) 
        self.file.seek(0)
        data = json.load(self.file)
        data["disabledKeys"].append(self.dKey)
        self.file.seek(0)
        json.dump(data,self.file)
        self.disableBtn.configure(state = DISABLED)
        
    def message(self,message):
        messagebox.showerror("Error", message)

# app = keyGUI()