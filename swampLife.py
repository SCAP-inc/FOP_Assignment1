#
# Author :
# ID :
#
# swampLife.py - Basic simulation of swamp life for assignment, S2 2022.
#
# Revisions:
#
# 01/09/2022 – Base version for assignment
#

import random
import matplotlib.pyplot as plt
import numpy as np
import time
from swamp import Duck, Newt

XMAX = 1000
YMAX = 500


def main():
    ducks = []
    newts = []

    for i in range(5):
        randX = random.randint(0, XMAX)
        randY = random.randint(0, YMAX)
        ducks.append(Duck([randX, randY]))
        print(ducks[i])

    for i in range(10):
        randX = random.randint(0, XMAX)
        randY = random.randint(0, YMAX)
        newts.append(Newt([randX, randY]))
        print(newts[i])

    for i in range(30):
        print("\n ### TIMESTEP ", i, "###")
        xvalues = []
        yvalues = []
        sizes = []
        for d in ducks:
            d.stepChange()
            # print(d)
            xvalues.append(d.pos[0])
            yvalues.append(d.pos[1])
            sizes.append(d.getSize())

        plt.scatter(
            xvalues, yvalues, s=sizes, color="orange"
        )  # Note plt origin is bottom left
        plt.xlim(0, XMAX)
        plt.ylim(0, YMAX)
        plt.pause(1)
        plt.clf()


if __name__ == "__main__":
    print("\nShe turned me into a newt!\n")
    main()
    print("\nI got better!\n")
