"""Exponential series over the zeros of G and of A, 3D plot of both, and centroids.

For a zero set {rho_k} let o_k be the coordinate of rho_k that varies:
  G: rho_k = beta_k + i gamma_k with gamma_k > 0, and o_k = gamma_k = Im rho_k;
  A: every zero in the window is real (zeros_A_check.txt), so Im rho_k = 0 and o_k = rho_k.
    S(x) = (1/N) sum_k exp(i o_k x),        0 <= x <= XMAX,
normalised by the number N of zeros.  Two centroids in the complex plane:
    c_zeros = (1/N) sum_k rho_k                    (centroid of the zero set)
    c_series = (1/XMAX) int_0^XMAX S(x) dx         (centroid of the curve x -> S(x))
            = (1/N) sum_k (exp(i o_k XMAX) - 1)/(i o_k XMAX)   (the term is 1 if o_k = 0).
Input: zeros_G.txt, zeros_A.txt.  Output: series_centroid_output.txt and PNG figures.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

XMAX = 2 * np.pi
X = np.linspace(0, XMAX, 6001)


def load(name):
    d = np.loadtxt('zeros_%s.txt' % name)
    d = np.atleast_2d(d)
    return d[:, 0] + 1j * d[:, 1]


def coord(z):
    return z.imag if np.any(z.imag != 0) else z.real


def series(z):
    g = coord(z)
    return np.exp(1j * np.outer(X, g)).sum(1) / len(g)


def centroids(z):
    g = coord(z)
    cz = z.mean()
    gs = np.where(g == 0, 1.0, g)
    cs = np.where(g == 0, 1.0, (np.exp(1j * gs * XMAX) - 1) / (1j * gs * XMAX)).mean()
    return cz, cs


def main():
    Z = {n: load(n) for n in ('G', 'A')}
    S = {n: series(Z[n]) for n in Z}
    C = {n: centroids(Z[n]) for n in Z}
    col = {'G': 'tab:blue', 'A': 'tab:red'}
    out = open('series_centroid_output.txt', 'w')
    for n in ('G', 'A'):
        cz, cs = C[n]
        # numerical check of the closed form of c_series
        cs_num = np.trapezoid(S[n], X) / XMAX
        line = ('%s: N=%d zeros, o_k in [%.4f, %.4f]\n'
                '   centroid of the zeros      = %.10f %+.10f i\n'
                '   centroid of the series     = %.10f %+.10f i   (trapezoid check %.10f %+.10f i)\n'
                '   mean |S(x)| on [0,2pi]     = %.6f\n'
                % (n, len(Z[n]), coord(Z[n]).min(), coord(Z[n]).max(), cz.real, cz.imag,
                   cs.real, cs.imag, cs_num.real, cs_num.imag, np.abs(S[n]).mean()))
        print(line, end='')
        out.write(line)
    out.close()

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection='3d')
    for n in ('G', 'A'):
        ax.plot(X, S[n].real, S[n].imag, color=col[n], lw=0.8, label=r'$S_%s(x)$, N=%d' % (n, len(Z[n])))
        cs = C[n][1]
        ax.plot([0, XMAX], [cs.real] * 2, [cs.imag] * 2, color=col[n], ls='--', lw=1.5,
                label=r'centroid of $S_%s$' % n)
    ax.set_xlabel('x')
    ax.set_ylabel('Re S(x)')
    ax.set_zlabel('Im S(x)')
    ax.set_title(r'$S(x)=\frac{1}{N}\sum_k e^{i o_k x}$: G with $o_k=\mathrm{Im}\,\rho_k$, A with $o_k=\rho_k$ (real)')
    ax.legend(loc='upper left')
    fig.tight_layout()
    fig.savefig('fig_series_3d.png', dpi=150)

    fig2, ax2 = plt.subplots(1, 2, figsize=(13, 5.5))
    for n in ('G', 'A'):
        ax2[0].plot(S[n].real, S[n].imag, color=col[n], lw=0.6, label=r'$S_%s$' % n)
        ax2[0].plot(C[n][1].real, C[n][1].imag, 'o', color=col[n], ms=9, mec='k', label='centroid of $S_%s$' % n)
        ax2[1].plot(Z[n].real, Z[n].imag, '.', color=col[n], ms=5, label='zeros of %s' % n)
        ax2[1].plot(C[n][0].real, C[n][0].imag, '*', color=col[n], ms=16, mec='k', label='centroid of the zeros of %s' % n)
    ax2[0].set_xlabel('Re S'); ax2[0].set_ylabel('Im S'); ax2[0].set_aspect('equal')
    ax2[0].set_title('The curves S(x), 0 <= x <= 2pi, in the complex plane'); ax2[0].legend(fontsize=8)
    ax2[1].set_xlabel('Re s'); ax2[1].set_ylabel('Im s')
    ax2[1].set_title('Zeros and their centroids'); ax2[1].legend(fontsize=8)
    fig2.tight_layout()
    fig2.savefig('fig_centroids.png', dpi=150)

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    for n in ('G', 'A'):
        ax3.plot(X, np.abs(S[n]), color=col[n], lw=0.8, label=r'$|S_%s(x)|$' % n)
    ax3.set_xlabel('x'); ax3.set_ylabel('|S(x)|'); ax3.legend()
    ax3.set_title('Modulus of the exponential series')
    fig3.tight_layout()
    fig3.savefig('fig_series_modulus.png', dpi=150)


if __name__ == '__main__':
    main()
