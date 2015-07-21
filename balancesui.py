from tkinter import *

import xml.etree.ElementTree as ET

import math

class BalanceUI(Toplevel):
  def __init__(self, parent, bal, cur):
    Toplevel.__init__(self, parent)
           
    self.balances = bal
    self.currencies = cur
    
    avail_bal_list = list()
    
    avail_bal_details = list()
    
    # reformat data
    for k, v in self.balances['data']['available'].items():
      if v != 0:
        avail_bal_list.append({k:v})
    
    print(avail_bal_list)
    
    for c in self.currencies['data']:
      if c['id'] in avail_bal_list:
        avail_bal_details.append(c)
    
    print(avail_bal_details)
            
    self.transient(parent)
        
    self.geometry("800x600+50+50")
      
    self.createWidgets()    
    self.updateWidgets()                       
    return
      
  def createWidgets(self):
    self.lblTrades = Label(self)
    self.lblTrades['text'] = "Balances"
    self.lblTrades.grid({"row":"0"})
    
    # Create lable for each currency
    r = 0
    for k, v in self.balances['data']['available'].items():
      if v != 0:
        lbl = Label(self.lblTrades)
        lbl['text'] = str(k) + " : " + str(v)
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

 
  
