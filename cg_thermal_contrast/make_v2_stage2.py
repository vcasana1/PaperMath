"""Stage 2 of Cg_Thermal_Contrast_v2: answers to the referee report of 12 Nov 2026 asked by the author
(comparison with the half-period contrast proved, damping bounded, idealisations stated, e^{C_g} -> exp(C_g)).
Input: Cg_Thermal_Contrast_v2.tex written by make_v2_from_v1.py.  Output: the same file."""
import re
src = open('Cg_Thermal_Contrast_v2.tex').read()
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


# ------------------------------------------------------------------ tips of the new labels (numbers fixed later from the .aux)
TIPS = r"""
\expandafter\gdef\csname CGTip@prop:cp\endcsname{Proposition 4.4: compound Poisson statistics; the geometric contrast gives the vacuum probability, the half-period contrast does not.}
\expandafter\gdef\csname CGTip@eq:cp\endcsname{sum\_n p\_n z\textasciicircum{}n = p\_0 exp(sum\_m b\_m z\textasciicircum{}m), b\_m >= 0, |z| <= 1.}
\expandafter\gdef\csname CGTip@eq:cpbound\endcsname{p\_0 < V\_1 <= p\_0\textasciicircum{}(1 - c\_1(1)), c\_1(1) = 1 - pi\textasciicircum{}2 + 2 pi Si(2 pi) = 0.0409047...}
\expandafter\gdef\csname CGTip@eq:dt\endcsname{Displaced thermal state: b\_m = q\textasciicircum{}m/m + |xi|\textasciicircum{}2 (1-q)\textasciicircum{}2 q\textasciicircum{}(m-1), p\_0 = (1-q) exp(-|xi|\textasciicircum{}2 (1-q)).}
\expandafter\gdef\csname CGTip@eq:cpsum\endcsname{0 < sum\_m b\_m c\_m(1) <= c\_1(1) sum\_m b\_m = -c\_1(1) log p\_0.}
\expandafter\gdef\csname CGTip@eq:psiineq\endcsname{psi\_n(t\_2) - psi\_n(t\_1) <= int (-Gamma\_n psi\_n + kappa(nbar+1)(n+1) psi\_(n+1) + kappa nbar n psi\_(n-1)) dr.}
\expandafter\gdef\csname CGTip@eq:etadiff\endcsname{|eta\_n(t) - p\_n exp(-2 i chi n t)| <= 2 p\_n (1 - exp(-Gamma\_n t)).}
\expandafter\gdef\csname CGTip@eq:c1\endcsname{c\_1(1) = 1 - 2 pi (pi/2 - Si(2 pi)).}
\expandafter\gdef\csname CGTip@eq:Pdt\endcsname{sum\_n p\_n z\textasciicircum{}n = exp(-|xi|\textasciicircum{}2 (1-z)/(1 + nbar (1-z)))/(1 + nbar (1-z)) for the displaced thermal state.}
\expandafter\gdef\csname CGTip@tab:robust\endcsname{Table 2: Poisson and displaced thermal statistics; geometric contrast against half-period contrast.}
\expandafter\gdef\csname CGTip@sec:real\endcsname{Section 5: Damping, intrinsic dephasing and a nonlinear shift}
\expandafter\gdef\csname CGTip@eq:master\endcsname{d rho/dt = -i[H, rho] + kappa (nbar+1) L\_a rho + kappa nbar L\_(a\textasciicircum{}dagger) rho.}
\expandafter\gdef\csname CGTip@eq:rate\endcsname{d eta\_n/dt = -(2 i chi n + Gamma\_n) eta\_n + kappa (nbar+1)(n+1) eta\_(n+1) + kappa nbar n eta\_(n-1).}
\expandafter\gdef\csname CGTip@eq:balance\endcsname{kappa (nbar+1)(n+1) p\_(n+1) + kappa nbar n p\_(n-1) = Gamma\_n p\_n (detailed balance).}
\expandafter\gdef\csname CGTip@prop:damp\endcsname{Proposition 5.1: damping at rate kappa changes the coherence by at most Lambda kappa t.}
\expandafter\gdef\csname CGTip@eq:damp\endcsname{|D\_kappa(t) - D(chi t/pi)| <= 2 sum\_n p\_n (1 - exp(-Gamma\_n t)) <= Lambda kappa t.}
\expandafter\gdef\csname CGTip@eq:duhamel\endcsname{eta\_n(t) = p\_n exp(-(2 i chi n + Gamma\_n) t) + int\_0\textasciicircum{}t exp(-(2 i chi n + Gamma\_n)(t - r)) F\_n(r) dr.}
\expandafter\gdef\csname CGTip@cor:damp\endcsname{Corollary 5.2: effect of damping on the geometric contrast and on the half-period contrast.}
\expandafter\gdef\csname CGTip@eq:dampfun\endcsname{|log V\textasciicircum{}kappa\_(s,U) - log V\_(s,U)| <= -log(1 - epsilon); |log V\_kappa(1/2) - log V(1/2)| <= -log(1 - epsilon/(2U)).}
\expandafter\gdef\csname CGTip@eq:Tdeph\endcsname{With f(t) = exp(-t/T): change of log V\_(1,U) = -(pi/(chi T)) U log U/(U-1).}
"""
rep("\\expandafter\\gdef\\csname CGTip@fig:bound\\endcsname", TIPS.strip() + "\n\\expandafter\\gdef\\csname CGTip@fig:bound\\endcsname")

