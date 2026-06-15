import lab4_ising_numba as ising
import argparse

# Parser setup
parser = argparse.ArgumentParser(description='parser')
parser.add_argument('--N', default=100)
parser.add_argument('--M', type=int, default=500)
parser.add_argument('--beta', type=float, default=1)
parser.add_argument('--B', type=float, default=0)
parser.add_argument('--J', type=float, default=1)
parser.add_argument('--show-animation', action='store_true')
parser.add_argument('--magnetization-file', nargs='?')
args = parser.parse_args()
N, M, beta, B, J, anim, mag = args.N, args.M, args.beta, args.B, args.J, args.show_animation, args.magnetization_file

# Script
print(f'Dane wejściowe: N = {N}, M = {M}, beta = {beta}, B = {B}, J = {J}, animacja = {anim}, plik magnetyzacji = {mag}')

try:
    state = ising.initialize(N)
    states = ising.calculate_steps(state,M,N,J,B,beta)
except ValueError as e:
    print(f'{e}')
    exit()
except TypeError as e:
    print(f'{e}')

if mag!= None:
    with open(mag, 'w') as f:
        f.write('Krok / Magnetyzacja \n')
        for i in range(M+1):
            f.write(f'{i+1} | {ising.mag(states[i])} \n')

if anim:
    ising.make_animation(states)
