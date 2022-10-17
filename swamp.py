#
# Author :
# ID :
#
# swamp.py - Class definitions for simulation of swamp life
#
# Revisions:
#
# 01/09/2022 – Base version for assignment
#

# ======================================================
# Modules
# ======================================================

import random
import math
import cv2

# Quick Map Color Key
mapKey = {29: "grass", 87: "wall", 234: "water", 76: "bush"}


def getTerrainColor(terrain, posX, posY):
    """
    Function to get terrain color from position

    :param terrain: cv2 image
    png or terrain image imported through opencv

    :param posX: int
    X position of image

    :param posY: int
    Y position of image

    :return: array
    Array with three elements giving red, green and blue values

    """
    return terrain[posY, posX]


class Duck:
    """
    Class to define a duck object

    ...

    Attributes
    ----------
    time2hatch : int
        Time taken to hatch from an egg
    states : array
        Different states of the animal in it's life cycle
    stomachSize : int
        Time taken before the animal is hungry again
    """
    time2hatch = 4
    states = ["egg", "adult"]
    stomachSize = 10

    def __init__(self, pos):
        """
        Initialize duck object given a position
        :param pos: array
        Array with two elements giving x and y positions

        Attributes
        ----------
        pos : array
            array containing the x and y position of the object
        state : array
            current state of the creature's lifecycle
        age : int
            current age of the creature
        parent : int
            fixed state between 1 and 0 to know if the creature has mated before
        name : str
            name of creature object
        hunger : int
            hunger level of creature
        """

        self.pos = pos
        self.state = self.states[0]
        self.age = 0
        self.parent = 0
        self.name = 'duck'
        self.hunger = self.stomachSize

    def __str__(self):
        """
        Method to print object state and position
        :return: str
        String with name, state and position of object
        """
        return self.name + " " + self.state + " @ " + str(self.pos)

    def interactWithTerrain(self, xmov, ymov, terrain):
        """
        Function to allow creature object to interact with terrain

        :param xmov: int
        Amount of movement in x direction

        :param ymov:
        Amount of movement in y direction

        :param terrain: cv2 image
        Png or jpg image imported through cv2

        :return: tuple
        Amount of movement in x and y directions

        """
        XMAX = terrain.shape[1]
        YMAX = terrain.shape[0]

        # Get possible future positions of object
        futureX = self.pos[0] + xmov
        futureY = self.pos[1] + ymov

        # Get Color of terrain at the future x and y positions
        terrainColor = self.getTerrainColor(terrain, futureX, futureY)
        terrainColorBlue = terrainColor[2]
        terrainType = mapKey[terrainColorBlue]

        # Affect movement of bject based on the terrain type
        if (terrainType == "wall"):
            xmov = -xmov
            ymov = -ymov
        return xmov, ymov

    def interactWithCreatures(self, creatures, speed):
        """
        Function to allow creature object to interact with others

        :param creatures: array
        List of creatures in simulation

        :param speed: int
        Speed of creature

        :return: tuple
        Amount of movement in x and y directions

        """

        # Get positions of creature object
        xPos = self.pos[0]
        yPos = self.pos[1]

        # Make Empty distance arrays
        distancesToOthers = []
        distancesToFood = []
        distancesToDucks = []

        # Copy creatures array and remove self
        otherCreatures = []
        otherCreatures = creatures.copy()
        otherCreatures.remove(self)

        # Iterate through other creatures
        for c in otherCreatures:
            # Get distance from other creatures
            dX = c.pos[0]
            dY = c.pos[1]
            distance = math.dist((xPos, yPos), (dX, dY))
            distancesToOthers.append(distance)

            # If other creature is an adult duck and not a parent, procreate
            if (c.name == "duck"):
                distancesToDucks.append(distance)

                if (c.state == "adult") and (c.parent == 0):
                    if distance < self.getSize():
                        print("Make a Duck!")
                        creatures.append(Duck([xPos, yPos]))
                        c.parent = 1
                        self.parent = 1

            # If other creature is a newt eat it and fill the duck's stomach
            elif (c.name == "newt"):
                distancesToFood.append(distance)
                if distance < self.getSize():
                    print("Duck ate a Newt!")
                    creatures.remove(c)
                    self.hunger = self.stomachSize

            # If other creature is a shrimp eat it and fill the ducks stomach
            elif (c.name == "shrimp"):
                distancesToFood.append(distance)
                if distance < self.getSize():
                    print("Duck ate a Shrimp!")
                    creatures.remove(c)
                    self.hunger = self.stomachSize

            # If other creature is a plant keep it alive but fill the ducks stomach
            if (c.name == "plant"):
                distancesToFood.append(distance)
                if distance < self.getSize():
                    self.hunger = self.stomachSize
                    print('Duck ate a Plant')

        dX = 0
        dY = 0

        # Prioritise hunger
        # If the creature object is hungry look for food
        # If the creature is not hungry and not a parent, look for a mate
        if (self.hunger < int(self.stomachSize / 2)) and (len(distancesToFood) > 0):
            shortestDistance = min(distancesToFood)
            closestCreature = otherCreatures[distancesToOthers.index(shortestDistance)]
            dX = closestCreature.pos[0]
            dY = closestCreature.pos[1]
        else:
            shortestDistance = min(distancesToDucks)
            closestCreature = otherCreatures[distancesToOthers.index(shortestDistance)]
            dX = closestCreature.pos[0]
            dY = closestCreature.pos[1]

        xmov = 0
        ymov = 0

        if dX > xPos:
            xmov = speed
        else:
            xmov = -speed

        if dY > yPos:
            ymov = speed
        else:
            ymov = -speed

        return xmov, ymov

    def stepChange(self, terrain, heightmap, creatures, creatureSpeed):
        """
        Function to update the position and attributes of an object
        :param terrain: cv2 image
        png or jpg image imported through opencv

        :param heightmap: numpy array
        2x2 array made through perlin noise function to simulate terrain

        :param creatures: array
        List containing all creatures in simulation

        :param creatureSpeed: int
        Speed of creature

        :return:none
        """

        # Update current hunger
        self.hunger -= 1

        # Update age and state of object
        self.age += 1
        if self.state == "egg":
            if self.age > self.time2hatch:
                self.state = "adult"
        else:

            # Alter creature speed based on age
            speed = creatureSpeed
            if self.age > 50:
                speed = creatureSpeed / 2

            # Adjust Speed for Height of Terrain
            height = heightmap[self.pos[1]][self.pos[0]] * 255
            speed = int(speed * height / 255)

            # If hungry or needs a mate seek food or a mate
            # Else perform a random walk
            if (self.parent == 0) or (self.hunger < int(self.stomachSize / 2)):
                movement = self.interactWithCreatures(creatures, speed)
            else:
                xmov = random.randint(-1, 1) * speed
                ymov = random.randint(-1, 1) * speed
                movement = [xmov, ymov]

            # Interact with terrain
            movement = self.interactWithTerrain(movement[0], movement[1], terrain)

            # Update Positions
            self.pos[0] += movement[0]
            self.pos[1] += movement[1]

    def getSize(m):
        """
        Get the size of the current object

        :return: int
        Size of object

        """
        if m.state == "egg":
            size = 40
        else:
            size = 100
        return size

    def getTerrainColor(self, terrain, posX, posY):
        """
        Function to get terrain color from position

        :param terrain: cv2 image
        png or terrain image imported through opencv

        :param posX: int
        X position of image

        :param posY: int
        Y position of image

        :return: array
        Array with three elements giving red, green and blue values

        """
        return terrain[posY, posX]


