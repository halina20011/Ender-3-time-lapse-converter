from ntpath import join
import os

import data

def listToString(_list):
    s = "".join([str(element) for element in _list])
    print(s)
    return s

def command(X, Y, layer):
    commands = []
    commands.append(f";Custom Timelapse start.")
    commands.append(f"M83 ;Switch to relative E values for retraction.")
    commands.append(f"G1 F1800 E{data.printerData.retraction} ;Retraction")
    commands.append(f"M82 ;Switch to absolute E values for retraction.")
    commands.append(f"G91   ;Switch to relative position.")
    commands.append(f"G0 Z1 ;Move Z axis up a bit")
    commands.append(f"G90   ;Switch back to absolute position")
    if(data.printerData.showLayerNumber):
        commands.append(f"M117 {layer} ;Show current layer.")
    commands.append(f"{data.printerData.GCodeTriggerPosition}")
    commands.append(f"M400 ;Wait to finish moving.")
    commands.append(f"G4 P{1000 * data.printerData.waitTime} ;Wait for camera")
    commands.append(f"G0 F1800 {X} {Y} ;Move back to original position.")
    commands.append(f"G91 ;Switch to relative position")
    commands.append(f"G0 Z-1 ;Restore Z axis")
    commands.append(f"G90 ;Switch back to absolute position")
    commands.append(f";Custom Timelapse end.")
    return commands

commands = [
    "X", "Y", "Z", "E"
]

def floatToIntToString(_float):
    return str(int(float(_float)))

class printer():
    def __init__(self, name, X, Y, Z, E):
        self.name = name
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

    def getValuesInt(self, type, values):
        returnValues = []
        if(values[0] == "True"):
            returnValues.append("X" + floatToIntToString(self.X))
        if(values[1] == "True"):
            returnValues.append("Y" + floatToIntToString(self.Y))
        if(values[2] == "True"):
            returnValues.append("Z" + floatToIntToString(self.Z))
        
        returnString = type
        for x in range(0, len(returnValues)):
            returnString += " " + returnValues[x]
        return returnString

printer1 = printer("Ender3", 0, 0, 0, 0)

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
    fileName =  os.path.join(os.path.dirname(__file__), fileName)
    print(fileName)
    with open(fileName, "w") as f:
        for line in content:
            f.write(f"{line}\n")


fileName = "propeller.gcode"
with open(fileName, "r") as f:
    fileContent = f.read()
    listOfLayers = fileContent.split("\n")
    zLayers = getZChanges(listOfLayers)
    print(len(zLayers))
    print(zLayers)

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
    
    newFilename = fileName.split(".")
    newFilename.insert(1, "New.")
    newFilename = listToString(newFilename)
    writeToNewFile(newFilename, newFileContent)