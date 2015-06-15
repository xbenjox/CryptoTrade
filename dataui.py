from tkinter import *

import matplotlib
import numpy as np
#from sklearn import linear_model

import xml.etree.ElementTree as ET

import math

class DataUI(Toplevel):
  def __init__(self, parent, c_api):
    Toplevel.__init__(self, parent)
    
    self.c = c_api
    
    self.transient(parent)
        
    self.geometry("800x600+50+50")
    
    self.createWidgets()
    
    self.updateWidgets()
                       
    return
      
  def createWidgets(self):
    self.lblDogeData = Label(self)
    self.lblDogeData['text'] = "Doge Data"
    self.lblDogeData.grid({"row":"1"})
    
    self.btnDogeCollect = Button(self)
    self.btnDogeCollect['text'] = "Collect Data"
    self.btnDogeCollect['command'] = lambda: self.CollectData(132, "Day")
    self.btnDogeCollect.grid({"row":"1", "column":"1"})
    
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

  def CollectData(self, mid, t):
    data = self.c.market_ohlc(mid, interval=t, )
    
    print(data)
        
    return data
  
  def get_history_xml(self):
    tree = ET.parse('sellpoints.xml')
    
    root = tree.getroot()
    
    for trade in root.findall('trade'):
      cur = trade.find('currency').text
      amt = trade.find('amount').text
      cost = trade.find('cost').text
      print(str(cur) + " " + str(amt) + " " + str(cost))
    
    return 