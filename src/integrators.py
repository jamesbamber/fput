def euler_simplettic(t, p, q, dt, f):
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