# ------------------------------------------------------------------ abstract
between("\\begin{abstract}", "\\end{abstract}", r"""\begin{abstract}
A two-level probe coupled dispersively to a cavity mode in a thermal state with mean occupation $\bar n$ has the well-known Ramsey contrast $V(u)=(1+4\bar n(\bar n+1)\sin^2\pi u)^{-1/2}$, where $u$ is the delay in units of the period of the dispersive phase. The contrast returns to $1$ at every integer $u$, and at the half period it equals $1/(2\bar n+1)$, which already gives the occupation exactly in this ideal model. This note does not propose a new measurement. It establishes exact properties of a global functional of the contrast, its geometric mean after the first return with a power weight, $\mathcal V_s=\exp\big(s\int_1^\infty\log V(u)\,u^{-s-1}du\big)$, $s>0$. The main result is a two-sided bound that holds for every positive occupation: $p_0<\mathcal V_s<e^{-sG(s)}\,p_0$, where $p_0=1/(\bar n+1)$ is the probability that the mode is empty and $G(s)=\int_1^\infty\log|2\sin\pi u|\,u^{-s-1}du$. Both constants are the best possible. For the weight $u^{-2}$ the upper constant is $\exp(C_g)/2=1.05195\ldots$, with $C_g=-\int_1^\infty\log|\sin\pi u|\,u^{-2}du=0.743794\ldots$ The link with the vacuum probability extends beyond thermal states: for every photon-number distribution of compound Poisson type, a class that contains the thermal, Poisson and displaced thermal distributions, $p_0<\mathcal V_1\le p_0^{\,1-c}$ with $c=0.0409\ldots$, whereas for a given $p_0$ the half-period contrast can take any value between $p_0^2$ and $1$. Damping of the mode at the rate $\kappa$ changes the coherence by at most $4\bar n(\bar n+1)\kappa t$; this bound restricts the use of the geometric contrast to low occupations and long-lived modes, where the half-period contrast is less affected. Further results are an expansion of $\mathcal V_1$ at high occupation with an explicit remainder, the error of a finite range of delays, the sum rule $\int_0^\infty\log V(u)\,u^{-2}du=-\pi^2\bar n$, the limit $\mathcal P(N)^{1/N}\to\mathcal V_1$ for the product $\mathcal P(N)$ of the contrasts at the delays $N/k$, $1\le k<N$, and the identity $G(s)-A(s)=\frac\pi s\cot(\frac{\pi s}2)\,\zeta(s)$ for the companion transform $A$ of the delays before the first return, so that in the strip $0<\operatorname{Re}s<2$ the non-real solutions of $G=A$ are the zeros of the Riemann zeta function. The functions $G$ and $A$ are shown with their computed zeros.
""")

# ------------------------------------------------------------------ introduction: paragraphs after the description of the ideal contrast
between("Nothing in the preceding paragraphs is new here:", "\\begin{table}[!htb]\n\\caption{Notation.}", r"""Nothing in the preceding paragraphs is new here: neither the Ramsey method, nor the contrast of a thermal mode, nor the fact that this contrast determines the occupation. Within the thermal model the half-period contrast is the simplest way to obtain $\bar n$, and the functional studied in this note does not improve on it. The subject of the note is a global functional of the known contrast, and its results are exact statements about that functional: best constants, a comparison with the half-period contrast when the photon statistics is not known, a bound for the effect of damping, a sum rule and the structure of a Mellin transform.

The objective is to determine how the contrast accumulated after the first return depends on the occupation of the mode, when it is averaged geometrically over the delay with a power weight, to find the best constants in that dependence, and to state precisely what this functional measures that the half-period contrast does not.

The answer to the first part is Theorem~\CGref{thm:main}. For every exponent $s>0$ of the weight and every positive occupation, the geometric contrast $\mathcal V_s$ lies strictly between the probability $p_0$ that the mode is empty and $e^{-sG(s)}p_0$, and neither constant can be improved. Here $G$ is the transform \CGeqref{eq:G} of $\log|2\sin\pi u|$ on $[1,\infty)$. For the weight $u^{-2}$ the upper constant is $\exp(C_g)/2$, where $C_g$ is the log-sine constant \CGeqref{eq:Cg}. Corollary~\CGref{cor:bracket} turns the bound into a bracket for the occupation, and Corollary~\CGref{cor:half} combines it with the half-period contrast into a relation without parameters that holds for every thermal state and fails for coherent states of mean photon number at least $0.3$.

The answer to the second part is Proposition~\CGref{prop:cp}. For every photon-number distribution of compound Poisson type, which includes the thermal, the Poisson and the displaced thermal distributions, the geometric contrast after the first return lies between $p_0$ and $p_0^{\,1-c_1(1)}$ with $c_1(1)=0.0409\ldots$, so that it determines $\log p_0$ within $4.1$ per cent without any hypothesis on the statistics. The half-period contrast is the modulus of the mean photon-number parity; for a given $p_0$ it can take any value between $p_0^2$ and $1$ in the same class, and it gives $p_0$ or $\bar n$ only through the thermal hypothesis. A mode that holds residual coherent photons together with thermal ones, the situation analysed in \cite{ClerkUtami2007,Yan2018}, is of this kind. This is the only comparative statement of the note.

Theorem~\CGref{thm:hot} gives the expansion of $\mathcal V_1$ at high occupation with an explicit remainder, and Proposition~\CGref{prop:trunc} bounds the effect of a finite range of delays. Section~\CGref{sec:real} treats the idealisations. Proposition~\CGref{prop:damp} bounds the effect of damping of the mode in the rate equations of \cite{Sears2012,ClerkUtami2007}: the coherence changes by at most $4\bar n(\bar n+1)\kappa t$. The condition it puts on the geometric contrast grows as $\bar n^3$, and it shows that the half-period contrast is less affected by damping. Proposition~\CGref{prop:sum} shows that the integral of $\log V$ over all delays with the weight $u^{-2}$ is exactly $-\pi^2\bar n$. Proposition~\CGref{prop:harm} shows that the product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$ satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$. Section~\CGref{sec:GA} treats the function $G$ at complex exponents together with the companion transform $A$ of \CGeqref{eq:A}, which collects the delays before the first return, proves the identity \CGeqref{eq:GAzeta} that links them to the Riemann zeta function, and shows both functions with their computed zeros.

On the mathematical side, the classical log-sine integrals are integrals of powers of $\log|2\sin(\theta/2)|$ against powers of $\theta$ over a finite interval, and their evaluation in terms of zeta values and polylogarithms has a long history; see \cite{BorweinStraub2012} and the references there. The function $G$ is of a different kind: it is a Mellin transform of $\log|2\sin\pi u|$ over the half-line $[1,\infty)$, and $C_g$ is $\log2$ minus its value at $s=1$. Mellin transforms over a half-line that represent the Riemann zeta function are classical, and the identity \CGeqref{eq:GAzeta} is of this type. We do not claim it as new; we prove it and use the way in which the first return splits it into $G$ and $A$. The sum rule \CGeqref{eq:sumrule} is an elementary consequence of the Dirichlet integral. To our knowledge the bounds \CGeqref{eq:bound} and \CGeqref{eq:cpbound}, and the role of $C_g$ as the sharp constant of the first, have not been stated before.

All statements except those of Section~\CGref{sec:real} concern the ideal model \CGeqref{eq:H}: a single mode without damping, a probe without intrinsic dephasing, and a dispersive shift that is exactly linear in the photon number. The returns of the contrast to $1$ rest on these three idealisations. The geometric contrast is an integral over unbounded delays, and it averages the logarithm of the contrast, so it gives weight to the delays where the contrast is small, down to $1/(2\bar n+1)$, where a measured contrast is most affected by noise and by damping. No experimental advantage over the existing methods of thermometry is claimed beyond Proposition~\CGref{prop:cp}.

The proofs are elementary and self-contained. Four classical facts are quoted: from \cite{DLMF} the product for the sine, the partial fractions of the cotangent and the Dirichlet integral, and from \cite{Glauber1963} the representation of the thermal state as a Gaussian mixture of coherent states. The figures and tables are computed in double precision or in multiple precision arithmetic and illustrate the statements; the scripts that produce them accompany the note. Table~\CGref{tab:notation} lists the notation.

""")

