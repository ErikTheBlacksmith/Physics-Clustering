import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from tqdm import tqdm
import numpy as np

NCOLORS = 500
MAX_SPAWN_DISTANCE = 1000
SPRING_LENGTH = 50
DIMENSIONS = 2
TICK_LENGTH = .05 # in seconds
NTICKS = 50
K_MULTIPLIER = 1
SPRING_MULTIPLIER = .5
SPRING_POWER = 5
ENTROPY = .6
COLOMBS_CONST = 10**9
ELECTRIC_FORCE_POWER = 10

ZERO_VECTOR = np.asarray([0]*DIMENSIONS, dtype=float)

class Node():
    def __init__(self, color):
        self.color: np.ndarray = color
        self.others: list[Node] = []
        self.otherPairs: list[tuple(Node, float)] = []
        self.position: np.ndarray = np.random.rand(DIMENSIONS)*MAX_SPAWN_DISTANCE*2 - MAX_SPAWN_DISTANCE
        self.nextPosition: np.ndarray = ZERO_VECTOR.copy()
        self.velocity: np.ndarray = ZERO_VECTOR.copy()
        
    
    def dist(self, other: 'Node'):
        return np.linalg.norm(self.position - other.position)
    
    def correlate(self,other: 'Node'):
        diff:np.ndarray = np.abs(self.color-other.color)
        return (1 - sum(diff.tolist())/(DIMENSIONS)) * K_MULTIPLIER
    
    def addOtherNodes(self, others):
        if isinstance(others, Node):
            others = [others]
        for other in others:
            if other in self.others or self == other:
                continue
            self.others.append(other)
            k_val = self.correlate(other)
            self.otherPairs.append((other, k_val, np.power(k_val,SPRING_POWER), np.power(K_MULTIPLIER-k_val,ELECTRIC_FORCE_POWER)))
    
    def nexttick(self):
        #generate force vector
        totalForce = ZERO_VECTOR.copy()
        for otherNode, k_val, k_spring_power, k_electric_power in self.otherPairs:
            dist = self.dist(otherNode)
            direction = (otherNode.position-self.position)/dist
            springdx = dist-SPRING_LENGTH
            springForce = direction * springdx * k_spring_power * SPRING_MULTIPLIER
            electricForce = -direction * COLOMBS_CONST * k_electric_power / dist**2
            totalForce += springForce + electricForce
        # affect velocity
        self.velocity += totalForce * TICK_LENGTH
        self.velocity *= ENTROPY
        #affect position
        self.nextPosition = self.position + self.velocity
    
    def tick(self):
        self.position = self.nextPosition

colorList = [np.random.choice(range(255),size = 3)/255 for _ in range(NCOLORS)]

nodeList = [Node(color) for color in colorList]

[node.addOtherNodes(nodeList) for node in nodeList]

writer = PillowWriter(fps = 1/TICK_LENGTH)
if DIMENSIONS == 2:
    fig = plt.figure()
    ax = plt.axes(xlim= (-MAX_SPAWN_DISTANCE,MAX_SPAWN_DISTANCE), ylim = (-MAX_SPAWN_DISTANCE,MAX_SPAWN_DISTANCE))
    x, y = np.stack([node.position for node in nodeList]).T
    scat = ax.scatter(x, y, c = colorList)
    with writer.saving(fig, "out.gif", 100):
        for frame in tqdm(range(NTICKS)):
            fig.clear()
            ax = plt.axes(xlim= (-MAX_SPAWN_DISTANCE,MAX_SPAWN_DISTANCE), ylim = (-MAX_SPAWN_DISTANCE,MAX_SPAWN_DISTANCE))
            [node.nexttick() for node in nodeList]
            [node.tick() for node in nodeList]
            x, y = np.stack([node.position for node in nodeList]).T
            scat = ax.scatter(x, y, c = colorList)
            writer.grab_frame()