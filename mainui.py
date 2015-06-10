import threading
import datetime
import time

from tkinter import *
from Cryptsy import Cryptsy
from CoinDesk import CoinDesk

from chartui import ChartUI
from orderbookui import TradeHistUI
from capitalui import CapitalUI

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
        
        self.master.title("Cryto Currency Trader.")
        
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
          
        self.last_trade_prices = {}
        for market in marketData['data']:
          self.last_trade_prices[market['label']] = market['last_trade']['price']
          if market['id'] == '473':
            #print(market['24hr'])
            ziftLastTrade = market['last_trade']['price']
            self.lblZiftPrice['text'] = "{:.8f}".format(ziftLastTrade)
          elif market['id'] == '120':
            pointsLastTrade = "{:.8f}".format(market['last_trade']['price'])
            self.lblPointsPrice['text'] = pointsLastTrade
          elif market['id'] == '3':
            ltcLastTrade = "{:.8f}".format(market['last_trade']['price'])
            self.lblLTCPrice['text'] = ltcLastTrade
          elif market['id'] == '454':
            xrpLastTrade = "{:.8f}".format(market['last_trade']['price'])
            self.lblXRPPrice['text'] = xrpLastTrade
          elif market['id'] == '132':
            dogeLastTrade = "{:.8f}".format(market['last_trade']['price'])
            self.lblDOGPrice['text'] = dogeLastTrade
          elif market['id'] == '119':
            btsLastTrade = "{:.8f}".format(market['last_trade']['price'])
            self.lblBTSPrice['text'] = btsLastTrade
        
        balances = self.c.balances()
        availableBalance = balances['data']['available']
        heldBalance = balances['data']['held']
        
        ziftValue = availableBalance['275'] * ziftLastTrade
        pointsValue = availableBalance['89'] * float(pointsLastTrade)
        dogeValue = availableBalance['94'] * float(dogeLastTrade)
        
        #print(availableBalance)
        #for x in availableBalance:
        #  print(x)
        
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
        
        self.lblBalBTS["text"] = "BitShares: "
        self.lblVolBTS["text"] = str(availableBalance['2'])
        self.lblValBTS["text"] = str(availableBalance['2'])
        
        self.lblBalDOG["text"] = "Dogecoin: "
        self.lblVolDOG["text"] = str(availableBalance['94'])
        self.lblValDOG["text"] = str(dogeValue)
        
        self.lblBalZift["text"] = "ZiftrCoin: "
        self.lblVolZift['text'] = str(availableBalance['275'])
        self.lblValZift['text'] = str(ziftValue)        
        
        self.lblBalPoints["text"] = "Points: "
        self.lblVolPoints['text'] = str(availableBalance['89'])
        self.lblValPoints['text'] = str(pointsValue)
        
        self.lblBTCValue['text'] = str(self.btcPrice)
        self.lblTotalBal["text"] = "{:.4f}".format(availableBalance['3'] + ziftValue + pointsValue + dogeValue) + " BTC"
        self.lblTotalVal["text"] = "{:.2f}".format((availableBalance['3'] + ziftValue + pointsValue + dogeValue) * self.btcPrice)  + " GBP"
        
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
        
        # Update Button
        self.btnUpdate = Button(self)
        self.btnUpdate["text"] = "Update"
        self.btnUpdate["command"] = self.update
        self.btnUpdate.grid({"row": "50", "column": "0"})
        
        # Capital Button
        self.btnCapital = Button(self)
        self.btnCapital["text"] = "Capital"
        self.btnCapital["command"] = self.Capital
        self.btnCapital.grid({"row": "50", "column": "1"})
        
        # Quit Button
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.exit
        self.QUIT.grid({"row": "50", "column":"2"})

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
        
        self.btnXRPOrders = Button(self.marketsLblFrame)
        self.btnXRPOrders["text"] = "Order Book"
        self.btnXRPOrders["command"] = lambda: self.OrderBook(275, 454)
        self.btnXRPOrders.grid({"row": "0", "column":"3"})
        
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
        
        self.btnLTCOrders = Button(self.marketsLblFrame)
        self.btnLTCOrders["text"] = "Order Book"
        self.btnLTCOrders["command"] = lambda: self.OrderBook(275, 3)
        self.btnLTCOrders.grid({"row": "1", "column":"3"})
        
        self.lblBTS = Label(self.marketsLblFrame)
        self.lblBTS["text"] = "Bitshares"
        self.lblBTS.grid({"row": "2"})
        
        self.lblBTSPrice = Label(self.marketsLblFrame)
        self.lblBTSPrice["text"] = "Price: xx" 
        self.lblBTSPrice.grid({"row": "2", "column":"1"})

        self.btnBTSChart = Button(self.marketsLblFrame)
        self.btnBTSChart["text"] = "Chart"
        self.btnBTSChart["command"] = lambda: self.Chart(119)
        self.btnBTSChart.grid({"row": "2", "column":"2"})
        
        self.btnBTSrders = Button(self.marketsLblFrame)
        self.btnBTSrders["text"] = "Order Book"
        self.btnBTSrders["command"] = lambda: self.OrderBook(275, 119)
        self.btnBTSrders.grid({"row": "2", "column":"3"})
        
        self.lblDOG = Label(self.marketsLblFrame)
        self.lblDOG["text"] = "Dogecoin"
        self.lblDOG.grid({"row": "3"})
        
        self.lblDOGPrice = Label(self.marketsLblFrame)
        self.lblDOGPrice["text"] = "Price: xx" 
        self.lblDOGPrice.grid({"row": "3", "column":"1"})

        self.btnDOGChart = Button(self.marketsLblFrame)
        self.btnDOGChart["text"] = "Chart"
        self.btnDOGChart["command"] = lambda: self.Chart(132)
        self.btnDOGChart.grid({"row": "3", "column":"2"})
        
        self.btnDOGOrders = Button(self.marketsLblFrame)
        self.btnDOGOrders["text"] = "Order Book"
        self.btnDOGOrders["command"] = lambda: self.OrderBook(275, 132)
        self.btnDOGOrders.grid({"row": "3", "column":"3"})
        
        self.lblZift = Label(self.marketsLblFrame)
        self.lblZift["text"] = "ZiftrCoin"
        self.lblZift.grid({"row": "4"})
        
        self.lblZiftPrice = Label(self.marketsLblFrame)
        self.lblZiftPrice["text"] = "Price: xx" 
        self.lblZiftPrice.grid({"row": "4", "column":"1"})

        self.btnZiftChart = Button(self.marketsLblFrame)
        self.btnZiftChart["text"] = "Chart"
        self.btnZiftChart["command"] = lambda: self.Chart(473)
        self.btnZiftChart.grid({"row": "4", "column":"2"})
        
        self.btnZiftOrders = Button(self.marketsLblFrame)
        self.btnZiftOrders["text"] = "Order Book"
        self.btnZiftOrders["command"] = lambda: self.OrderBook(275, 473)
        self.btnZiftOrders.grid({"row": "4", "column":"3"})

        self.lblPoints = Label(self.marketsLblFrame)
        self.lblPoints["text"] = "Points"
        self.lblPoints.grid({"row": "5"})
        
        self.lblPointsPrice = Label(self.marketsLblFrame)
        self.lblPointsPrice["text"] = "Price: xx"
        self.lblPointsPrice.grid({"row": "5", "column":"1"})
  
        self.btnPointsChart = Button(self.marketsLblFrame)
        self.btnPointsChart["text"] = "Chart"
        self.btnPointsChart["command"] = lambda: self.Chart(120)
        self.btnPointsChart.grid({"row": "5", "column":"2"})
               
        self.btnPointsOrders = Button(self.marketsLblFrame)
        self.btnPointsOrders["text"] = "Order Book"
        self.btnPointsOrders["command"] = lambda: self.OrderBook(275, 120)
        self.btnPointsOrders.grid({"row": "5", "column":"3"})
        
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

        self.lblBalBTS = Label(self.coinsbalLblFrame)
        self.lblBalBTS["text"] = "Bitshares"
        self.lblBalBTS.grid({"row": "5", "column":"0"})
        
        self.lblVolBTS = Label(self.coinsbalLblFrame)
        self.lblVolBTS["text"] = ""
        self.lblVolBTS.grid({"row": "5", "column":"1"})
        
        self.lblValBTS = Label(self.coinsbalLblFrame)
        self.lblValBTS["text"] = ""
        self.lblValBTS.grid({"row": "5", "column":"2"})

        self.lblBalDOG = Label(self.coinsbalLblFrame)
        self.lblBalDOG["text"] = "Dogecoins"
        self.lblBalDOG.grid({"row": "6", "column":"0"})
        
        self.lblVolDOG = Label(self.coinsbalLblFrame)
        self.lblVolDOG["text"] = ""
        self.lblVolDOG.grid({"row": "6", "column":"1"})
        
        self.lblValDOG = Label(self.coinsbalLblFrame)
        self.lblValDOG["text"] = ""
        self.lblValDOG.grid({"row": "6", "column":"2"})

        self.lblBalZift = Label(self.coinsbalLblFrame)
        self.lblBalZift["text"] = "ZiftrCoin"
        self.lblBalZift.grid({"row": "7", "column":"0"})
        
        self.lblVolZift = Label(self.coinsbalLblFrame)
        self.lblVolZift["text"] = ""
        self.lblVolZift.grid({"row": "7", "column":"1"})
        
        self.lblValZift = Label(self.coinsbalLblFrame)
        self.lblValZift["text"] = ""
        self.lblValZift.grid({"row": "7", "column":"2"})
                
        self.lblBalPoints = Label(self.coinsbalLblFrame)
        self.lblBalPoints["text"] = "Points"
        self.lblBalPoints.grid({"row": "8", "column":"0"})
        
        self.lblVolPoints = Label(self.coinsbalLblFrame)
        self.lblVolPoints["text"] = ""
        self.lblVolPoints.grid({"row": "8", "column":"1"})
        
        self.lblValPoints = Label(self.coinsbalLblFrame)
        self.lblValPoints["text"] = ""
        self.lblValPoints.grid({"row": "8", "column":"2"})
        return 

    def Chart(self, mid):
      chart = ChartUI(self,mid,self.c, self.fs)
      return
    
    def OrderBook(self, cid, mid):
      trad_hist = TradeHistUI(self, cid, mid,self.c)
      return
    
    def Capital(self):
      capital = CapitalUI(self, self.c, self.last_trade_prices)
      return

    def update(self):
      #while not self.finish:
      print("Updating Market Data")
      marketData = self.c.markets()
        
      for market in marketData['data']:
          #print(market)
        if market['id'] == '473':
          self.lblZiftPrice['text'] = "{:.8f}".format(market['last_trade']['price'])
        elif market['id'] == '120':
          self.lblPointsPrice['text'] = "{:.8f}".format(market['last_trade']['price'])
            
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