# ------------------------------------------------------------------ notation table additions
rep(r"$\nu$ & mean photon number of a coherent state, \CGeqref{eq:coh}\\",
    r"""$\nu$ & mean photon number of a coherent state, \CGeqref{eq:coh}\\
$b_m$, $m\ge1$ & coefficients of the compound Poisson form \CGeqref{eq:cp}\\
$\operatorname{Si}$ & sine integral, $\operatorname{Si}(x)=\int_0^x\frac{\sin y}y\,dy$\\
$\xi$, $\beta$ & amplitude of the displacement in \CGeqref{eq:dt}; complex integration variable in its proof\\
$\hat\rho$, $\kappa$, $\mathcal L_{\hat O}$ & state of probe and mode, damping rate of the mode, dissipator of an operator $\hat O$, \CGeqref{eq:master}\\
$\ket\uparrow$, $\ket\downarrow$ & eigenstates of $\hat\sigma_z$ with eigenvalues $1$ and $-1$\\
$\eta_n(t)$, $\Gamma_n$, $F_n(r)$ & elements of the coherence of the damped mode, jump rates and gain terms, \CGeqref{eq:rate} and \CGeqref{eq:duhamel}\\
$\psi_n$, $\Delta_n$ & moduli $|\eta_n|$ and their excess $\max(\psi_n-p_n,0)$ over $p_n$\\
$D_\kappa$, $V_\kappa$, $\mathcal V^\kappa_{s,U}$ & coherence, contrast and geometric contrast of the damped mode\\
$\epsilon$ & tolerance in Corollary~\CGref{cor:damp}\\
$f(t)$, $T$, $\chi_2$ & intrinsic coherence factor of the probe, its decay time, coefficient of a nonlinear shift\\""")
rep(r"\usepackage{graphicx}", "\\usepackage{graphicx}\n\\providecommand{\\ket}[1]{|#1\\rangle}")

# ------------------------------------------------------------------ section 4: half-period paragraph and compound Poisson statistics
rep(r"As an estimator of $\bar n$ the bracket \CGeqref{eq:bracket} is therefore not an improvement on the half-period contrast. What the geometric contrast adds is a second number, and Theorem~\CGref{thm:main} fixes its relation to the first.",
    r"Within the thermal model, therefore, the bracket \CGeqref{eq:bracket} is not an improvement on the half-period contrast as an estimator of $\bar n$. The two contrasts measure different things, which matters when the statistics is not known (Proposition~\CGref{prop:cp}), and Theorem~\CGref{thm:main} fixes their relation for thermal states.")
