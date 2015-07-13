from tkinter import *

import xml.etree.ElementTree as ET

import math

class CapitalUI(Toplevel):
  def __init__(self, parent, c_api, last_trade_prices):
    Toplevel.__init__(self, parent)
    
    self.c = c_api
    self.last_trade_prices = last_trade_prices
    
    self.transient(parent)
        
    self.geometry("800x600+50+50")
    
    self.get_history_xml()
    
    self.createWidgets()
    
    self.updateWidgets()
                       
    return
      
  def createWidgets(self):
    self.lblTrades = Label(self)
    self.lblTrades['text'] = "Trades"
    self.lblTrades.grid({"row":"0"})
    
    self.lblFrameDoge = LabelFrame(self)
    self.lblFrameDoge['text'] = "Dogecoin"
    self.lblFrameDoge.grid({"row":"1"})
    
    self.lblDogeCap = Label(self.lblFrameDoge)
    self.lblDogeCap.grid({"row":"0"})
    
    self.lblDogePL = Label(self.lblFrameDoge)
    self.lblDogePL.grid({"row":"15"})

    self.lblDogeReqP = Label(self.lblFrameDoge)
    self.lblDogeReqP.grid({"row":"15", "column":"1"})
    
    self.lblDogeCurPL = Label(self.lblFrameDoge)
    self.lblDogeCurPL.grid({"row":"16"})
    
    self.lblFrameXRP = LabelFrame(self)
    self.lblFrameXRP['text'] = "Ripple"
    self.lblFrameXRP.grid({"row":"2"})
    
    self.lblXRPCap = Label(self.lblFrameXRP)
    self.lblXRPCap.grid({"row":"0"})
    
    self.lblXRPPL = Label(self.lblFrameXRP)
    self.lblXRPPL.grid({"row":"15"})

    self.lblXRPReqP = Label(self.lblFrameXRP)
    self.lblXRPReqP.grid({"row":"15", "column":"1"})
    
    self.lblXRPCurPL = Label(self.lblFrameXRP)
    self.lblXRPCurPL.grid({"row":"16"})
    
    self.Close = Button(self)
    self.Close["text"] = "Close"
    self.Close["fg"] = "red"
    self.Close["command"] = self._quit
    self.Close.grid({"row": "5", "columnspan":"1"})
    
    return 
  
  def updateWidgets(self):
    trades = self.get_trades()
    
    tradeText = ""
    
    dogePL = 0 
    dogePLQty = 0
    
    xrpPL = 0
    xrpPLQty = 0
    
    for trade in trades['data']:
      if trade['marketid'] == "132":
        self.lblDogeCap['text'] = "Type: " + trade['initiate_ordertype'] + " Quantity: " + str(trade['quantity']) + " Price: " + str(trade['total']) + " Fee: " + str(trade['fee']) + "."
        
        if trade['initiate_ordertype'] == "Buy":
          dogePL -= (trade['total'] + trade['fee'])
          dogePLQty += trade['quantity']
        elif trade['initiate_ordertype'] == "Sell":
          dogePL += (trade['total'] - trade['fee'])
          dogePLQty -= trade['quantity']
        
        print(trade)
      if trade['marketid'] == "454":
        
        
        if trade['initiate_ordertype'] == "Buy":
          xrpPL -= (trade['total'] + trade['fee'])
          xrpPLQty += trade['quantity']
        elif trade['initiate_ordertype'] == "Sell":
          xrpPL += (trade['total'] - trade['fee'])
          xrpPLQty -= trade['quantity']
        
        self.lblXRPCap['text'] = "Type: " + trade['initiate_ordertype'] + " Quantity: " + str(trade['quantity']) + " Price: " + str(trade['total']) + " Fee: " + str(trade['fee']) + "."
        
        print(trade)
      else:
        tradeText += trade['orderid'] + "\n"
      
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

  def get_trades(self):
    trade_hist = self.c.tradehistory()
        
    #for x in range(0, len(trade_hist['data'])):
    #  print(trade_hist['data'][x])
      
    
    return trade_hist
  
  def get_history_xml(self):
    tree = ET.parse('./Data/sellpoints.xml')
    
    root = tree.getroot()
    
    for trade in root.findall('trade'):
      cur = trade.find('currency').text
      amt = trade.find('amount').text
      cost = trade.find('cost').text
      print(str(cur) + " " + str(amt) + " " + str(cost))
    
    return 