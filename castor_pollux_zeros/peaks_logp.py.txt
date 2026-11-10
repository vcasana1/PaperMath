"""Peaks of |S_G(x)|, S_G(x) = (1/N) sum_k exp(i gamma_k x) over the 79 zeros of G in zeros_G.txt,
compared with log n, and the value of S_G at x = log n for n <= 31.
Output: peaks_logp_output.txt
"""
import math
import numpy as np
from scipy.signal import find_peaks

d = np.loadtxt('zeros_G.txt')
g = d[:, 1]
x = np.linspace(0.3, 4.2, 200001)
S = np.abs(np.exp(1j * np.outer(x, g)).sum(1)) / len(g)
p, _ = find_peaks(S, height=0.12)
lines = ['# peaks of |S_G| with height > 0.12 on [0.3, 4.2]; resolution about 2pi/(gamma_max-gamma_min) = %.4f' % (2 * math.pi / (g.max() - g.min())),
         '# x_peak  |S_G|  exp(x_peak)  nearest n  log n']
for i in p:
    n = round(math.exp(x[i]))
    lines.append('%.4f  %.3f  %8.3f  %3d  %.4f' % (x[i], S[i], math.exp(x[i]), n, math.log(n)))
lines.append('')
lines.append('# S_G(log n) for n <= 31:  n  Re  Im  |S|')
for n in range(2, 32):
    v = np.exp(1j * g * math.log(n)).sum() / len(g)
    lines.append('%3d  %+.3f  %+.3f  %.3f' % (n, v.real, v.imag, abs(v)))
open('peaks_logp_output.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