rep(r"Every coherent state with $\nu\ge0.3$ therefore violates the upper inequality of \CGeqref{eq:half}.",
    r"""Every coherent state with $\nu\ge0.3$ therefore violates the upper inequality of \CGeqref{eq:half}.

Theorem~\CGref{thm:main}, Corollaries~\CGref{cor:bracket} and~\CGref{cor:half}, and the estimate of $\bar n$ from the half-period contrast all assume thermal statistics. We say that a probability distribution $(p_n)_{n\ge0}$ with $p_0>0$ is of compound Poisson type if there are real numbers $b_m\ge0$, $m\ge1$, with $\sum_mb_m<\infty$, such that
\begin{equation}\label{eq:cp}
\sum_{n\ge0}p_n\,z^n=p_0\exp\Big(\sum_{m\ge1}b_m\,z^m\Big),\qquad z\in\mathbb C,\quad|z|\le1 .
\end{equation}
At $z=1$ this gives $\sum_mb_m=-\log p_0$. For such a distribution we keep the definitions \CGeqref{eq:D} of the coherence $D$ and the contrast $V$, and \CGeqref{eq:Vs} of the geometric contrast. The sine integral is $\operatorname{Si}(x)=\int_0^x\frac{\sin y}y\,dy$ \cite[(6.2.9)]{DLMF}.

\begin{proposition}\label{prop:cp}
Let $(p_n)_{n\ge0}$ be of compound Poisson type with $p_0<1$.

(a) $\log\mathcal V_1=\log p_0+\sum_{m\ge1}b_m\,c_m(1)$, and
\begin{equation}\label{eq:cpbound}
p_0<\mathcal V_1\le p_0^{\,1-c_1(1)},\qquad c_1(1)=1-\pi^2+2\pi\operatorname{Si}(2\pi)=0.0409047\ldots,
\end{equation}
with equality on the right exactly when $b_m=0$ for every $m\ge2$, that is, for the Poisson distributions. The quotient $\log\mathcal V_1/\log p_0$ takes values arbitrarily close to $1$ in this class, so that both exponents in \CGeqref{eq:cpbound} are the best possible.

(b) $\log V(\frac12)=\log p_0+\sum_{m\ge1}(-1)^mb_m$, so that $p_0^2\le V(\frac12)\le1$. For every value of $p_0$ in $(0,1)$ both bounds are attained in this class.

(c) The thermal distributions \CGeqref{eq:pn}, the Poisson distributions and the photon-number distributions of displaced thermal states are of compound Poisson type. For the state obtained from the thermal state of ratio $q$, $0<q<1$, by a displacement of amplitude $\xi\in\mathbb C$,
\begin{equation}\label{eq:dt}
b_m=\frac{q^m}m+|\xi|^2(1-q)^2q^{m-1},\qquad p_0=(1-q)\,e^{-|\xi|^2(1-q)} .
\end{equation}
\end{proposition}

\begin{proof}
(a) At $z=e^{-2\pi iu}$, \CGeqref{eq:cp} and \CGeqref{eq:D} give $D(u)=p_0\exp\big(\sum_mb_me^{-2\pi imu}\big)$, and since the $b_m$ are real, $\log V(u)=\log p_0+\sum_{m\ge1}b_m\cos(2\pi mu)$, a series that converges absolutely and uniformly in $u$. Since $\sum_mb_m\int_1^\infty u^{-2}du<\infty$, it may be integrated term by term against $u^{-2}$ on $[1,\infty)$, which gives the formula for $\log\mathcal V_1$ by \CGeqref{eq:Vs} and \CGeqref{eq:cm}. By \CGeqref{eq:cmpos} with $s=1$, $0<c_m(1)<1/(\pi^2m^2)$ for every $m\ge1$, so that $c_m(1)<1/(4\pi^2)=0.0253303\ldots$ for $m\ge2$. One integration by parts, the substitution $y=2\pi u$ and \cite[(6.2.14)]{DLMF} give
\begin{equation}\label{eq:c1}
c_1(1)=\Big[-\frac{\cos2\pi u}u\Big]_1^\infty-2\pi\int_1^\infty\frac{\sin2\pi u}u\,du=1-2\pi\Big(\frac\pi2-\operatorname{Si}(2\pi)\Big),
\end{equation}
and the computed value $\operatorname{Si}(2\pi)=1.4181516\ldots$ gives $c_1(1)=0.0409047\ldots>1/(4\pi^2)$. Hence $c_m(1)\le c_1(1)$ for every $m$, with equality only for $m=1$, and
\begin{equation}\label{eq:cpsum}
0<\sum_{m\ge1}b_m\,c_m(1)\le c_1(1)\sum_{m\ge1}b_m=-c_1(1)\log p_0 .
\end{equation}
The left inequality is strict because some $b_m$ is positive, since $p_0<1$, and the right one is an equality exactly when $b_m=0$ for $m\ge2$. Exponentiating gives \CGeqref{eq:cpbound}. For an integer $M\ge1$ and $\lambda>0$, the choice $b_M=\lambda$ and $b_m=0$ for $m\ne M$ satisfies \CGeqref{eq:cp} with $p_0=e^{-\lambda}$, because $e^{-\lambda}\exp(\lambda z^M)$ is the generating function of $M$ times a Poisson variable of mean $\lambda$. It gives $\log\mathcal V_1/\log p_0=1-c_M(1)>1-1/(\pi^2M^2)$, which tends to $1$ as $M\to\infty$.

(b) At $u=\frac12$, $\cos(\pi m)=(-1)^m$. Since $|\sum_m(-1)^mb_m|\le\sum_mb_m=-\log p_0$, we get $2\log p_0\le\log V(\frac12)\le0$. The Poisson distribution of mean $-\log p_0$, with $b_1=-\log p_0$ and $b_m=0$ for $m\ge2$, attains the lower bound; the choice $b_2=-\log p_0$ and $b_m=0$ for $m\ne2$ attains the upper one.

(c) By \CGeqref{eq:pn} and the power series of $-\log(1-qz)$, $\sum_np_nz^n=(1-q)/(1-qz)=(1-q)\exp\big(\sum_{m\ge1}q^mz^m/m\big)$. The Poisson distribution of mean $\nu$ has $\sum_np_nz^n=e^{-\nu}e^{\nu z}$. Let $\bar n=q/(1-q)$. The thermal state of ratio $q$ is the mixture of coherent states $\ket\beta$, $\beta\in\mathbb C$, with the Gaussian weight $(\pi\bar n)^{-1}e^{-|\beta|^2/\bar n}$ \cite{Glauber1963}. A displacement by $\xi$ maps $\ket\beta$ to $\ket{\beta+\xi}$ up to a phase, so the displaced state is the mixture of the $\ket\beta$ with the weight $(\pi\bar n)^{-1}e^{-|\beta-\xi|^2/\bar n}$. The photon number of $\ket\beta$ has the generating function $e^{-|\beta|^2(1-z)}$. Hence, for $|z|\le1$, by the Gaussian integral over $\beta$,
\begin{equation}\label{eq:Pdt}
\sum_{n\ge0}p_nz^n=\frac1{\pi\bar n}\int_{\mathbb C}e^{-|\beta-\xi|^2/\bar n-(1-z)|\beta|^2}\,d^2\beta=\frac1{1+\bar n(1-z)}\exp\Big(-\frac{|\xi|^2(1-z)}{1+\bar n(1-z)}\Big).
\end{equation}
Now $1+\bar n(1-z)=(\bar n+1)(1-qz)$ and $(1-z)/(1-qz)=1-(1-q)\sum_{m\ge1}q^{m-1}z^m$. With $1/(\bar n+1)=1-q$, the right side of \CGeqref{eq:Pdt} is $(1-q)e^{-|\xi|^2(1-q)}\exp\big(\sum_mb_mz^m\big)$ with the $b_m$ of \CGeqref{eq:dt}, which are non-negative.
\end{proof}

Table~\CGref{tab:robust} illustrates Proposition~\CGref{prop:cp} with the Poisson distribution of mean $1$ and with displaced thermal states of thermal occupation $\frac12$, that is, modes that hold thermal photons and a coherent field at the same time. In every row $\log\mathcal V_1/\log p_0$ lies between $1-c_1(1)=0.9591$ and $1$, as \CGeqref{eq:cpbound} requires. The last column is the vacuum probability that the half-period contrast gives under the thermal hypothesis, $2V(\frac12)/(1+V(\frac12))$, divided by the true $p_0$. It is exact for the thermal state, $9$ per cent too low for $|\xi|^2=1$ and $35$ per cent too low for the Poisson distribution.

\begin{table}[!htb]
\caption{Vacuum probability $p_0$, geometric contrast $\mathcal V_1$ and half-period contrast $V(\frac12)$ for the Poisson distribution of mean $1$ and for the displaced thermal states \CGeqref{eq:dt} with $q=\frac13$ (thermal occupation $\frac12$). The last column is $2V(\frac12)/(1+V(\frac12))$, the vacuum probability given by the half-period contrast under the thermal hypothesis, divided by $p_0$.}\label{tab:robust}
\small
\begin{tabular}{llllll}
\toprule
state & $p_0$ & $\mathcal V_1$ & $\log\mathcal V_1/\log p_0$ & $V(\frac12)$ & last column\\
\midrule
Poisson, mean $1$ & $0.36788$ & $0.38324$ & $0.9591$ & $0.13534$ & $0.648$\\
$q=\frac13$, $|\xi|^2=0$ & $0.66667$ & $0.67632$ & $0.9646$ & $0.50000$ & $1.000$\\
$q=\frac13$, $|\xi|^2=0.25$ & $0.56432$ & $0.57540$ & $0.9660$ & $0.38940$ & $0.993$\\
$q=\frac13$, $|\xi|^2=1$ & $0.34228$ & $0.35434$ & $0.9677$ & $0.18394$ & $0.908$\\
$q=\frac13$, $|\xi|^2=2$ & $0.17573$ & $0.18565$ & $0.9684$ & $0.06768$ & $0.721$\\
\bottomrule
\end{tabular}
\end{table}

This is the comparative statement that the note proves. With an unknown mixture of thermal and coherent photons, the geometric contrast after the first return determines the vacuum probability within the factor $p_0^{-c_1(1)}$, that is, $\log p_0$ within $4.1$ per cent. The half-period contrast is the modulus of the mean parity $D(\frac12)=\sum_n(-1)^np_n$ and gives $p_0$ only through a hypothesis on the statistics. The vacuum probability is the quantity read by a pulse selective on the zero-photon line \cite{Johnson2010,Sears2012}; the geometric contrast reaches it without selective pulses. Within the thermal model the half-period contrast remains the simpler way to obtain $\bar n$, and Section~\CGref{sec:real} shows that it is also less affected by damping.""")

