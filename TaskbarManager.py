from infi.systray.traybar import SysTrayIcon
from pyvda import VirtualDesktop
import threading
import os
import subprocess
import keyboard as key
import ctypes
import json
from tendo import singleton
singleSession = singleton.SingleInstance()
from specificKeyGUI import keyGUI
from customTaskbarGUI import tbGUI

specKeyRunning = False
customTbRunning = False
stop_thread = False
directory = os.getcwd()
currentDesktop = 1
previousDesktop = 0 # Change Later

if os.path.isdir("data") is False:
    path = os.path.join(directory, "data")
    os.mkdir(path)

initial = {
            0:  {
                "Pinned Apps": [["",""],["",""]],
                "Custom Name": "",
                "Other":""
            }
        }

try:
    tbFile = open("data/taskbarData.json", "x")
    json.dump(initial, tbFile, indent=2, separators=(',', ':'))
except Exception as e:
    print(e)
finally:
    tbFile = open("data/taskbarData.json", "r+")

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    
def getCurrentDesktop():
    global currentDesktop
    global previousDesktop
    
    tbFile.seek(0)
    data = json.load(tbFile)
    while(True):
        global stop_thread
        if stop_thread is True:
            break
        
        if os.path.isfile("syspin.exe") is False:
            ctypes.windll.user32.MessageBoxW(0, "Make sure \"syspin\" is downloaded and in the same folder!", "Error", 0)
            break
        
        if str(currentDesktop) not in data:
            ctypes.windll.user32.MessageBoxW(0, "Current desktop not Configured", "Error", 0)
            break
        
        desktop = VirtualDesktop.current()
        currentDesktop = desktop.number
        if currentDesktop!=previousDesktop:
            for app in data[str(previousDesktop)]["Pinned Apps"]:
                subprocess_cmd('cd / & cd '+directory+' & syspin "'+app[0].encode('unicode-escape').decode().replace('/', '\\')+'" "Unpin from taskbar" ')
            for app in data[str(currentDesktop)]["Pinned Apps"]:
                subprocess_cmd('cd / & cd '+directory+' & syspin "'+app[0].encode('unicode-escape').decode().replace('/', '\\')+'" "Pin to taskbar" ')
            previousDesktop = currentDesktop

def disableKey(systray):
    for i in range(150):
        key.block_key(i)

def enableKey(systray):
    key.unhook_all()
    

class threadManager():
    def run(self,systray):
        global stop_thread
        stop_thread = False
        self.bgRun = threading.Thread(target = getCurrentDesktop)
        self.bgRun.start()
    def stop(self,systray):
        global stop_thread
        stop_thread = True
        self.bgRun.join()
    
def specKey(systray):
    global specKeyRunning
    if specKeyRunning is False: 
        specKeyRunning = True
        app = keyGUI()
        specKeyRunning = False
    else:
        ctypes.windll.user32.MessageBoxW(0, "Already Open", "Error", 1)
        
def customTaskbar(systray):
    global customTbRunning
    if customTbRunning is False: 
        customTbRunning = True
        app = tbGUI()
        customTbRunning = False
    else:
        ctypes.windll.user32.MessageBoxW(0, "Already Open", "Error", 1)

def quit(systray):
    thread.stop

thread = threadManager()

menu_options = (("Keyboard",None,(("Enable Keyboard", "icons/green_icon.ico", enableKey),
                                        ("Disable Keyboard", "icons/red_icon.ico", disableKey),
                                        ("Disable Specific Key", None, specKey)
                                        )),
                ("Taskbar AutoPin",None,(("Enable", "icons/green_icon.ico", thread.run),
                                        ("Disable", "icons/red_icon.ico", thread.stop),
                                        ("Customize", None, customTaskbar)
                                        ))
                )
systray = SysTrayIcon("icons/main_icon.ico", "Taskbar Manager", menu_options, on_quit = quit)

systray.start()