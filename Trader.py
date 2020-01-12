import utils
import json
from Strategy import * 

class Trader:
    def __init__(self):
        self.configs = None
        self.states = None
        self.initState = True
        self.strategies = []
        self.configLoaded = False
        self.stateLoaded = False
        self.strategiesLoaded = False


    def loadConfig(self):
        config = utils.loadConf()

        if config != 0 and config != None:
            self.configs = config

            self.configLoaded = True
        else:
            print("Couldn't load config from a file!")
            self.initState = False

        
    def saveState(self):
        objects = []
        
        for strategy in self.strategies:
            objects.append(strategy.toJson())

        utils.writeFile(utils.getStateFilename(), json.dumps(objects), False)


    def loadState(self):
        state = utils.loadState()

        if state != 0 and state != None:
            
            self.states = json.dumps(state)
            self.stateLoaded = True


    def getStrategyState(self, name):
        try:
            if self.strategiesLoaded:
                for state in self.states:
                    if state['name'] == name:
                        return state
        except:
            print("Can't get strategy name")

        return None


    def loadStrategies(self):
        try:
            if self.configLoaded:
                for config in self.configs:
                    
                    name = config['name']
                    
                    stratState = self.getStrategyState(name)
                    
                    strat = Strategy(config, stratState)
                    
                    self.strategies.append(strat)
                
            self.strategiesLoaded = True
        except:
            self.initState = False


    def initialize(self):
        self.loadConfig()
        self.loadState()
        self.loadStrategies()

        if not self.stateLoaded:
            self.saveState()

        if not self.initState:
            print("Initialization failed!")
            if not self.configLoaded:
                print("Configs not loaded!")
            if not self.stateLoaded:
                print("States not loaded")
            if not self.strategiesLoaded:
                print("Strategies not loaded")
        else:
            print("Initialization OK!")
        print("Strategy count: " + str(len(self.strategies)))