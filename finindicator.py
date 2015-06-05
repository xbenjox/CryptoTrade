import numpy as np

class FinIndicator:
  def __init__(self):
    return 
  
  def stochastic(self, hp, lp, cp):
    highestHigh = [0] * len(hp)
    lowestLow = [0] * len(lp)
    k = [float('nan')] * len(hp)
    d = [float('nan')] * len(hp)
    period = 14
    
    #print("Calculating Stochastic")
    
    for i in range(period, len(hp) +1):
      highestHigh[i-1] = max(hp[i-period:i])
      lowestLow[i-1] = min(lp[i-period:i])
      if highestHigh[i-1] == lowestLow[i-1]:
        k[i-1] = 0
      else:
        k[i-1] = (cp[i-1] - lowestLow[i-1]) / (highestHigh[i-1] - lowestLow[i-1]) * 100
      
    for i in range(period + 2, len(hp)+1):  
      d[i-1] = self.sma(k[(i-3):(i)])
      
    return [[k],[d]]
  
  def calcRSI(self, cp, period=14):
    #print("Calculating RSI")
    #print(cp)
    
    deltas = np.diff(cp)
    deltas = np.insert(deltas, 0, float('nan'))
    
    #print("Deltas")
    #print(deltas)
    
    gains = [0] * len(cp)
    losses = [0] * len(cp)
    
    for i in range(1,len(cp)):
      if deltas[i] > 0:
        gains[i] = deltas[i]
        losses[i] = 0
      elif deltas[i] < 0:
        gains[i] = 0
        losses[i] = -deltas[i]
      else:
        gains[i] = 0
        losses[i] = 0
      
    avgGain = [float('nan')] * len(cp)
    avgLoss = [float('nan')] * len(cp)
    rs = [float('nan')] * len(cp)
    rsi = [float('nan')] * len(cp)
        
    avgGain[period] = sum(gains[:period-1]) / period
    avgLoss[period] = sum(losses[:period-1]) / period
    
    #print("Avg Gains")
    #print(avgGain)
    #print("Avg Losses")
    #print(avgLoss)
    
    for i in range(period+1, len(cp)):
      if avgGain[i-1] == 0:
        avgGain[i] = 0
      else:
        avgGain[i] = (avgGain[i-1] * (period - 1) + gains[i]) / period
        
      if avgLoss[i-1] == 0:
        avgLoss[i] = 0
      else:	
        avgLoss[i] = (avgLoss[i-1] * (period - 1) + losses[i]) / period
        rs[i] = avgGain[i] / avgLoss[i]
      
      rsi[i] = 100 - (100  / (1 + rs[i]))
      
         
    return rsi
  
  def macd(self):
    return 
  
  def sma(self, l):
    sma = sum(l)/ len(l)
    return sma
  
  def calcSMA(self, values, period=14):
    weights = np.repeat(1.0, period)/period
    smas = np.convolve(values, weights,'valid')
    
    packer = [float('nan')] * (period - 1)
    
    smas = np.concatenate((packer, smas))
    
    return smas 
 

class FinStrategy:
  def __init__(self):
    self.risk = 0.03
    self.trend = ""
    self.sellPoints = []
    
    return 

  def getTrend(self):
    return 

  def getSellPoint(self, mid):
    sp = 0.0
    
    return sp