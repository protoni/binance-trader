import json
import time
import os
import constants
from pathlib import Path

# Save the state machine
def saveState():
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

def writeFile(path, data, append):
    ensureFileExists(path)

    if append:
        f = open(path, 'a+')
    else:
        f = open(path, 'w+')

    f.write(data)

    f.close()

def ensureFileExists(path):
    filename = Path(path)
    filename.touch(exist_ok=True)

def getConfigFilename():
    parentDir = os.getcwd().replace('\\', '/')
    
    path = parentDir + '/' + constants.CONFIG_FILE
    
    return path

def getStateFilename():
    parentDir = os.getcwd().replace('\\', '/')
    
    path = parentDir + '/' + constants.STATE_FILE
    
    return path

# Load the state machine
def loadState():
    return readJson(getStateFilename())

def loadConf():
    return readJson(getConfigFilename())