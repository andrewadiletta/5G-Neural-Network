
#import packages
import pygame
from pygame import mouse
import mesh
import random as rand

#define colors for easy reference
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED  = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (200, 150, 150)
LIGHT_GREEN = (150, 150, 200)
BLUE = (0, 0, 255)

#pygame constants
FPS = 30
size = (1050, 700)


#set up pygame screen
screen = pygame.display.set_mode(size)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)
pygame.display.set_caption("Dr. Lucky's Cool Game")
interface = []
RESOLUTION = 25


#show city on screen
def showCity(city):
    pygame.display.flip()
    screen.fill(WHITE)
    blocks = city.buildBasicCity()
    for current in blocks:
        pygame.draw.rect(screen, BLACK, [current[0], current[1], current[2], current[3]],2)

def buildButtonPanel(city):
    numOfButtons = 12
    for i in range(numOfButtons):
        tmp = Button(city.width+25, (city.height*i)/numOfButtons, 200, city.height/numOfButtons)
        interface.append(tmp)
    interface[0].setText("Increase Node Count")
    interface[0].touch = True
    interface[1].setText("Decrease Node Count")
    interface[1].touch= True
    interface[2].setText("Next City")
    interface[2].touch = True
    interface[3].setText("Begin Movement")
    interface[4].setText("Draw Full Mesh")
    interface[5].setText("Draw Batman Mesh")
    interface[6].setText("Dijkstras Algorithum")
    interface[7].setText("Train Skynet Algorithum")
    interface[8].setText("Blank Skynet Algorithum")
    interface[9].setText("Slim Skynet Algorithum")
    interface[10].setText("Basic Skynet Algorithum")
    interface[11].setText("Shuffle")
    interface[11].touch = True

def showButtonPanel(self):
    for current in interface:
        current.draw()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def drawGlass(input, start, city):
    for y in range(RESOLUTION):
        for x in range(RESOLUTION):
            colorRaw = translate(input[(x*RESOLUTION)+y], 0, 1, 255, 0)
            if(colorRaw < 255):
                color = (colorRaw, colorRaw, colorRaw)
            elif(colorRaw > 255):
                color = (255, 255, 255)
            elif(colorRaw < 0):
                 color = (0, 0, 0)
            if(int(translate(start.x, 0, city.width, 0, 100)) == x and int(translate(start.y, 0, city.height, 0, 100)) == y):
                color = (0, 0, 255)
            pygame.draw.rect(screen, color, [(city.width/RESOLUTION)*x,
                                             (city.height/RESOLUTION)*y, city.width/RESOLUTION, city.height/RESOLUTION],0)

def drawGraphs(power, loss, city, devices, world):
    powerLength = translate(power, 0, 100, 0, city.width)
    powerColorRaw = translate(power, 0, 100, 0, 255)
    lossLength = translate(loss, 0, 255, 0, city.width)
    if powerColorRaw < 255:
        powerColor = (powerColorRaw, 255-powerColorRaw, 0)
    else:
        powerColor = (255, 0, 0)
        powerLength = city.width

    if(loss < 255):
        lossColor = (loss, 255-loss, 0)
    else:
        lossColor = (255, 0, 0)

    devicesLength = translate(devices/len(world), 0, 1, 0, city.width)
    devicesColorRaw = translate(devices/len(world), 0, 1, 0, 255)
    devicesColor = (devicesColorRaw, 255-devicesColorRaw, 0)
    
    pygame.draw.rect(screen, powerColor, [0, city.height, powerLength, 50],0)
    pygame.draw.rect(screen, lossColor, [0, city.height+50, lossLength, 50],0)
    pygame.draw.rect(screen, devicesColor, [0, city.height+100, devicesLength, 50],0)
    
    textsurface2 = myfont.render("System Power Consumption", False, (0, 0, 0))
    screen.blit(textsurface2,(20, city.height+20))
    textsurface3 = myfont.render("System Average Signal Loss", False, (0, 0, 0))
    screen.blit(textsurface3,(20, city.height+70))
    textsurface3 = myfont.render("System Device Usage", False, (0, 0, 0))
    screen.blit(textsurface3,(20, city.height+120))
    

    
