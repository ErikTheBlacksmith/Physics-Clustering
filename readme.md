# Physics Clustering
A way of clustering complex data using a physics simulation of nodes with attached springs of varying lengths  
(See example gifs)

Required Libraries:
* Numpy
* Matplotlib
* Pillow

Global Variables (Edit in settings.json):
* NCOLORS: Number of different colored nodes
* MAX_SPAWN_DISTANCE: Distance from the origin that nodes are allowed to spawn in. Also sets a boudning box for the animation
* Tick_Length: (in seconds) How often to recalcuate velocity. Also FPS for the animation
* SPRING_MULTIPLIER: Spring force multiplier. Decrease in low frame rates and high node counts
* SPRING_POWER: Scaling power for spring lengths
* MAX_SPRING_LENTH: self-explanatory
* MIN_SPRING_LENTH: self-explanatory
* K_MULTIPLIER: Multiplier to K (correlation) values
* ENTROPY: Multiplier to velocity every tick

K values (correlation):  
* a number between 0 and 1 [* K_MULTIPLIER] that represents how correlated two nodes are. A K of 1 should mean that two nodes have identical data.

Things to do:
* Increase effeciency and reduce reduncany
* Replace the objects with a table for increased speed
