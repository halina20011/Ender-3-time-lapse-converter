import os
import json

settings = os.path.join(os.path.dirname(__file__), "settings.json")

class JSON():
    def __init__(self, jsonDataContent, filePath):
        self.jsonDataContent = jsonDataContent
        self.GCodeTriggerPosition = jsonDataContent['GCodeTriggerPosition']
        self.speed = jsonDataContent['speed']
        self.runCommandWhenTakingPicture = jsonDataContent['runCommandWhenTakingPicture']
        self.commandsToRunWhenTakingPicture = jsonDataContent['commandsToRunWhenTakingPicture']
        self.retraction = jsonDataContent['retraction']
        self.showLayerNumber = jsonDataContent['showLayerNumber']
        self.waitTime = jsonDataContent['waitTime']

        self.videoMode = jsonDataContent['videoMode']
        self.fileOutput = jsonDataContent['fileOutput']
        self.takePhotoOnFirstLayer = jsonDataContent['takePhotoOnFirstLayer']
        self.filePath = filePath

    def changeValue(self, index, newValue):
        self.jsonDataContent[index] = newValue
        with open(settings, 'w') as file:
            json.dump(self.jsonDataContent, file, indent=4)
        self.readJson()

    def readJson(self):
        jsonData = open(self.filePath, "r+")
        jsonDataContent = json.load(jsonData)
        self.jsonDataContent = jsonDataContent

jsonData = open(settings, "r+")
jsonDataContent = json.load(jsonData)

printerData = JSON(jsonDataContent, settings)

print(printerData.jsonDataContent)