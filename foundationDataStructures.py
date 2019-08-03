#import packages
import random as rand
from math import cos, sin, radians, sqrt
import numpy as np

#object for containing data simulating infrastructure of a city
class infrastructure:
    buildings = []
    def __init__(self, width, height):
        self.width = width
        self.height = height

    #method for building a city
    def buildBasicCity(self):
        global buildings
        buildings = []
        for x in range(1,9):
            for y in range(1,9):
                if(x % 2 == 1 and y % 2 == 1):
                    tmp = []
                    tmp.append(x*(self.width/10))
                    tmp.append(y*(self.height/10))
                    tmp.append(self.width/10)
                    tmp.append(self.height/10)
                    buildings.append(tmp)
        return buildings

    #method tests if a node is within a building area
    def onRoad(self, node):
        output = True
        global buildings
        for current in buildings:
            x2 = int(current[0])
            y2 = int(current[1])
            if(node.x+10 > x2 and node.x < x2 + (current[2])):
                if(node.y +10 > y2 and node.y < y2 + (current[3])):
                    output = False
        return output

    #get the signal strength between two nodes based on distance and infrastructure
    def getSignal(self, current, target):
        differenceVector = []
        differenceVector.append(current.x - target.x)
        differenceVector.append(current.y - target.y)
        distance = sqrt(pow(differenceVector[0], 2) + pow(differenceVector[1], 2))
        scalar = distance
        precision = 50
        for i in range(precision):
            test = node((current.x + differenceVector[0]*(i/precision)),
                        (current.y + differenceVector[1]*(i/precision)), None)
            if(not self.onRoad(test)):
                scalar = scalar + 10
        return scalar


#object representing a device (in a city) with mobile adhoc functionality
class node:
    RESOLUTION = 25
    distance = float("inf")
    via = None
    direction = rand.randint(0, 360)
    def __init__(self, inputX, inputY, city):
        #if x and y were defined in constructor, don't worry about their locations
        if inputX is not None and inputY is not None:
            self.x = inputX
            self.y = inputY
            self.city = city

        #x and y were not defined, find a place for them outside the buildings
        else:
            self.x = rand.randrange(0, city.width)
            self.y = rand.randrange(0, city.height)
            self.city = city
            while(not city.onRoad(self)):
                self.x = rand.randrange(0, city.width)
                self.y = rand.randrange(0, city.height)

    
    def getHotSpot(self):
        def translate(value, leftMin, leftMax, rightMin, rightMax):
            # Figure out how 'wide' each range is
            leftSpan = leftMax - leftMin
            rightSpan = rightMax - rightMin

            # Convert the left range into a 0-1 range (float)
            valueScaled = float(value - leftMin) / float(leftSpan)

            # Convert the 0-1 range into a value in the right range.
            return rightMin + (valueScaled * rightSpan)

        
        plane = np.zeros((self.RESOLUTION, self.RESOLUTION, 1))
        xRaw = translate(self.x, 0, self.city.width, 0, self.RESOLUTION)
        yRaw = translate(self.y, 0, self.city.height, 0, self.RESOLUTION)
        tmp = []
        tmp.append(1)
        plane[int(xRaw), int(yRaw)] = tmp
        return plane

    def drop(self):
        self.x = rand.randrange(0, self.city.width)
        self.y = rand.randrange(0, self.city.height)
        while(not self.city.onRoad(self)):
            self.x = rand.randrange(0, self.city.width)
            self.y = rand.randrange(0, self.city.height)
        

#class for holding information related to connections between nodes
class connection:

    #accept two nodes and strength of signal as arguements
    def __init__(self, myNode1, myNode2, myStrength):
        self.node1 = myNode1
        self.node2 = myNode2
        self.strength = myStrength

    #return information of connection in format easy to read by gui
    def getDrawable(self):
        tmp = []
        tmp.append(self.node1.x)
        tmp.append(self.node1.y)
        tmp.append(self.node2.x)
        tmp.append(self.node2.y)
        tmp.append(self.strength)
        return tmp

