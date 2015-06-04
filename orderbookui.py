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

class TradeHistUI(Toplevel):
    c = NONE
    fi = NONE
    
    def __init__(self,parent, cid, mid, cr):
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
        
        data = self.getData(mid, cid)
        
        self.update(data, cid)
        
        self.graph(data)                
        
        
        self.Close = Button(self)
        self.Close["text"] = "Close"
        self.Close["fg"] = "red"
        self.Close["command"] = self._quit
        self.Close.grid({"row": "5", "columnspan":"2"})
                       
        return
      
    def createWidgets(self):
      self.lblAvailable = Label(self)
      self.lblAvailable.grid({"row":"2", "column":"0"})
      
      self.frmSellOrders = LabelFrame(self)
      self.frmSellOrders['text'] = "Sell Orders"
      self.frmSellOrders.grid({"row":"3", "column":"0"})
      
      self.lblSellOrderBook = Label(self)
      self.lblSellOrderBook.grid({"row":"4", "column":"0"})
      
      self.lblBuyOrderBook = Label(self)
      self.lblBuyOrderBook.grid({"row":"4", "column":"1"})
      
      return 

    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        return
      
    def getData(self, mid, cid):
      balance = self.c.balance(cid)
      orders = self.c.market_orderbook(str(mid), limit=100, otype="both", mine=False)
      buyorders = orders['data']['buyorders']
      sellorders = orders['data']['sellorders']
             
      return [balance, buyorders, sellorders]
    
    def update(self, data, cid):
      self.lblAvailable['text'] = "Available Balance: " + str(data[0]['data']['available'][str(cid)])
      
      sSellOrders = ""
      for order in data[2][:10]:
        sSellOrders += str(order['quantity']) + " @ " + "{:.8f}".format(order['price']) + "\n"

      sBuyOrders = ""
      for order in data[1][:10]:
        sBuyOrders += str(order['quantity']) + " @ " + "{:.8f}".format(order['price']) + "\n"
      
      self.lblSellOrderBook['text'] = sSellOrders
      self.lblBuyOrderBook['text'] = sBuyOrders
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
      
      
      a.scatter(bop, boq, color="green")
      a.scatter(sop, soq, color="red")
      #a.bar(x+10, soq)
      #a.plot(so[1], so[0])
      #a.plot(bo[1], bo[0])
      
      
      
      
                   
      canvas = FigureCanvasTkAgg(f, master=self)
        
      canvas.show()
        
      canvas.get_tk_widget().grid(row="0")
       
      navFrame = Frame(self) 
      navFrame.grid({"row":"1", "columnspan":"2"})
      toolbar = NavigationToolbar2TkAgg(canvas, navFrame)
      toolbar.update()
        
      return

    def _quit(self):
      self.destroy()
      return

