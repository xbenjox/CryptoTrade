import urllib
import json

class CoinDesk:
  def __init__(self):
    self.url = "http://api.coindesk.com/v1/bpi/currentprice/GBP.json"
    return
  
  def getPrice(self):
    response = urllib.request.urlopen(self.url)
    decodeResponse = response.read().decode('utf8')
    
    data = json.loads(decodeResponse)
    
    price = data['bpi']['GBP']['rate_float']
    
    return price