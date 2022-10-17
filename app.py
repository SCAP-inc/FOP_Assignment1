#
# Author :
# ID :
#
# app.py - Basic simulation of swamp life for assignment, S2 2022.
#
# Revisions:
#
# 01/09/2022 – Base version for assignment
#

"""
#======================================================
# Modules
#======================================================
"""

#Import Graphics Modules
from svgpath2mpl import parse_path
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib as mpl
import cv2

#Import Built In Python Modules
from pathlib import Path
import pandas as pd
import numpy as np
import random
import pickle
import time

#Import Third Party Modules
from swamp import Duck, Newt, Shrimp, Plant, mapKey, getTerrainColor
from noise import generateAndSaveHeightMap

"""
#======================================================
# Setup
#======================================================
"""

#Set Seed to ensure that all randomised variables stay same between runs
random.seed(10)

#Import Terrain Walls
terrain = cv2.imread("terrain.png")
terrain = cv2.cvtColor(terrain, cv2.COLOR_BGR2RGB)

#Create Empty Heightmap Array
heightmap = []

#Check For heightmap file and create it if it doesn't exist
#Load the file if it already exists
my_file = Path("heightmap.ob")
if my_file.is_file():
    #Heightmap exists already, load the heightmap
    with open('heightmap.ob', 'rb') as fp:
        heightmap = pickle.load(fp)
else:
    #Create Heightmap, save it for future, then load it
    generateAndSaveHeightMap(terrain)

    with open('heightmap.ob', 'rb') as fp:
        heightmap = pickle.load(fp)


"""
#======================================================
# Creature Icons
#======================================================
"""

#SVG Path Icons for Creatures
duck = parse_path("""M 105.572 101.811 c 9.889 -6.368 27.417 -16.464 28.106 -42.166 c 0.536 -20.278 -9.971 -49.506 -49.155 -50.878 C 53.041 7.659 39.9 28.251 36.071 46.739 l -0.928 -0.126 c -1.932 0 -3.438 1.28 -5.34 2.889 c -2.084 1.784 -4.683 3.979 -7.792 4.308 c -3.573 0.361 -8.111 -1.206 -11.698 -2.449 c -4.193 -1.431 -6.624 -2.047 -8.265 -0.759 c -1.503 1.163 -2.178 3.262 -2.028 6.226 c 0.331 6.326 4.971 18.917 16.016 25.778 c 7.67 4.765 16.248 5.482 20.681 5.482 c 0.006 0 0.006 0 0.006 0 c 2.37 0 4.945 -0.239 7.388 -0.726 c 2.741 4.218 5.228 7.476 6.037 9.752 c 2.054 5.851 -27.848 25.087 -27.848 55.01 c 0 29.916 22.013 48.475 56.727 48.475 h 55.004 c 30.593 0 70.814 -29.908 75.291 -92.48 C 180.781 132.191 167.028 98.15 105.572 101.811 Z M 18.941 77.945 C 8.775 71.617 4.992 58.922 5.294 55.525 c 0.897 0.24 2.194 0.689 3.228 1.042 c 4.105 1.415 9.416 3.228 14.068 2.707 c 4.799 -0.499 8.253 -3.437 10.778 -5.574 c 0.607 -0.509 1.393 -1.176 1.872 -1.491 c 0.87 0.315 0.962 0.693 1.176 3.14 c 0.196 2.26 0.473 5.37 2.362 9.006 c 1.437 2.761 3.581 5.705 5.646 8.542 c 1.701 2.336 4.278 5.871 4.535 6.404 c -0.445 1.184 -4.907 3.282 -12.229 3.282 C 30.177 82.591 23.69 80.904 18.941 77.945 Z M 56.86 49.368 c 0 -4.938 4.001 -8.943 8.931 -8.943 c 4.941 0 8.942 4.005 8.942 8.943 c 0 4.931 -4.001 8.942 -8.942 8.942 C 60.854 58.311 56.86 54.299 56.86 49.368 Z M 149.159 155.398 l -20.63 11.169 l 13.408 9.293 c 0 0 -49.854 15.813 -72.198 -6.885 c -11.006 -11.16 -13.06 -28.533 4.124 -38.84 c 17.184 -10.312 84.609 3.943 84.609 3.943 L 134.295 147.8 L 149.159 155.398 Z""")
duck = duck.transformed(mpl.transforms.Affine2D().rotate_deg(180))
duck = duck.transformed(mpl.transforms.Affine2D().scale(-1,1))