class Newt:
    time2hatch = 2
    time2grow = 3
    states = ["egg", "tadpole", "adult"]
    stomachSize = 7

    def __init__(self, position):
        self.pos = position
        self.state = self.states[0]
        self.name = 'newt'
        self.age = 0
        self.parent = 0
        self.hunger = self.stomachSize

    def __str__(self):
        return self.state + " @ " + str(self.pos)

    def stepChange(self, terrain, heightmap, creatures, creatureSpeed):

        self.hunger -= 1

        self.age += 1
        if self.state == "egg":
            if self.age > self.time2hatch:
                self.state = "tadpole"

        else:
            if self.state == "tadpole":
                if self.age > self.time2grow:
                    self.state = "adult"
            speed = creatureSpeed
            # Slow speed if newt age more than 15
            if self.age > 25:
                speed = creatureSpeed / 2

            # Adjust Speed for Height of Terrain
            height = heightmap[self.pos[1]][self.pos[0]] * 255
            speed = int(speed * height / 255)

            if (self.parent == 0) or (self.hunger < int(self.stomachSize / 2)):
                movement = self.interactWithCreatures(creatures, speed)
            else:
                xmov = random.randint(-1, 1) * speed
                ymov = random.randint(-1, 1) * speed
                movement = [xmov, ymov]

            movement = self.interactWithTerrain(movement[0], movement[1], terrain)

            self.pos[0] += movement[0]
            self.pos[1] += movement[1]

    def getSize(m):
        if m.state == "egg":
            size = 30
        elif m.state == "tadpole":
            size = 40
        else:
            size = 80
        return size

    def interactWithTerrain(self, xmov, ymov, terrain):
        XMAX = terrain.shape[1]
        YMAX = terrain.shape[0]
        futureX = self.pos[0] + xmov
        futureY = self.pos[1] + ymov
        terrainColor = self.getTerrainColor(terrain, futureX, futureY)
        terrainColorBlue = terrainColor[2]
        terrainType = mapKey[terrainColorBlue]
        # print(terrainType)
        if (terrainType == "wall"):
            xmov = -xmov
            ymov = -ymov

        # if 0 < futureX < XMAX:
        #     xmov = - xmov
        # if 0 < futureY < YMAX:
        #     ymov = - ymov

        return xmov, ymov

    def interactWithCreatures(self, creatures, speed):
        xPos = self.pos[0]
        yPos = self.pos[1]

        distancesToOthers = []
        distancesToNewts = []
        distancesToShrimp = []

        otherCreatures = []
        otherCreatures = creatures.copy()
        otherCreatures.remove(self)
        for c in otherCreatures:
            # If an adult newt interacts with another adult newt
            dX = c.pos[0]
            dY = c.pos[1]
            distance = math.dist((xPos, yPos), (dX, dY))
            distancesToOthers.append(distance)
            if (c.name == "newt"):
                distancesToNewts.append(distance)
                if (c.state == "adult") and (c.parent == 0):
                    if distance < self.getSize():
                        print("Make a Newt!")
                        creatures.append(Newt([xPos, yPos]))
                        c.parent = 1
                        self.parent = 1
            # Newt interacting with a shrimp
            elif (c.name == "shrimp"):
                distancesToShrimp.append(distance)
                if distance < self.getSize():
                    print("Newt ate a Shrimp!")
                    creatures.remove(c)
                    self.hunger = self.stomachSize

        dX = 0
        dY = 0

        if (self.hunger < int(self.stomachSize / 2)) and (len(distancesToShrimp) > 0):
            shortestDistance = min(distancesToShrimp)
            closestCreature = otherCreatures[distancesToOthers.index(shortestDistance)]
            dX = closestCreature.pos[0]
            dY = closestCreature.pos[1]
        else:
            shortestDistance = min(distancesToNewts)
            closestCreature = otherCreatures[distancesToOthers.index(shortestDistance)]
            dX = closestCreature.pos[0]
            dY = closestCreature.pos[1]

        xmov = 0
        ymov = 0

        if dX > xPos:
            xmov = speed
        else:
            xmov = -speed

        if dY > yPos:
            ymov = speed
        else:
            ymov = -speed

        return xmov, ymov

    def getTerrainColor(self, terrain, posX, posY):
        # print(terrain)
        return terrain[posY, posX]


