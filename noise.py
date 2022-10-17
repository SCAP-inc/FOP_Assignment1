#======================================================
# Modules
#======================================================

#Import all modules
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import pickle
import cv2

def generateAndSaveHeightMap(terrain):
    """
    Function To generate Perlin noise given a specific terrain and save it
    :param terrain: cv2 image
    png or jpg image imported through cv2
    :return: none
    """
    noise = PerlinNoise(octaves=5, seed=1)
    xpix, ypix = terrain.shape[1], terrain.shape[0]
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    with open('heightmap.ob', 'wb') as fp:
        pickle.dump(pic, fp)

def visualizeCurrentTerrain():
    """
    Function to visualize the current noise as terrain given a file

    :return: none
    """
    heightmap = []
    with open('heightmap.ob', 'rb') as fp:
        heightmap = pickle.load(fp)

    plt.imshow(heightmap)
    plt.show()

if __name__ == "__main__":
    visualizeCurrentTerrain()
