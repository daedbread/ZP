import numpy as np
import matplotlib.pyplot as plt
import numba as nb
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import random

def initialize(n):

    #if not n.isnumeric():
        #raise TypeError('Parametr N (rozmiar siatki) musi mieć typ int')
    
    n = int(n)

    if n < 0:
        raise ValueError('Parametr N (rozmiar siatki) musi być dodatni')

    return np.random.choice([-1,1],(n,n))

@nb.njit
def hamiltonian_cell(state, i, j, J, B):
    height, width = state.shape
    H = 0

    for di in range(-1,2):
        for dj in range(-1,2):
            if (di == 0) and (dj == 0):
                continue
            ni = (i + di) % height
            nj = (j + dj) % width
            H -= J * state[i, j] * state[ni, nj]
    
    H = H/2
    
    H -= B * state[i, j]

    return H

@nb.njit
def hamiltonian(state, J, B):
    height, width = state.shape
    H = 0

    for i in range(height):
        for j in range(width):
            H += hamiltonian_cell(state, i, j, J, B)

    return H

@nb.njit
def mag(state):
    suma = 0
    height, width = state.shape
    for i in range(height):
        for j in range(width):
            suma += state[i, j]
    
    return suma/(height*width)

@nb.njit
def change_spin(state, J, B, beta):
    height, width = state.shape
    ri = random.randint(0, height - 1)
    rj = random.randint(0, width - 1)
    r = random.random()

    E0 = hamiltonian_cell(state, ri, rj, J, B) # energia przed zmianą spinu
    E1 = E0 * (-1) # enrgia po zmianie spinu

    # energia mniejsza po zmianie
    if E1 <= E0:
        state[ri, rj] = (-1) * state[ri, rj]
        
    # energia większa po zmianie
    else:
        p = np.exp(-beta * (E1 - E0))
        if r <= p:
            state[ri, rj] = (-1) * state[ri, rj]

    return state

@nb.njit
def next_state(state,n,J,B,beta):

    for _ in range(n*n):
        state = change_spin(state, J, B, beta)
    
    return state

def calculate_steps(state,steps,n,J,B,beta):

    n = int(n)

    if steps < 0:
        raise ValueError('Parametr M (liczba mikrokroków) musi być dodatni')
    
    if beta < 0:
        raise ValueError('Parametr beta musi być dodatni')
    
    history = [state.copy()]
    for _ in range(steps):
        next_state(state, n, J, B, beta)
        history.append(state.copy())

    return history

def make_animation(states):
    fig = plt.figure(figsize=(4,4))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('off')

    img = plt.imshow(states[0])

    def update(i):
        img.set_data(states[i])
        return img,

    ani = FuncAnimation(fig,update,frames=len(states),interval=100,blit=True)
    plt.show()

@nb.njit
def mag(state):
    suma = 0
    height, width = state.shape
    for i in range(height):
        for j in range(width):
            suma += state[i, j]
    
    return suma/(height*width)