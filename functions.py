import json
import numpy as np

# Open the JSON file
with open('settings.json', 'r') as json_file:
    data = json.load(json_file)
    json_file.close()

# Assign the values from the JSON file to variables
NCOLORS = data['NCOLORS']
MAX_SPAWN_DISTANCE = data['MAX_SPAWN_DISTANCE']
DIMENSIONS = data['DIMENSIONS']
TICK_LENGTH = data['TICK_LENGTH']
NTICKS = data['NTICKS']
K_MULTIPLIER = data['K_MULTIPLIER']
SPRING_MULTIPLIER = data['SPRING_MULTIPLIER']
SPRING_POWER = data['SPRING_POWER']
MAX_SPRING_LENGTH = data['MAX_SPRING_LENGTH']
MIN_SPRING_LENGTH = data['MIN_SPRING_LENGTH']
ENTROPY = data['ENTROPY']

#np.random.seed(0)

ZERO_VECTOR = np.asarray([0] * DIMENSIONS, dtype=float)

def correlateColor1(a: 'Node', b: 'Node'):
        diff: np.ndarray = np.abs(a.data - b.data)
        return (1 - sum(diff.tolist()) / 3) * K_MULTIPLIER

def correlateColor2(a: 'Node', b: 'Node', sameNearWeight = .1):
        diff: np.ndarray = np.abs(a.data[0] - b.data[0])
        diffPercent = (1 - sum(diff.tolist()) / 3)
        
        return (sameNearWeight*(a.data[1] == b.data[1]) + (1-sameNearWeight)*diffPercent )* K_MULTIPLIER

commonColors = np.asarray([[1,0,0], [0,1,0], [0,0,1],
                          [1,1,0], [1,0,1], [0,1,1]])
def findNearestColor(color):
    dist_2 = np.sum((commonColors-color)**2,axis=1)
    return np.argmin(dist_2)


class Node():
    def __init__(self, data):
        self.data: np.ndarray = data
        self.others: list[Node] = []
        self.otherPairs: list[tuple] = []
        self.position: np.ndarray = np.random.rand(DIMENSIONS) * MAX_SPAWN_DISTANCE * 2 - MAX_SPAWN_DISTANCE
        self.nextPosition: np.ndarray = ZERO_VECTOR
        self.velocity: np.ndarray = ZERO_VECTOR

    def dist(self, other: 'Node'):
        return np.linalg.norm(self.position - other.position)

    def addOtherNodes(self, others, func, *args):
        if isinstance(others, Node):
            others = [others]
        for other in others:
            if other in self.others or self == other:
                continue
            self.others.append(other)
            k_val = func(self, other, *args)
            self.otherPairs.append((other, k_val, np.power((K_MULTIPLIER-k_val), SPRING_POWER) * (MAX_SPRING_LENGTH-MIN_SPRING_LENGTH) + MIN_SPRING_LENGTH))

    def nexttick(self):
        
        spring_lengths = []
        other_positions = []
        for otherNode, k_val, spring_length in self.otherPairs:
            spring_lengths.append(spring_length)
            other_positions.append(otherNode.position)
        spring_lengths = np.array(spring_lengths)
        other_positions = np.array(other_positions)
        
        # generate force vector
        dists = np.linalg.norm(other_positions - self.position, axis=1)
        directions = (other_positions - self.position) / dists[:, np.newaxis]
        springdx = dists - spring_lengths
        springForce = directions * springdx[:, np.newaxis] * SPRING_MULTIPLIER
        totalForce = np.sum(springForce, axis=0)
        
        # affect velocity
        self.velocity += totalForce * TICK_LENGTH
        self.velocity *= ENTROPY
        
        # affect position
        self.nextPosition = self.position + self.velocity

    def tick(self):
        self.position = self.nextPosition