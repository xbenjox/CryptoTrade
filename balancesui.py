from tkinter import *

import xml.etree.ElementTree as ET

import math

class BalanceUI(Toplevel):
  def __init__(self, parent, bal):
    Toplevel.__init__(self, parent)
           
    self.balances = bal
    
    self.transient(parent)
        
    self.geometry("800x600+50+50")
      
    self.createWidgets()    
    self.updateWidgets()                       
    return
      
  def createWidgets(self):
    self.lblTrades = Label(self)
    self.lblTrades['text'] = "Trades"
    self.lblTrades.grid({"row":"0"})
        
    self.Close = Button(self)
    self.Close["text"] = "Close"
    self.Close["fg"] = "red"
    self.Close["command"] = self._quit
    self.Close.grid({"row": "5", "columnspan":"1"})
    
    return 
  
  def updateWidgets(self):
   
    
    tradeText = ""
    
    dogePL = 0 
    dogePLQty = 0
    
    xrpPL = 0
    xrpPLQty = 0
    
          
    self.lblDogePL['text'] = "Profit/Loss: " + str(dogePL)
    self.lblXRPPL['text'] = "Profit/Loss: " + str(xrpPL)
   
    # Calculate required price for profit
    
    if dogePL < 0:
      posDogePL = dogePL * -1
      reqp = (posDogePL + ( posDogePL * 0.025 )) / dogePLQty
    else:
      reqp = 0
      
    reqp = math.ceil(reqp * 100000000) / 100000000
    
    if xrpPL < 0:
      posXRPPL = xrpPL * -1
      reqXRPp = (posXRPPL + (posXRPPL * 0.025)) / xrpPLQty
    else:
      reqXRPp = 0
    
    reqXRPp = math.ceil(reqXRPp * 100000000) / 100000000
      
    # Calculate current PL
    print(self.last_trade_prices['DOGE/BTC'])
    
    self.lblDogeCurPL['text'] = "Current PL: " + "{:.8f}".format(dogePL + ((self.last_trade_prices['DOGE/BTC'] * dogePLQty) - (self.last_trade_prices['DOGE/BTC'] * dogePLQty * 0.025)))
    self.lblXRPCurPL['text'] = "Current PL: " + "{:.8f}".format(xrpPL + ((self.last_trade_prices['XRP/BTC'] * xrpPLQty) - (self.last_trade_prices['XRP/BTC'] * xrpPLQty * 0.025)))
        
    self.lblDogeReqP['text'] = "{:.8f}".format(reqp)
    self.lblXRPReqP['text'] = "{:.8f}".format(reqXRPp)
    
    self.lblTrades['text'] = tradeText
    
    return 

  def on_key_event(self, event):
    print('you pressed %s'%event.key)
    return
      
  def _quit(self):
    self.destroy()
    return

 
  
