import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from config import *
from state import SimulationState

state = SimulationState()

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

ax_hamiltonian = fig.add_subplot(2,2,3,autoscale_on=False, xlim=(0, TIME_WINDOW))
ax_hamiltonian.grid()
energy_level, = ax_hamiltonian.plot([], [], '-')

ax_modes = fig.add_subplot(2,2,4,autoscale_on=False, xlim=(0, TIME_WINDOW))
ax_modes.grid()

mode_energy_levels = [ax_modes.plot([], [], '-')[0] for i in range(N)]

def animate(frame):

    curr_t = frame / FPS * TIME_SCALE
    i = int(curr_t / dt)

    while len(state.t) <= i:
        state.step(integrator)

    if curr_t > TIME_WINDOW:
        ax_hamiltonian.set_xlim((curr_t - TIME_WINDOW, curr_t + 0.01 * TIME_WINDOW))
        ax_modes.set_xlim((curr_t - TIME_WINDOW, curr_t + 0.01 * TIME_WINDOW))

    start_index = int(max(0, (curr_t - TIME_WINDOW) / dt))
    h_slice = state.H[start_index:i]

    if h_slice:
        min_h = np.min(h_slice)
        max_h = np.max(h_slice)

        padding = (max_h - min_h)*0.05 if min_h != max_h else 1.0
        ax_hamiltonian.set_ylim((min_h - padding, max_h + padding))
        
    points.set_data(displacement + state.q[i], np.zeros(N))
    vertical_points.set_data(np.concatenate(([0], displacement, [N+1])), np.concatenate(([0], state.q[i], [0])))
    energy_level.set_data(state.t[start_index:i], state.H[start_index:i])

    e_slice = np.atleast_2d(state.mode_E[start_index:i])

    if e_slice.size > 0:

        min_h = np.min(e_slice)
        max_h = np.max(e_slice)

        padding = (max_h - min_h)*0.05 if min_h != max_h else 1.0
        ax_modes.set_ylim((min_h - padding, max_h + padding))

        for k in range(PLOT_MODES):
            mode_energy_levels[k].set_data(state.t[start_index:i], e_slice[:, k])

    return points, vertical_points, energy_level,

ani = animation.FuncAnimation (
    fig, animate, 10000, interval=1000 / FPS, blit=False
)

plt.show()
