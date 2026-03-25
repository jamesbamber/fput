# symplectic methods

def euler_symplectic(t, p, q, dt, f):
    dhdq, dhdp = f(t, p, q)

    next_p = p - dt * dhdq

    dhdq, dhdp = f(t, next_p, q)
    next_q = q + dt * dhdp

    return t+dt, next_p, next_q

def verlet_stormer(t, p, q, dt, f):
    dhdq, dhdp = f(t, p, q)

    half_p = p - 1/2 * dt * dhdq

    dhdq, dhdp = f(t, half_p, q)
    next_q = q + dt * dhdp

    dhdq, dhdp = f(t, half_p, next_q)
    next_p = half_p - 1/2 * dt * dhdq

    return t+dt, next_p, next_q

# non-symplectic methods

def rk4(t, p, q, dt, f): 
    k1p, k1q = f(t, p, q)
    k2p, k2q = f(t + dt/2, p - dt/2 * k1p, q + dt/2 * k1q)
    k3p, k3q = f(t + dt/2, p - dt/2 * k2p, q + dt/2 * k2q)
    k4p, k4q = f(t + dt, p - dt * k3p, q + dt * k3q)
    return t+dt, p - dt/6 * (k1p + 2 * k2p + 2 * k3p + k4p), q + dt/6 * (k1q + 2 * k2q + 2 * k3q + k4q)

def euler_explicit(t, p, q, dt, f):
    dhdq, dhdp = f(t, p, q)

    next_p = p - dt * dhdq
    next_q = q + dt * dhdp

    return t+dt, next_p, next_q