# ------------------------------------------------------------------ section 5: idealisations
rep("\\section{The sum rule and the harmonic delays}\\label{sec:sum}", r"""\section{Damping, intrinsic dephasing and a nonlinear shift}\label{sec:real}

The returns of the contrast to $1$ rest on three idealisations: no damping of the mode, no intrinsic dephasing of the probe, and a shift exactly linear in the photon number. We bound the effect of the first and discuss the other two.

Let the mode be damped at the rate $\kappa>0$ by a bath with the same occupation $\bar n$, so that the thermal state of the mode is stationary. In the Lindblad description used for this problem \cite{Rigetti2012,ClerkUtami2007,Sears2012}, the state $\hat\rho$ of probe and mode obeys
\begin{equation}\label{eq:master}
\frac{d\hat\rho}{dt}=-i\big[\hat H,\hat\rho\big]+\kappa(\bar n+1)\,\mathcal L_{\hat a}\hat\rho+\kappa\bar n\,\mathcal L_{\hat a^\dagger}\hat\rho,\qquad \mathcal L_{\hat O}\hat\rho=\hat O\hat\rho\hat O^\dagger-\frac12\big(\hat O^\dagger\hat O\hat\rho+\hat\rho\hat O^\dagger\hat O\big),
\end{equation}
with $\hat H$ as in \CGeqref{eq:H}. Initially the probe is in $(\ket\uparrow+\ket\downarrow)/\sqrt2$, where $\hat\sigma_z\ket\uparrow=\ket\uparrow$ and $\hat\sigma_z\ket\downarrow=-\ket\downarrow$, and the mode is thermal. For $n\ge0$ let $\eta_n(t)$ be $2e^{i\omega_pt}$ times the diagonal element in the state with $n$ photons of the operator $\bra\uparrow\hat\rho(t)\ket\downarrow$ on the mode, so that $\eta_n(0)=p_n$. The coherence of the damped mode is $D_\kappa(t)=\sum_n\eta_n(t)$ and its contrast is $V_\kappa(t)=|D_\kappa(t)|$; without damping $D_\kappa(t)=D(\chi t/\pi)$. The operator $\bra\uparrow\hat\rho\ket\downarrow$ starts diagonal in the photon number, and the Hamiltonian part and both dissipators of \CGeqref{eq:master} map such operators to operators of the same kind. With $\eta_{-1}=0$ and
\begin{equation}\label{eq:rate}
\frac{d\eta_n}{dt}=-(2i\chi n+\Gamma_n)\,\eta_n+\kappa(\bar n+1)(n+1)\,\eta_{n+1}+\kappa\bar n\,n\,\eta_{n-1},\qquad \Gamma_n=\kappa\big[(\bar n+1)n+\bar n(n+1)\big],
\end{equation}
these are the rate equations of \cite{Sears2012} with the phase of each photon number added, the system solved in closed form in \cite{DykmanKrivoglaz1987,ClerkUtami2007}. The thermal distribution satisfies detailed balance: since $p_{n+1}=qp_n$ and $q(\bar n+1)=\bar n$,
\begin{equation}\label{eq:balance}
\kappa(\bar n+1)(n+1)\,p_{n+1}+\kappa\bar n\,n\,p_{n-1}=\Gamma_n\,p_n,\qquad n\ge0 .
\end{equation}

\begin{proposition}\label{prop:damp}
Let $(\eta_n)$ be the solution of \CGeqref{eq:rate} with $\eta_n(0)=p_n$ for which $\sum_n(n+1)|\eta_n(t)|$ is bounded on bounded intervals of $t$; this is the solution given by the density operator, whose mean energy is finite. Then, for every $t\ge0$,
\begin{equation}\label{eq:damp}
\big|D_\kappa(t)-D(\chi t/\pi)\big|\le2\sum_{n\ge0}p_n\big(1-e^{-\Gamma_nt}\big)\le\Lambda\,\kappa\,t,\qquad\Lambda=4\bar n(\bar n+1),
\end{equation}
and in particular $|V_\kappa(t)-V(u)|\le\pi\Lambda\,(\kappa/\chi)\,u$ with $u=\chi t/\pi$.
\end{proposition}

\begin{proof}
Step 1: $|\eta_n(t)|\le p_n$ for all $n$ and $t\ge0$. Let $\psi_n=|\eta_n|$ and $\Delta_n=\max(\psi_n-p_n,0)$. Since $\operatorname{Re}\big(\bar\eta_n\cdot(-2i\chi n)\eta_n\big)=0$, \CGeqref{eq:rate} gives, for $t_1<t_2$,
\begin{equation}\label{eq:psiineq}
\psi_n(t_2)-\psi_n(t_1)\le\int_{t_1}^{t_2}\Big(-\Gamma_n\psi_n+\kappa(\bar n+1)(n+1)\psi_{n+1}+\kappa\bar n\,n\,\psi_{n-1}\Big)dr .
\end{equation}
Subtracting \CGeqref{eq:balance} and using $\psi_k-p_k\le\Delta_k$, the same inequality holds for $\Delta_n$ on every interval on which $\psi_n>p_n$, with $\Delta$ in place of $\psi$. Since $\Delta_n$ is absolutely continuous, vanishes at $t=0$ and is constant on the intervals where it is $0$, this gives $\Delta_n(t)\le\int_0^t\big(-\Gamma_n\Delta_n+\kappa(\bar n+1)(n+1)\Delta_{n+1}+\kappa\bar n\,n\,\Delta_{n-1}\big)dr$. Sum over $n$. The sums converge, because $\Gamma_n\le\kappa(2\bar n+1)(n+1)$ and $\sum_n(n+1)(\psi_n+p_n)$ is bounded on $[0,t]$, and the gain terms add up to $\sum_k\big(\kappa(\bar n+1)k+\kappa\bar n(k+1)\big)\Delta_k=\sum_k\Gamma_k\Delta_k$. So $\sum_n\Delta_n(t)\le0$, and every $\Delta_n(t)$ is $0$.

Step 2. Put $F_n(r)=\kappa(\bar n+1)(n+1)\eta_{n+1}(r)+\kappa\bar n\,n\,\eta_{n-1}(r)$. Solving \CGeqref{eq:rate} as a linear equation for $\eta_n$,
\begin{equation}\label{eq:duhamel}
\eta_n(t)=p_n\,e^{-(2i\chi n+\Gamma_n)t}+\int_0^te^{-(2i\chi n+\Gamma_n)(t-r)}\,F_n(r)\,dr .
\end{equation}
By Step 1 and \CGeqref{eq:balance}, $|F_n(r)|\le\Gamma_np_n$. Hence
\begin{equation}\label{eq:etadiff}
\big|\eta_n(t)-p_n\,e^{-2i\chi nt}\big|\le p_n\big(1-e^{-\Gamma_nt}\big)+\int_0^te^{-\Gamma_n(t-r)}\,\Gamma_np_n\,dr=2p_n\big(1-e^{-\Gamma_nt}\big).
\end{equation}
Summing over $n$, with $D(\chi t/\pi)=\sum_np_ne^{-2i\chi nt}$, gives the first inequality of \CGeqref{eq:damp}. Since $1-e^{-y}\le y$ for $y\ge0$ and $\sum_nnp_n=\bar n$, the sum is at most $2t\sum_np_n\Gamma_n=2\kappa t\big((\bar n+1)\bar n+\bar n(\bar n+1)\big)=\Lambda\kappa t$. Finally $\big||a|-|b|\big|\le|a-b|$ and $t=\pi u/\chi$.
\end{proof}

For the geometric contrast of the damped mode over $1\le u\le U$, $\mathcal V^\kappa_{s,U}$, defined by \CGeqref{eq:VsU} with $V_\kappa(\pi u/\chi)$ in place of $V(u)$, the bound gives the following.

\begin{corollary}\label{cor:damp}
Let $s>0$, $U>1$, and suppose that $\epsilon=\pi\Lambda(2\bar n+1)(\kappa/\chi)\,U<1$. Then
\begin{equation}\label{eq:dampfun}
\big|\log\mathcal V^\kappa_{s,U}-\log\mathcal V_{s,U}\big|\le-\log(1-\epsilon),\qquad\Big|\log V_\kappa\Big(\frac\pi{2\chi}\Big)-\log V\Big(\frac12\Big)\Big|\le-\log\Big(1-\frac\epsilon{2U}\Big).
\end{equation}
\end{corollary}

\begin{proof}
For $0\le u\le U$, Proposition~\CGref{prop:damp} and $V(u)\ge1/(2\bar n+1)$ give $|V_\kappa(\pi u/\chi)-V(u)|\le\pi\Lambda(\kappa/\chi)U=\epsilon/(2\bar n+1)\le\epsilon V(u)$. So $1-\epsilon\le V_\kappa/V\le1+\epsilon$ and $|\log(V_\kappa/V)|\le-\log(1-\epsilon)$, because $\log(1+\epsilon)\le-\log(1-\epsilon)$. The weight in \CGeqref{eq:VsU} is a probability measure on $[1,U]$. At $u=\frac12$, Proposition~\CGref{prop:damp} gives $|V_\kappa(\frac\pi{2\chi})-V(\frac12)|\le\pi\Lambda(\kappa/\chi)/2=\epsilon/(2U(2\bar n+1))\le\frac\epsilon{2U}V(\frac12)$, and the logarithm is bounded as before with $\frac\epsilon{2U}$ in place of $\epsilon$.
\end{proof}

The condition $\epsilon<1$ asks for $\kappa/\chi<1/\big(\pi\Lambda(2\bar n+1)U\big)$, which decreases as $\bar n^{-3}$. With $U=20$ and $\epsilon=0.1$ it reads $\kappa/\chi<3.0\times10^{-3}$ for $\bar n=0.1$, $\kappa/\chi<6.6\times10^{-5}$ for $\bar n=1$ and $\kappa/\chi<2.3\times10^{-8}$ for $\bar n=20$. For $\chi/2\pi=1$~MHz these are $\kappa/2\pi<3.0$~kHz, $66$~Hz and $0.023$~Hz. Cavity linewidths $\kappa/2\pi$ between $6$ and $120$~kHz are reported in \cite{Sears2012}, and a single-photon lifetime of $25.6$~ms, that is $\kappa/2\pi=6.2$~Hz, in \cite{Milul2023}. The geometric contrast is therefore usable at low occupation in long-lived modes, and the statements of Section~\CGref{sec:main} at high occupation, such as the example $\bar n=20$ after Corollary~\CGref{cor:bracket}, are statements about the ideal model only. The half-period contrast is affected less, by the factor $1/(2U)$ in \CGeqref{eq:dampfun}, because its delay is short. The bound \CGeqref{eq:damp} is not sharp: for $\bar n$ in $\{0.05,1,5,20\}$, $\kappa/(2\chi)$ between $10^{-5}$ and $10^{-2}$ and $0<u\le6$, the difference $|V_\kappa-V|$ computed from the closed form of \cite{ClerkUtami2007} is at most $0.51$ times the bound.

Intrinsic dephasing of the probe. If, independently of the photons, the probe has a coherence factor $f(t)$ with $0<f(t)\le1$, the measured contrast without damping is $f(t)V(u)$. Since $V(k)=1$ at the returns, the contrast measured at $u=k$ is $f(\pi k/\chi)$: the returns measure the decay of the probe itself, which can then be divided out. Without that correction, a factor $f(t)=e^{-t/T}$ changes $\log\mathcal V_{1,U}$ by
\begin{equation}\label{eq:Tdeph}
\frac1{1-U^{-1}}\int_1^U\Big(-\frac{\pi u}{\chi T}\Big)u^{-2}\,du=-\frac{\pi}{\chi T}\cdot\frac{U\log U}{U-1} .
\end{equation}

Nonlinear shift. If the phase acquired by the component with $n$ photons is not exactly $2\chi nt$, for example $2\chi nt+\chi_2n(n-1)t$ with a real $\chi_2\ne0$, the contrast at the return $u=k$ becomes $\big|\sum_np_ne^{-i\pi k\chi_2n(n-1)/\chi}\big|$, which is below $1$ in general. With the decay of the probe divided out, a measured contrast below $1$ at the returns therefore signals damping or a nonlinear shift, and Proposition~\CGref{prop:damp} bounds the part due to damping. None of the results of Sections~\CGref{sec:main}, \CGref{sec:sum} and~\CGref{sec:GA} is claimed for a nonlinear shift.

\section{The sum rule and the harmonic delays}\label{sec:sum}""")

