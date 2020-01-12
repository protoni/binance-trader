

class Strategy:
    def __init__(self, config, state):
        
        # Current strategy config
        self.config = config

        # Loaded state machine
        self.state = state

        # Strategy name
        self.name = None

        # Is the state machine initialized
        self.initState = None

        # Starting amount of BTC
        self.initialBtc = None

        # Current amount of BTC
        self.currentBtc = None

        # Current amount of XMR
        self.currentXmr = None

        # Current market price
        self.latestPrice = None

        # Last buy price
        self.buyPrice = None

        # Next move, SELL = 0, BUY = 1
        self.nextMove = None

        # Trade status ( percentage )
        self.tradeStatus = None

        # Price where asset was bought / sold last time
        self.tradePrice = None

        # Price gain that triggers a sell ( percentage )
        self.sellThreshold = None

        # Price gain that triggers a sell ( percentage )
        self.buyThreshold = None

        # Trailing buy threshold ( percentage )
        self.trailingBuy = None

        # Trailing sell threshold ( percentage )
        self.trailingSell = None

        # Set strategy state
        self.initialize()


    def checkAllVariables(self):
        variablesOk = True

        # Config params
        if self.config != None:
            if self.name == None:
                print("param 'name' missing!")
                variablesOk = False
            if self.sellThreshold == None:
                print("param 'sellThreshold' missing!")
                variablesOk = False
            if self.buyThreshold == None:
                print("param 'buyThreshold' missing!")
                variablesOk = False
            if self.trailingBuy == None:
                print("param 'trailingBuy' missing!")
                variablesOk = False
            if self.trailingSell == None:
                print("param 'trailingSell' missing!")
                variablesOk = False

        # State params
        if self.state != None:
            if self.initState == None:
                print("param 'initState' missing!")
                variablesOk = False
            if self.initialBtc == None:
                print("param 'initialBtc' missing!")
                variablesOk = False
            if self.currentBtc == None:
                print("param 'currentBtc' missing!")
                variablesOk = False
            if self.currentXmr == None:
                print("param 'currentXmr' missing!")
                variablesOk = False
            if self.latestPrice == None:
                print("param 'latestPrice' missing!")
                variablesOk = False
            if self.buyPrice == None:
                print("param 'buyPrice' missing!")
                variablesOk = False
            if self.nextMove == None:
                print("param 'nextMove' missing!")
                variablesOk = False
            if self.tradeStatus == None:
                print("param 'tradeStatus' missing!")
                variablesOk = False
            if self.tradePrice == None:
                print("param 'tradePrice' missing!")
                variablesOk = False

        return variablesOk


    def initializeState(self):
        if self.initState != None:
            if self.initState == False:
                print("Initializing state!")
        

    def initialize(self):
        initOk = True

        try:
            # Set data from config file
            if self.config != None:
                self.name = self.config['name']
                self.sellThreshold = self.config['sellThreshold']
                self.buyThreshold = self.config['buyThreshold']
                self.trailingBuy = self.config['trailingBuy']
                self.trailingSell = self.config['trailingSell']

            # Set data from states file
            if self.state != None:
                self.initState = self.state['initState']
                self.initialBtc = self.state['initialBtc']
                self.currentBtc = self.state['currentBtc']
                self.currentXmr = self.state['currentXmr']
                self.latestPrice = self.state['latestPrice']
                self.buyPrice = self.state['buyPrice']
                self.nextMove = self.state['nextMove']
                self.tradeStatus = self.state['tradeStatus']
                self.tradePrice = self.state['tradePrice']

            if not self.checkAllVariables():
                initOk = False
        except:
            initOk = False

        self.initializeState()

        if not initOk:
            print("Initialization failed!")

    def toJson(self):
        return {
                "name"          : self.name,
                "initState"     : self.initState,
                "initialBtc"    : self.initialBtc,
                "currentBtc"    : self.currentBtc,
                "currentXmr"    : self.currentXmr,
                "latestPrice"   : self.latestPrice,
                "buyPrice"      : self.buyPrice,
                "nextMove"      : self.nextMove,
                "tradeStatus"   : self.tradeStatus,
                "tradePrice"    : self.tradePrice
            }

        