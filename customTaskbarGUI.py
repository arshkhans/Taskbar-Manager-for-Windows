import tkinter
from tkinter import Frame, Listbox, Scrollbar, Button, Label, messagebox, filedialog
from tkinter import StringVar, OptionMenu, Spinbox, _setit, Entry
from tkinter.constants import *
import json

class tbGUI():
    def __init__(self):
        self.pathData = []
        self.file = open("data/taskbarData.json", "r+")
        
        data = json.load(self.file)
        
        self.root = tkinter.Tk()
        self.root.title('App')
        self.root.resizable(False, False)
 
        windowWidth = 380
        windowHeight = 500
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        self.root.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        self.root.grid_columnconfigure(4, minsize=100) 
        
        self.scrollbar = Scrollbar(self.root)
        
        f1 = Frame(self.root)
        
        self.desktopNum = Spinbox(f1, from_ = 1, to = 10, width=4, state = 'readonly')
        self.desktopNum.pack(side = LEFT,padx = 6)
        
        addBtn = Button(f1, text = 'Add', bd = '5', width = 6, command = self.desktopAdd)
        addBtn.pack(side = LEFT)
        
        f1.grid(row = 0, column = 0,pady = 2)

        desktopList = ["--None--"]
        
        self.file.seek(0)
        data = json.load(self.file)
        for i in data.values():
            if i["Custom Name"] != "":
                desktopList.append(i["Custom Name"])
        self.options = StringVar(self.root)
        self.options.set("--None--")
        
        self.allDesktop = OptionMenu( self.root , self.options , *desktopList)
        self.allDesktop.grid(row = 1, column = 0)
        
        configBth = Button(self.root, text = 'Config', bd = '5', width = 6,command = self.desktopConfig)
        configBth.grid(row = 1, column = 1)
        
        emptyLabel = Label(self.root, text = "")
        emptyLabel.grid(row = 0, column = 2, rowspan=2, ipadx = 60)
        emptyLabel = Label(self.root, text = "")
        emptyLabel.grid(row = 0, column = 3, rowspan=2, ipadx = 30)
        
        self.root.mainloop()
    
    def desktopConfig(self):
        if self.options.get() == "--None--":
            messagebox.showinfo("Dumbass", "Select one first")
        else:
            self.file.seek(0)
            data = json.load(self.file)
            
            f2 = Frame(self.root, border=4, borderwidth=4, background="grey")
            
            pinnedLabel = Label(f2, text = "Pinned App")
            pinnedLabel.grid(row = 0, column = 0, sticky=W, padx = 4)
            
            self.Lb = Listbox(f2, yscrollcommand = self.scrollbar.set, font=("Helvetica", 20),
                          bg = "white", activestyle = 'dotbox', fg = "black", selectforeground="pink",
                          selectbackground="grey", width = 16, height = 8)
            self.Lb.grid(row = 1, column = 0,)
            self.Lb.bind('<Double-1>', self.removeApp)
            
            for i in data[self.options.get()[8:]]["Pinned Apps"]:
                self.Lb.insert(self.Lb.size()+1,i[1])
            
            self.pathData = data[self.options.get()[8:]]["Pinned Apps"]

            self.pathEntry = Entry(f2,textvariable = "none", font=('calibre',10,'normal'), width = 32)
            self.pathEntry.grid(row = 2, column = 0,pady = 9, padx = 12)
            
            addPathBth = Button(f2, text = 'Enter', bd = '3', width = 6,command = self.addAppByPath)
            addPathBth.grid(row = 2, column = 1)
            
            addBth = Button(f2, text = 'Browse', bd = '3', width = 6,command = self.addApp)
            addBth.grid(row = 2, column = 2, padx = 6)
            
            testBth = Button(f2, text = 'Save', bd = '5', width = 6,command = self.save)
            testBth.grid(row = 3, column = 0, sticky=W)
            
            deleteBtn = Button(f2, text = 'Delete Config', bd = '3',command = lambda: self.desktopRemove(f2))
            deleteBtn.grid(row = 4, column = 0)
            
            f2.grid(row = 2, column = 0, columnspan=4)      
        
    def desktopAdd(self):
        self.file.seek(0)
        data = json.load(self.file)
        name = "Desktop "+self.desktopNum.get()
        menu = self.allDesktop["menu"]
        last = menu.index("end")
        all = []
        for index in range(last+1):
            all.append(menu.entrycget(index, "label"))
        if name in all:
            messagebox.showinfo("Dumbass", "Alredy Added")
        else:
            data[self.desktopNum.get()] = {
                        "Pinned Apps": [],
                        "Custom Name": name,
                        "Other": ""
                    }
            self.file.seek(0)
            self.file.truncate()
            json.dump(data, self.file, indent=2, separators=(',', ':'))
            self.file.flush()
            self.allDesktop['menu'].add_command(label=name, command = _setit(self.options, name))
    
    def desktopRemove(self,f2):
        f2.grid_forget()
        self.file.seek(0)
        data = json.load(self.file)
        del data[self.options.get()[8:]]
        self.file.seek(0)
        self.file.truncate()
        json.dump(data, self.file, indent=2, separators=(',', ':'))
        self.file.flush()
        if self.options.get() != "--None--":
            self.allDesktop['menu'].delete(self.options.get())
        self.options.set("--None--")
    
    def addAppByPath(self):
        filePath = self.pathEntry.get()
        if filePath:
            try:
                temp = filePath[::-1]
                temp = temp[:temp.find("/")][::-1]
                self.Lb.insert(self.Lb.size()+1,temp)
                self.pathData.append([filePath,temp])
            except Exception as e:
                print(e)
        self.pathEntry.delete(0, 'end')
    
    def addApp(self):
        filePath = filedialog.askopenfilename()
        if filePath and filePath.endswith(".exe"):
            temp = filePath[::-1]
            temp = temp[:temp.find("/")][::-1]
            if self.pathData == []:
                self.Lb.insert(self.Lb.size()+1,temp)
                self.pathData.append([filePath,temp])
            else:
                if [filePath,temp] in self.pathData:
                    messagebox.showinfo("Error", "Alredy Added")
                else:
                    self.Lb.insert(self.Lb.size()+1,temp)
                    self.pathData.append([filePath,temp])
        else:
            messagebox.showinfo("Error", "Make sure the file exists and is a .exe file.")

    def removeApp(self,event):
        cs = self.Lb.curselection()
        self.Lb.configure(state=DISABLED)
        res = messagebox.askokcancel("Remove App \""+self.Lb.get(cs).strip()+"\"", "Are you sure?")
        self.Lb.configure(state=NORMAL)

        remove = None
        for index,i in enumerate(self.pathData):
            if i[1] == self.Lb.get(cs):
                remove = index
        del self.pathData[remove]
        print(self.pathData)
        
        if res is True:
            self.Lb.delete(cs)
    
    def save(self):
        self.file.seek(0)
        data = json.load(self.file)
        data[self.options.get()[8:]]["Pinned Apps"] = self.pathData
        self.file.seek(0)
        self.file.truncate()
        json.dump(data, self.file, indent=2, separators=(',', ':'))
        self.file.flush()
        
    def onEnter(self, event):
        self.hoverLabel.configure(text="Double click on added desktop to Edit")
    
    def onLeave(self, event):
        self.hoverLabel.configure(text="")
    
# app = tbGUI()