"""Cg_Thermal_Contrast_v2 -> v3: minor revision asked by the second referee report (12 Nov 2026).
1 every value of V(1/2) in [p0^2,1] attained; 2 truncation N -> infinity in the damping proof, with the
energy bound of the density operator; 3 numerical procedure for the zeros; 5 shorter abstract;
6 the 4.1 per cent stated as a bound on log V_1 / log p_0.  Point 4 (checker block) left to the author."""
src = open('Cg_Thermal_Contrast_v2_received.tex').read()
head, tail = src.split('\n\\end{document}\n', 1)
s = head


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


def between(start, end, new):
    global s
    i0 = s.index(start)
    i1 = s.index(end, i0)
    s = s[:i0] + new + s[i1:]


# ---- tips of the two new displays
rep("\\expandafter\\gdef\\csname CGTip@eq:duhamel\\endcsname",
    r"\expandafter\gdef\csname CGTip@eq:energy\endcsname{d<a\textasciicircum{}dagger a>/dt = -kappa(<a\textasciicircum{}dagger a> - nbar): the mean photon number stays nbar.}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:truncsum\endcsname{sum over n <= N of Delta\_n(t) <= kappa (nbar+1) int\_0\textasciicircum{}t (N+1) psi\_(N+1)(r) dr.}" "\n"
    "\\expandafter\\gdef\\csname CGTip@eq:duhamel\\endcsname")

# ---- 5. shorter abstract
between("\\begin{abstract}", "\\end{abstract}", r"""\begin{abstract}
A two-level probe coupled dispersively to a cavity mode in a thermal state with mean occupation $\bar n$ has the well-known Ramsey contrast $V(u)=(1+4\bar n(\bar n+1)\sin^2\pi u)^{-1/2}$, where $u$ is the delay in units of the period of the dispersive phase. At the half period it equals $1/(2\bar n+1)$, which already gives $\bar n$ in this ideal model, and no new measurement is proposed. We study the geometric mean of the contrast after the first return, $\mathcal V_s=\exp\big(s\int_1^\infty\log V(u)\,u^{-s-1}du\big)$, $s>0$. For every positive occupation, $p_0<\mathcal V_s<e^{-sG(s)}p_0$, where $p_0=1/(\bar n+1)$ is the vacuum probability and $G(s)=\int_1^\infty\log|2\sin\pi u|\,u^{-s-1}du$. Both constants are the best possible, and for $s=1$ the upper one is $\exp(C_g)/2=1.05195\ldots$, with $C_g=-\int_1^\infty\log|\sin\pi u|\,u^{-2}du$. For every photon-number distribution of compound Poisson type, which includes thermal, Poisson and displaced thermal states, $p_0<\mathcal V_1\le p_0^{\,1-c}$ with $c=0.0409\ldots$, whereas for a given $p_0$ the half-period contrast can take every value in $[p_0^2,1]$. We also bound the effect of damping and of a finite range of delays, prove a sum rule, and relate $G$ and the transform $A$ of the delays before the first return to the Riemann zeta function. The functions $G$ and $A$ are shown with their computed zeros.
""")

# ---- 6. the 4.1 per cent, three occurrences
rep(r"so that it determines $\log p_0$ within $4.1$ per cent without any hypothesis on the statistics.",
    r"that is, the ratio $\log\mathcal V_1/\log p_0$ lies in $[1-c_1(1),1)=[0.959\ldots,1)$ without any further hypothesis on the statistics. This is an exact property of the ideal contrast, not an experimental error bar.")
rep(r"determines the vacuum probability within the factor $p_0^{-c_1(1)}$, that is, $\log p_0$ within $4.1$ per cent.",
    r"determines the vacuum probability within the factor $p_0^{-c_1(1)}$: the ratio $\log\mathcal V_1/\log p_0$ lies in $[1-c_1(1),1)$. This is an exact property of the ideal contrast, not an experimental error bar.")
rep(r"so that the geometric contrast determines $\log p_0$ within $4.1$ per cent without a hypothesis on the statistics;",
    r"so that the ratio $\log\mathcal V_1/\log p_0$ lies in $[1-c_1(1),1)$ without a further hypothesis on the statistics;")

# ---- 1. every value of V(1/2) in [p0^2,1]
rep(r"For every value of $p_0$ in $(0,1)$ both bounds are attained in this class.",
    r"For every value of $p_0$ in $(0,1)$, every value in $[p_0^2,1]$ is attained in this class.")
rep(r"The Poisson distribution of mean $-\log p_0$, with $b_1=-\log p_0$ and $b_m=0$ for $m\ge2$, attains the lower bound; the choice $b_2=-\log p_0$ and $b_m=0$ for $m\ne2$ attains the upper one.",
    r"Let $0\le a\le-\log p_0$, and take $b_1=a$, $b_2=-\log p_0-a$ and $b_m=0$ for $m\ge3$. These $b_m$ are non-negative with sum $-\log p_0$, and $p_0\exp(b_1z+b_2z^2)$ is the generating function of $X_1+2X_2$, where $X_1$ and $X_2$ are independent Poisson variables of means $b_1$ and $b_2$; so this distribution is of compound Poisson type with vacuum probability $p_0$. Its half-period contrast is $p_0\,e^{-b_1+b_2}=e^{-2a}$, which takes every value in $[p_0^2,1]$ as $a$ runs through $[0,-\log p_0]$; $a=-\log p_0$ is the Poisson distribution.")

# ---- 2. damping proof: energy bound and explicit truncation
rep(r"is bounded on bounded intervals of $t$; this is the solution given by the density operator, whose mean energy is finite. Then, for every $t\ge0$,",
    r"is bounded on bounded intervals of $t$. The solution given by the density operator of \CGeqref{eq:master} has this property, with the bound $\bar n+1$ (Step 0 of the proof). Then, for every $t\ge0$,")
