from tkinter import *

import xml.etree.ElementTree as ET

import math

class SettingsUI(Toplevel):
  def __init__(self, parent):
    Toplevel.__init__(self, parent)
            
    self.transient(parent)
        
    #self.geometry("800x600+50+50")
    try:
      self.load_settings()
      
    except FileNotFoundError:
      print("Settings File Not Found!")
      self.createSettingsFile()
      self.load_settings()
      
    self.createWidgets()    
    self.updateWidgets()                       
    return
      
  def createWidgets(self):
    self.lblTrades = Label(self)
    self.lblTrades['text'] = "Cryptsy Keys"
    self.lblTrades.grid({"row":"0"})
    
    self.lblPubKey = Label(self)
    self.lblPubKey['text'] = "Public Key"
    self.lblPubKey.grid({"row":"1"})
    
    self.entPubKey = Entry(self)
    self.entPubKey['width'] = 100
    self.entPubKey.insert(0, self.pubKey)
    self.entPubKey.grid({"row":"1","column":"1"})
    
    self.lblPrivKey = Label(self)
    self.lblPrivKey['text'] = "Private Key"
    self.lblPrivKey.grid({"row":"2"})
    
    self.entPrivKey = Entry(self)
    self.entPrivKey['width'] = 100
    self.entPrivKey.insert(0, self.privKey)
    self.entPrivKey.grid({"row":"2","column":"1"})
    
    
    self.Close = Button(self)
    self.Close["text"] = "Ok"
    self.Close["command"] = self.ok
    self.Close.grid({"row": "5", "column":"0", "columnspan":"1"})
    
    self.Close = Button(self)
    self.Close["text"] = "Cancel"
    self.Close["fg"] = "red"
    self.Close["command"] = self._quit
    self.Close.grid({"row": "5", "column":"1", "columnspan":"1"})
    
    return 
  
  def updateWidgets(self):   
    
    return 

  def on_key_event(self, event):
    print('you pressed %s'%event.key)
    return
  
  def ok(self):
    
    root = self.tree.getroot()
      
    for keys in root.findall('keys'):
      print(self.entPubKey.get())
      keys.find('public').text = self.entPubKey.get()
      keys.find('private').text = self.entPrivKey.get()
    
    self.tree.write('Data/settings.xml')
    self.destroy()
    return 
      
  def _quit(self):
    self.destroy()
    return

  def createSettingsFile(self):
    f = open("Data/settings.xml", 'w')
    
    f.write("""
<?xml version="1.0"?>
<settings>
  <keys>
    <public>Not Set</public>
    <private>Not Set</private>
  </keys>
</settings>
      """)
    
    f.close()
    return
 
  def load_settings(self):
    self.tree = ET.parse('Data/settings.xml')
    root = self.tree.getroot()
      
    for keys in root.findall('keys'):
      self.pubKey = keys.find('public').text
      self.privKey = keys.find('private').text
    
    return
