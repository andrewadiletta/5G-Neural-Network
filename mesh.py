#import packages
import foundationDataStructures as aj
import tensorflow as tf
import tflearn as tl
import numpy as np
from tflearn import DNN
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

#class for holding data related to the mobile adhoc meshes
class mesh:

    #global variable holds all connections between nodes
    connections = []
    RESOLUTION = 25
    tf.device("/gpu:0")
    input_layer = input_data(shape=[None, RESOLUTION, RESOLUTION, 1])
    segment1 = conv_2d(input_layer, 64, 3, strides=1, activation='relu')
    segment2 = max_pool_2d(segment1, 2,strides=4)
    hidden_layer = fully_connected(segment2, 1024, activation='tanh')
    hidden_layer = dropout(hidden_layer, 0.5)
    output_layer = fully_connected(hidden_layer, RESOLUTION*RESOLUTION, activation='softmax')

    net = regression(output_layer , optimizer='momentum', loss='categorical_crossentropy', learning_rate=0.001)
    model = DNN(net)
    #model.load('modelsFinal/model', weights_only=True)
    
    def __init__(self, myNodes, myInfrastructure):
        self.nodes = myNodes
        self.infrastructure = myInfrastructure

    #mesh where every node connects to every other node if possible
    def rawMesh(self):
        print("creating full mesh")
        global connections
        self.connections = []
        for current in self.nodes:
            for target in self.nodes:
                if(target is not current):
                    signal = self.infrastructure.getSignal(current, target)
                    if(signal < 255):
                        tmp = aj.connection(current, target, signal)
                        self.connections.append(tmp)

    #protocal based on a "hello" outbound signal
    def batmanMesh(self):
        global connections
        self.connections = []

        #method creates connections based on shout outs by other nodes
        def getNeighbors(root, stem, world):
            global connections
            complete = False
            signalArray = []
            for current in world:
                signalArray.append(self.infrastructure.getSignal(root, current))
            world2 = [world for _, world in sorted(zip(signalArray, world), key=lambda pair: pair[0])]

            targets = []
            #first establish connection with available nodes
            for current in (world2):
                if(current is not root and current not in stem and not complete):
                    scalar = self.infrastructure.getSignal(root, current)
                    if(scalar < 255):
                        tmp = aj.connection(root, current, scalar)
                        self.connections.append(tmp)
                        stem.append(current)
                        if(current is world[len(world)-1]):
                            complete = True
                        else:
                            targets.append(current)
                            
            for current in (targets):
                if not complete:
                    getNeighbors(current, stem, world)
                        
        if(len(self.nodes) > 1):
            tmpStem = []
            getNeighbors(self.nodes[0], tmpStem, self.nodes)

    def getLossAndPower(self):
        loss = 0
        power = 0
        devices = []
        if(len(self.connections) > 0):
            for current in self.connections:
                power += pow(current.strength, 2)*0.0001
                loss += current.strength
                if current.node1 not in devices:
                    devices.append(current.node1)
                if current.node2 not in devices:
                    devices.append(current.node2)
                    
            loss = loss/len(self.connections)
        return power, loss, len(devices)

    def dijkstrasAlgorithum(self):
        global connections
        global done
        
        self.connections = []
        def trace(startNode, endNode):
            global connections
            path = []
            prevStep = endNode.via
            while(prevStep is not None):
                self.connections.append(aj.connection(prevStep, endNode, self.infrastructure.getSignal(prevStep, endNode)))
                path.append(endNode)
                endNode = prevStep
                prevStep = endNode.via
            return path
        
        def prioritize(priorityQueue, world):
            if(len(priorityQueue) > 1):
                if(priorityQueue[0] is world[len(world)-1]):
                    return trace(world[0], world[len(world)-1])
                else:
                    getNeighbors(priorityQueue[0], priorityQueue)
                    newlist = sorted(priorityQueue[1:], key=lambda node: node.distance, reverse=False)
                    prioritize(newlist, world)
            else:
                emptyPath = []
                return emptyPath

        #method creates connections based on shout outs by other nodes
        def getNeighbors(root, world):
            global connections
            complete = False
            signalArray = []
            for current in world:
                signalArray.append(self.infrastructure.getSignal(root, current))
            world2 = [world for _, world in sorted(zip(signalArray, world), key=lambda pair: pair[0])]

            targets = []
            #first establish connection with available nodes
            for current in (world2):
                if(current is not root and current and not complete):
                    scalar = self.infrastructure.getSignal(root, current)
                    if(scalar < 255):
                        current.distance = scalar + root.distance
                        current.via = root
                        if(current is world[len(world)-1]):
                            complete = True
                        else:
                            targets.append(current)
            return targets

        for current in self.nodes:
            current.distance = float("inf")
            current.via = None
            self.nodes[0].distance = 0
        prioritize(self.nodes, self.nodes)

    def train(self):
        print("building model")
        input = []
        output = []
        for j in range(1):
            self.dijkstrasAlgorithum()
            index = 0
            for current in self.connections:
                input.append(current.node1.getHotSpot())
                output.append(current.node2.getHotSpot().flatten())
            for i in self.nodes:
                i.drop()
            print("{0}% complete".format((j/200)*100))
        print("training")
        self.model.fit(input, output, n_epoch=1, show_metric=True, run_id="deep_nn")
        self.model.save('modelsFinal/modelNew')

    def getNode(self, start, stem, index):
        output = None
        for current in self.nodes:
            if current is not start and current not in stem:
                city = self.infrastructure
                #print("index:{0}".format(index))
                x =  (int(index%self.RESOLUTION))*(city.width/self.RESOLUTION)
                y = int(index/self.RESOLUTION)*(city.height/self.RESOLUTION)
                width = (city.width/self.RESOLUTION)
                height = (city.height/self.RESOLUTION)
                #print("x:{0}, y{1}, width:{2}, height:{3}".format(current.x, current.y, 10, 10))
                #print("x:{0}, y{1}, width:{2}, height:{3}".format(x, y, width, height))
                if current.x >= x and current.x <= x+width:
                    if current.y >= y and current.y <= y+height:
                        if(city.getSignal(start, current) < 255):
                            output = current
        connections = []
        return output
        
    def test(self, mode):
        self.connections = []
        input = []
        inputTmp = []
        inputTmp.append(self.nodes[0].getHotSpot())
        input.append(inputTmp)
        output = self.model.predict(inputTmp)[0]
        index = np.argmax(output)
        y = int(index/100)
        x = int(index-(y*100))
        return output

    def testMesh(self, mode):
        self.connections = []
        stem = []
        if mode == 0:
            self.model.load('modelsFinal/modelBlank', weights_only=True)
        if mode == 1:
            self.model.load('modelsFinal/modelSlim', weights_only=True)
        if mode == 2:
            self.model.load('modelsFinal/model', weights_only=True)

        def recursive(start):
            stem.append(start)
            input = []
            inputTmp = []
            inputTmp.append(start.getHotSpot())
            input.append(inputTmp)
            output = self.model.predict(inputTmp)[0]
            output = np.argsort(output)[::-1]
            if start is not self.nodes[len(self.nodes)-1]:
                current = None
                index = 0
                while current is None and index < 625:
                    current = self.getNode(start, stem, output[index])
                    index = index + 1
                if(current is not None):
                    self.connections.append(aj.connection(start, current, self.infrastructure.getSignal(start, current)))
                    recursive(current)

        recursive(self.nodes[0])


    
                
    

    #return connections calculated by mesh
    def getConnections(self):
        global connections
        return self.connections