newt = parse_path("""M 4010 12778 c -52 -34 -80 -98 -80 -179 c 0 -55 6 -79 36 -145 c 21 -43 39 -98 42 -121 l 5 -43 l -47 0 c -25 0 -90 9 -144 20 c -53 11 -117 24 -141 29 c -81 16 -239 -52 -281 -122 c -53 -86 12 -198 177 -307 c 40 -26 70 -50 68 -52 c -3 -3 6 -15 19 -27 c 18 -17 26 -19 31 -10 c 5 7 4 10 -2 6 c -6 -4 -18 2 -28 13 c -23 25 -24 26 64 -10 c 40 -17 80 -30 90 -31 c 9 0 -3 -6 -26 -14 c -169 -52 -321 -231 -298 -352 c 14 -75 129 -153 251 -170 c 30 -4 48 -13 58 -28 c 23 -35 78 -49 169 -42 c 60 5 90 13 123 32 c 24 14 62 32 84 40 l 41 14 l 20 -32 c 65 -106 78 -290 26 -380 c -37 -62 -77 -84 -198 -107 c -249 -46 -437 -137 -669 -323 c -109 -87 -552 -535 -645 -652 c -217 -271 -335 -510 -400 -810 c -22 -105 -32 -181 -55 -464 c -21 -252 -88 -299 -331 -232 c -163 44 -190 51 -260 60 c -129 18 -223 -20 -340 -138 c -83 -84 -141 -166 -217 -311 c -59 -110 -145 -320 -192 -467 c -18 -57 -37 -103 -42 -103 c -4 0 -83 38 -175 85 c -92 47 -191 94 -221 105 c -62 24 -132 26 -171 5 c -63 -32 -140 -165 -148 -255 c -11 -121 55 -195 273 -305 c 79 -40 138 -75 137 -82 c -2 -7 3 -12 9 -10 c 7 1 14 -8 16 -19 c 5 -36 -59 -80 -126 -88 c -113 -13 -212 -54 -275 -115 c -53 -49 -67 -81 -67 -145 c 0 -46 5 -61 33 -98 c 39 -52 135 -105 210 -118 c 30 -5 71 -20 92 -34 c 44 -30 147 -64 204 -67 c 35 -3 39 -5 30 -22 c -51 -94 -63 -237 -28 -313 c 34 -70 118 -124 196 -124 c 31 0 43 -6 65 -34 c 16 -19 47 -42 73 -52 c 39 -14 52 -15 86 -5 c 50 15 109 69 180 161 c 29 39 55 70 58 70 c 4 0 22 -30 41 -67 c 26 -51 52 -82 104 -125 c 70 -58 159 -108 194 -108 c 10 0 38 -10 63 -22 c 34 -17 62 -23 121 -23 c 69 0 80 3 119 30 c 62 44 89 101 89 191 c 0 97 -25 173 -115 351 c -84 163 -115 260 -115 351 c 0 78 17 120 66 160 c 54 45 110 62 169 51 c 91 -17 121 -29 150 -59 c 24 -25 26 -30 10 -24 c -11 4 -17 4 -13 0 c 3 -4 13 -9 22 -10 c 36 -5 127 -122 199 -256 c 81 -151 124 -307 198 -730 c 93 -536 252 -875 559 -1194 c 97 -101 279 -256 392 -335 c 43 -29 75 -58 71 -64 c -3 -6 -1 -7 5 -3 c 14 8 64 -23 57 -34 c -3 -5 0 -12 6 -16 c 8 -4 9 -3 5 4 c -4 7 -5 12 -2 12 c 10 0 550 -324 681 -410 c 117 -76 245 -170 196 -144 c -9 5 -12 3 -7 -5 c 4 -6 11 -9 15 -7 c 12 8 107 -80 155 -142 c 112 -147 149 -293 126 -506 c -31 -295 -139 -535 -350 -782 c -177 -206 -499 -436 -820 -587 c -480 -225 -1118 -388 -1525 -390 c -157 -1 -205 8 -370 65 c -78 27 -282 124 -398 189 c -139 78 -418 266 -543 366 c -220 175 -434 379 -440 419 c -1 7 -9 35 -18 61 c -8 26 -29 111 -46 188 c -49 226 -70 309 -86 333 c -16 25 -31 21 -43 -10 c -5 -14 -12 6 -24 69 c -31 160 -102 263 -183 263 c -36 0 -40 -8 -66 -125 c -20 -93 -16 -408 6 -520 c 69 -344 222 -674 466 -1007 c 131 -178 392 -425 567 -538 c 29 -18 50 -36 48 -41 c -3 -4 19 -24 47 -45 c 29 -20 47 -30 39 -21 c -7 9 -29 26 -48 38 c -19 12 -32 23 -30 26 c 3 2 43 -18 90 -45 c 47 -27 124 -66 171 -87 c 48 -21 83 -42 79 -48 c -3 -6 -1 -7 6 -3 c 12 8 146 -38 171 -59 c 32 -28 248 -108 402 -149 c 166 -45 321 -67 523 -73 c 278 -8 696 18 1005 63 c 881 128 1614 458 2101 943 c 689 689 912 1802 530 2648 c -27 60 -63 131 -80 159 c -16 27 -53 92 -81 144 c -29 52 -82 140 -119 195 c -70 105 -85 133 -54 100 c 11 -11 35 -33 54 -50 c 19 -16 10 -4 -20 27 c -30 31 -57 56 -60 56 c -3 -1 -55 48 -116 108 c -189 187 -374 312 -685 462 c -484 232 -616 301 -704 369 c -84 64 -90 71 -108 128 c -28 86 -34 242 -14 328 c 40 169 156 301 305 343 c 131 38 259 122 491 324 c 172 149 247 204 345 251 c 125 59 128 60 153 1 c 47 -108 72 -296 72 -526 l -1 -171 l -41 -25 c -64 -39 -152 -131 -191 -201 c -83 -150 -89 -298 -16 -400 c 40 -57 136 -85 202 -60 c 20 8 26 5 41 -24 c 24 -44 73 -70 117 -61 c 70 13 149 67 205 140 c 17 23 47 54 67 68 l 34 27 l 28 -72 c 67 -175 162 -257 297 -257 c 21 0 37 -3 37 -7 c -4 -23 7 -33 63 -58 c 133 -60 243 -39 302 58 c 25 40 30 61 34 130 c 5 101 -13 183 -65 286 l -37 73 l 25 20 c 38 30 99 48 92 27 c -1 -3 4 -6 10 -6 c 7 0 30 -11 53 -25 c 48 -31 112 -53 177 -63 c 26 -4 47 -11 47 -15 c 0 -4 33 -22 73 -41 c 129 -60 244 -48 311 31 c 51 61 42 155 -20 209 c -22 20 -34 39 -34 56 c 0 37 -35 100 -79 143 c -53 50 -130 95 -237 138 c -86 33 -206 90 -173 80 c 12 -3 15 1 12 12 c -5 20 31 62 53 62 c 27 0 115 51 161 93 c 99 92 123 207 64 312 c -17 30 -31 63 -31 72 c 0 58 -96 170 -180 210 c -73 35 -214 43 -310 19 c -115 -29 -306 -133 -370 -201 c -13 -14 -28 -25 -34 -25 c -6 0 -34 33 -62 73 c -81 115 -276 446 -269 457 c 4 6 2 9 -3 8 c -8 -2 -142 186 -142 200 c 0 2 6 0 13 -4 c 7 -4 9 -3 4 2 c -5 5 -12 9 -16 9 c -4 0 -36 32 -72 71 c -147 162 -260 228 -418 245 c -47 5 -102 12 -121 17 c -33 7 -35 10 -32 47 c 10 132 87 277 236 443 c 46 51 57 60 62 45 c 40 -123 112 -269 176 -355 c 40 -55 61 -73 111 -98 c 34 -16 82 -34 107 -38 c 28 -5 56 -19 73 -36 c 41 -41 103 -64 192 -71 c 93 -6 114 -9 255 -37 c 104 -20 150 -44 133 -71 c -3 -6 -1 -7 5 -3 c 7 4 41 -38 89 -111 c 121 -185 228 -275 345 -290 c 24 -4 57 -16 73 -29 c 105 -78 234 -70 282 18 c 22 40 24 180 4 216 c -7 13 -11 25 -9 27 c 6 6 113 -87 111 -96 c -2 -5 5 -5 14 -2 c 12 5 14 3 8 -7 c -5 -8 -4 -11 2 -7 c 5 3 37 -5 70 -18 c 87 -35 196 -51 252 -36 c 56 16 91 51 91 91 c 0 35 -37 113 -74 158 c -17 20 -26 42 -26 65 c 0 24 -9 46 -27 68 c -21 25 -23 31 -10 26 c 10 -4 16 -3 12 3 c -8 14 26 33 160 90 c 204 86 255 118 255 159 c 0 23 -38 55 -85 72 l -34 13 l 20 24 c 32 41 25 80 -24 126 c -67 64 -210 109 -384 123 l -82 6 l 14 27 c 12 24 11 32 -9 76 c -13 28 -37 61 -53 75 c -23 20 -31 36 -35 73 c -8 68 -50 124 -117 159 c -99 50 -238 33 -367 -44 c -64 -39 -160 -137 -199 -204 c -33 -55 -45 -56 -175 -15 c -127 40 -124 37 -117 103 c 14 135 103 240 250 293 c 151 56 308 65 597 35 c 310 -31 385 -35 490 -22 c 134 17 285 69 340 116 c 21 19 169 83 371 161 c 530 203 734 313 909 485 c 76 75 136 155 156 210 c 76 210 55 379 -75 579 c -25 39 -40 72 -37 83 c 2 11 2 16 -1 13 c -4 -3 -19 15 -35 41 c -29 50 -35 68 -18 58 c 16 -10 11 1 -7 16 c -11 10 -14 10 -9 2 c 17 -29 -2 -10 -39 39 c -78 101 -330 294 -550 420 c -257 146 -775 384 -1129 518 c -125 47 -161 49 -356 17 c -301 -50 -321 -58 -555 -214 c -223 -150 -298 -183 -410 -183 c -84 0 -146 24 -319 124 c -183 105 -405 156 -680 156 c -119 0 -259 30 -335 70 c -34 18 -61 36 -61 40 c 0 24 78 115 182 212 c 66 62 131 131 144 154 c 40 68 28 134 -36 187 c -21 18 -30 34 -30 56 c 0 24 -15 48 -63 104 c -75 86 -112 112 -186 134 c -123 35 -258 -9 -354 -119 c -28 -31 -54 -55 -58 -52 c -4 2 -11 -1 -15 -7 c -5 -8 -3 -9 6 -4 c 10 6 12 4 7 -9 c -4 -10 -7 -20 -7 -23 c 0 -13 -49 68 -85 141 c -75 151 -225 270 -357 282 c -55 5 -67 3 -98 -18 Z""")
newt = newt.transformed(mpl.transforms.Affine2D().rotate_deg(180))
newt = newt.transformed(mpl.transforms.Affine2D().scale(-1,1))

