from tkinter import *

import matplotlib
import numpy as np

from os import listdir
from os.path import isfile, join

import xml.etree.ElementTree as ET

import math

class DataUI(Toplevel):
  doge_data = list()
  
  def __init__(self, parent, c_api):
    Toplevel.__init__(self, parent)
    
    self.c = c_api
    
    self.transient(parent)
        
    self.geometry("800x600+50+50")
        
    self.get_history_xml()
    
    self.createWidgets()
    
    self.updateWidgets()
                       
    return
      
  def createWidgets(self):
    self.lblDogeData = Label(self)
    self.lblDogeData['text'] = "Doge Data"
    self.lblDogeData.grid({"row":"1"})
    
    self.btnDogeCollect = Button(self)
    self.btnDogeCollect['text'] = "Collect Data"
    self.btnDogeCollect['command'] = lambda: self.CollectData(132, "day")
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

  def CollectData(self, 
                  mid: int, 
                  t): 
    root = self.tree.getroot()
    
    for market in root.findall('market'):
      print(mid)
      print(market.get('id'))
      if market.get('id') is str(mid):
        data = self.c.market_ohlc(mid, interval=t, )
    
        print(data)
    
        for sample in data['data']:
          print(sample)
          date = sample['date']
          timestamp = sample['timestamp']
          high = sample['high']
          low = sample['low']
          open = sample['open']
          close = sample['close']
          volume = sample['volume']
      
    return

  def get_history_xml(self):
    self.tree = ET.parse('Data/Markets/markets_day_hist.xml')
    
    root = self.tree.getroot()
    
    for market in root.findall('market'):
      print(market.get('label'))
      
    return 
  