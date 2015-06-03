import sys
import time
from tkinter import *

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mpdates
import matplotlib.finance as mfinance

import numpy as np

from numpy import arange, sin, pi

from finindicator import FinIndicator
from finindicator import FinStrategy

class ChartUI(Toplevel):
    c = NONE
    fi = NONE
    
    def __init__(self,parent, mid, cr):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        
        self.geometry("800x600+50+50")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(1, weight=3)

        self.Close = Button(self)
        self.Close["text"] = "Close"
        self.Close["fg"] = "red"
        self.Close["command"] = self._quit
        self.Close.grid({"row": "3"})
                        
        self.c = cr
        self.fi = FinIndicator()
        self.fs = FinStrategy()
        
        matplotlib.rc('ytick', labelsize=8) 
        
        Prices = self.getPrices(mid)
        
        self.graphFrame(Prices[0],Prices[1], Prices[2], Prices[3], Prices[4])
        
        self.strategyFrame()
        
        return

    def graphFrame(self, op, hp, lp, cp, tp):
        dates = mpdates.datestr2num(tp)
        
        f = Figure(figsize=(9,6), dpi=100)
        
        a = f.add_subplot(411)
        aRSI = f.add_subplot(412, sharex=a)
        aMACD = f.add_subplot(413, sharex=a)
        aSto = f.add_subplot(414, sharex=a)

        a.set_title('Price Action')
                              
        sma = self.fi.calcSMA(cp,25)
        smaSlow = self.fi.calcSMA(cp,50)
        
        if smaSlow[-1] > cp[-1]:
          self.fs.trend = "down"
        else:
          self.fs.trend = "up"
        
        a.plot_date(dates, cp, '-')
        a.plot_date(dates, hp, '-')
        a.plot_date(dates, lp, '-')
        a.plot_date(dates, sma, '-')
        a.plot_date(dates, smaSlow, '-')
        
        fmt = mpdates.DateFormatter('%b %d')
        a.xaxis.set_major_locator(mpdates.DayLocator())
        a.xaxis.set_major_formatter(fmt)
        a.xaxis.set_minor_locator(mpdates.HourLocator())
        a.set_xlim(dates.min(), dates.max())
        
        a.yaxis.set_major_formatter(FormatStrFormatter('%1.6f'))
                
        a.autoscale_view()
        
        rsi = self.fi.calcRSI(cp, 14)
        #print(rsi)
        
        aRSI.set_title('RSI - 14')
        aRSI.xaxis.set_major_locator(mpdates.DayLocator())
        aRSI.xaxis.set_major_formatter(fmt)
        aRSI.xaxis.set_minor_locator(mpdates.HourLocator())
        aRSI.set_xlim(dates.min(), dates.max())
        
        aRSI.plot_date(dates, rsi, '-')
        
        aRSI.set_ylim([0,100])
        aRSI.set_yticks([30,50,70])
        aRSI.set_yticklabels((30,50,70),fontsize="8")
        aRSI.grid(b=TRUE, which='major', color='r', axis='y', linestyle='--')
        #aRSI.set_xticks(ind)
        aRSI.set_xticklabels(tp, fontsize="8", rotation="45", ha="right")
        
        aMACD.set_title('MACD')
        macd = self.calcEMA(cp,12) - self.calcEMA(cp,26)
        macdSignal = self.calcEMA(macd, 9)
        
        aMACD.xaxis.set_major_locator(mpdates.DayLocator())
        aMACD.xaxis.set_major_formatter(fmt)
        aMACD.xaxis.set_minor_locator(mpdates.HourLocator())
        aMACD.set_xlim(dates.min(), dates.max())
        
        aMACD.plot_date(dates, macd, "-")
        aMACD.plot_date(dates, macdSignal, "-")
        
        sto = self.fi.stochastic(hp, lp, cp)
        aSto.set_title('Stochastic')
        
        aSto.xaxis.set_major_locator(mpdates.DayLocator())
        aSto.xaxis.set_major_formatter(fmt)
        aSto.xaxis.set_minor_locator(mpdates.HourLocator())
        aSto.set_xlim(dates.min(), dates.max())
        
        aSto.plot_date(dates, sto[0][0], "-")
        aSto.plot_date(dates, sto[1][0], "-")
                
        f.subplots_adjust(hspace=0.75)
        f.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(f, master=self)
        
        canvas.show()
        
        canvas.get_tk_widget().grid(row="1")
       
        navFrame = Frame(self) 
        navFrame.grid({"row":"2"})
        toolbar = NavigationToolbar2TkAgg(canvas, navFrame)
        toolbar.update()

        return

    def strategyFrame(self):
        self.lbl_frame_strategy = LabelFrame(self)
        self.lbl_frame_strategy["text"] = "Strategy"
        self.lbl_frame_strategy.grid({"row":"1", "column":"1"})
        
        self.lbl_trend = Label(self.lbl_frame_strategy)
        if self.fs.trend == "up":
          self.lbl_trend['text'] = "Buy"
        else:
          self.lbl_trend['text'] = "Sell"
  
        self.lbl_trend.grid({"row":"0","column":"0"})
        return 

    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        return
      
    def getPrices(self, mid):
      ohlc = self.c.market_ohlc(mid, start=0, stop=time.time(), interval="hour", limit=100)

      openPrices = []
      highPrices = []
      lowPrices = []
      closePrices = []
      timePrices = []
      
      for price in reversed(ohlc['data']):
        openPrices.append(price['open'])
        highPrices.append(price['high'])
        lowPrices.append(price['low'])
        closePrices.append(price['close'])
        timePrices.append(price['date'])
        
      return [openPrices, highPrices, lowPrices, closePrices, timePrices]

    def _quit(self):
      self.destroy()
      return
              
    def calcEMA(self, values, period):
      weights = np.exp(np.linspace(-1., 0., period))
      weights /= weights.sum()
      
      a = np.convolve(values, weights)[:len(values)]
      a[:period]=a[period]
            
      return a
    
    def calcStochastic(self):
      return 
