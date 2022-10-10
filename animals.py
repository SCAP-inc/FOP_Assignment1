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
import random
import math
import cv2

DUCK_SPEED = 50
NEWT_SPEED = 10
SHRIMP_SPEED = 5

mapKey = {29: "grass", 87: "wall", 234: "water", 76: "bush"}


class Duck:
    time2hatch = 4
    states = ["egg", "adult"]

    def __init__(self, pos):
        self.pos = pos
        self.state = self.states[0]
        self.age = 0
        self.parent = 0

    def __str__(self):
        return self.state + " @ " + str(self.pos)

    def interactWithTerrain(self, xmov, ymov, terrain):
        futureX = self.pos[0] + xmov
        futureY = self.pos[1] + ymov
        terrainColor = self.getTerrainColor(terrain, futureX, futureY)
        terrainColorBlue = terrainColor[2]
        terrainType = mapKey[terrainColorBlue]
        print(terrainType)
        if (terrainType == "wall") or (terrainType == "bush"):
            xmov = -xmov
            ymov = -ymov
        return xmov, ymov

    def interactWithCreatures(self, ducks):
        xPos = self.pos[0]
        yPos = self.pos[1]

        otherDucks = ducks.copy()
        otherDucks.remove(self)
        for d in otherDucks:
            if (d.state == "adult") and (d.parent == 0):
                dX = d.pos[0]
                dY = d.pos[1]
                distance = math.dist((xPos, yPos), (dX, dY))
                # print(distance)
                # print(self.getSize())
                if distance < self.getSize() * 5:
                    print("Make a Duck!")
                    ducks.append(Duck([xPos, yPos]))
                    d.parent = 1
                    self.parent = 1

    def stepChange(self, terrain, heightmap, ducks):
        XMAX = terrain.shape[1]
        YMAX = terrain.shape[0]

        self.age += 1
        if self.state == "egg":
            if self.age > self.time2hatch:
                self.state = "adult"

        else:
            speed = DUCK_SPEED
            if self.age > 20:
                speed = DUCK_SPEED / 3

            # Adjust Speed for Height of Terrain
            height = heightmap[self.pos[1], self.pos[0]]
            speed = int(speed * height / 255)

            xmov = random.randint(-speed, speed)
            ymov = random.randint(-speed, speed)
            futureX = self.pos[0] + xmov
            futureY = self.pos[1] + ymov

            if 0 < futureX < XMAX:
                futureX = self.pos[0] - xmov
            if 0 < futureY < YMAX:
                futureY = self.pos[0] - ymov

            movement = self.interactWithTerrain(xmov, ymov, terrain)
            self.interactWithCreatures(ducks)

            self.pos[0] += movement[0]
            self.pos[1] += movement[1]

    def getSize(m):
        if m.state == "egg":
            size = 5
        else:
            size = 15
        return size

    def getTerrainColor(self, terrain, posX, posY):
        # print(terrain)
        return terrain[posY, posX]


class Newt:
    states = ["egg", "tadpole", "adult"] 

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return self.state + " @ " + str(self.pos)

    def stepChange(self):
        XMAX = terrain.shape[1]
        YMAX = terrain.shape[0]

        self.age += 1
        if self.state == "egg":
            if self.age > self.time2hatch:
                self.state = "adult"

        else:
            speed = NEWT_SPEED
            if self.age > :
                speed = DUCK_SPEED / 3

            # Adjust Speed for Height of Terrain
            height = heightmap[self.pos[1], self.pos[0]]
            speed = int(speed * height / 255)

            xmov = random.randint(-speed, speed)
            ymov = random.randint(-speed, speed)
            futureX = self.pos[0] + xmov
            futureY = self.pos[1] + ymov

            if 0 < futureX < XMAX:
                futureX = self.pos[0] - xmov
            if 0 < futureY < YMAX:
                futureY = self.pos[0] - ymov

            movement = self.interactWithTerrain(xmov, ymov, terrain)
            self.interactWithCreatures(ducks)

            self.pos[0] += movement[0]
            self.pos[1] += movement[1]

    def getSize(m):
        return 10

    def interactWithCreatures(self, newts, ducks, shrimps):
        xPos = self.pos[0]
        yPos = self.pos[1]

        otherCreatures = []
        otherCreatures = otherCreatures.append(newts, ducks, shrimps)
        otherCreatures.remove(self)
        for creature in otherCreatures:
            # If an adult newt interacts with another adult newt
            creature_type = type(creature).__name__
            if (creature_type == "Newt") and (creature.state == "adult") and (creature.parent == 0):
                dX = creature.pos[0]
                dY = creature.pos[1]
                distance = math.dist((xPos, yPos), (dX, dY))
                # print(distance)
                # print(self.getSize())
                if distance < self.getSize() * 5:
                    print("Make a Newt!")
                    newts.append(Newt([xPos, yPos]))
                    creature.parent = 1
                    self.parent = 1
            #  Newt interacting with a Duck
            elif (creature.state == "adult") and (creature.parent == 0):
                dX = creature.pos[0]
                dY = creature.pos[1]
                distance = math.dist((xPos, yPos), (dX, dY))
                # print(distance)
                # print(self.getSize())
                if distance < self.getSize() * 5:
                    print("Duck ate a Newt!")
                    newts.remove(self)
            # Newt interacting with a shrimp
            elif (creature.state == "shrimp") and (creature.parent == 0):
                dX = creature.pos[0]
                dY = creature.pos[1]
                distance = math.dist((xPos, yPos), (dX, dY))
                # print(distance)
                # print(self.getSize())
                if distance < self.getSize() * 5:
                    print("Newt ate a Shrimp!")
                    shrimps.remove(creature)


class Shrimp:

    state = "shrimp"

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return self.state + " @ " + str(self.pos)


    def stepChange(self):
        self.age += 1
        xmov = 10
        ymov = 10
        self.pos[0] -= xmov
        self.pos[1] -= ymov

    def getSize(m):
        return 10

    def interactWithCreatures(self, newts, ducks, shrimps):
        xPos = self.pos[0]
        yPos = self.pos[1]

        otherCreatures = []
        otherCreatures = otherCreatures.append(newts, ducks, shrimps)
        otherCreatures.remove(self)
        for creature in otherCreatures:
            # If a shrimp interacts with another shrimp
            if (creature.state == "shrimp") and (creature.parent == 0):
                dX = creature.pos[0]
                dY = creature.pos[1]
                distance = math.dist((xPos, yPos), (dX, dY))
                # print(distance)
                # print(self.getSize())
                if distance < self.getSize() * 5:
                    print("Make a Shrimp!")
                    shrimps.append(Shrimp([xPos, yPos]))
                    creature.parent = 1
                    self.parent = 1
            # Shrimp interacting with a Newt
            elif (creature.state == "newt") and (creature.parent == 0):
                dX = creature.pos[0]
                dY = creature.pos[1]
                distance = math.dist((xPos, yPos), (dX, dY))
                # print(distance)
                # print(self.getSize())
                if distance < self.getSize() * 5:
                    print("Newt ate a Shrimp!")
                    shrimps.remove(self)