rep("\\begin{proof}\nStep 1: $|\\eta_n(t)|\\le p_n$", r"""\begin{proof}
Step 0. Let $P_n(t)$ be the probability of $n$ photons in $\hat\rho(t)$. Positivity of $\hat\rho(t)$ gives $|\bra{n,\uparrow}\hat\rho\ket{n,\downarrow}|^2\le\bra{n,\uparrow}\hat\rho\ket{n,\uparrow}\bra{n,\downarrow}\hat\rho\ket{n,\downarrow}$, so that $|\eta_n(t)|\le P_n(t)$ by the inequality between the geometric and the arithmetic mean. The Hamiltonian $\hat H$ commutes with $\hat a^\dagger\hat a$, and $\hat a^\dagger(\hat a^\dagger\hat a)\hat a-\frac12\{\hat a^\dagger\hat a,\hat a^\dagger\hat a\}=-\hat a^\dagger\hat a$, $\hat a(\hat a^\dagger\hat a)\hat a^\dagger-\frac12\{\hat a\hat a^\dagger,\hat a^\dagger\hat a\}=\hat a^\dagger\hat a+1$. Hence the mean photon number $\langle\hat a^\dagger\hat a\rangle_t=\sum_nnP_n(t)$ obeys
\begin{equation}\label{eq:energy}
\frac{d\langle\hat a^\dagger\hat a\rangle_t}{dt}=-\kappa(\bar n+1)\langle\hat a^\dagger\hat a\rangle_t+\kappa\bar n\big(\langle\hat a^\dagger\hat a\rangle_t+1\big)=-\kappa\big(\langle\hat a^\dagger\hat a\rangle_t-\bar n\big),
\end{equation}
so that $\langle\hat a^\dagger\hat a\rangle_t=\bar n$ for all $t\ge0$, and $\sum_n(n+1)|\eta_n(t)|\le\sum_n(n+1)P_n(t)=\bar n+1$.

Step 1: $|\eta_n(t)|\le p_n$""")
rep(r"Sum over $n$. The sums converge, because $\Gamma_n\le\kappa(2\bar n+1)(n+1)$ and $\sum_n(n+1)(\psi_n+p_n)$ is bounded on $[0,t]$, and the gain terms add up to $\sum_k\big(\kappa(\bar n+1)k+\kappa\bar n(k+1)\big)\Delta_k=\sum_k\Gamma_k\Delta_k$. So $\sum_n\Delta_n(t)\le0$, and every $\Delta_n(t)$ is $0$.",
    r"""Let $N\ge0$ be an integer and sum these inequalities over $0\le n\le N$. Since $\Gamma_k=\kappa(\bar n+1)k+\kappa\bar n(k+1)$, the gain terms with index $k\le N$ cancel the loss terms, and what remains is
\begin{equation}\label{eq:truncsum}
\sum_{n=0}^{N}\Delta_n(t)\le\kappa(N+1)\int_0^t\Big((\bar n+1)\Delta_{N+1}(r)-\bar n\,\Delta_N(r)\Big)dr\le\kappa(\bar n+1)\int_0^t(N+1)\,\psi_{N+1}(r)\,dr .
\end{equation}
By hypothesis $\sum_n(n+1)\psi_n(r)$ is bounded for $0\le r\le t$. Hence $(N+1)\psi_{N+1}(r)$ is bounded uniformly in $N$ and $r$, and it tends to $0$ as $N\to\infty$ for each $r$, as the terms of a convergent series do. By dominated convergence the right side of \CGeqref{eq:truncsum} tends to $0$. The left side is non-negative and non-decreasing in $N$, so $\sum_{n\ge0}\Delta_n(t)=0$, and every $\Delta_n(t)$ is $0$.""")
rep(r"$\psi_n$, $\Delta_n$ & moduli $|\eta_n|$ and their excess $\max(\psi_n-p_n,0)$ over $p_n$\\",
    r"$\psi_n$, $\Delta_n$ & moduli $|\eta_n|$ and their excess $\max(\psi_n-p_n,0)$ over $p_n$\\" "\n"
    r"$P_n(t)$, $\langle\hat a^\dagger\hat a\rangle_t$ & probability of $n$ photons and mean photon number of the damped mode\\")

# ---- 3. numerical procedure for the zeros
rep(r"Table~\CGref{tab:zeros} lists the zeros of $G$ computed in the rectangle $0<\sigma<2$, $0<\theta\le40$, and Figure~\CGref{fig:Gsurf} shows $|G|$ there.",
    r"Table~\CGref{tab:zeros} lists the zeros of $G$ computed in the rectangle $0<\sigma<2$, $0<\theta\le40$, and Figure~\CGref{fig:Gsurf} shows $|G|$ there. The zeros were computed numerically. Local minima of $\log|G|$ on a grid of step $0.05$ were refined by Newton's method in double precision and then with $20$-digit arithmetic, which leaves $|G|<10^{-20}$ at the listed points. The argument principle, evaluated numerically on the boundary of the larger rectangle $-1.5<\sigma<3$, $0.2<\theta<200$, gives $79$, the number of zeros found there. This is a numerical check; we do not claim that the list is complete. The real zeros of $A$ in Table~\CGref{tab:zeros} were computed with a root finder on the real axis in $25$-digit arithmetic, with $|A|<10^{-25}$ at the listed points.")

open('Cg_Thermal_Contrast_v3.tex', 'w').write(s + '\n\\end{document}\n' + tail)
print('wrote v3')
