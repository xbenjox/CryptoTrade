import threading
import time
from tkinter import *

from mainui import MainFrame

#def DataCollect():
#  while not finish:
#    print("Collecting Data")
#    time.sleep(3)
#  return 
 
#finish = FALSE
#Process = threading.Thread(target=DataCollect)
#Process.start()
   
root = Tk()
mg = MainFrame(master=root)
mg.mainloop()
finish = TRUE
#Process.join()