tadpole = parse_path("""M 502 10 c 35.7 0 68.5 10.7 98.6 32.2 c 30.1 21.5 55.8 48.6 77.3 81.3 c 21.5 32.7 38.3 68.2 50.5 106.5 c 12.2 38.3 18.3 74 18.3 107 c 0 27.7 -4.6 54.3 -13.9 79.8 c -9.2 25.4 -22.1 48.4 -38.6 68.9 c -16.5 20.5 -36 38 -58.5 52.5 c -22.5 14.5 -46.9 25.1 -73.3 31.7 c 0 12.6 -0.3 24.6 -1 36.2 c -0.7 11.6 -1 23 -1 34.2 c 0.7 23.1 1 45.4 1 66.9 c 0 21.5 -1.7 44.4 -5 68.9 c -4.6 31.7 -14.2 59 -28.7 81.7 c -14.5 22.8 -31.2 42.1 -50 58 s -39 28.7 -60.4 38.6 c -21.5 9.9 -41 17.5 -58.5 22.8 s -32.2 8.8 -44.1 10.4 c -11.9 1.7 -18.2 2.5 -18.8 2.5 h -2 c -5.3 0 -9.7 -1.7 -13.4 -5 c -3.6 -3.3 -6.1 -7.6 -7.4 -12.9 c -0.7 -5.9 1 -11.1 5 -15.4 c 4 -4.3 8.6 -6.8 13.9 -7.4 c 1.3 0 6.9 -0.8 16.8 -2.5 c 9.9 -1.7 22 -4.8 36.2 -9.4 c 14.2 -4.6 29.6 -10.9 46.1 -18.8 c 16.5 -7.9 32.2 -18.5 47.1 -31.7 c 14.9 -13.2 27.9 -29.2 39.1 -48.1 S 496 797.4 500 771 c 2.6 -20.5 2.8 -41.5 0.5 -62.9 s -7.1 -40.8 -14.4 -58 c -5.3 -11.2 -10.7 -23.3 -16.3 -36.2 c -5.6 -12.9 -10.4 -26.3 -14.4 -40.1 c -29.1 -5.3 -55.8 -15 -80.3 -29.2 c -24.4 -14.2 -45.7 -31.7 -63.9 -52.5 c -18.2 -20.8 -32.4 -44.4 -42.6 -70.8 s -15.4 -54.5 -15.4 -84.2 c 0 -33 6.3 -68.7 18.8 -107 c 12.6 -38.3 30.1 -73.8 52.5 -106.5 c 22.5 -32.7 48.7 -59.8 78.8 -81.3 C 433.4 20.7 466.3 10 502 10 L 502 10 Z""")
tadpole = tadpole.transformed(mpl.transforms.Affine2D().rotate_deg(180))
tadpole = tadpole.transformed(mpl.transforms.Affine2D().scale(-1,1))

