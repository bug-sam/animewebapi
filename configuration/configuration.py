import os
import json

def loadConfiguration():
    configpath = os.path.dirname(os.path.realpath(__file__)) + '\\configuration.json'
    f = open(configpath)
    configuration = json.loads(f.read())
    f.close()
    return configuration