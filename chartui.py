import sys
import time
from tkinter import *
from tkinter import ttk

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
    fs = NONE
    
    def __init__(self,parent, mid, cr, fs):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        
        self.geometry("800x600+50+50")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(1, weight=3)


        self.timescale = StringVar()                
        self.comboTime = ttk.Combobox(self, textvariable=self.timescale)
        self.comboTime['values'] = ('minute', 'hour', 'day')
        self.comboTime.current(1)
        self.comboTime.bind('<<ComboboxSelected>>', self.timeSelect)
        self.comboTime.grid({"row":"0"})
        
        self.Close = Button(self)
        self.Close["text"] = "Close"
        self.Close["fg"] = "red"
        self.Close["command"] = self._quit
        self.Close.grid({"row": "3"})
        
        self.mid = mid
        
        self.c = cr
        self.fi = FinIndicator()
        self.fs = fs
        
        matplotlib.rc('ytick', labelsize=8) 
        
        Prices = self.getPrices("hour")
        self.dates = mpdates.datestr2num(Prices[4])
        self.lblDates = Prices[4]
        self.op = Prices[0]
        self.hp = Prices[1]
        self.lp = Prices[2]
        self.cp = Prices[3]
        
        fractals = self.getFractals(self.hp)
        if len(fractals) > 0:
          self.last_high_fractal = self.hp[fractals[-1]]
        
          self.fs.sellPoints.append(self.last_high_fractal)
        
        self.graphFrame()
        
        self.strategyFrame()
        
        return

    def graphFrame(self):
                
        f = Figure(figsize=(9,6), dpi=100)
        
        self.a = f.add_subplot(411)
        aRSI = f.add_subplot(412, sharex=self.a)
        aMACD = f.add_subplot(413, sharex=self.a)
        aSto = f.add_subplot(414, sharex=self.a)

        self.a.set_title('Price Action')
                              
        sma = self.fi.calcSMA(self.cp,25)
        smaSlow = self.fi.calcSMA(self.cp,50)
        
        if smaSlow[-1] > self.cp[-1]:
          self.fs.trend = "down"
        else:
          self.fs.trend = "up"
        
        self.a.plot_date(self.dates, self.cp, '-')
        #self.a.plot_date(self.dates, self.hp, '-')
        #self.a.plot_date(self.dates, self.lp, '-')
        self.a.plot_date(self.dates, sma, '-')
        self.a.plot_date(self.dates, smaSlow, '-')
        
        #if self.last_high_fractal != NONE:
        #  self.a.plot(self.last_high_fractal, '--')
        
        
        
        fmt = mpdates.DateFormatter('%b %d')
        self.a.xaxis.set_major_locator(mpdates.DayLocator())
        self.a.xaxis.set_major_formatter(fmt)
        self.a.xaxis.set_minor_locator(mpdates.HourLocator())
        self.a.set_xlim(self.dates.min(), self.dates.max())
        
        self.a.yaxis.set_major_formatter(FormatStrFormatter('%1.6f'))
                
        self.a.autoscale_view()
        
        #print(cp)
        
        rsi = self.fi.calcRSI(self.cp, 14)
        #print(rsi)
        
        aRSI.set_title('RSI - 14')
        aRSI.xaxis.set_major_locator(mpdates.DayLocator())
        aRSI.xaxis.set_major_formatter(fmt)
        aRSI.xaxis.set_minor_locator(mpdates.HourLocator())
        aRSI.set_xlim(self.dates.min(), self.dates.max())
        
        aRSI.plot_date(self.dates, rsi, '-')
        
        aRSI.set_ylim([0,100])
        aRSI.set_yticks([30,50,70])
        aRSI.set_yticklabels((30,50,70),fontsize="8")
        aRSI.grid(b=TRUE, which='major', color='r', axis='y', linestyle='--')
        #aRSI.set_xticks(ind)
        aRSI.set_xticklabels(self.lblDates, fontsize="8", rotation="45", ha="right")
        
        aMACD.set_title('MACD')
        macd = self.calcEMA(self.cp,12) - self.calcEMA(self.cp,26)
        macdSignal = self.calcEMA(macd, 9)
        
        aMACD.xaxis.set_major_locator(mpdates.DayLocator())
        aMACD.xaxis.set_major_formatter(fmt)
        aMACD.xaxis.set_minor_locator(mpdates.HourLocator())
        aMACD.set_xlim(self.dates.min(), self.dates.max())
        
        aMACD.plot_date(self.dates, macd, "-")
        aMACD.plot_date(self.dates, macdSignal, "-")
        
        sto = self.fi.stochastic(self.hp, self.lp, self.cp)
        aSto.set_title('Stochastic')
        
        aSto.xaxis.set_major_locator(mpdates.DayLocator())
        aSto.xaxis.set_major_formatter(fmt)
        aSto.xaxis.set_minor_locator(mpdates.HourLocator())
        aSto.set_xlim(self.dates.min(), self.dates.max())
        
        aSto.plot_date(self.dates, sto[0][0], "-")
        aSto.plot_date(self.dates, sto[1][0], "-")
                
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
      
    def getPrices(self, ts):      
      print("Getting " + ts + " prices")
      
      if ts == "day":
        ohlc = self.c.market_ohlc(self.mid, start=0, stop=time.time(), interval=ts, limit=60)
      else:
        ohlc = self.c.market_ohlc(self.mid, start=0, stop=time.time(), interval=ts, limit=100)

      #print(ohlc)

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
    
    def timeSelect(self, event):
      ts = event.widget.get()
      
      prices = self.getPrices(ts)
      self.op = prices[0]
      self.hp = prices[1]
      self.lp = prices[2]
      self.cp = prices[3]
      self.tp = prices[4]
      
      self.dates = mpdates.datestr2num(self.tp)
      
      self.graphFrame()
        
      return
    
    def getFractals(self, data):
      fractals = []
            
      for x in range(2, len(data)-3):
        if data[x] > data[x-2] and data[x] > data[x-1] and data[x] > data[x+1] and data[x] > data[x+2]:
          fractals.append(x)

      return fractals
