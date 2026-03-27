import numpy as np
from scipy.fft import idst

import integrators

N = 32          # number of moving particles
K = 1.0        # linear factor
alpha = 0.0    # quadratic factor
beta = 0.0      # cubic factor

initial_Q = np.zeros(N)
initial_Q[5] = 10.0  # Large displacement in the second mode
initial_q = idst(initial_Q, type=1, norm='ortho')
initial_p = np.zeros(N)
displacement = np.arange(1, N+1, 1)

# simulation parameters

integrator = integrators.verlet_stormer
dt = 0.01
FPS = 60
TIME_SCALE = 100
TIME_WINDOW = 1000
PLOT_MODES = 10 # how many energy modes to plot
