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

import app

def parameterSweep(min,max):
    """

    :param parameter:
    :param min:
    :param max:
    :return:
    """
    results = pd.DataFrame()
    for i in range(min,max):
        df = app.main(False,False)
        # df = df.loc[(df['type'] == 'duck') & (df['timestep'] == 49)]
        df = df.loc[(df['timestep'] == 49)]
        results = pd.concat([df,results])

    return results


parameterSweepOutput = parameterSweep(10,12)

# parameterSweepOutput = parameterSweepOutput.drop('timestep', axis=1)
print(parameterSweepOutput)

plt.figure();
# parameterSweepOutput.plot(color="type");

parameterSweepOutput["total"].plot(kind = 'hist')

plt.show()




