import sys
import time
from tkinter import *

class TradeHistUI(Toplevel):
    c = NONE
    fi = NONE
    
    def __init__(self,parent, cid, mid, cr):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        
        self.geometry("400x300+50+50")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(1, weight=3)
                               
        self.c = cr
        
        balance = self.c.balance(cid)
        #hist = self.getHistory(mid)
        orders = self.c.market_orderbook(str(mid), limit=100, otype="both", mine=False)
        buyorders = orders['data']['buyorders']
        sellorders = orders['data']['sellorders']
        
        self.lblAvailable = Label(self)
        self.lblAvailable['text'] = "Available Balance: " + str(balance['data']['available'][str(cid)])
        self.lblAvailable.grid({"row":"0", "column":"0"})
                
        #self.lblType = Label(self)
        #self.lblType['text'] = hist['data'][0]['initiate_ordertype']
        #self.lblType.grid({"row":"1", "column":"0"})
        
        #self.lblPrice = Label(self)
        #self.lblPrice['text'] = "{:.8f}".format(hist['data'][0]['tradeprice'])
        #self.lblPrice.grid({"row":"1", "column":"1"})
             
        self.lblOrderBook = Label(self)
        self.lblOrderBook['text'] = "{:.8f}".format(sellorders[0]['price']) + " @ " + str(sellorders[0]['quantity'])
        self.lblOrderBook.grid({"row":"2", "column":"0"})
        
        self.lblOrderBook = Label(self)
        self.lblOrderBook['text'] = "{:.8f}".format(buyorders[0]['price']) + " @ " + str(buyorders[0]['quantity'])
        self.lblOrderBook.grid({"row":"2", "column":"1"})

        self.Close = Button(self)
        self.Close["text"] = "Close"
        self.Close["fg"] = "red"
        self.Close["command"] = self._quit
        self.Close.grid({"row": "3", "columnspan":"2"})
                       
        return

    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        return
      
    def getHistory(self, mid):
      history = self.c.market_tradehistory(mid, limit=1)
       
      return history

    def _quit(self):
      self.destroy()
      return

