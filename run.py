import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from tqdm import tqdm
import numpy as np

from functions import *

#np.random.seed(0)


# generates a list of rgb colors to represent each data point
colorList = [np.random.choice(range(255), size=3) / 255 for _ in range(NCOLORS)]

# generates a list of data for each node
dataList = [(color, findNearestColor(color)) for color in colorList]

# creates nodes from the data
nodeList = [Node(data) for data in dataList]

# connects each node with all ofther nodes based off of the function and args
[node.addOtherNodes(nodeList, correlateColor2, .1) for node in nodeList]


# generates as gif
plotRange = (-MAX_SPAWN_DISTANCE, MAX_SPAWN_DISTANCE)
writer = PillowWriter(fps=1 / TICK_LENGTH)
if DIMENSIONS == 2:
    fig = plt.figure()
    ax = plt.axes(xlim= plotRange, ylim= plotRange)
    x, y = np.stack([node.position for node in nodeList]).T
    scat = ax.scatter(x, y, c=colorList)
    with writer.saving(fig, "out.gif", 100):
        for frame in tqdm(range(NTICKS)):
            fig.clear()
            ax = plt.axes(xlim=plotRange, ylim=plotRange)
            
            # next tick
            [node.nexttick() for node in nodeList]
            [node.tick() for node in nodeList]
            
            # update positions
            positions = np.array([node.position for node in nodeList])
            x, y = positions.T
            scat = ax.scatter(x, y, c = colorList)
            writer.grab_frame()