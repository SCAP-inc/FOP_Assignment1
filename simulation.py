import random
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
from animals import Duck, Newt

# XMAX = 1000
# YMAX = 500

terrain = cv2.imread("terrain.png")
terrain = cv2.cvtColor(terrain, cv2.COLOR_BGR2RGB)

heightmap = cv2.imread("heightmap.png")
heightmap = cv2.cvtColor(heightmap, cv2.COLOR_BGR2GRAY)

XMAX = terrain.shape[1]
YMAX = terrain.shape[0]

PADDING = 50
TIMESTEPS = 50


def main():
    ducks = []
    newts = []
    shrimps = []

    fig, ax = plt.subplots()

    for i in range(5):
        randX = random.randint(0 + PADDING, XMAX - PADDING)
        randY = random.randint(0 + PADDING, YMAX - PADDING)
        ducks.append(Duck([randX, randY]))
        print(ducks[i])

    for i in range(10):
        randX = random.randint(0, XMAX)
        randY = random.randint(0, YMAX)
        newts.append(Newt([randX, randY]))
        print(newts[i])

    for i in range(TIMESTEPS):
        print("\n ### TIMESTEP ", i, "###")
        xvalues = []
        yvalues = []
        sizes = []

        allCreatures = []
        allCreatures.append(ducks, newts, shrimps)

        for creature in allCreatures:

            creature.stepChange(terrain, heightmap, allCreatures)

            # print(d)
            xvalues.append(d.pos[0])
            yvalues.append(d.pos[1])
            sizes.append(d.getSize())
            if d.age > 30:
                ducks.remove(d)

        ax.imshow(terrain)
        plt.scatter(
            xvalues, yvalues, s=sizes, color="orange"
        )  # Note plt origin is bottom left
        plt.xlim(0, XMAX)
        plt.ylim(0, YMAX)
        plt.axis("off")
        plt.pause(1)
        plt.cla()


if __name__ == "__main__":
    print("\nShe turned me into a newt!\n")
    main()
    print("\nI got better!\n")