#draw the nodes to screen
def showNodes(population):
    index = 0
    for current in population:
        if index == 0:
            pygame.draw.ellipse(screen, BLUE, [current.x, current.y, 10, 10],0)
        elif index == len(population)-1:
            pygame.draw.ellipse(screen, RED, [current.x, current.y, 10, 10],0)
        else:
            pygame.draw.ellipse(screen, GREEN, [current.x, current.y, 10, 10],0)
        index = index+1

def moveNodes(population, city):
    for current in population:
        direction = rand.randint(0, 1000)
        if(direction == 1):
            current.direction = rand.randint(0, 360)
         
        xMove = cos(radians(current.direction))
        yMove = sin(radians(current.direction))
        if(not pause):
            if(xMove >= 0 and current.x < city.width-10 and city.onRoad(current)):
                current.x += cos(radians(monster[2]))*speed
            elif(xMove < 0 and monster[0] > creatureSize and onRoad(monster, size)):
                monster[0] += cos(radians(monster[2]))*speed
            else:
                monster[2] = opposite(monster[2])
                monster[0] += cos(radians(monster[2]))*speed*2
                monster[1] += sin(radians(monster[2]))*speed*2
                    
            if(yMove >= 0 and monster[1] < height-creatureSize and onRoad(monster, size)):
                monster[1] += sin(radians(monster[2]))*speed
            elif(yMove < 0 and monster[1] > creatureSize and onRoad(monster, size)):
                monster[1] += sin(radians(monster[2]))*speed
            else:
                monster[2] = opposite(monster[2])
                monster[0] += cos(radians(monster[2]))*speed*2
                monster[1] += sin(radians(monster[2]))*speed*2


#draw lines to represent connections in mesh network
def drawMesh(myMesh):
    for line in myMesh.getConnections():
        color = (line.strength, 255-line.strength, 0)
        locs = line.getDrawable()
        pygame.draw.line(screen, color, (locs[0], locs[1]), (locs[2], locs[3]),2)

def getEvents():
    output = -1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                output = 12
                print("User asked to quit.")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for current in interface:
                    if(mouse.get_pos()[0] > current.x and mouse.get_pos()[0] < current.x + current.width and
                       mouse.get_pos()[1] > current.y and mouse.get_pos()[1] < current.y + current.height and current.available):
                        output = interface.index(current)
                        if(not current.touch):
                            if(current.on):
                                current.on = False 
                            else:
                                for currentButton in interface:
                                    currentButton.on = False
                                current.on = True
                    
    return output

class Button:
    available = True
    on = False
    touch = False
    def __init__(self, myX, myY, myWidth, myHeight, myText="", oneTouch=False):
        self.x = myX
        self.y = myY
        self.width = myWidth
        self.height = myHeight
        self.text = myText
        self.touch = oneTouch

    def setText(self, inText):
        self.text = inText
    def draw(self):
        if(mouse.get_pos()[0] > self.x and mouse.get_pos()[0] < self.x + self.width and
           mouse.get_pos()[1] > self.y and mouse.get_pos()[1] < self.y + self.height and self.available):
            pygame.draw.rect(screen, GREY, [self.x, self.y, self.width, self.height],0)
            pygame.draw.rect(screen, BLACK, [self.x, self.y, self.width, self.height],2)

        elif self.available and not self.on:
            pygame.draw.rect(screen, BLACK, [self.x, self.y, self.width, self.height],2)
        elif self.available and self.on:
            pygame.draw.rect(screen, LIGHT_GREEN, [self.x, self.y, self.width, self.height],0)
            pygame.draw.rect(screen, BLACK, [self.x, self.y, self.width, self.height],2)
        else: 
            pygame.draw.rect(screen, DARK_GREY, [self.x, self.y, self.width, self.height],0)
            pygame.draw.rect(screen, BLACK, [self.x, self.y, self.width, self.height],2)
        textsurface = myfont.render(self.text, False, (0, 0, 0))
        screen.blit(textsurface,(self.x+15,self.y+15))
