# yWaves
yWaves solves the 1D kinematic wave and Saint-Venant equations on a staggered grid by employing operator splitting 
(see e.g. http://www.tat.physik.uni-tuebingen.de/~kley/lehre/cp-prakt/projekte/projekt-kley.pdf).
Implemented are the numerical schemes Upwind, Lax-Wendroff, Beam-Warming, Fromm as well as Leer- and Minmod-Slope limiter. 
The code was used in 2014 for the lecture hydrosystems analysis at Dresden Technical University, 
Germany. As far as I know, it is the first time that somebody uses the implemented 
numerical scheme in the context of surface runoff and flow networks.
The following figure shows results of the dam break problem:

![riemann](https://cloud.githubusercontent.com/assets/12182426/8646870/885ac396-2953-11e5-83ea-d62e0ea2a4fb.jpg)

##Get yWaves run
Requirements are Python and Matplotlib. Latter to get simulation results into plots, which are dynamically updated in runtime. 
I used the Anaconda Python distribution. This contains everything needed.
The yWaves source code can be imported as
```python
import sys
sys.path.append("path2yWaves")
import yWaves
```
To start a simulation, type then
```python
yWaves.run("inputFile")
```
Make sure you set the paths correctly (you may need \\\ instead \\ on Windows).
##Input files
A number of example input files are in the repository and cover various aspects of the code

1. damBreak.sim: The classic dam break (Riemann) problem. The analogy to the shock tube for the Euler equations;

2. runoff.sim: Precipitation runs off over an inclined plane;

3. shock.sim: A kinematic shock develops;

4. yJunction.sim: A (linear) advection wave forks at a junction;

5. infiltration.sim: An infiltration front percolates through two types of soil.

##Source code
The main file yWaves.py generates a single instance of `ySimulationClass` that itself hosts an instance of `yNetworkClass`, `yTimeSteppingClass`, `yNumericsClass`, among others.
Each instance of `ySimulationClass` hosts two instances of `yBalanceClass` and `yGridClass`. 
The grids alternate in their role as a primary grid and a partner grid, when mass and momentum (`yBalanceClass`) are calculated. Of course, in case of kinematic wave simulation the velocity update is based on constitutive relationships (`yLawsClass`). 
Implemented are the resistance to flow relationships by Manning and
Darcy-Weissbach for runoff and Brooks-Corey for infiltration.
They are assignes to yNetwork links (of `yNodeClass`) by their identity number.
This way links can share a constitutive relationship or can have individual ones (see input file infiltration.sim).