# ------------------------------------------------------------------ Titchmarsh remark replaced by an elementary one
rep(r"This equivalence is a consequence of the explicit factor in \CGeqref{eq:GAzeta} and gives no information on the location of those zeros. The identity \CGeqref{eq:GAzeta} is a Mellin representation of $\zeta$ of the classical type \cite[Chapter~II]{Titchmarsh1986}.",
    r"This equivalence is a consequence of the explicit factor in \CGeqref{eq:GAzeta} and gives no information on the location of those zeros. Mellin representations of $\zeta$ over a half-line are classical; the simplest, $\zeta(s)=\frac s{s-1}-s\int_1^\infty(u-\lfloor u\rfloor)u^{-s-1}du$ for $\sigma>0$, follows for $\sigma>1$ from $\zeta(s)=s\int_1^\infty\lfloor u\rfloor u^{-s-1}du$ and extends to $\sigma>0$ because the integral is analytic there. The identity \CGeqref{eq:GAzeta} is of the same type.")

# ------------------------------------------------------------------ conclusions
between("\\section{Conclusions}\\label{sec:concl}", "\\begin{thebibliography}", r"""\section{Conclusions}\label{sec:concl}

The main conclusion is the bound \CGeqref{eq:boundCg}. For a two-level probe coupled dispersively to a thermal mode, the geometric mean of the Ramsey contrast after the first return, taken with the weight $u^{-2}$, satisfies $p_0<\mathcal V_1<\frac12\exp(C_g)\,p_0$ for every positive occupation, where $p_0$ is the probability that the mode is empty and $C_g=0.743794\ldots$ is the log-sine constant \CGeqref{eq:Cg}. The two constants $1$ and $\frac12\exp(C_g)=1.05195\ldots$ cannot be improved. The log-sine constant is thus the sharp constant of a functional of the ideal contrast that can in principle be estimated from a sequence of Ramsey measurements: no thermal state gives a ratio $\mathcal V_1/p_0$ above $\frac12\exp(C_g)$, and every smaller constant is exceeded at a sufficiently high occupation.

The second conclusion states what this functional measures that the half-period contrast does not. For every photon statistics of compound Poisson type, including thermal, Poisson and displaced thermal statistics, $p_0<\mathcal V_1\le p_0^{\,1-c_1(1)}$ with $c_1(1)=0.0409\ldots$, so that the geometric contrast determines $\log p_0$ within $4.1$ per cent without a hypothesis on the statistics; the half-period contrast is the modulus of the mean parity and, for a given $p_0$, can take any value between $p_0^2$ and $1$ (Proposition~\CGref{prop:cp}). Within the thermal model the half-period contrast gives $\bar n$ exactly and more simply.

The third conclusion concerns damping. In the rate equations of the damped mode the coherence differs from the ideal one by at most $4\bar n(\bar n+1)\kappa t$ (Proposition~\CGref{prop:damp}). For the geometric contrast over $1\le u\le U$ this requires $\kappa/\chi$ well below $1/\big(4\pi\bar n(\bar n+1)(2\bar n+1)U\big)$, a condition met at low occupation in long-lived modes and not at high occupation, and the half-period contrast is less affected (Corollary~\CGref{cor:damp}). The returns of the contrast measure the intrinsic decay of the probe and test the linearity of the shift.

Further conclusions follow from the same analysis. The bound holds for every power weight $u^{-s-1}$ with $s>0$, with the sharp constant $e^{-sG(s)}$, so that the function $G$ on the positive real axis is the logarithm of the sharp constant divided by $-s$ (Theorem~\CGref{thm:main}). For thermal states the occupation is bracketed by the geometric contrast alone, $1/\mathcal V_1-1<\bar n<\exp(C_g)/(2\mathcal V_1)-1$ (Corollary~\CGref{cor:bracket}), and the geometric and half-period contrasts satisfy the relation \CGeqref{eq:half}, which contains no parameter and which coherent states of mean photon number at least $0.3$ violate (Corollary~\CGref{cor:half}). At high occupation $\mathcal V_1=\frac12\exp(C_g)p_0\,q^{\pi^2/12-3/4}e^{R}$ with $0<R\le\frac{\tau^2}{\pi^2}(\frac52+\frac12\log\frac1\tau)$ (Theorem~\CGref{thm:hot}). A finite range of delays $1\le u\le U$ changes $\log\mathcal V_s$ by at most $U^{-s}\log(2\bar n+1)$ (Proposition~\CGref{prop:trunc}). The integral of the logarithm of the contrast over all delays with the weight $u^{-2}$ is exactly $-\pi^2\bar n$, and the first return separates it into a part within $C_g-\log2$ of $\log p_0$ and a part that carries the linear term (Proposition~\CGref{prop:sum}). The product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$ satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$, with the explicit bound \CGeqref{eq:harm} for its logarithmic rate (Proposition~\CGref{prop:harm}).

At complex exponents $G$ is the hot limit of the transform of $\log(V/p_0)$ after the first return, and its zeros are the weights on which that excess has no component (Proposition~\CGref{prop:complex}). Together with the transform $A$ of the delays before the first return it satisfies $G-A=\frac\pi s\cot(\frac{\pi s}2)\zeta$, so that in the strip $0<\operatorname{Re}s<2$ the two transforms coincide at a non-real exponent exactly at the zeros of the Riemann zeta function (Proposition~\CGref{prop:A}). This is a consequence of an explicit factorisation and gives no information on the location of those zeros.

""")

