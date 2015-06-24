import sys
import time
from tkinter import *

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches
import matplotlib.dates as mpdates
import numpy as np

class MarketOverviewUI(Toplevel):
    c = NONE
    fi = NONE
    
    def __init__(self,parent, cr, markets):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        
        self.geometry("800x600+50+50")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.markets = markets
        
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
      data = []
      for market in self.markets:
        print("Getting data for :" + str(market))
        market_data = self.c.market_ohlc(market,interval="day")
             
        data.append(market_data['data'])
        
      return data
    
    def update(self, data):
      return
    
    def graph(self, data):
      
      print(data)
      
      
        
      
      f = Figure(figsize=(6,4), dpi=100)
        
      a = f.add_subplot(111)
      a.set_title('Market Overview')
             
      #a.set_xlim([min(bop),max(sop)])
      colours = ['red', 'blue', 'green', 'yellow', 'cyan', 'black' ]
      mLabels=['ZiftrCoins','Points','LiteCoin','Ripple','Dogecoin','Dash']
      legHandles = []
      
      # format data
      counter = 0
      for d in data:
        print(d)
        cp = []
        for p in d:
          cp.append(p['close'])
        
        npcp = np.array(cp)
        revnpcp = list(reversed(npcp))
        percdiff = revnpcp / revnpcp[0] * 100.
        adjprice = revnpcp - revnpcp[0]
        
        p = a.plot(percdiff, label=mLabels[counter], color=colours[counter])
        legHandles.append(mpatches.Patch(color=colours[counter], label=colours[counter]))
        
        counter += 1
      
      a.legend(handles=legHandles, labels=['ZiftrCoins','Points','LiteCoin','Ripple','Dogecoin','Dash'], loc='upper left', prop={'size':8})
      
      for tick in a.xaxis.get_major_ticks():
        tick.label.set_fontsize(8) 
        tick.label.set_rotation(15) 
                   
      canvas = FigureCanvasTkAgg(f, master=self)
      
      canvas.show()
        
      canvas.get_tk_widget().grid({"row":"0", "columnspan":"2", "sticky":"NSEW"})
       
      navFrame = Frame(self) 
      navFrame.grid({"row":"1", "columnspan":"2"})
      toolbar = NavigationToolbar2TkAgg(canvas, navFrame)
      toolbar.update()
        
      return

    def _quit(self):
      self.destroy()
      return

