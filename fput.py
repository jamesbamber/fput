import random

import matplotlib.animation as animation
import matplotlib.pyplot as plt

import numpy as np
from numpy import cos, sin
from scipy.fft import dst, idst

# define constants

N = 20 # number of moving particles
K = 10.0
alpha = 2.0     # quadratic factor
beta = 0.0      # cubic factor
rest_distance = 1.0


initial_p = np.array(idst(np.concat(([5, 0, 0, 0, 0, 0, 0], np.zeros(N-7))), type=1, norm='ortho'))
# initial_p = np.array([ 1 for _ in range(N) ])
# initial_p = np.zeros(N)
# initial_p[0] = 5

initial_q = np.zeros(N)
displacement = np.arange(1, N+1, 1)

dt = 0.01
FPS = 60
TIME_SCALE = 50
TIME_WINDOW = 100

def spring_force(d):
    return K*d + alpha*(d**2) + beta*(d**3)

def spring_energy(d):
    return 1/2*K*(d**2) + 1/3*alpha*(d**3) + 1/4*beta*(d**4)


def hamiltonian(t, p, q):
    T = 0.5*np.sum(p * p)
    U = sum(spring_energy(q[i] - q[i-1]) for i in range(1, N)) + spring_energy(q[0]) + spring_energy(-q[N-1])

    return T + U


def f(t, p, q):
    dhdq = np.zeros(N)
    dhdp = p

    for i in range(0, N):
        ext_left = q[i] - q[i-1] if i > 0 else q[i]
        ext_right = q[i+1] - q[i] if i < N-1 else -q[i]
        dhdq[i] = spring_force(ext_left) - spring_force(ext_right)

    return dhdq, dhdp

def euler_simplettic(t, p, q):
    dhdq, dhdp = f(t, p, q)

    next_p = p - dt * dhdq

    dhdq, dhdp = f(t, next_p, q)
    next_q = q + dt * dhdp

    return t+dt, next_p, next_q

# might be bugged
def verlet_stormer(t, p, q):
    dhdq, dhdp = f(t, p, q)

    half_p = p - 1/2 * dt * dhdq

    dhdq, dhdp = f(t, half_p, q)
    next_q = q + dt * dhdp

    dhdq, dhdp = f(t, half_p, next_q)
    next_p = half_p - 1/2 * dt * dhdq

    return t+dt, next_p, next_q


t = [0]
states_p = [initial_p]
states_q = [initial_q]
states_h = [hamiltonian(0, initial_p, initial_q)]

k_values = np.arange(1, N+1)

# omega is the resonating frequencies
omega = 2 * np.sqrt(K) * np.sin(k_values * np.pi / (2 * (N + 1)))

#capital Q and P for mode space values
states_P = [ dst(initial_p, type=1, norm='ortho') ]
states_Q = [ dst(initial_q, type=1, norm='ortho') ]

# Energy per mode
states_E = [ 0.5 * (states_P[-1] ** 2 + omega**2 * states_Q[-1]**2)]


def numeric_iteration(numeric_method = verlet_stormer):
    new_t, new_p, new_q = numeric_method(t[-1], states_p[-1], states_q[-1])
    t.append(new_t)
    states_p.append(new_p)
    states_q.append(new_q)
    states_h.append(hamiltonian(new_t, new_p, new_q))

    states_Q.append(dst(new_q, type=1, norm='ortho'))
    states_P.append(dst(new_p, type=1, norm='ortho'))
    states_E.append(0.5 * (states_P[-1] ** 2 + omega**2 * states_Q[-1]**2))

#plotting

fig = plt.figure(figsize=(10, 20))
ax = fig.add_subplot(2,2,1,autoscale_on=False, xlim=(0, N+1), ylim=(-N/2, N/2))
ax.set_aspect('equal')
ax.grid()

points, = ax.plot([], [], '.')

ax2 = fig.add_subplot(2,2,2,autoscale_on=False, xlim=(0, N+1), ylim=(-N/2, N/2))
ax2.set_aspect('equal')
ax2.grid()
vertical_points, = ax2.plot([], [], 'g-')

ax3 = fig.add_subplot(2,2,3,autoscale_on=False, xlim=(0, TIME_WINDOW), ylim=(9/10*states_h[0], 11/10*states_h[0]))
ax3.grid()
energy_level, = ax3.plot([], [], '-')

ax4 = fig.add_subplot(2,2,4,autoscale_on=False, xlim=(0, TIME_WINDOW))
ax4.grid()

mode_energy_levels = [ax4.plot([], [], '-')[0] for i in range(N)]

def animate(frame):

    curr_t = frame / FPS * TIME_SCALE
    i = int(curr_t / dt)

    while len(t) <= i:
        numeric_iteration()

    if curr_t > TIME_WINDOW:
        ax3.set_xlim((curr_t - TIME_WINDOW, curr_t + 0.01 * TIME_WINDOW))
        ax4.set_xlim((curr_t - TIME_WINDOW, curr_t + 0.01 * TIME_WINDOW))

    start_index = int(max(0, (curr_t - TIME_WINDOW) / dt))
    h_slice = states_h[start_index:i]

    if h_slice:
        min_h = min(h_slice)
        max_h = max(h_slice)

        padding = (max_h - min_h)*0.05 if min_h != max_h else 1.0
        ax3.set_ylim((min_h - padding, max_h + padding))
        
    points.set_data(displacement + states_q[i], np.zeros(N))
    vertical_points.set_data(np.concatenate(([0], displacement, [N+1])), np.concatenate(([0], states_q[i], [0])))
    energy_level.set_data(t[start_index:i], states_h[start_index:i])

    if states_E[start_index:i]:
        e_slice = np.atleast_2d(states_E[start_index:i])

        min_h = np.min(e_slice)
        max_h = np.max(e_slice)

        padding = (max_h - min_h)*0.05 if min_h != max_h else 1.0
        ax4.set_ylim((min_h - padding, max_h + padding))

        for k in range(N):
            mode_energy_levels[k].set_data(t[start_index:i], e_slice[:, k])

    return points, vertical_points, energy_level,

ani = animation.FuncAnimation (
    fig, animate, 10000, interval=1000 / FPS, blit=False
)

plt.show()
