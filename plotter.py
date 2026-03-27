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

    H = np.array(data['H'], dtype=float)
    H_mean = np.mean(H)
    std = np.std(H)
    max_rel_semi_disp = np.max(np.abs(H - H_mean)) / np.abs(H_mean)

    with open("hamiltonian_results.txt", 'a') as f:
        f.write(f"integrator: {data['integrator']}\n")
        f.write(f"iterations: {data['t'].size}\n")
        f.write(f"Mean: {H_mean}\n")
        f.write(f"Standard deviation: {std}\n")
        f.write(f"Relative standard deviation: {std / np.abs(H_mean)}\n")
        f.write(f"Maximum relative deviation from the mean: {max_rel_semi_disp}\n")
        f.write("\n\n")

    plt.show()

hamiltonian()
# modal_energy()
