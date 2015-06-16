import sys
import time
from tkinter import *

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mpdates
import numpy as np

class MarketOverviewUI(Toplevel):
    c = NONE
    fi = NONE
    
    def __init__(self,parent, cr):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        
        self.geometry("800x600+50+50")
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.rowconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(1, weight=3)
        
        self.createWidgets()
        
        self.c = cr
        
        data = self.getData()
        
        self.update(data)
        
        self.graph(data)                
        
        
        self.Close = Button(self)
        self.Close["text"] = "Close"
        self.Close["fg"] = "red"
        self.Close["command"] = self._quit
        self.Close.grid({"row": "5", "columnspan":"2"})
                       
        return
      
    def createWidgets(self):
      
      return 

    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        return
      
    def getData(self):
      data = self.c.market_ohlc(2,interval="day")
             
      return data
    
    def update(self, data):
      return
    
    def graph(self, data):
      f = Figure(figsize=(6,4), dpi=100)
        
      a = f.add_subplot(111)
      a.set_title('Current Orders')
            
      soq = []
      sop = []
      for order in data[2][:10]:
       soq.append(order['quantity'])
       sop.append(order['price'])

      boq = []
      bop = []
      for order in data[1][:10]:
        boq.append(order['quantity'])
        bop.append(order['price'])
             
      a.set_xlim([min(bop),max(sop)])
      
      #a.scatter(bop, boq, color="green")
      #a.scatter(sop, soq, color="red")
      
      #values, base = np.histogram(data, bins=10)
      #evaluate the cumulative
      cumSell = np.cumsum(soq)
      cumBuy = np.cumsum(boq)
      # plot the cumulative function
      a.plot(sop, cumSell, c='red')
      a.fill_between(sop, 0, cumSell, where=cumSell>=0, facecolor='red', interpolate=True)
      
      a.plot(bop, cumBuy, c='green')
      a.fill_between(bop, 0, cumBuy, where=cumBuy>=0, facecolor='green', interpolate=True)
      
      for tick in a.xaxis.get_major_ticks():
        tick.label.set_fontsize(8) 
        tick.label.set_rotation(15) 
                   
      canvas = FigureCanvasTkAgg(f, master=self)
        
      canvas.show()
        
      canvas.get_tk_widget().grid({"row":"0", "columnspan":"2"})
       
      navFrame = Frame(self) 
      navFrame.grid({"row":"1", "columnspan":"2"})
      toolbar = NavigationToolbar2TkAgg(canvas, navFrame)
      toolbar.update()
        
      return

    def _quit(self):
      self.destroy()
      return

