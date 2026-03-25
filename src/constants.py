import numpy as np
from scipy.fft import idst

N = 20          # number of moving particles
K = 10.0        # linear factor
alpha = 0.0     # quadratic factor
beta = 0.0      # cubic factor

# momentum in the mode space
initial_P = np.zeros(N)
initial_P[0] = 5 # adding momentum to first mode

initial_p = np.array(idst(initial_P, type=1, norm='ortho'))
initial_q = np.zeros(N)
displacement = np.arange(1, N+1, 1)

# simulation parameters

dt = 0.01
FPS = 60
TIME_SCALE = 50
TIME_WINDOW = 100
PLOT_MODES = 5 # how many modes energy to plot