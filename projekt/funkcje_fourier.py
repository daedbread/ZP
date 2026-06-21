import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import math

def czas(fs = 1024, tk = 1):
  return np.linspace(0, tk, int(fs*tk), endpoint=False)

def rozdziel(*args):
  r = []
  for i in range(math.ceil(len(args)/3)):
    a = list(args[3*i:3*(i+1)])
    r.append(a)
  if len(r[-1]) == 1: r[-1].append(0)
  if len(r[-1]) == 2: r[-1].append(0)
  return r

def create_sin(A = 1, f = 1, phi = 0, t = np.linspace(0,1)):
  return A * np.sin(2 * np.pi * f * np.array(t) + phi * np.pi)

def create_sig(*args, t, const=0, noise_lvl=0):
  result = const
  roz = rozdziel(*args)
  for i in range(len(roz)):
    result += create_sin(roz[i][0], roz[i][1], roz[i][2], t)
  noise = noise_lvl * np.random.randn(len(t)) # szum
  return result + noise

def fourier(sig, tk): # potrzeba czasu końcowego by nie zmieniało częstotliwości
  if tk < 1: tk1 = 1
  else: tk1 = tk
  wartosci = np.fft.rfft(sig[0:int(len(sig)//tk)]) # transformata Fouriera
  dodatnie = np.fft.rfftfreq(int(len(sig)//tk1), tk/len(sig)) #tylko dodatnie częstotliwości
  amplituda = np.abs(wartosci) * 2 * tk / len(sig)
  faza = np.angle(wartosci)
  return amplituda, dodatnie, faza

def okno(s, typ=''):
  if typ == 'hann':
    return sig.windows.hann(len(s))
  if typ == 'hamming':
    return sig.windows.hamming(len(s))
  if typ == 'blackman':
    return sig.windows.blackman(len(s))
  if typ == 'tukey':
    return sig.windows.tukey(len(s))
  if typ == 'kaiser':
    return sig.windows.kaiser(len(s), 14)
  return 1

def spectr(s):
  F, T, Sxx = sig.spectrogram(s, len(s), nperseg=100)
  plt.pcolormesh(T, F, Sxx, shading='gouraud')
  plt.ylabel('Częstotliwość [Hz]')
  plt.xlabel('Czas [s]')
  plt.show()

# filtry
def filtr(sig, f1, f2=0, typ=''):
########################################      dolnoprzepustowy
  if typ == 'lowpass':
    values = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(len(sig), 1/len(sig))

    for i in range(len(values)):
      if freqs[i] > f1:
        values[i] = 0

    new_sig = np.fft.irfft(values, len(sig))

    return new_sig

########################################      górnoprzepustowy
  elif typ == 'highpass':
    values = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(len(sig), 1/len(sig))

    for i in range(len(values)):
      if freqs[i] < f1:
        values[i] = 0

    new_sig = np.fft.irfft(values, len(sig))

    return new_sig

########################################      pasmowoprzepustowy
  elif typ == 'bandpass':

    values = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(len(sig), 1/len(sig))

    for i in range(len(values)):
      if freqs[i] <= min(f1,f2) or freqs[i] > max(f1,f2):
        values[i] = 0

    new_sig = np.fft.irfft(values, len(sig))

    return new_sig
  
########################################      pasmowozaporowy
  elif typ == 'bandstop':

    values = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(len(sig), 1/len(sig))

    for i in range(len(values)):
      if freqs[i] >= min(f1,f2) and freqs[i] < max(f1,f2):
        values[i] = 0

    new_sig = np.fft.irfft(values, len(sig))

    return new_sig
  
  elif typ == 'none':
    return sig
  
def odczyt(nazwa):
  val = []
  time = []
  with open(f'{nazwa}') as o:
    kol = len(o.readline().split())
    for l in o:
      if kol == 1:
        temp1 = 0
        temp2 = l.split()[0]
      if kol == 2:
        temp1, temp2 = l.split()

      time.append(float(temp1))
      val.append(float(temp2))

  if kol == 1: return val, czas(len(val), 1)
  if kol == 2: return val, time

def zapis(syg, nazwa, rozsz, cza=None):
  if type(cza) != np.ndarray: # jak nie poda się array'a czasu zwraca jedną kolumnę
    np.savetxt(f'{nazwa}.{rozsz}', syg)

  else: # jak się poda czas daje dwie kolumny
    with open(f'{nazwa}.{rozsz}', 'w') as o:
      # o.write(f'Czas[s] ' 'Amplituda\n')
      for k in range(len(syg)):
        o.write(f'{cza[k]} {syg[k]}\n')