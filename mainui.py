import threading
import datetime
import time

from tkinter import *
from Cryptsy import Cryptsy
from CoinDesk import CoinDesk

from chartui import ChartUI
from tradehistui import TradeHistUI
import matplotlib.finance

from finindicator import FinStrategy


class MainFrame(Frame):
    BIG_FONT = 12
    SMALL_FONT = 8
    
    c = NONE
    lblPointsRSI = NONE
    lblZiftPrice = None
    
    strBTCValue = NONE
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.finish = FALSE
        
        self.pack()
        self.createWidgets()
        
        f = open('keys.txt', 'r')
        pubKey = f.readline().rstrip('\n')
        privKey = f.readline().rstrip('\n')
        f.close()
        
        self.c = Cryptsy(str(pubKey), str(privKey))
        
        self.cd = CoinDesk()
        self.btcPrice = self.cd.getPrice()
        
        self.fs = FinStrategy()
        
        marketData = self.c.markets()
                
        for market in marketData['data']:
          if market['id'] == '473':
            print(market['24hr'])
            ziftLastTrade = market['last_trade']['price']
            self.lblZiftPrice['text'] = "{:.6f}".format(ziftLastTrade)
          elif market['id'] == '120':
            pointsLastTrade = "{:.6f}".format(market['last_trade']['price'])
            self.lblPointsPrice['text'] = pointsLastTrade
          elif market['id'] == '3':
            ltcLastTrade = "{:.6f}".format(market['last_trade']['price'])
            self.lblLTCPrice['text'] = ltcLastTrade
          elif market['id'] == '454':
            xrpLastTrade = "{:.6f}".format(market['last_trade']['price'])
            self.lblXRPPrice['text'] = xrpLastTrade
        
        balances = self.c.balances()
        availableBalance = balances['data']['available']
        heldBalance = balances['data']['held']
        
        ziftValue = availableBalance['275'] * ziftLastTrade
        pointsValue = availableBalance['89'] * float(pointsLastTrade)
        
        self.lblBalBTC["text"] = "Bitcoin: "
        self.lblVolBTC["text"] = str(availableBalance['3'])
        self.lblValBTC["text"] = str(availableBalance['3'])        
        self.lblInvBTC["text"] = str(availableBalance['3'] * self.fs.risk)
        
        self.lblBalXRP["text"] = "Ripple: "
        self.lblVolXRP["text"] = str(availableBalance['2'])
        self.lblValXRP["text"] = str(availableBalance['2'])
        
        self.lblBalLTC["text"] = "Litecoin: "
        self.lblVolLTC["text"] = str(availableBalance['2'])
        self.lblValLTC["text"] = str(availableBalance['2'])        
        
        self.lblBalZift["text"] = "ZiftrCoin: "
        self.lblVolZift['text'] = str(availableBalance['275'])
        self.lblValZift['text'] = str(ziftValue)        
        
        self.lblBalPoints["text"] = "Points: "
        self.lblVolPoints['text'] = str(availableBalance['89'])
        self.lblValPoints['text'] = str(pointsValue)
        
        self.lblBTCValue['text'] = str(self.btcPrice)
        self.lblTotalBal["text"] = "{:.4f}".format(availableBalance['3'] + ziftValue + pointsValue) + " BTC"
        self.lblTotalVal["text"] = "{:.2f}".format((availableBalance['3'] + ziftValue + pointsValue) * self.btcPrice)  + " GBP"
        
        #self.updateThread = threading.Thread(target= self.update)
        #self.updateThread.start()
        return

    def createWidgets(self):
        # Markets
        self.coins_marketFrame()
                        
        # Balances        
        self.coins_balFrame()
        
        # Values
        self.total_balFrame()
        
        # Quit Button
        self.QUIT = Button(self)
        self.QUIT["text"] = "Update"
        self.QUIT["command"] = self.update
        self.QUIT.grid({"row": "50", "column": "0"})
        
        # Quit Button
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.exit
        self.QUIT.grid({"row": "50", "column":"2", "columnspan": "2"})

        return
      
    def coins_marketFrame(self):
        self.marketsLblFrame = LabelFrame(self)
        self.marketsLblFrame["text"] = "Markets"
        self.marketsLblFrame.grid({"row": "0", "column":"0", "columnspan":"3"})
        
        self.lblXRP = Label(self.marketsLblFrame)
        self.lblXRP["text"] = "Ripple"
        self.lblXRP.grid({"row": "0"})
        
        self.lblXRPPrice = Label(self.marketsLblFrame)
        self.lblXRPPrice["text"] = "Price: xx" 
        self.lblXRPPrice.grid({"row": "0", "column":"1"})

        self.btnXRPChart = Button(self.marketsLblFrame)
        self.btnXRPChart["text"] = "Chart"
        self.btnXRPChart["command"] = lambda: self.Chart(454)
        self.btnXRPChart.grid({"row": "0", "column":"2"})
        
        self.lblLTC = Label(self.marketsLblFrame)
        self.lblLTC["text"] = "Litecoin"
        self.lblLTC.grid({"row": "1"})
        
        self.lblLTCPrice = Label(self.marketsLblFrame)
        self.lblLTCPrice["text"] = "Price: xx" 
        self.lblLTCPrice.grid({"row": "1", "column":"1"})

        self.btnLTCChart = Button(self.marketsLblFrame)
        self.btnLTCChart["text"] = "Chart"
        self.btnLTCChart["command"] = lambda: self.Chart(3)
        self.btnLTCChart.grid({"row": "1", "column":"2"})
        
        self.lblZift = Label(self.marketsLblFrame)
        self.lblZift["text"] = "ZiftrCoin"
        self.lblZift.grid({"row": "2"})
        
        self.lblZiftPrice = Label(self.marketsLblFrame)
        self.lblZiftPrice["text"] = "Price: xx" 
        self.lblZiftPrice.grid({"row": "2", "column":"1"})

        self.btnZiftChart = Button(self.marketsLblFrame)
        self.btnZiftChart["text"] = "Chart"
        self.btnZiftChart["command"] = lambda: self.Chart(473)
        self.btnZiftChart.grid({"row": "2", "column":"2"})
        
        self.btnZiftChart = Button(self.marketsLblFrame)
        self.btnZiftChart["text"] = "Trade History"
        self.btnZiftChart["command"] = lambda: self.TradeHist(473)
        self.btnZiftChart.grid({"row": "2", "column":"3"})

        self.lblPoints = Label(self.marketsLblFrame)
        self.lblPoints["text"] = "Points"
        self.lblPoints.grid({"row": "3"})
        
        self.lblPointsPrice = Label(self.marketsLblFrame)
        self.lblPointsPrice["text"] = "Price: xx"
        self.lblPointsPrice.grid({"row": "3", "column":"1"})
  
        self.btnZiftChart = Button(self.marketsLblFrame)
        self.btnZiftChart["text"] = "Chart"
        self.btnZiftChart["command"] = lambda: self.Chart(120)
        self.btnZiftChart.grid({"row": "3", "column":"2"})
                
        return 
      
    def total_balFrame(self):
        self.balLblFrame = LabelFrame(self)
        self.balLblFrame["text"] = "Total Value"
        self.balLblFrame.grid({"row": "30", "column":"0", "columnspan":"3"})
                
        self.lblTotalBal = Label(self.balLblFrame)
        self.lblTotalBal["text"] = ""
        self.lblTotalBal.grid({"row": "0", "column":"1"})
        
        self.lblBTCValue = Label(self.balLblFrame)
        self.lblBTCValue['text'] = '0'
        self.lblBTCValue.grid({"row": "1", "column":"0"})
        
        self.lblTotalVal = Label(self.balLblFrame)
        self.lblTotalVal["text"] = ""
        self.lblTotalVal["fg"] = "green"
        self.lblTotalVal.grid({"row": "1", "column":"1"})
                
        return 

    def coins_balFrame(self):
        self.coinsbalLblFrame = LabelFrame(self)
        self.coinsbalLblFrame["text"] = "Coin Balances"
        self.coinsbalLblFrame["font"] = self.BIG_FONT
        self.coinsbalLblFrame.grid({"row": "20", "column": "0", "columnspan":"3"})
                
        self.lblHdrCurrency = Label(self.coinsbalLblFrame)
        self.lblHdrCurrency["text"] = "Currency"
        self.lblHdrCurrency.grid({"row": "1", "column":"0"})
        
        self.lblHdrVolume = Label(self.coinsbalLblFrame)
        self.lblHdrVolume["text"] = "Volume"
        self.lblHdrVolume.grid({"row": "1", "column":"1"})
        
        self.lblHdrValue = Label(self.coinsbalLblFrame)
        self.lblHdrValue["text"] = "Value"
        self.lblHdrValue.grid({"row": "1", "column":"2"})
        
        self.lblHdrInvestable = Label(self.coinsbalLblFrame)
        self.lblHdrInvestable["text"] = "Investable"
        self.lblHdrInvestable.grid({"row": "1", "column":"3"})

        self.lblBalBTC = Label(self.coinsbalLblFrame)
        self.lblBalBTC["text"] = "Bitcoins"
        self.lblBalBTC.grid({"row": "2", "column":"0"})
        
        self.lblVolBTC = Label(self.coinsbalLblFrame)
        self.lblVolBTC["text"] = ""
        self.lblVolBTC.grid({"row": "2", "column":"1"})
        
        self.lblValBTC = Label(self.coinsbalLblFrame)
        self.lblValBTC["text"] = ""
        self.lblValBTC.grid({"row": "2", "column":"2"})
        
        self.lblInvBTC = Label(self.coinsbalLblFrame)
        self.lblInvBTC["text"] = ""
        self.lblInvBTC.grid({"row": "2", "column":"3"})

        self.lblBalXRP = Label(self.coinsbalLblFrame)
        self.lblBalXRP["text"] = "Ripple"
        self.lblBalXRP.grid({"row": "3", "column":"0"})
        
        self.lblVolXRP = Label(self.coinsbalLblFrame)
        self.lblVolXRP["text"] = ""
        self.lblVolXRP.grid({"row": "3", "column":"1"})
        
        self.lblValXRP = Label(self.coinsbalLblFrame)
        self.lblValXRP["text"] = ""
        self.lblValXRP.grid({"row": "3", "column":"2"})

        self.lblBalLTC = Label(self.coinsbalLblFrame)
        self.lblBalLTC["text"] = "Litecoins"
        self.lblBalLTC.grid({"row": "4", "column":"0"})
        
        self.lblVolLTC = Label(self.coinsbalLblFrame)
        self.lblVolLTC["text"] = ""
        self.lblVolLTC.grid({"row": "4", "column":"1"})
        
        self.lblValLTC = Label(self.coinsbalLblFrame)
        self.lblValLTC["text"] = ""
        self.lblValLTC.grid({"row": "4", "column":"2"})


        self.lblBalZift = Label(self.coinsbalLblFrame)
        self.lblBalZift["text"] = "ZiftrCoin"
        self.lblBalZift.grid({"row": "5", "column":"0"})
        
        self.lblVolZift = Label(self.coinsbalLblFrame)
        self.lblVolZift["text"] = ""
        self.lblVolZift.grid({"row": "5", "column":"1"})
        
        self.lblValZift = Label(self.coinsbalLblFrame)
        self.lblValZift["text"] = ""
        self.lblValZift.grid({"row": "5", "column":"2"})
                
        self.lblBalPoints = Label(self.coinsbalLblFrame)
        self.lblBalPoints["text"] = "Points"
        self.lblBalPoints.grid({"row": "6", "column":"0"})
        
        self.lblVolPoints = Label(self.coinsbalLblFrame)
        self.lblVolPoints["text"] = ""
        self.lblVolPoints.grid({"row": "6", "column":"1"})
        
        self.lblValPoints = Label(self.coinsbalLblFrame)
        self.lblValPoints["text"] = ""
        self.lblValPoints.grid({"row": "6", "column":"2"})
        return 

    def Chart(self, mid):
      chart = ChartUI(self,mid,self.c)
      return
    
    def TradeHist(self, mid):
      trad_hist = TradeHistUI(self,mid,self.c)
      return

    def update(self):
      #while not self.finish:
      print("Updating Market Data")
      marketData = self.c.markets()
        
      for market in marketData['data']:
          #print(market)
        if market['id'] == '473':
          self.lblZiftPrice['text'] = "{:.6f}".format(market['last_trade']['price'])
        elif market['id'] == '120':
          self.lblPointsPrice['text'] = "{:.6f}".format(market['last_trade']['price'])
            
      #time.sleep(10)
      return 
    
    def exit(self):
      self.finish = TRUE
      #self.updateThread.join()
      self.quit()
      return
    
    def getClosePrices(self, mid):
      ohlc = self.c.market_ohlc(mid, start=0, stop=time.time(), interval="hour", limit=14)

      closePrices = []

      for price in reversed(ohlc['data']):
        closePrices.append(price['close'])
        
      return closePrices
    
    def getSpread(self, mid):
      spread = 0
      
      bid = self.c.market_orderbook(mid, 1, "buy")              
      ask = self.c.market_orderbook(mid, 1, "sell")
      
      spread = ask - bid
      
      return spread
    
    def calcRSI(self, cp): 
      gains = 0
      iGains = 0
      losses = 0
      iLosses = 0

      for i in range(1, len(cp)):
        if cp[i] > cp[i-1]:
            gains += cp[i] - cp[i-1]
            iGains += 1
        elif cp[i] < cp[i-1]:
            losses += cp[i-1] - cp[i]
            iLosses += 1

      rs = (gains / iGains) / (losses / iLosses)

      RSI = 100 - 100/(1+rs)
    
      return RSI
    
    def calcEMA(self, curPrice, periods, prevEMA):
      k = 2/(periods + 1)
      (curPrice * k) + (prevEMA * (1- k))
      return 