class Shrimp:
    time2hatch = 3
    time2grow = 3
    states = ["egg", "larvae", "adult"]
    stomachSize = 3

    def __init__(self, pos):
        self.pos = pos
        self.state = self.states[0]
        self.age = 0
        self.parent = 0
        self.name = 'shrimp'
        self.hunger = self.stomachSize

    def __str__(self):
        return self.state + " @ " + str(self.pos)

    def interactWithTerrain(self, xmov, ymov, terrain):
        XMAX = terrain.shape[1]
        YMAX = terrain.shape[0]
        futureX = self.pos[0] + xmov
        futureY = self.pos[1] + ymov
        terrainColor = self.getTerrainColor(terrain, futureX, futureY)
        terrainColorBlue = terrainColor[2]
        terrainType = mapKey[terrainColorBlue]
        # print(terrainType)
        if (terrainType == "grass"):
            xmov = -xmov
            ymov = -ymov

        # if 0 < futureX < XMAX:
        #     xmov = - xmov
        # if 0 < futureY < YMAX:
        #     ymov = - ymov

        return xmov, ymov

    def stepChange(self, terrain, heightmap, creatures, creatureSpeed):

        self.hunger -= 1

        self.age += 1
        if self.state == "egg":
            if self.age > self.time2hatch:
                self.state = "larvae"

        else:
            if self.state == "larvae":
                if self.age > self.time2grow:
                    self.state = "adult"

            speed = creatureSpeed
            # Slow speed if shrimp age more than 15
            if self.age > 15:
                speed = creatureSpeed / 3

            # Adjust Speed for Height of Terrain
            height = heightmap[self.pos[1]][self.pos[0]] * 255
            speed = int(speed * height / 255)

            if (self.parent == 0) or (self.hunger < int(self.stomachSize / 2)):
                movement = self.interactWithCreatures(creatures, speed)
            else:
                xmov = random.randint(-1, 1) * speed
                ymov = random.randint(-1, 1) * speed
                movement = [xmov, ymov]

            movement = self.interactWithTerrain(movement[0], movement[1], terrain)

            self.pos[0] += movement[0]
            self.pos[1] += movement[1]

    def getSize(m):
        if m.state == "egg":
            size = 10
        elif m.state == "larvae":
            size = 30
        else:
            size = 60
        return size

    def interactWithCreatures(self, creatures, speed):
        xPos = self.pos[0]
        yPos = self.pos[1]

        distancesToShrimp = []

        otherCreatures = []
        otherCreatures = creatures.copy()
        otherCreatures.remove(self)
        for c in otherCreatures:
            dX = c.pos[0]
            dY = c.pos[1]
            distance = math.dist((xPos, yPos), (dX, dY))
            if (c.name == 'shrimp'):
                distancesToShrimp.append(distance)
                if (c.state == "adult") and (c.parent == 0):
                    if distance < self.getSize():
                        print("Make a Shrimp!")
                        creatures.append(Shrimp([xPos, yPos]))
                        c.parent = 1
                        self.parent = 1

        dX = 0
        dY = 0

        if (len(distancesToShrimp) > 0):
            shortestDistance = min(distancesToShrimp)
            closestCreature = otherCreatures[distancesToShrimp.index(shortestDistance)]
            dX = closestCreature.pos[0]
            dY = closestCreature.pos[1]

        xmov = 0
        ymov = 0

        if dX > xPos:
            xmov = speed
        else:
            xmov = -speed

        if dY > yPos:
            ymov = speed
        else:
            ymov = -speed

        return xmov, ymov

    def getTerrainColor(self, terrain, posX, posY):
        return terrain[posY, posX]


class Plant:

    def __init__(self, pos):
        self.pos = pos
        self.name = 'plant'
        self.state = 'plant'

    def getSize(m):
        return 20
