#import packages
import GUI as gui
import mesh
import foundationDataStructures as aj

#define constants
QUIT = 12
INCREASE_NODE_COUNT = 0
DECREASE_NODE_COUNT = 1
NEXT_CITY = 2
BEGIN_MOVEMENT = 3
FULL_MESH = 4
BATMAN_MESH = 5
DIJKSTRAS_MESH = 6
TRAIN = 7
BLANK = 8
SLIM = 9
BASIC = 10
POPULATE = 11

batman = False
fullMesh = False
dijkstras = False
blank = False
slim = False
basic = False

POPULATION_SIZE = 70

#create set of nodes, and test infrastructure
world = []
city = aj.infrastructure(800, 500)
city.buildBasicCity()
for i in range(POPULATION_SIZE):
    world.append(aj.node(None, None, city))
world.append(aj.node(city.width-10, city.height-10, city))

#create mesh network
network = mesh.mesh(world, city)
gui.buildButtonPanel(city)
gui.drawMesh(network)

def refresh(full=True):
    global world
    global dijkstras
    global batman
    global fullMesh
    global network
    if(full):
        world = []
        print(POPULATION_SIZE)
        for i in range(POPULATION_SIZE):
            world.append(aj.node(None, None, city))
        world.append(aj.node(city.width-10, city.height-10, city))
    network.nodes = world
    network.infrastructure = city
    if dijkstras:
        network.dijkstrasAlgorithum()
    if batman:
        network.batmanMesh()
    if fullMesh:
        network.rawMesh()
    if blank:
        network.testMesh(0)
    if slim:
        network.testMesh(1)
    if basic:
        network.testMesh(2)
    
#begin loop
go = True
while go:
    for current in gui.interface:
        current.available = True
    if POPULATION_SIZE > 30:
        gui.interface[FULL_MESH].available = False
    if POPULATION_SIZE > 70:
        gui.interface[BATMAN_MESH].available = False
    if ((POPULATION_SIZE > 50 and batman) or (POPULATION_SIZE > 15 and FULL_MESH) or (POPULATION_SIZE > 25 and dijkstras)):
        gui.interface[BEGIN_MOVEMENT].available = False
    
   #draw relevant information to screen
    gui.showCity(city)
    gui.showButtonPanel(city)
    gui.showNodes(world)
    gui.drawMesh(network)
    power, loss, devices = network.getLossAndPower()
    gui.drawGraphs(power, loss, city, devices, world)

    #if user asks to quit
    event = gui.getEvents()
    if event == QUIT:
        go = False

    #user ased to repopulate
    if event == POPULATE:
        refresh()
       
    if event == DIJKSTRAS_MESH:
        if dijkstras:
            dijkstras = False
        else:
            dijkstras = True
            batman = False
            fullMesh = False
            slim = False
            blank = False
            basic = False
        refresh(False)

    if event == BATMAN_MESH:
        if batman:
            batman = False
        else:
            batman = True
            dijkstras = False
            fullMesh = False
            slim = False
            blank = False
            basic = False

        refresh(False)

    if event == FULL_MESH:
        if fullMesh:
            fullMesh = False
        else:
            fullMesh = True
            dijkstras = False
            batman = False
            slim = False
            blank = False
            basic = False
        refresh(False)

    if event == TRAIN:
        network.train()

    if event == SLIM:
        if(slim):
            slim = False
        else:
            slim = True
            blank = False
            basic = False
            batman = False
            dijkstras = False
            fullMesh = False
        refresh(False)
    if event == BLANK:
        if blank:
            blank = False
        else:
            slim = False
            blank = True
            basic = False
            batman = False
            dijkstras = False
            fullMesh = False
        refresh(False)
            
    if event == BASIC:
        if basic:
            basic = False
        else:
            slim = False
            blank = False
            basic = True
            batman = False
            dijkstras = False
            fullMesh = False
        refresh(False)

    if event == DECREASE_NODE_COUNT:
        POPULATION_SIZE -= 10
        refresh()
    if event == INCREASE_NODE_COUNT:
        POPULATION_SIZE += 10
        refresh()

#close program
gui.pygame.quit()

