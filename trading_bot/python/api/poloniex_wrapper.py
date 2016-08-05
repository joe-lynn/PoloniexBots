import urllib
import requests
import time
import hmac,hashlib
 
def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))
 
class poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret
 
    def post_process(self, before):
        after = before
 
        # Add timestamps if there isnt one but is a datetime
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
                           
        return after
 
    def api_query(self, command, req={}):
 
        # TODO(stfinancial): Do we need https here, does speed imrpove without it?
        if(command == "returnTicker" or command == "return24Volume"):
            ret = requests.get('https://poloniex.com/public?command=' + command)
            return ret.json()
        elif(command == "returnOrderBook"):
            ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']))
            return ret.json()
        elif(command == "returnMarketTradeHistory"):
            ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']))
            return ret.json()
        elif(command == "returnLoanOrders"):
            ret = requests.get('https://poloniex.com/public?command=' + command + '&currency=' + str(req['currency']))
            return ret.json()
        elif(command == "returnChartData"):
            ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']) + '&start=' + str(req['start']) + '&end=' + str(req['end']) + '&period=' + str(req['period']))
            return ret.json()
        else:
            req['command'] = command
            req['nonce'] = int(time.time()*1000)
            post_data = urllib.parse.urlencode(req)
 
            sign = hmac.new(self.Secret, post_data.encode('utf-8'), hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }
 
            ret = requests.post('https://poloniex.com/tradingApi', data=req, headers=headers)
            # jsonRet = json.loads(ret.read())
            return self.post_process(ret.json())
 
    def returnLoanOrders(self, currency):
        return self.api_query("returnLoanOrders", {'currency': currency})
 
    def returnTicker(self):
        return self.api_query("returnTicker")
 
    def return24Volume(self):
        return self.api_query("return24Volume")
 
    def returnOrderBook (self, currencyPair):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})
 
    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})
 
    def returnChartData(self, currencyPair, period, start, end):
        return self.api_query("returnChartData", {'currencyPair': currencyPair, 'period': period, 'start': start, 'end': end})
 
    # Returns all of your balances.
    # Outputs:
    # {"BTC":"0.59098578","LTC":"3.31117268", ... }
    def returnBalances(self):
        return self.api_query('returnBalances')


    def returnAvailableAccountBalances(self, account):
        return self.api_query('returnAvailableAccountBalances', {'account': account})

    def returnOpenLoanOffers(self):
        return self.api_query('returnOpenLoanOffers')
 
    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs:
    # orderNumber   The order number
    # type          sell or buy
    # rate          Price the order is selling or buying at
    # Amount        Quantity of order
    # total         Total value of order (price * quantity)
    def returnOpenOrders(self,currencyPair):
        return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})
 
 
    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs:
    # date          Date in the form: "2014-02-19 03:44:59"
    # rate          Price the order is selling or buying at
    # amount        Quantity of order
    # total         Total value of order (price * quantity)
    # type          sell or buy
    def returnTradeHistory(self,currencyPair):
        return self.api_query('returnTradeHistory',{"currencyPair":currencyPair})
 
    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # OPTIONAL:     KILL OR FILL or IMMEDIATE (check API documentation)
    # Outputs:
    # orderNumber   The order number
    def buy(self,currencyPair,rate,amount):
        return self.api_query('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})
 
    # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is selling at
    # amount        Amount of coins to sell
    # OPTIONAL:     KILL OR FILL or IMMEDIATE (check API documentation)
    # Outputs:
    # orderNumber   The order number
    def sell(self,currencyPair,rate,amount):
        return self.api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})
 
    # Cancels an order you have placed in a given market. Required POST parameters are "currencyPair" and "orderNumber".
    # Inputs:
    # currencyPair  The currency pair
    # orderNumber   The order number to cancel
    # Outputs:
    # succes        1 or 0
    def cancel(self,currencyPair,orderNumber):
        return self.api_query('cancelOrder',{"currencyPair":currencyPair,"orderNumber":orderNumber})
 
    # Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."}
    # Inputs:
    # currency      The currency to withdraw
    # amount        The amount of this coin to withdraw
    # address       The withdrawal address
    # Outputs:
    # response      Text containing message about the withdrawal
    def withdraw(self, currency, amount, address):
        return self.api_query('withdraw',{"currency":currency, "amount":amount, "address":address})


    # Places a loan offer for a given currency. Required POST parameters are "currency", "amount", and "lendingRate"
    # Inputs:
    # currency      The currency to loan out
    # amount        The amount of this currency to loan out
    # lendingRate   The percentage interest rate divided by 100 of the loan offer
    # duration      The duration of the loan, can be between 2 and 60 days
    # autoRenew     If set to 1, will place an identical loan order after the loan has been repaid
    # Outputs:
    # response      Text containing message about the loan offer
    def createLoanOffer(self, currency, amount, lendingRate, duration=2, autoRenew=0):
        return self.api_query('createLoanOffer',{"currency":currency, "amount":amount, "lendingRate":lendingRate, "duration":duration, "autoRenew":autoRenew})

    def cancelLoanOffer(self, orderNumber):
        return self.api_query('cancelLoanOffer',{"orderNumber":orderNumber})        
