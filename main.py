from decimal import Decimal
from decimal import getcontext
import json
import requests
import time
import os
from Trader import *

'''
Trading bot for XMR / BTC swing trading
'''

''' Constants '''
# Data indexes in candle data list
CANDLE_OPEN_TIME_IDX = 0
CANDLE_OPEN_IDX = 1
CANDLE_HIGH_IDX = 2
CANDLE_LOW_IDX = 3
CANDLE_CLOSE_IDX = 4
CANDLE_VOLUME_IDX = 5
CANDLE_CLOSE_TIME_IDX = 6
CANDLE_QUOTE_ASSET_VOL_IDX = 7
CANDLE_NUM_OF_TRADEX_IDX = 8
CANDLE_TAKER_BUY_BASE_ASSET_VOL_IDX = 9
CANDLE_TAKER_BUY_QUOTE_ASSET_VOL_IDX = 10
CANDLE_IGNORE_IDX = 11

CONFIG_FILE = 'config.json'

XMR = 'XMR'
BTC = 'BTC'

INITIAL_BTC = 0.02

''' State machine '''
# Initialize state machine
state = {

    
        # Strategy name
        'name' : 'strategy1',

        # Is the state machine initialized
        'initState' : False,

        # Starting amount of BTC
        'initialBtc' : INITIAL_BTC,

        # Current amount of BTC
        'currentBtc' : INITIAL_BTC,

        # Current amount of XMR
        'currentXmr' : 0,

        # Current market price
        'latestPrice' : 0,

        # Last buy price
        'buyPrice' : 0,

        # Next move, SELL = 0, BUY = 1
        'nextMove' : 0,

        # Trade status ( percentage )
        'tradeStatus' : 0,

        # Price where asset was bought / sold last time
        'tradePrice' : 0,

        # Price gain that triggers a sell ( percentage )
        'sellThreshold' : 0.04,

        # Price gain that triggers a sell ( percentage )
        'buyThreshold' : 0.04
    

}

''' API '''
# Binance API base URL
BASE_URL_BN = "https://api.binance.com"

# Binance API candle data URL
CANDLES_URL = "{}/api/v3/klines".format(BASE_URL_BN)

''' Utils'''
# Save the state machine
def saveState():
    pass

# Load the state machine
def loadState():
    pass

def getCurrentTimestamp():
    return int(time.time() * 1000)

def printState():
    print(json.dumps(state))

def readJson(file):
    if os.path.exists(file):
        try:
            with open(file) as jsonFile:
                return json.load(jsonFile)
        except:
            print("Failed to load config file!")
    
    return 0

def readFile(path):
    if os.path.exists(path):
         return open(path, "r")
    else:
        return 0

def getConfigFilename():
    parentDir = os.getcwd().replace('\\', '/')
    
    path = parentDir + '/' + CONFIG_FILE
    
    return path

def loadConf():
    return readJson(getConfigFilename())

''' Trader '''
# Get the current market data
def getCurrentData():

    currentTime = getCurrentTimestamp()
    startTime = currentTime - ( 1000 * 60 ) * 5 # 5 minutes
    endTime = currentTime

    params = {
        'symbol': XMR + BTC,
        "interval": '1m',
        "startTime": startTime,
        "endTime": endTime,
        "limit": 100
    }

    r = requests.get(CANDLES_URL, params=params)

    return json.loads(r.content)

def updateState(data):

    currentPrice = float(data[CANDLE_CLOSE_IDX])
    latestPrice = state['latestPrice']

    if state['initState']:
        # Change Decimal precision to 6 decimals
        getcontext().prec = 6

        
        #print("currentPrice: " + str(currentPrice))
        
        tradePrice = state['tradePrice']
        #print("tradePrice: " + str(tradePrice))
        change = Decimal(currentPrice) - Decimal(tradePrice)
        #print("change: " + str(change))

        if currentPrice != 0 and change != 0:
            percentageChange = (Decimal(change) / Decimal(tradePrice)) * 100
        
            print("percentageChange: " + str(percentageChange))

            # Looking to buy XMR
            if state['nextMove'] == 1:
                if percentageChange >= buyThreshold:
                    print("BUY! %: " + str(percentageChange))

                    # Update purchace price
                    state['tradePrice'] = currentPrice

                    state['nextMove'] = 0
            
            # Looking to sell XMR
            elif state['nextMove'] == 0:
                if percentageChange >= sellThreshold:
                    print("SELL! %: " + str(percentageChange))

                    # Update sell price
                    state['tradePrice'] = currentPrice

                    # Update balance
                    state['currentBtc'] += float(change)

                    state['nextMove'] = 1

    else:
        state['tradePrice'] = currentPrice
        state['initState'] = True


    state['latestPrice'] = currentPrice


# Main
def play():

    

    informBalanceInterval = 5
    informBalanceCounter = 0

    running = True

    # Main loop
    while running:
        #printState()

        if informBalanceCounter >= informBalanceInterval:
            print("Balance: " + str(state['currentBtc']))

            informBalanceCounter = 0

        informBalanceCounter += 1

        data = getCurrentData()
    
        if len(data) > 0:
            currentData = data[-1]

            updateState(currentData, config)
        else:
            print("No data")

        time.sleep( 1 )

def init():

    config = loadConf()

    if config != 0:
        print(config)
    else:
        print("Couldn't load config from a file!")
        return

    state = loadState()

    if state != 0:
        print(json.dumps(state))
    else:
        print("Couldn't load state from a file!")
        return
    
    


#play()

trader = Trader()

trader.initialize()