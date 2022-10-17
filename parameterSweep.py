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

#import Graphics modules

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import plotly.express as px
import numpy as np
import app

def parameterSweep(min,max):
    """
    Function that Creates a graph of the end state of different simulations as a parameter is changed
    :param min: int
    Minimum value of parameter
    :param max: int
    Maximum value of parameter
    :return:
    """
    results = pd.DataFrame()
    for i in range(min,max):
        #Paremter to sweep in this example Duck Speed
        app.DUCK_SPEED = i

        #Run simulation without plotting anything
        df = app.main(False,False)
        #Get all end point data
        df = df.loc[(df['timestep'] == 49)]
        rows = df.shape[0]

        #Make Parameter Id column
        df["Parameter"] = lst = [i] * rows

        results = pd.concat([df,results])

    return results

#Get Parameter sweep data and drop timestep column
parameterSweepOutput = parameterSweep(5,15)
parameterSweepOutput = parameterSweepOutput.drop('timestep', axis=1)

#Plot Parameter sweep as line chart
df = parameterSweepOutput
fig = px.line(df, x="Parameter", y="total", color='type')
fig.show()




