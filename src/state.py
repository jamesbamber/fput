import numpy as np
from scipy.fft import dst

from config import *
from physics import hamiltonian, f

class SimulationState:
    def __init__(self):
        self.t = [ 0 ]
        self.p = [ initial_p ]
        self.q = [ initial_q ]
        self.H = [ hamiltonian(0, initial_p, initial_q) ]

        # omega contains the resonating frequencies
        k_values = np.arange(1, N+1)
        self.omega = 2 * np.sqrt(K) * np.sin(k_values * np.pi / (2 * (N + 1)))

        initial_mode_P = dst(initial_p, type=1, norm='ortho')
        initial_mode_Q = dst(initial_q, type=1, norm='ortho')

        self.mode_P = [ initial_mode_P ]
        self.mode_Q = [ initial_mode_Q ]
        self.mode_E = [ 0.5 * (initial_mode_P ** 2 + self.omega**2 * initial_mode_Q[-1]**2) ]

    def step(self, integrator):
        '''
        performs one iteration of a given numeric integrator
        '''

        t, p, q = integrator(self.t[-1], self.p[-1], self.q[-1], dt, f)

        self.t.append(t)
        self.p.append(p)
        self.q.append(q)
        self.H.append(hamiltonian(t, p, q))

        mode_P = dst(p, type=1, norm='ortho')
        mode_Q = dst(q, type=1, norm='ortho')

        self.mode_P.append(mode_P)
        self.mode_Q.append(mode_Q)
        self.mode_E.append(0.5 * (mode_P ** 2 + self.omega**2 * mode_Q**2))
