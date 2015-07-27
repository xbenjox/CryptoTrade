from tkinter import *

import matplotlib
import numpy as np

from os import listdir
from os.path import isfile, join

from lxml import etree as ET

import math

class DataUI(Toplevel):
  markets = list()
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
                  t: str): 
    root = self.tree.getroot()
    
    for market in root.findall('market'):
      #print(mid)
      #print(market.get('id'))
      
      if market.get('id') == str(mid):
        data = self.c.market_ohlc(mid, interval=t, )
        
        #clear old data
        for time in market.findall('time'):
          market.remove(time)
          
        for sample in data['data']:
          print(sample)
          date = sample['date']
          timestamp = sample['timestamp']
          high = sample['high']
          low = sample['low']
          open = sample['open']
          close = sample['close']
          volume = sample['volume']
          
          element = ET.Element('date')
          element.set('date', date)
                    
          ET.SubElement(element, 'timestamp').text = str(timestamp)
          
          ET.SubElement(element, 'high').text = str(high)
          
          ET.SubElement(element, 'low').text = str(low)
          
          ET.SubElement(element, 'open').text = str(open)
          
          ET.SubElement(element, 'close').text = str(close)
          
          ET.SubElement(element, 'volume').text = str(volume)
          
          market.append(element)
    
    self.tree.write('Data/Markets/markets_day_hist.xml', pretty_print=True)
    return

  def get_history_xml(self):
    parser = ET.XMLParser(remove_blank_text=True)
    
    self.tree = ET.parse('Data/Markets/markets_day_hist.xml', parser)
    
    root = self.tree.getroot()
    
    for market in root.findall('market'): 
      print(market.get('label'))
      
    return 
  