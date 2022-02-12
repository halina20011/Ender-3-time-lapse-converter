import sys
import os

import data

def checkFile(filePath):
    lower = sys.argv[1].lower()
    if(lower.find(".gcode") != -1):
        return True
    else: return False

def getRunArguments():
    filePath1 = None
    filePath2 = None
    print(len(sys.argv))
    if(len(sys.argv) > 1):
        arguments = sys.argv
        fileN = sys.argv[0]
        if(len(sys.argv) >= 2):
            filePath1 = os.path.abspath(sys.argv[1])
        if(len(sys.argv) == 3):
            filePath2 = os.path.abspath(sys.argv[2])
    
    return [filePath1, filePath2]

def getFilesPaths():
    originalFile = input("Original Gcode file: ")
    newFile = input("Path of generated file: ")
    filePath1 = os.path.abspath(originalFile)
    filePath2 = os.path.abspath(newFile)

    return [filePath1, filePath2]

def listToString(_list):
    s = "".join([str(element) for element in _list])
    print(s)
    return s

def command(X, Y, layer):
    speed = data.printerData.speed #Get speed from settings
    if(speed.find("F") == -1): #Check if is in string "F"
        speed = f"F{speed}"    #If its not, add it.
    
    if(data.printerData.takePhotoOnFirstLayer != True and layer == 0): #If in settings is not set to take picture on 0 or
        return []                                                      #or layer is not 0 then retrun empty list
    
    commands = []
    commands.append(f"; Custom Timelapse start.")
    commands.append(f"M83; Switch to relative E values for retraction.")
    commands.append(f"G1 E{data.printerData.retraction} {speed}; Retraction")
    commands.append(f"M82; Switch to absolute E values for retraction.")
    commands.append(f"G91   ; Switch to relative position.")
    commands.append(f"G0 Z1 ; Move Z axis up a bit")
    commands.append(f"G90   ; Switch back to absolute position")
    if(data.printerData.showLayerNumber):
        commands.append(f"M117 {layer} layer.; Show current layer.")
    
    commands.append(f"{data.printerData.GCodeTriggerPosition} {speed}")
    commands.append(f"M400; Wait to finish moving.")

    if(data.printerData.runCommandWhenTakingPicture != None):
        for command in data.printerData.commandsToRunWhenTakingPicture:
            commands.append(f"{command}")

    commands.append(f"G4 P{1000 * data.printerData.waitTime} ;Wait for camera")
    commands.append(f"G0 {X} {Y} {speed};Move back to original position.")
    commands.append(f"G91; Switch to relative position")
    commands.append(f"G0 Z-1; Restore Z axis")
    commands.append(f"G90; Switch back to absolute position")
    commands.append(f"; Custom Timelapse end.")
    return commands

commands = [
    "X", "Y", "Z", "E"
]

def floatToIntToString(_float):
    return str(int(float(_float)))

class printer():
    def __init__(self, X, Y, Z, E):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.E = E

    def setValue(self, name, val):
        if(name == "X"):
            self.X = float(val)
        elif(name == "Y"):
            self.Y = float(val)
        elif(name == "Z"):
            self.Z = float(val)
        elif(name == "E"):
            self.E = float(val)

    def debug(self):
        return self.X, self.Y, self.Z, self.E

    def getValues(self, type, values):
        returnValues = []
        if(values[0] == "True"):
            returnValues.append("X" + str(self.X))
        if(values[1] == "True"):
            returnValues.append("Y" + str(self.Y))
        if(values[2] == "True"):
            returnValues.append("Z" + str(self.Z))
        
        returnString = type
        for x in range(0, len(returnValues)):
            returnString += " " + returnValues[x]
        return returnString
    
    def getValue(self, value):
        if(value == "X"):
            return f"X{str(self.X)}"

        elif(value == "Y"):
            return f"Y{str(self.Y)}"
            
        elif(value == "Z"):
            return f"Z{str(self.Z)}"

        elif(value == "E"):
            return f"E{str(self.E)}"
        return None

printer1 = printer(0, 0, 0, 0)

def setValues(command, _printer): #G1 X100 Y65 Z2.8
    listOfCommands = command.split(" ") #["G1", "X187.8", "Y65", "Z2.8"]
    for type in listOfCommands:
        for command in commands:
            if(type[0:1] == command):
                #X187.8           X                    187.8
                _printer.setValue(type[0:1], type[1:len(type)]) 
    # print(_printer.debug())

def getZChanges(lines, cura = True):
    ZLines = []
    if(cura == False):
        for var, line in enumerate(lines):
            if(line.count(";") > 0):
                indexOfSemicolom = line.find(";")
                if(line.count("G0") > 0 and line[0:indexOfSemicolom].count("Z") > 0):
                    ZLines.append(var) 
            elif(line.count("G0") > 0 and line.count("Z") > 0):
                ZLines.append(var) 
    else:
        for var, line in enumerate(lines):
            if(line.count(";LAYER:") > 0):
                indexOfEnd = line.find(";LAYER:")
                number = line[len(";LAYER:"):]
                # print(len(";LAYER:"))
                ZLines.append(var + 1 + 1) #Add one because it start from 0 and file don't have 0 line and +1 to get next line
    return ZLines

def writeToNewFile(fileName, content):
    print(fileName)
    with open(fileName, "w") as f:
        for line in content:
            f.write(f"{line}\n")

def main():
    files = getRunArguments()
    filePath1 = files[0] 
    filePath2 = files[1]
    print(f"Input  file: {filePath1}")
    print(f"Output file:{filePath2}")
    if(filePath1 == None):
        files = getFilesPaths()
        filePath1 = files[0]
        filePath2 = files[0]
    
    with open(filePath1, "r") as f:
        fileContent = f.read()
        listOfLayers = fileContent.split("\n")
        zLayers = getZChanges(listOfLayers)
        print(f"Number of layers: {len(zLayers)}")
        # print(zLayers)

        newFileContent = []
        zLayerIndex = 0
        for index, layer in enumerate(listOfLayers):
            if(len(zLayers) > zLayerIndex):
                if(int(index + 1) == zLayers[zLayerIndex]):
                    listOfCommandsToAdd = command(printer1.getValue("X"), printer1.getValue("Y"), zLayerIndex)
                    for index, commandToAdd in enumerate(listOfCommandsToAdd):
                        newFileContent.append(commandToAdd)
                    zLayerIndex += 1

            newFileContent.append(layer)
            if(layer.count(";") == 0):
                setValues(layer, printer1)
        
        # newFilename = filePath2.split(".")
        # newFilename.insert(1, "New.")
        # newFilename = listToString(newFilename)
        writeToNewFile(filePath2, newFileContent)

if __name__ == '__main__':
    main()