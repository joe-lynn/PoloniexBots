import requests


# Do public methods need to be https? Is it slower?
def public_api_query(command, req={}):
	if(command == 'returnTicker' or command == 'return24Volume' or command == 'returnCurrencies'):
        ret = requests.get('https://poloniex.com/public?command=' + command)
        return ret.json()
    elif(command == 'returnLoanOrders'):
        ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']))
        return ret.json()
    elif(command == 'returnOrderBook'):
    	ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']) + '&depth=' + str(req['depth']))
    	return ret.json()
    elif(command == 'returnChartData'):
    	# Change to handle additional parameters.
    	ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']))
    	return ret.json()
    elif(command == 'returnTradeHistory'):
    	# Change to handle additional parameters.
    	ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']))
    	return ret.json()
    else:
    	return {}