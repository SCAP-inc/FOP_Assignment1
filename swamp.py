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

DUCK_SPEED = 30


class Duck:
    time2hatch = 4
    states = ["egg", "adult"]

    def __init__(self, pos):
        self.pos = pos
        self.state = self.states[0]
        self.age = 0

    def __str__(self):
        return self.state + " @ " + str(self.pos)

    def stepChange(self):
        self.age += 1
        if self.state == "egg":
            if self.age > self.time2hatch:
                self.state = "adult"
        else:
            speed = DUCK_SPEED
            if self.age > 20:
                speed = DUCK_SPEED / 3
            xmov = random.randint(-speed, speed)
            ymov = random.randint(-speed, speed)
            self.pos[0] += xmov
            self.pos[1] += ymov

    def getSize(m):
        if m.state == "egg":
            size = 5
        else:
            size = 15
        return size


class Newt:

    state = "newt"

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
