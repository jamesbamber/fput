import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# script to plot data after the simulation dump

data = np.load("simulation_dump.npz")

def modal_energy():
    fig = plt.figure(figsize=(10, 20))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()
    ax.set_title("Modal Energy")

    mode_energy_levels = [ax.plot([], [], '-', label=f'Mode {i+1}')[0] for i in range(5)]
    ax.legend(loc='upper right', fontsize='small')

    for i in range(5):
        mode_energy_levels[i].set_data(data['t'], data['mode_E'][:, i])

    ax.relim()        
    ax.autoscale_view()

    plt.show()

def hamiltonian():
    fig = plt.figure(figsize=(10, 20))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()
    ax.set_title("Hamiltonian")

    hamiltonian, = ax.plot([], [], '-')
    ax.legend(loc='upper right', fontsize='small')

    hamiltonian.set_data(data['t'][::50], data['H'][::50])

    ax.relim()        
    ax.autoscale_view()

    plt.show()

# hamiltonian()
modal_energy()
