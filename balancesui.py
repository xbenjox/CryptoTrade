from tkinter import *

import xml.etree.ElementTree as ET

import math

class BalanceUI(Toplevel):
  def __init__(self, parent, bal, cur):
    Toplevel.__init__(self, parent)
           
    self.balances = bal
    self.currencies = cur
    
    self.avail_bal_dict = dict()
    
    self.avail_bal_details = list()
    
    # reformat data
    #print(self.balances)
    for k, v in self.balances.items():
      if v != 0:
        self.avail_bal_dict[k] = v
    
    #print("Available Balance List: " + str(self.avail_bal_dict))
    
    for c in self.currencies['data']:
      if c['id'] in self.avail_bal_dict:
        self.avail_bal_details.append(c)
    
    #print("Available Balance Details: " + str(self.avail_bal_details))
            
    self.transient(parent)
        
    self.geometry("800x600+50+50")
      
    self.createWidgets()    
    self.updateWidgets()                       
    return
      
  def createWidgets(self):
    self.lblBalFrame = LabelFrame(self)
    self.lblBalFrame['text'] = "Balances"
    self.lblBalFrame.grid({"row":"0"})
    
    # Create lable for each currency
    r = 0
    for bd in self.avail_bal_details:
      lbl = Label(self.lblBalFrame)
      lbl['text'] = str(bd['name']) + " : " + str(bd['code'] + " : " + str(self.avail_bal_dict[bd['id']]))
      lbl.grid({"row":r})
      r += 1
        
    self.Close = Button(self)
    self.Close["text"] = "Close"
    self.Close["fg"] = "red"
    self.Close["command"] = self._quit
    self.Close.grid({"row": "5", "columnspan":"1"})
    
    return 
  
  def updateWidgets(self):   
    
    return 

  def on_key_event(self, event):
    print('you pressed %s'%event.key)
    return
      
  def _quit(self):
    self.destroy()
    return

 
  
