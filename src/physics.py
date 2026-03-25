import numpy as np
from config import K, alpha, beta

def spring_force(d):
    return K*d + alpha*(d**2) + beta*(d**3)

def spring_energy(d):
    return 1/2*K*(d**2) + 1/3*alpha*(d**3) + 1/4*beta*(d**4)

def hamiltonian(t, p, q):
    T = 0.5*np.sum(p * p)

    q_with_walls = np.concat(([0], q, [0]))
    spring_extensions = np.diff(q_with_walls)

    U = np.sum(spring_energy(spring_extensions))

    return T + U

def f(t, p, q):
    q_with_walls = np.concat(([0], q, [0]))
    spring_extensions = np.diff(q_with_walls)
    forces = spring_force(spring_extensions)

    dhdq = forces[:-1] - forces[1:]
    dhdp = p
    return dhdq, dhdp