shrimp = parse_path(""""M 50.85 51.63 C 39.94 50.25 32.07 47 29.78 40.17 a 88.2 88.2 0 0 0 22.5 -4.85 c 10.46 -4 21.85 -7.31 33.53 -5.51 A 46.4 46.4 0 0 1 83.5 42.54 a 44.27 44.27 0 0 1 -4.81 10.75 c -9 -1.58 -18.91 -0.53 -27.84 -1.66 Z M 86.77 62.46 l 0.09 -1.66 a 22.47 22.47 0 0 0 -3 -1.45 c -0.4 -0.15 -0.8 -0.3 -1.19 -0.43 c -6.39 2.44 -9.22 10.06 -9.4 17 C 75.6 71.64 78.76 62.61 84 62.47 Z m -18.84 -7.4 l 4.42 0.67 l -5.07 7.42 C 64.81 66.77 60.88 66 57.22 65 l -21.41 -5.9 C 32 63.45 30 68.67 28 74.54 A 28.62 28.62 0 0 1 32.73 58.3 a 3.64 3.64 0 0 1 3.74 -1.9 l 25.82 6 l 5.64 -7.34 Z M 98.29 85.57 c -5.58 2.3 -8.37 8.61 -9 14.84 c 0.48 -0.34 1 -0.69 1.4 -1 c 1.73 -3.59 3.89 -8 6.81 -9.66 a 20.22 20.22 0 0 0 0.66 -3.13 c 0 -0.33 0.09 -0.67 0.12 -1 Z m -0.79 -6 L 97.65 77 c -0.13 -0.58 -0.28 -1.17 -0.45 -1.74 c -9.07 0.46 -13 9.59 -13.19 17.78 c 2.32 -4.28 5.49 -13.31 10.71 -13.45 Z M 93.41 70 l 0.15 -2.69 l -0.27 -0.4 a 4.09 4.09 0 0 1 -0.52 -1 a 1.44 1.44 0 0 1 -0.25 -0.18 c -8.65 0.82 -12.4 9.73 -12.6 17.74 C 82.24 79.19 85.4 70.16 90.62 70 Z M 27.12 45 c -1.49 -0.35 -2.93 -0.72 -4.33 -1.13 a 61 61 0 0 1 -8.44 -3.06 c -4.84 -2.22 -9.22 -5.14 -11.81 -8.26 A 9.88 9.88 0 0 1 0 27.08 A 7 7 0 0 1 2.3 21.52 c 0.2 -0.2 0.4 -0.39 0.63 -0.58 A 13 13 0 0 1 1.6 16 a 14 14 0 0 1 1 -6 a 14.46 14.46 0 0 1 7.71 -7.37 A 32.55 32.55 0 0 1 22.11 0.05 a 46.74 46.74 0 0 1 19.06 3 a 163.81 163.81 0 0 1 14.77 7.37 c 0.17 0.08 0.34 0.17 0.49 0.26 c 7.33 4 13.4 7.28 18 6.87 a 1 1 0 0 1 0.17 2 l -0.57 0 l 0.86 0.05 c 2.21 0.12 4.39 0.18 6.52 0.17 s 4.22 -0.09 6.32 -0.25 a 1 1 0 1 1 0.16 2 q -3.15 0.24 -6.48 0.25 c -2.19 0 -4.41 -0.05 -6.63 -0.17 c -6.63 -0.36 -13.22 -1.25 -19.81 -2.15 c -5.28 -0.71 -10.57 -1.43 -15.94 -1.87 S 28.61 17 24.14 17 a 43.47 43.47 0 0 0 -11.58 1.44 a 27.17 27.17 0 0 0 -7 3 a 25.66 25.66 0 0 0 4 4.85 a 54.46 54.46 0 0 0 9.15 6.92 c 2.3 1.44 4.8 2.85 7.46 4.23 a 4.49 4.49 0 0 0 -0.8 1.88 C 22.59 38 20 36.5 17.61 35 a 57.23 57.23 0 0 1 -9.49 -7.19 a 27.53 27.53 0 0 1 -4.18 -5.06 l -0.2 0.19 a 5 5 0 0 0 -1.69 4 a 8 8 0 0 0 2.06 4.35 C 6.5 34.18 10.62 36.91 15.2 39 a 59.06 59.06 0 0 0 8.15 3 q 1.24 0.36 2.55 0.69 A 16.27 16.27 0 0 0 27.12 45 Z M 4.6 19.71 A 29.67 29.67 0 0 1 12 16.52 A 45.14 45.14 0 0 1 24.12 15 c 4.6 -0.06 9.68 0.24 15.11 0.69 s 10.69 1.16 16 1.89 s 10.8 1.46 16.2 1.9 c -4.56 -0.75 -9.86 -3.63 -16 -7 L 55 12.24 A 159.65 159.65 0 0 0 40.39 5 a 44.67 44.67 0 0 0 -18.2 -2.89 A 30.51 30.51 0 0 0 11.13 4.45 a 12.37 12.37 0 0 0 -6.66 6.3 a 11.79 11.79 0 0 0 -0.84 5.12 a 10.61 10.61 0 0 0 1 3.84 Z m 51.91 18 a 3.83 3.83 0 1 1 -3.82 3.83 a 3.83 3.83 0 0 1 3.82 -3.83 Z m 32 -7.36 a 43.8 43.8 0 0 1 16.26 7.46 a 41.42 41.42 0 0 1 5.77 5 a 47.76 47.76 0 0 1 -6.39 10.62 a 41.74 41.74 0 0 1 -8.79 8.78 A 24 24 0 0 0 89.29 57 a 29.15 29.15 0 0 0 -7.78 -3.12 a 49.11 49.11 0 0 0 4.57 -10.54 a 50.1 50.1 0 0 0 2.42 -13 Z m 24 14.75 a 45.74 45.74 0 0 1 10 23 a 51.14 51.14 0 0 1 -8.33 6.41 a 41.61 41.61 0 0 1 -11.5 5.27 A 34.24 34.24 0 0 0 97 64.37 a 45.38 45.38 0 0 0 9.29 -9.28 a 52.6 52.6 0 0 0 6.22 -10 Z m 10.32 26.39 a 36.58 36.58 0 0 1 -8.62 26.29 c -0.63 -0.13 -1.26 -0.27 -1.88 -0.42 a 43.55 43.55 0 0 1 -11.25 -4.19 c 0.22 -0.53 0.42 -1.08 0.6 -1.63 a 26.92 26.92 0 0 0 1.2 -9 c 3.6 -0.75 8.3 -2.92 12.73 -5.7 a 57.8 57.8 0 0 0 7.22 -5.32 Z M 112.09 100 q -7.8 7.88 -21 13 c -4.19 3.12 -9 4.46 -12.77 4.07 c -9.5 -1 -9.51 -13.61 -0.44 -13.87 c 2.75 -0.08 6.48 0.71 11.4 2.57 A 27.7 27.7 0 0 0 99.89 95.56 a 46.62 46.62 0 0 0 11.81 4.38 l 0.39 0.1 Z""")
shrimp = shrimp.transformed(mpl.transforms.Affine2D().rotate_deg(180))
shrimp = shrimp.transformed(mpl.transforms.Affine2D().scale(-1,1))

