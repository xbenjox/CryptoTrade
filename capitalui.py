from tkinter import *

class CapitalUI(Toplevel):
  def __init__(self, parent, c_api):
    Toplevel.__init__(self, parent)
    
    self.c = c_api
    
    self.transient(parent)
        
    self.geometry("800x600+50+50")
    
    self.get_trades()
    
    self.createWidgets()
                       
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

  def on_key_event(self, event):
    print('you pressed %s'%event.key)
    return
      
  def _quit(self):
    self.destroy()
    return

  def get_trades(self):
    trade_hist = self.c.tradehistory()
        
    for x in range(0, len(trade_hist['data'])):
      print(trade_hist['data'][x])
      
    
    return 