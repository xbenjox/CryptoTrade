from tkinter import *

class CapitalUI(Toplevel):
  def __init__(self, parent):
    Toplevel.__init__(self, parent)
    self.transient(parent)
        
    self.geometry("800x600+50+50")
        
    self.createWidgets()

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
      
  def _quit(self):
    self.destroy()
    return