#Terrain Boundaries based on Image height and width
XMAX = terrain.shape[1]
YMAX = terrain.shape[0]

#Terrain Padding
PADDING = 300

#======================================================
# Input variables that can be changed via console
#======================================================

TIMESTEPS = 50

STARTING_DUCKS = 10
STARTING_NEWTS = 20
STARTING_SHRIMP = 20
STARTING_PLANTS = 20

DUCK_SPEED = 80
NEWT_SPEED = 50
SHRIMP_SPEED = 30

summary_dataframe = pd.DataFrame()

#======================================================
# Main Function
#======================================================

def main(summary=True,plots=True):
    """
    Main function to run simulation

    :return: none
    """
    #Make Empty Array to store all creatures
    allCreatures = []

    #Steup subplots
    fig, ax = plt.subplots()

    # Setup Dataframe for collecting creature total statistics
    df = pd.DataFrame(columns=['type', 'state', 'total', 'timestep'])

    #Generate ducks only on grass
    for i in range(STARTING_DUCKS):
        #Run loop until all ducks are generated
        while True:
            #Make random positions
            randX = random.randint(0 + PADDING, XMAX - PADDING)
            randY = random.randint(0 + PADDING, YMAX - PADDING)
            terrainColor = getTerrainColor(terrain, randX, randY)
            terrainColorBlue = terrainColor[2]
            terrainType = mapKey[terrainColorBlue]
            #Only Generate creature on grass
            if (terrainType == "grass"):
                allCreatures.append(Duck([randX, randY]))
                break
            else:
                continue

    for i in range(STARTING_NEWTS):
        #Run while loop until all newts are generated
        while True:
            #Make random positions
            randX = random.randint(0 + PADDING, XMAX - PADDING)
            randY = random.randint(0 + PADDING, YMAX - PADDING)
            terrainColor = getTerrainColor(terrain, randX, randY)
            terrainColorBlue = terrainColor[2]
            terrainType = mapKey[terrainColorBlue]
            #Only generate creature on bush
            if (terrainType == "bush"):
                allCreatures.append(Newt([randX, randY]))
                break
            else:
                continue

    for i in range(STARTING_SHRIMP):
        #Run while loop until all shrimps are generated
        while True:
            randX = random.randint(0 + PADDING, XMAX - PADDING)
            randY = random.randint(0 + PADDING, YMAX - PADDING)
            terrainColor = getTerrainColor(terrain, randX, randY)
            terrainColorBlue = terrainColor[2]
            terrainType = mapKey[terrainColorBlue]
            #Only generate creature on water
            if (terrainType == "water"):
                allCreatures.append(Shrimp([randX, randY]))
                break
            else:
                continue

    for i in range(STARTING_PLANTS):
        #Run while loop until all plants are placed
        while True:
            randX = random.randint(0 + PADDING, XMAX - PADDING)
            randY = random.randint(0 + PADDING, YMAX - PADDING)
            terrainColor = getTerrainColor(terrain, randX, randY)
            terrainColorBlue = terrainColor[2]
            terrainType = mapKey[terrainColorBlue]
            #Only generate creatures on bush
            if (terrainType == "bush"):
                allCreatures.append(Plant([randX, randY]))
                break
            else:
                continue

    # ======================================================
    # Generate Data for each timestep
    # ======================================================

    for i in range(TIMESTEPS):
        print("\n ### TIMESTEP ", i, "###")

        #Create Empty Arrays and Variables to collect data
        totalDucks = 0
        totalNewts = 0
        totalShrimps = 0

        totalDuckEggs = 0
        totalDuckAdults = 0
        totalNewtEggs = 0
        totalNewtTadpoles = 0
        totalNewtAdults = 0
        totalShrimpEggs = 0
        totalShrimpLarvae = 0
        totalShrimpAdults = 0

        DuckEggXValues = []
        DuckEggYValues = []
        DuckEggZValues = []
        DuckEggSizes = []

        DuckAdultXValues = []
        DuckAdultYValues = []
        DuckAdultZValues = []
        DuckAdultSizes = []

        NewtEggXValues = []
        NewtEggYValues = []
        NewtEggZValues = []
        NewtEggSizes = []

        NewtTadpoleXValues = []
        NewtTadpoleYValues = []
        NewtTadpoleZValues = []
        NewtTadpoleSizes = []

        NewtAdultXValues = []
        NewtAdultYValues = []
        NewtAdultZValues = []
        NewtAdultSizes = []

        ShrimpEggXValues = []
        ShrimpEggYValues = []
        ShrimpEggZValues = []
        ShrimpEggSizes = []

        ShrimpLarvaeXValues = []
        ShrimpLarvaeYValues = []
        ShrimpLarvaeZValues = []
        ShrimpLarvaeSizes = []

        ShrimpAdultXValues = []
        ShrimpAdultYValues = []
        ShrimpAdultZValues = []
        ShrimpAdultSizes = []

        PlantXValues = []
        PlantYValues = []
        PlantZValues = []
        PlantSizes = []

        #Iterate through all creatures and update their states
        for c in allCreatures:

            #Update states of ducks and position them
            if c.name == "duck":
                totalDucks += 1
                if c.state == "egg":
                    totalDuckEggs += 1
                    c.stepChange(terrain, heightmap, allCreatures,DUCK_SPEED)
                    DuckEggXValues.append(c.pos[0])
                    DuckEggYValues.append(c.pos[1])
                    DuckEggZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    DuckEggSizes.append(c.getSize()*3)
                if c.state == "adult":
                    totalDuckAdults += 1
                    c.stepChange(terrain, heightmap, allCreatures,DUCK_SPEED)
                    DuckAdultXValues.append(c.pos[0])
                    DuckAdultYValues.append(c.pos[1])
                    DuckAdultZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    DuckAdultSizes.append(c.getSize()*3)

                    #Kill Duck if it's older than 100 timesteps
                    if c.age > 100:
                        allCreatures.remove(c)

            #Update states of newts and position them
            if c.name == "newt":
                totalNewts += 1
                if c.state == "egg":
                    totalNewtEggs += 1
                    c.stepChange(terrain, heightmap, allCreatures,NEWT_SPEED)
                    NewtEggXValues.append(c.pos[0])
                    NewtEggYValues.append(c.pos[1])
                    NewtEggZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    NewtEggSizes.append(c.getSize()*3)
                if c.state == "tadpole":
                    totalNewtTadpoles += 1
                    c.stepChange(terrain, heightmap, allCreatures,NEWT_SPEED)
                    NewtTadpoleXValues.append(c.pos[0])
                    NewtTadpoleYValues.append(c.pos[1])
                    NewtTadpoleZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    NewtTadpoleSizes.append(c.getSize()*3)
                if c.state == "adult":
                    totalNewtAdults += 1
                    c.stepChange(terrain, heightmap, allCreatures,NEWT_SPEED)
                    NewtAdultXValues.append(c.pos[0])
                    NewtAdultYValues.append(c.pos[1])
                    NewtAdultZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    NewtAdultSizes.append(c.getSize()*3)

                    #Kill Newt if its older than 40
                    if c.age > 40:
                        allCreatures.remove(c)

            #Update states of newts and position them
            if c.name == "shrimp":
                totalShrimps += 1
                if c.state == "egg":
                    totalShrimpEggs += 1
                    c.stepChange(terrain, heightmap, allCreatures,SHRIMP_SPEED)
                    ShrimpEggXValues.append(c.pos[0])
                    ShrimpEggYValues.append(c.pos[1])
                    ShrimpEggZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    ShrimpEggSizes.append(c.getSize()*3)
                if c.state == "larvae":
                    totalShrimpLarvae += 1
                    c.stepChange(terrain, heightmap, allCreatures,SHRIMP_SPEED)
                    ShrimpLarvaeXValues.append(c.pos[0])
                    ShrimpLarvaeYValues.append(c.pos[1])
                    ShrimpLarvaeZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    ShrimpLarvaeSizes.append(c.getSize()*3)
                if c.state == "adult":
                    totalShrimpAdults += 1
                    c.stepChange(terrain, heightmap, allCreatures,SHRIMP_SPEED)
                    ShrimpAdultXValues.append(c.pos[0])
                    ShrimpAdultYValues.append(c.pos[1])
                    ShrimpAdultZValues.append( heightmap[c.pos[0]][c.pos[1]])
                    ShrimpAdultSizes.append(c.getSize()*3)

                    #Kill shrimp if its older than 30
                    if c.age > 30:
                        allCreatures.remove(c)

            #Position plants
            if c.name == "plant":
                PlantXValues.append(c.pos[0])
                PlantYValues.append(c.pos[1])
                PlantZValues.append(heightmap[c.pos[0]][c.pos[1]])
                PlantSizes.append(c.getSize())

        #Create next row for summary dataframe
        data = {'type': [
                            'newt',
                            'newt',
                            'newt',
                            'shrimp',
                            'shrimp',
                            'shrimp',
                            'duck',
                            'duck'
                            ],
                'state': [
                            'egg',
                            'tadpole',
                            'adult',
                            'egg',
                            'larvae',
                            'adult',
                            'egg',
                            'adult'
                ],
                'total': [
                            totalNewtEggs,
                            totalNewtTadpoles,
                            totalNewtAdults,
                            totalShrimpEggs,
                            totalShrimpLarvae,
                            totalShrimpAdults,
                            totalDuckEggs,
                            totalDuckAdults
                ],
                'timestep':[i,i,i,i,i,i,i,i]}

        # Append row to summary dataframe
        new_df = pd.DataFrame(data)
        df = pd.concat([df, new_df])

        if(plots):

            #Plot Plants
            plt.scatter(PlantXValues, PlantYValues, s=PlantSizes, color="darkgreen", marker="2",label="Plant")  # Note plt origin is bottom left

            #Plot Ducks
            plt.scatter(DuckEggXValues, DuckEggYValues, s=DuckEggSizes, color="red", marker=".",label="Duck Egg")  # Note plt origin is bottom left
            plt.scatter(DuckAdultXValues, DuckAdultYValues, s=DuckAdultSizes, color="orange", marker=duck,label="Duck Adult")  # Note plt origin is bottom left

            #Plot Newts
            plt.scatter(NewtEggXValues, NewtEggYValues, s=NewtEggSizes, color="blue", marker=".",label="Newt Egg")  # Note plt origin is bottom left
            plt.scatter(NewtTadpoleXValues, NewtTadpoleYValues, s=NewtTadpoleSizes, color="cyan", marker=tadpole,label="Newt Tadpole")  # Note plt origin is bottom left
            plt.scatter(NewtAdultXValues, NewtAdultYValues, s=NewtAdultSizes, color="teal", marker=newt,label="Newt Adult")  # Note plt origin is bottom left

            #Plot Shrimp
            plt.scatter(ShrimpEggXValues, ShrimpEggYValues, s=ShrimpEggSizes, color="olive", marker=".",label="Shrimp Egg")  # Note plt origin is bottom left
            plt.scatter(ShrimpLarvaeXValues, ShrimpLarvaeYValues, s=ShrimpLarvaeSizes, color="yellow", marker="*",label="Shrimp Larvae")  # Note plt origin is bottom left
            plt.scatter(ShrimpAdultXValues, ShrimpAdultYValues, s=ShrimpAdultSizes, color="olivedrab", marker=shrimp,label="Shrimp Adult")  # Note plt origin is bottom left

            #Add terrain Background
            ax.imshow(terrain)

            #Set limits of axes
            plt.xlim(0, XMAX)
            plt.ylim(0, YMAX)

            #Turn off plot axes
            plt.axis("off")
            plt.legend(loc='best')

            #Animate Matplotlit Plot
            plt.pause(1)
            plt.cla()

    # ======================================================
    # Plotly Plot
    # ======================================================

    if(summary):
        #Generate Summary Plot using Plotly and open window in browser to show animation
        fig = px.bar(df,
                     x="type",
                     y="total",
                     color="state",
                     animation_frame="timestep",
                     animation_group="type",
                     barmode = "stack",
        )
        fig.show()

    return df

# ======================================================
# Run Main Function
# ======================================================

#Print Console Instructions
#Allow console input with default values

if __name__ == "__main__":
    print("\nShe turned me into a newt!\n")
    print("Welcome to the Swamp Simulation")
    print("Please input the numbers for your starting variables:")

    TIMESTEPS = int(input("Total time steps for simulation (50): ") or "50")

    STARTING_DUCKS = int(input("Starting Number of Ducks (10): ") or "10")
    STARTING_NEWTS = int(input("Starting Number of Newts (20): ") or "20")
    STARTING_SHRIMP = int(input("Starting Number of Shrimp (20): ") or "20")
    STARTING_PLANTS = int(input("Starting Number of Shrimp (20): ") or "20")

    DUCK_SPEED = int(input("Starting Speed of Ducks (80): ") or "80")
    NEWT_SPEED = int(input("Starting Speed of Newts (50): ") or "50")
    SHRIMP_SPEED = int(input("Starting Speed of Shrimp (30): ") or "30")

    main()
