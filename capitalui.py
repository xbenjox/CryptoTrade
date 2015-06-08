from tkinter import *

import xml.etree.ElementTree as ET

import math

class CapitalUI(Toplevel):
  def __init__(self, parent, c_api):
    Toplevel.__init__(self, parent)
    
    self.c = c_api
    
    self.transient(parent)
        
    self.geometry("800x600+50+50")
    
    self.get_history_xml()
    
    #self.get_trades()
    
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
      else:
        tradeText += trade['orderid'] + "\n"
      
    self.lblDogePL['text'] = "Profit/Loss: " + str(dogePL)
   
    # Calculate required price for profit
    if dogePL < 0:
      posDogePL = dogePL * -1
      reqp = (posDogePL + ( posDogePL * 0.025 )) / dogePLQty
    else:
      reqp = 0
      
      reqp = math.ceil(reqp * 100000000) / 100000000
    
    self.lblDogeReqP['text'] = "{:.8f}".format(reqp)
    
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
    tree = ET.parse('sellpoints.xml')
    
    root = tree.getroot()
    
    for trade in root.findall('trade'):
      cur = trade.find('currency').text
      amt = trade.find('amount').text
      cost = trade.find('cost').text
      print(str(cur) + " " + str(amt) + " " + str(cost))
    
    return 