# ------------------------------------------------------------------ bibliography
rep(r"\bibitem{Gambetta2006}", r"""\bibitem{Glauber1963}
R.~J.~Glauber, Coherent and incoherent states of the radiation field, \emph{Phys. Rev.} \textbf{131} (1963), 2766--2788.
\href{https://doi.org/10.1103/PhysRev.131.2766}{doi:10.1103/PhysRev.131.2766}.

\bibitem{Gambetta2006}""")
rep(r"\bibitem{Peng2015}", r"""\bibitem{Milul2023}
O.~Milul, B.~Guttel, U.~Goldblatt, S.~Hazanov, L.~M.~Joshi, D.~Chausovsky, N.~Kahn, E.~\c{C}ifty\"urek, F.~Lafont and S.~Rosenblum, Superconducting cavity qubit with tens of milliseconds single-photon coherence time, \emph{PRX Quantum} \textbf{4} (2023), 030336.
\href{https://doi.org/10.1103/PRXQuantum.4.030336}{doi:10.1103/PRXQuantum.4.030336};
\href{https://arxiv.org/abs/2302.06442}{arXiv:2302.06442}.

\bibitem{Peng2015}""")

rep(r"differs from $\log p_0$ by less than $C_g-\log2=0.0506\ldots$ at every temperature.", r"differs from $\log p_0$ by less than $C_g-\log2=0.0506\ldots$ for every positive occupation.")
# ------------------------------------------------------------------ exp(C_g) everywhere in the text
b0 = s.index('\\begin{document}')
body = s[b0:]
n_before = body.count('e^{C_g}')
body = body.replace('e^{C_g}', '\\exp(C_g)')
s = s[:b0] + body
print('e^{C_g} replaced in the text:', n_before)
rep(r"\providecommand{\ket}[1]{|#1\rangle}", "\\providecommand{\\ket}[1]{|#1\\rangle}\n\\providecommand{\\bra}[1]{\\langle#1|}")
open('Cg_Thermal_Contrast_v2.tex', 'w').write(s + '\n\\end{document}\n' + tail)
print('stage 2 written')
