"""Cg_Thermal_Contrast_v3 -> v4 (12 Nov 2026).
Positioning and bibliography reworked after the physics literature review brought by the author;
new Proposition (first period, Fourier coefficients of log V) after reviewer point 9.
The statements and proofs of v3 are not changed."""
import sys
src = open(sys.argv[1]).read()
head, tail = src.split('\n\\end{document}\n', 1)
s = head


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


def between(start, end, new):
    global s
    i0 = s.index(start)
    i1 = s.index(end, i0)
    s = s[:i0] + new + s[i1:]


# ------------------------------------------------------------------ tips of the new labels
rep("\\expandafter\\gdef\\csname CGTip@sec:real\\endcsname",
    r"\expandafter\gdef\csname CGTip@eq:inv\endcsname{p\_n = int\_0\textasciicircum{}1 D(u) e\textasciicircum{}(2 pi i n u) du for every photon-number distribution.}" "\n"
    r"\expandafter\gdef\csname CGTip@sec:fourier\endcsname{Section 6: The first period and the Fourier coefficients of the logarithm of the contrast}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:ellm\endcsname{ell\_0 = int\_0\textasciicircum{}1 log V(u) du, ell\_m = 2 int\_0\textasciicircum{}1 log V(u) cos(2 pi m u) du.}" "\n"
    r"\expandafter\gdef\csname CGTip@prop:fourier\endcsname{Proposition 6.1: compound Poisson statistics; ell\_0 = log p\_0, ell\_m = b\_m; displaced thermal q and |xi|\textasciicircum{}2 in closed form.}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:recursion\endcsname{n p\_n = sum\_(m=1)\textasciicircum{}n m ell\_m p\_(n-m), n >= 1.}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:l12\endcsname{ell\_2 - q ell\_1 = -q\textasciicircum{}2/2 and ell\_1\textasciicircum{}2 - 2 ell\_2 = |xi|\textasciicircum{}4 (1-q)\textasciicircum{}4.}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:qxi\endcsname{q = ell\_1 - sqrt(ell\_1\textasciicircum{}2 - 2 ell\_2), |xi|\textasciicircum{}2 = sqrt(ell\_1\textasciicircum{}2 - 2 ell\_2)/(1-q)\textasciicircum{}2.}" "\n"
    "\\expandafter\\gdef\\csname CGTip@sec:real\\endcsname")

# ------------------------------------------------------------------ keywords
rep(r"\keywords{circuit quantum electrodynamics; dispersive coupling; thermal photons; Ramsey contrast; photon statistics;",
    r"\keywords{circuit quantum electrodynamics; dispersive coupling; thermal photons; Ramsey contrast; photon statistics; compound Poisson distribution;")

# ------------------------------------------------------------------ abstract
between("\\begin{abstract}", "\\end{abstract}", r"""\begin{abstract}
A two-level probe coupled dispersively to a cavity mode in a thermal state with mean occupation $\bar n$ has the well-known Ramsey contrast $V(u)=(1+4\bar n(\bar n+1)\sin^2\pi u)^{-1/2}$, where $u$ is the delay in units of the period of the dispersive phase. At the half period it equals $1/(2\bar n+1)$, which already gives $\bar n$ in this ideal model. No new coupling or measurement is proposed; the results are exact properties of functionals of the ideal contrast. We study the geometric mean of the contrast after the first return, $\mathcal V_s=\exp\big(s\int_1^\infty\log V(u)\,u^{-s-1}du\big)$, $s>0$. For every positive occupation, $p_0<\mathcal V_s<e^{-sG(s)}p_0$, where $p_0=1/(\bar n+1)$ is the vacuum probability and $G(s)=\int_1^\infty\log|2\sin\pi u|\,u^{-s-1}du$. Both constants are the best possible, and for $s=1$ the upper one is $\exp(C_g)/2=1.05195\ldots$, with $C_g=-\int_1^\infty\log|\sin\pi u|\,u^{-2}du$. For every photon-number distribution of compound Poisson type, that is, infinitely divisible with $p_0>0$, which includes thermal, Poisson and displaced thermal states, $p_0<\mathcal V_1\le p_0^{\,1-c}$ with $c=0.0409\ldots$, whereas for a given $p_0$ the half-period contrast can take every value in $[p_0^2,1]$. In the same class the Fourier coefficients of $\log V$ over the first period are $\log p_0$ and the coefficients of the compound Poisson form, so that the contrast before the first return determines the photon-number distribution; for a displaced thermal state two of them give the thermal ratio and the coherent amplitude in closed form. We also bound the effect of damping and of a finite range of delays, prove a sum rule, and relate $G$ and the transform $A$ of the delays before the first return to the Riemann zeta function. The functions $G$ and $A$ are shown with their computed zeros.
""")

# ------------------------------------------------------------------ introduction
between("\\section{Introduction}\\label{sec:intro}", "\\begin{table}[!htb]\n\\caption{Notation.}", r"""\section{Introduction}\label{sec:intro}

In a superconducting quantum processor each qubit is read out through a microwave resonator, and a few thermal photons left in that resonator are enough to dephase the qubit \cite{Rigetti2012,Sears2012}. The interaction responsible is dispersive: when the qubit is detuned from the resonator, its transition frequency shifts by a fixed amount for every photon in the mode \cite{Blais2004,Blais2021}. The same interaction turns the qubit into a probe of the photon statistics. This note is about exact properties of that probe. It does not introduce a new coupling or a new measurement primitive, and we first state what is known.

The dispersive phase as a meter of the photon number comes from atomic cavity quantum electrodynamics. Brune et al.\ proposed a quantum non-demolition measurement of small photon numbers by the phase-sensitive detection of Rydberg atoms coupled dispersively to the field \cite{Brune1990}: each photon shifts the phase of an atomic superposition, and a Ramsey interferometer converts that phase into a detection probability. With this method the quantum jumps of the photon number in a cavity were recorded \cite{Gleyzes2007}, and the progressive collapse of the field onto a photon number was observed by repeated measurements \cite{Guerlin2007}; see \cite[Sect.~6.2]{HarocheRaimond2006} and \cite{Haroche2013} for accounts of this work. A Ramsey sequence on a dispersively coupled qubit is the same measurement in a superconducting circuit \cite{Johnson2010}. With a trapped ion coupled dispersively to an optical cavity, the phase shift and the dephasing measured by Ramsey spectroscopy were used to reconstruct the photon-number distributions of coherent states and of a mixed thermal and coherent state \cite{Lee2019}.

In circuit quantum electrodynamics the same interaction is also read in the frequency domain. When the shift per photon exceeds all linewidths, the transition of the qubit splits into one line for each photon number. This was predicted in \cite{Gambetta2006} and observed in \cite{Schuster2007}, where the strengths of the lines distinguished a coherent field from a thermal one. A pulse that is selective on one line maps a chosen photon number onto the state of the qubit \cite{Johnson2010}, and Rabi oscillations driven on the separate lines are used to determine the occupation of the mode \cite{Sears2012}. The two families are Fourier-dual readings of one interaction: the resolved lines expose the individual probabilities $p_n$ of the photon number, and the coherence of the probe after a delay is their characteristic function \CGeqref{eq:D}. This holds for every photon-number distribution, and when both quadratures of the coherence are measured over one period the probabilities follow by Fourier inversion, \CGeqref{eq:inv}.

With a delay of half the period of the dispersive phase, the Ramsey sequence maps the photon-number parity of a cavity onto the qubit \cite{Sun2014}. Parity measurements are much more than one number: the Wigner function at a point of phase space is the expectation value of the parity displaced to that point \cite{Royer1977}, and parities measured after controlled displacements of the mode give the Wigner function of a cavity state \cite{Vlastakis2013}. In this note only the parity of the undisplaced mode enters, as the contrast at the half period.

For a thermal mode in contact with a bath the coherence of the probe is known in closed form: the result is due to Dykman and Krivoglaz \cite{DykmanKrivoglaz1987} and was derived again, including a drive, by Clerk and Utami \cite{ClerkUtami2007}. In this stationary Markovian model its decay at long times gives a dephasing rate that is used to interpret coherence times \cite{Rigetti2012}, and Ramsey experiments with injected thermal photons test it quantitatively \cite{Sears2012}. Thermal and coherent photon noise have been distinguished through the noise spectrum seen by the qubit \cite{Yan2018}, and a superconducting circuit has been used as a primary thermometer of the thermal occupation of propagating microwave modes \cite{Scigliuzzo2020}. More generally, the coherence of a probe is a partition function of the system to which it is coupled, continued to a complex parameter \cite{WeiLiu2012}, and such functions and their zeros have been measured \cite{Peng2015}.

In a mode without damping the photon number is constant during the sequence, and the contrast of a thermal state is the elementary closed form \CGeqref{eq:V}, the case without damping of \cite{DykmanKrivoglaz1987,ClerkUtami2007}. It is periodic in the delay and returns to $1$ at every multiple of the period $\pi/\chi$ of the dispersive phase, where $2\chi$ is the shift of the transition frequency per photon; we call these instants the returns (revivals). The loss of contrast between returns is a reversible dephasing among the photon-number sectors, undone at every return, not a decoherence. At the half period the contrast is the modulus of the mean parity, $1/(2\bar n+1)$, where $\bar n$ is the mean occupation. In this ideal model a single Ramsey delay therefore determines $\bar n$ exactly.

Nothing in the preceding paragraphs is new here: neither the Ramsey method, nor the contrast of a thermal mode, nor the fact that this contrast determines the occupation, nor the Fourier inversion of the coherence. Our contribution is not a new coupling or measurement primitive. We study nonlinear functionals of the ideal contrast $u\mapsto V(u)$ and prove exact relations between them and the photon statistics: best constants, statements that hold over a class of photon statistics, a bound for the effect of damping, a sum rule and the structure of a Mellin transform. Within the thermal model the half-period contrast is the simplest way to obtain $\bar n$, and the functionals studied here do not improve on it.

The objective is twofold. The first part is to determine how the contrast accumulated after the first return depends on the occupation of the mode, when it is averaged geometrically over the delay with a power weight, and to find the best constants in that dependence. The second part is to state precisely what functionals of the contrast alone, without its phase, determine about the photon statistics when the statistics is not known to be thermal.

The answer to the first part is Theorem~\CGref{thm:main}. For every exponent $s>0$ of the weight and every positive occupation, the geometric contrast $\mathcal V_s$ lies strictly between the probability $p_0$ that the mode is empty and $e^{-sG(s)}p_0$, and neither constant can be improved. Here $G$ is the transform \CGeqref{eq:G} of $\log|2\sin\pi u|$ on $[1,\infty)$. For the weight $u^{-2}$ the upper constant is $\exp(C_g)/2$, where $C_g$ is the log-sine constant \CGeqref{eq:Cg}. Corollary~\CGref{cor:bracket} turns the bound into a bracket for the occupation, and Corollary~\CGref{cor:half} combines it with the half-period contrast into a relation without parameters that holds for every thermal state and fails for coherent states of mean photon number at least $0.3$.

The answer to the second part has two pieces, which are the physical contributions of the note. Both concern photon-number distributions of compound Poisson type \CGeqref{eq:cp}; on the non-negative integers these are exactly the infinitely divisible distributions with $p_0>0$ \cite[p.~290]{Feller1968}. The class contains the thermal, the Poisson and the displaced thermal distributions, the last being the photon statistics of a coherent field superposed on thermal noise in one mode. It is a mathematically defined domain, not a standard classification of quantum optics, and it excludes many states: every state with $p_0=0$, such as the Fock states with at least one photon, and every distribution of finite support other than that of the vacuum. The first piece is Proposition~\CGref{prop:cp}. In this class the geometric contrast after the first return lies between $p_0$ and $p_0^{\,1-c_1(1)}$ with $c_1(1)=0.0409\ldots$, that is, the ratio $\log\mathcal V_1/\log p_0$ lies in $[1-c_1(1),1)=[0.959\ldots,1)$ without any further hypothesis on the statistics. This is an exact property of the ideal contrast, not an experimental error bar. The half-period contrast is the modulus of the mean photon-number parity; for a given $p_0$ it can take any value between $p_0^2$ and $1$ in the same class, and it gives $p_0$ or $\bar n$ only through the thermal hypothesis. A mode that holds residual coherent photons together with thermal ones, the situation analysed in \cite{ClerkUtami2007,Yan2018,Lee2019}, is of this kind. The second piece is Proposition~\CGref{prop:fourier}. Over the first period alone, $0<u<1$, the Fourier coefficients of $\log V$ are $\log p_0$ and the coefficients $b_m$ of the compound Poisson form, so that the contrast before the first return determines the whole distribution. For a displaced thermal state the first two coefficients give the thermal ratio and the coherent amplitude in closed form \CGeqref{eq:qxi}, a further relation tests that hypothesis, and a negative coefficient proves that the statistics is not of compound Poisson type. Both pieces concern the modulus $V$ alone. With the phase of the coherence, \CGeqref{eq:inv} gives the distribution for every statistics; what $V$ does not need is a phase reference, and an unknown static detuning between the probe and its analysis pulses changes the coherence but not the contrast.

Theorem~\CGref{thm:hot} gives the expansion of $\mathcal V_1$ at high occupation with an explicit remainder, and Proposition~\CGref{prop:trunc} bounds the effect of a finite range of delays. Section~\CGref{sec:real} treats the idealisations. Proposition~\CGref{prop:damp} bounds the effect of damping of the mode in the stationary Markovian thermal model, the rate equations of \cite{Sears2012,ClerkUtami2007}: the coherence changes by at most $4\bar n(\bar n+1)\kappa t$. This is a sufficient, worst-case bound. The condition it puts on the geometric contrast grows as $\bar n^3$, and the half-period contrast and the first period are less affected. Proposition~\CGref{prop:sum} shows that the integral of $\log V$ over all delays with the weight $u^{-2}$ is exactly $-\pi^2\bar n$. Proposition~\CGref{prop:harm} shows that the product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$ satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$. Section~\CGref{sec:GA} is about mathematical structure: it treats the function $G$ at complex exponents together with the companion transform $A$ of \CGeqref{eq:A}, which collects the delays before the first return, proves the identity \CGeqref{eq:GAzeta} that links them to the Riemann zeta function, and shows both functions with their computed zeros. These transforms are not proposed as observables, and their zeros are not interpreted as physical critical points.

On the mathematical side, the classical log-sine integrals are integrals of powers of $\log|2\sin(\theta/2)|$ against powers of $\theta$ over a finite interval, and their evaluation in terms of zeta values and polylogarithms has a long history; see \cite{BorweinStraub2012} and the references there. The function $G$ is of a different kind: it is a Mellin transform of $\log|2\sin\pi u|$ over the half-line $[1,\infty)$, and $C_g$ is $\log2$ minus its value at $s=1$. Mellin transforms over a half-line that represent the Riemann zeta function are classical, and the identity \CGeqref{eq:GAzeta} is of this type. We do not claim it as new; we prove it and use the way in which the first return splits it into $G$ and $A$. The sum rule \CGeqref{eq:sumrule} is an elementary consequence of the Dirichlet integral. The fact behind Proposition~\CGref{prop:fourier}, that in the class \CGeqref{eq:cp} the logarithm of the coherence has only non-negative frequencies, so that its real part determines it, is elementary as well. To our knowledge the bounds \CGeqref{eq:bound} and \CGeqref{eq:cpbound}, the role of $C_g$ as the sharp constant of the first, and the use of the Fourier coefficients of $\log V$ to separate thermal and coherent photons have not been stated before.

All statements except those of Section~\CGref{sec:real} and the remarks after Proposition~\CGref{prop:fourier} concern the ideal model \CGeqref{eq:H}: a single mode without damping, a probe without intrinsic dephasing, and a dispersive shift that is exactly linear in the photon number. The returns of the contrast to $1$ rest on these three idealisations, and Section~\CGref{sec:model} states the domain of validity of the model. The functionals studied here are computed from a set of Ramsey measurements; they are not measured in one shot. The deterministic bounds do not address the statistical problems of an estimator: shot noise, the bias of the logarithm of an estimated contrast at low contrast, detection floors and readout errors, the choice of the delays and of the quadrature, and drifts of $\chi$. The geometric contrast is an integral over unbounded delays, and it averages the logarithm of the contrast, so it gives weight to the delays where the contrast is small, down to $1/(2\bar n+1)$, where a measured contrast is most affected by noise and by damping. Propositions~\CGref{prop:cp} and~\CGref{prop:fourier} describe robust summaries of visibility data over a specified class of statistics; they are not optimal estimators and not a replacement for state tomography, and no experimental advantage over the existing methods of thermometry is claimed.

The proofs are elementary and self-contained. Four classical facts are used in the proofs: from \cite{DLMF} the product for the sine, the partial fractions of the cotangent and the Dirichlet integral, and from \cite{Glauber1963} the representation of the thermal state as a Gaussian mixture of coherent states. The characterisation of infinitely divisible distributions \cite{Feller1968} is quoted only to place the class \CGeqref{eq:cp}. The figures and tables are computed in double precision or in multiple precision arithmetic and illustrate the statements; the scripts that produce them accompany the note. Table~\CGref{tab:notation} lists the notation.

""")

# ------------------------------------------------------------------ notation
rep(r"$b_m$, $m\ge1$ & coefficients of the compound Poisson form \CGeqref{eq:cp}\\",
    r"$b_m$, $m\ge1$ & coefficients of the compound Poisson form \CGeqref{eq:cp}\\" "\n"
    r"$\ell_m$, $m\ge0$ & Fourier coefficients of $\log V$ over one period, \CGeqref{eq:ellm}\\" "\n"
    r"$\gamma$, $Q$ & $|\xi|^2(1-q)^2$; number of delays in the midpoint rule\\")

# ------------------------------------------------------------------ section 2: inversion and domain of validity
rep(r"The function $D$ is the coherence of the probe and $V$ is its contrast, the quantity measured in a Ramsey experiment with delay $t$. ",
    r"""The function $D$ is the coherence of the probe and $V$ is its contrast, the quantity measured in a Ramsey experiment with delay $t$; a Ramsey experiment that measures both quadratures gives $D$ itself, in the frame of the analysis pulses. The definition \CGeqref{eq:D} makes sense for every probability distribution $(p_n)_{n\ge0}$ on the non-negative integers, and then $D$ is its characteristic function. Since the series in \CGeqref{eq:D} converges uniformly in $u$ and $\int_0^1e^{2\pi i(n-k)u}du$ is $1$ for $k=n$ and $0$ otherwise, every such distribution is recovered from $D$ over one period:
\begin{equation}\label{eq:inv}
p_n=\int_0^1D(u)\,e^{2\pi inu}\,du,\qquad n\ge0 .
\end{equation}
""")
rep(r"The integers $u=1,2,3,\dots$ are the returns of the contrast. Figure~\CGref{fig:bound} shows $V$ for three temperatures.",
    r"""The integers $u=1,2,3,\dots$ are the returns of the contrast. Figure~\CGref{fig:bound} shows $V$ for three temperatures.

Domain of validity. The Hamiltonian \CGeqref{eq:H} is an effective model. It holds in the dispersive regime, in which the probe is detuned from the mode and the photon number is well below a critical number fixed by the coupling and the detuning \cite{Blais2004,Blais2021}. For a transmon, $\chi$ is the measured effective shift, which includes the contribution of the higher levels of the transmon \cite{Koch2007}, and corrections that depend on the photon number are analysed in \cite{Boissonneault2009}. A negative $\chi$ is absorbed by writing $|\chi|$ in $u$, because it replaces $D$ by its complex conjugate and leaves $V$ unchanged. We further assume a single mode coupled to the probe, a photon-number distribution that does not change during the sequence, no exchange of energy between probe and mode, a shift $\chi$ calibrated and stable over the largest delay used, and a phase exactly linear in the photon number over that delay. Since the evolution is diagonal in the photon number, the coherence \CGeqref{eq:D} depends only on the probabilities $p_n$, that is, on the diagonal of the state of the mode; coherences between different photon numbers are not seen by this sequence. Section~\CGref{sec:real} treats damping, intrinsic dephasing and a nonlinear shift. Finally, $\bar n$ is the effective occupation of the mode. It is the Bose--Einstein occupation at a temperature only if the mode is in equilibrium with an environment at that temperature; residual photons from imperfect filtering or from earlier drives need not be thermal, which is one reason to consider other statistics in Section~\CGref{sec:main}.""")

# ------------------------------------------------------------------ section 4: the class
rep(r"""At $z=1$ this gives $\sum_mb_m=-\log p_0$. For such a distribution we keep""",
    r"""At $z=1$ this gives $\sum_mb_m=-\log p_0$. On the non-negative integers the distributions of compound Poisson type are exactly the infinitely divisible distributions with $p_0>0$ \cite[p.~290]{Feller1968}; this characterisation is not used in the proofs. If $p_0<1$, some $b_M$ is positive, and expanding the exponential in \CGeqref{eq:cp}, a product of power series with non-negative coefficients, gives $p_{kM}\ge p_0b_M^k/k!>0$ for every integer $k\ge0$. A distribution of this type with $p_0<1$ therefore has infinite support: the distributions of finite support other than that of the vacuum, for example those of the Fock states with at least one photon and the binomial distributions, are outside the class, and so is every state with $p_0=0$. For such a distribution we keep""")

rep(r"""It is exact for the thermal state, $9$ per cent too low for $|\xi|^2=1$ and $35$ per cent too low for the Poisson distribution.""",
    r"""It is exact for the thermal state, $9$ per cent too low for $|\xi|^2=1$ and $35$ per cent too low for the Poisson distribution. The photon number of a displaced thermal state is not the sum of independent thermal and Poisson photon numbers: that sum has $b_1=q+|\xi|^2$ and $b_m=q^m/m$ for $m\ge2$, which differ from \CGeqref{eq:dt}.""")

rep(r"""The vacuum probability is the quantity read by a pulse selective on the zero-photon line \cite{Johnson2010,Sears2012}; the geometric contrast reaches it without selective pulses. Within the thermal model the half-period contrast remains the simpler way to obtain $\bar n$, and Section~\CGref{sec:real} shows that it is also less affected by damping.""",
    r"""This concerns one parity value of the undisplaced mode; parities measured after displacements determine the state \cite{Royer1977,Vlastakis2013}. The vacuum probability is the quantity read by a pulse selective on the zero-photon line \cite{Johnson2010,Sears2012}; in the ideal model the geometric contrast brackets it without selective pulses, but an estimate from data is subject to the statistical caveats of the introduction. The geometric contrast is a robust summary of visibility data over this class, not an optimal estimator. Within the thermal model the half-period contrast remains the simpler way to obtain $\bar n$, and Section~\CGref{sec:real} shows that it is also less affected by damping. Proposition~\CGref{prop:fourier} below shows that, in the same class, the first period gives more than $p_0$.""")

# ------------------------------------------------------------------ section 5: damping, conditional language
rep(r"""Let the mode be damped at the rate $\kappa>0$ by a bath with the same occupation $\bar n$, so that the thermal state of the mode is stationary.""",
    r"""Let the mode be damped at the rate $\kappa>0$ by a bath with the same occupation $\bar n$, so that the thermal state of the mode is stationary. This equality is an assumption: the bound below does not cover a mode that relaxes from another occupation, driven nonequilibrium noise or a non-Markovian bath.""")

rep(r"""For $\chi/2\pi=1$~MHz these are $\kappa/2\pi<3.0$~kHz, $66$~Hz and $0.023$~Hz. Cavity linewidths $\kappa/2\pi$ between $6$ and $120$~kHz are reported in \cite{Sears2012}, and a single-photon lifetime of $25.6$~ms, that is $\kappa/2\pi=6.2$~Hz, in \cite{Milul2023}. The geometric contrast is therefore usable at low occupation in long-lived modes, and the statements of Section~\CGref{sec:main} at high occupation, such as the example $\bar n=20$ after Corollary~\CGref{cor:bracket}, are statements about the ideal model only.""",
    r"""For $\chi/2\pi=1$~MHz these are $\kappa/2\pi<3.0$~kHz, $66$~Hz and $0.023$~Hz. The relevant comparison is that of $\kappa/\chi$ within one device. For orientation only, since the following figures come from different devices: cavity linewidths $\kappa/2\pi$ between $6$ and $120$~kHz with $\chi/2\pi=7$~MHz are reported in \cite{Sears2012}, a cavity memory with millisecond coherence in circuit quantum electrodynamics in \cite{Reagor2016}, and a single-photon lifetime of $25.6$~ms, that is $\kappa/2\pi=6.2$~Hz, in \cite{Milul2023}. Corollary~\CGref{cor:damp} is a sufficient condition derived from a worst-case bound in the stationary Markovian thermal model. It shows where the ideal statements remain valid in that model, at low occupation and in long-lived modes, but it does not show where an estimate becomes unusable; for a given device the exact solution of \cite{DykmanKrivoglaz1987,ClerkUtami2007} or a simulation of \CGeqref{eq:master} is the benchmark. The statements of Section~\CGref{sec:main} at high occupation, such as the example $\bar n=20$ after Corollary~\CGref{cor:bracket}, are statements about the ideal model only.""")

rep(r"""Since $V(k)=1$ at the returns, the contrast measured at $u=k$ is $f(\pi k/\chi)$: the returns measure the decay of the probe itself, which can then be divided out.""",
    r"""This is a factorised phenomenological model: it assumes that the decay of the probe is independent of the photons, and the relaxation of the probe is not of this form in general. Since $V(k)=1$ at the returns, the contrast measured at $u=k$ is $f(\pi k/\chi)$: when damping and a nonlinear shift, which also lower the contrast at the returns, are negligible, the returns measure the decay of the probe itself, which can then be divided out; otherwise independent calibrations of the probe are needed.""")

rep(r"""which is below $1$ in general.""",
    r"""which is below $1$ in general. Corrections of this kind to the linear dispersive shift appear at larger photon numbers \cite{Boissonneault2009}. As an order of magnitude, for a thermal state the phases $\pi k\chi_2n(n-1)/\chi$ spread over an interval of width comparable to $\pi k|\chi_2|\bar n^2/\chi$, so that late returns and high occupation are affected together. The self-Kerr term of the mode, which shifts the energy of $n$ photons by an amount independent of the state of the probe, does not enter $D$; it causes the collapse and revival of a coherent state of the mode itself, observed in \cite{Kirchmair2013}.""")

# ------------------------------------------------------------------ new section 6
rep(r"""\section{The sum rule and the harmonic delays}\label{sec:sum}""",
    r"""\section{The first period and the Fourier coefficients of the logarithm of the contrast}\label{sec:fourier}

Proposition~\CGref{prop:cp} uses the delays after the first return. The delays before it, $0<u<1$, carry more: in the compound Poisson class they determine the whole photon-number distribution through the Fourier coefficients of $\log V$. For a distribution $(p_n)_{n\ge0}$ for which $\log V$ is integrable on $(0,1)$, put
\begin{equation}\label{eq:ellm}
\ell_0=\int_0^1\log V(u)\,du,\qquad \ell_m=2\int_0^1\log V(u)\cos(2\pi mu)\,du,\quad m\ge1 .
\end{equation}
For a distribution of compound Poisson type, $\log V(u)=\log p_0+\sum_mb_m\cos(2\pi mu)\ge2\log p_0$ by the proof of Proposition~\CGref{prop:cp}, so that $\log V$ is bounded and the $\ell_m$ are defined.

\begin{proposition}\label{prop:fourier}
(a) Let $(p_n)_{n\ge0}$ be of compound Poisson type \CGeqref{eq:cp}. Then $\ell_0=\log p_0$ and $\ell_m=b_m$ for every $m\ge1$. The numbers $\ell_m$ determine the distribution: $p_0=e^{\ell_0}$ and
\begin{equation}\label{eq:recursion}
n\,p_n=\sum_{m=1}^{n}m\,\ell_m\,p_{n-m},\qquad n\ge1 .
\end{equation}
The mean photon number $\sum_nnp_n$ equals $\sum_mm\,\ell_m$, both sides being possibly infinite.

(b) Let $(p_n)_{n\ge0}$ be a distribution with $p_0>0$ for which $\log V$ is integrable on $(0,1)$. If $\ell_m<0$ for some $m\ge1$, then $(p_n)$ is not of compound Poisson type.

(c) For the photon-number distribution of the displaced thermal state \CGeqref{eq:dt}, with $0<q<1$ and $\xi\in\mathbb C$,
\begin{equation}\label{eq:l12}
\ell_2-q\,\ell_1=-\frac{q^2}2,\qquad \ell_1^2-2\ell_2=|\xi|^4(1-q)^4,
\end{equation}
so that
\begin{equation}\label{eq:qxi}
q=\ell_1-\sqrt{\ell_1^2-2\ell_2},\qquad |\xi|^2=\frac{\sqrt{\ell_1^2-2\ell_2}}{(1-q)^2},
\end{equation}
and $\ell_0=\log(1-q)-|\xi|^2(1-q)$.
\end{proposition}

\begin{proof}
(a) By the proof of Proposition~\CGref{prop:cp}, $\log V(u)=\log p_0+\sum_{m\ge1}b_m\cos(2\pi mu)$, a series that converges absolutely and uniformly in $u$. Integrating it term by term over $[0,1]$, with $\int_0^1\cos(2\pi mu)\,du=0$ and $2\int_0^1\cos(2\pi mu)\cos(2\pi ku)\,du$ equal to $1$ for $k=m$ and to $0$ for $k\ne m$, $m,k\ge1$, gives $\ell_0=\log p_0$ and $\ell_m=b_m$. For complex $z$ with $|z|<1$ put $f(z)=\sum_mb_mz^m$. Since $0\le b_m\le-\log p_0$, the series $f$ and $f'(z)=\sum_mm\,b_mz^{m-1}$ converge for $|z|<1$, and the derivative of \CGeqref{eq:cp} is $\sum_nn\,p_nz^{n-1}=\big(\sum_np_nz^n\big)f'(z)$. Comparing the coefficients of $z^{n-1}$ gives \CGeqref{eq:recursion} with $b_m$ in place of $\ell_m$. It determines $p_n$ from $p_0,\dots,p_{n-1}$ and $\ell_1,\dots,\ell_n$. For $0<z<1$ all the series involved have non-negative terms, and as $z\to1^-$, $\sum_nn\,p_nz^{n-1}\to\sum_nn\,p_n$, $\sum_np_nz^n\to1$ and $f'(z)\to\sum_mm\,b_m$, each limit in $[0,\infty]$, by monotone convergence. This gives the mean.

(b) If $(p_n)$ were of compound Poisson type, (a) would give $\ell_m=b_m\ge0$ for every $m\ge1$.

(c) By \CGeqref{eq:dt} and (a), $\ell_1=q+\gamma$ and $\ell_2=\frac{q^2}2+q\gamma$ with $\gamma=|\xi|^2(1-q)^2\ge0$. Hence $\ell_2-q\ell_1=-\frac{q^2}2$ and $\ell_1^2-2\ell_2=q^2+2q\gamma+\gamma^2-q^2-2q\gamma=\gamma^2$. Since $\gamma\ge0$, $\sqrt{\ell_1^2-2\ell_2}=\gamma$, which gives $q=\ell_1-\gamma$ and $|\xi|^2=\gamma/(1-q)^2$. The value of $\ell_0$ is $\log p_0$ with $p_0$ from \CGeqref{eq:dt}.
\end{proof}

The other root of the quadratic equation $q^2-2\ell_1q+2\ell_2=0$ given by \CGeqref{eq:l12} is $\ell_1+\gamma=q+2|\xi|^2(1-q)^2$, which is not the thermal ratio unless $\xi=0$; so \CGeqref{eq:qxi} is the only solution. The relation for $\ell_0$ is not used in \CGeqref{eq:qxi} and tests the displaced thermal hypothesis, and so do the higher coefficients, $\ell_m=q^m/m+|\xi|^2(1-q)^2q^{m-1}$. The independent sum of a thermal and a Poisson photon number has instead $\ell_1=q+|\xi|^2$ and $\ell_m=q^m/m$ for $m\ge2$, and the two statistics are distinguished. Near $\xi=0$ the estimate of $|\xi|^2$ is sensitive: an error $\delta>0$ in $\ell_1^2-2\ell_2$ near $0$ gives an error of order $\sqrt\delta/(1-q)^2$ in $|\xi|^2$.

Part (b) is one-sided. For the distribution with $p_0=\frac23$ and $p_1=\frac13$, $D(u)=\frac23\big(1+\frac12e^{-2\pi iu}\big)$, and the power series of the principal logarithm at $-\frac12e^{-2\pi iu}$ gives $\log V(u)=\log\frac23+\sum_{m\ge1}\frac{(-1)^{m+1}}{m\,2^m}\cos(2\pi mu)$, so that $\ell_0=\log p_0$ and $\ell_2=-\frac18<0$, which excludes the class. For the Fock state with one photon $V\equiv1$, and all the $\ell_m$ vanish, as for the vacuum: the contrast alone does not distinguish the two.

What the phase adds. With both quadratures of the coherence, \CGeqref{eq:inv} gives every $p_n$ for every distribution, so Proposition~\CGref{prop:fourier} is a statement about the contrast alone. An unknown static detuning between the probe and its analysis pulses multiplies $D(u)$ by a phase factor linear in $u$, which changes the result of \CGeqref{eq:inv} but not $V$. For the thermal state with $\bar n=\frac12$ and a detuning equal to $0.1$ times the shift $2\chi$ per photon, \CGeqref{eq:inv} evaluated on the detuned coherence gives $0.647$, $0.146$ and $0.016$ in place of $p_0=0.667$, $p_1=0.222$ and $p_2=0.074$, while \CGeqref{eq:qxi} applied to the coefficients of $\log V$ returns $q=\frac13$ and $|\xi|^2=0$ with errors below $2\times10^{-8}$, which come from the square root of rounding errors in $\ell_1^2-2\ell_2$.

Sampling. The midpoint rule with equally spaced delays $u=(j+\frac12)/Q$, $0\le j\le Q-1$, replaces $\ell_m$, for $1\le m<Q/2$, by $\ell_m$ plus a signed sum of the $\ell_k$ with $k\equiv\pm m$ modulo $Q$ and $k\ne m$, all of which have $k\ge Q-m$, because the rule integrates $\cos(2\pi ku)$ exactly to $0$ unless $Q$ divides $k$. Since $\ell_k$ decays like $q^k$ for a displaced thermal state, the number $Q$ of delays must be large compared with $1/\log(1/q)$, which is about $\bar n$ at high occupation. With $Q=64$ the coefficients $\ell_0$, $\ell_1$, $\ell_2$ of the displaced thermal states of Table~\CGref{tab:robust} are reproduced to $10^{-15}$, and with $Q=16$ to $6\times10^{-7}$; for $q=0.8$, $Q=16$ leaves errors between $3\times10^{-3}$ and $10^{-2}$ in $\ell_1$ and $\ell_2$, and $Q=64$ errors below $2\times10^{-7}$. These are statements about noise-free samples; the statistical caveats of the introduction apply, and $\log V$ is least reliable near the half period, where $V$ is smallest.

Window and damping. The coefficients \CGeqref{eq:ellm} use only delays shorter than the first return, $t<\pi/\chi$. For the thermal state, the proof of Corollary~\CGref{cor:damp} with $U$ replaced by $1$ gives $|\log V_\kappa(\pi u/\chi)-\log V(u)|\le-\log(1-\epsilon_1)$ for $0\le u\le1$, where $\epsilon_1=\pi\Lambda(2\bar n+1)\kappa/\chi<1$. Since $|\cos(2\pi mu)|\le1$, the coefficients computed from the damped contrast differ from those of \CGeqref{eq:ellm} by at most $-\log(1-\epsilon_1)$ for $m=0$ and $-2\log(1-\epsilon_1)$ for $m\ge1$. The largest delay is $U$ times smaller than in the range $1\le u\le U$ of Corollary~\CGref{cor:damp}. For $\bar n=\frac12$ and $\kappa/(2\chi)=10^{-3}$ the closed form of \cite{ClerkUtami2007} on $64$ delays gives $q$ too low by $2.1\times10^{-3}$, with $\ell_1^2-2\ell_2<0$, that is, no spurious coherent part. Proposition~\CGref{prop:damp} is proved for the stationary thermal state only, and no bound is claimed for a damped displaced thermal state.

The separation of thermal and coherent photons by the qubit has been obtained from the noise spectrum seen by the qubit \cite{Yan2018} and, with a trapped ion, from the phase shift and the dephasing \cite{Lee2019}. Proposition~\CGref{prop:fourier} gives it from the contrast over one period, in closed form, within the ideal model and the class \CGeqref{eq:cp}.

\section{The sum rule and the harmonic delays}\label{sec:sum}""")

# ------------------------------------------------------------------ harmonic product: engineered realization
rep(r"""and equal occupation $\bar n$, because the coherences of independent modes multiply.""",
    r"""and equal occupation $\bar n$, because the coherences of independent modes multiply. This multimode reading is an engineered realisation: it needs modes in independent thermal states of equal occupation, couplings exactly $\chi/k$ and no couplings between the modes, and it is not a property of a generic multimode cavity.""")

# ------------------------------------------------------------------ section GA: mathematical structure
rep(r"""Theorem~\CGref{thm:main} uses $G$ on the positive real axis. At complex exponents the same function describes the hot limit of the contrast against weights that oscillate in the logarithm of the delay.""",
    r"""This section is about mathematical structure. The coherence of a probe encodes a generating function, and the zeros of such functions at complex parameters have a physical meaning in other settings \cite{WeiLiu2012,Peng2015}. The transforms below are a different object: weighted integrals of $\log V$ against powers of the delay with complex exponents, computed from the contrast and not proposed as observables of circuit quantum electrodynamics. A zero of $G$ is a cancellation under this transform, not a zero of a physical partition function nor a critical point, and the identity with the Riemann zeta function gives no physical access to the zeros of that function.

Theorem~\CGref{thm:main} uses $G$ on the positive real axis. At complex exponents the same function describes the hot limit of the contrast against weights that oscillate in the logarithm of the delay.""")

# ------------------------------------------------------------------ conclusions
between("\\section{Conclusions}\\label{sec:concl}", "\\begin{thebibliography}", r"""\section{Conclusions}\label{sec:concl}

The Ramsey method, the dispersive coherence as characteristic function of the photon number, the thermal contrast, its value at the half period and the Fourier inversion of the coherence are established. The conclusions below are exact statements about functionals of the ideal contrast.

The main conclusion is the bound \CGeqref{eq:boundCg}. For a two-level probe coupled dispersively to a thermal mode, the geometric mean of the Ramsey contrast after the first return, taken with the weight $u^{-2}$, satisfies $p_0<\mathcal V_1<\frac12\exp(C_g)\,p_0$ for every positive occupation, where $p_0$ is the probability that the mode is empty and $C_g=0.743794\ldots$ is the log-sine constant \CGeqref{eq:Cg}. The two constants $1$ and $\frac12\exp(C_g)=1.05195\ldots$ cannot be improved. The log-sine constant is thus the sharp constant of a functional of the ideal contrast that can in principle be estimated from a sequence of Ramsey measurements: no thermal state gives a ratio $\mathcal V_1/p_0$ above $\frac12\exp(C_g)$, and every smaller constant is exceeded at a sufficiently high occupation.

The second conclusion is the physical one and concerns photon statistics that are not known to be thermal. Over the compound Poisson class, that is, the infinitely divisible photon-number distributions with $p_0>0$, which contains the thermal, Poisson and displaced thermal distributions, $p_0<\mathcal V_1\le p_0^{\,1-c_1(1)}$ with $c_1(1)=0.0409\ldots$, so that the ratio $\log\mathcal V_1/\log p_0$ lies in $[1-c_1(1),1)$ without a further hypothesis on the statistics, whereas one parity value of the undisplaced mode, the half-period contrast, can take any value between $p_0^2$ and $1$ for a given $p_0$ (Proposition~\CGref{prop:cp}). Over the same class the first period alone determines the statistics: the Fourier coefficients of $\log V$ on $0<u<1$ are $\log p_0$ and the coefficients $b_m$; for a displaced thermal state the first two give the thermal ratio and the coherent amplitude in closed form, with a relation that tests the hypothesis, and a negative coefficient excludes the class (Proposition~\CGref{prop:fourier}). Both statements use the contrast without its phase, and so need no phase reference; with the phase, \CGeqref{eq:inv} gives every $p_n$. They describe robust summaries of visibility data over a specified class, not optimal estimators, and the class excludes many states, among them every state with $p_0=0$ and every distribution of finite support other than that of the vacuum.

The third conclusion concerns damping. In the stationary Markovian thermal model the coherence differs from the ideal one by at most $4\bar n(\bar n+1)\kappa t$ (Proposition~\CGref{prop:damp}). For the geometric contrast over $1\le u\le U$ this sufficient, worst-case bound asks for $\kappa/\chi$ well below $1/\big(4\pi\bar n(\bar n+1)(2\bar n+1)U\big)$, a condition that can be met at low occupation in long-lived modes and not at high occupation; the half-period contrast and the first period are less affected (Corollary~\CGref{cor:damp} and Section~\CGref{sec:fourier}). When damping and nonlinear shifts are negligible, the returns of the contrast measure the intrinsic decay of the probe; a contrast below $1$ at the returns after that correction signals damping or a nonlinear shift.

Further conclusions follow from the same analysis. The bound holds for every power weight $u^{-s-1}$ with $s>0$, with the sharp constant $e^{-sG(s)}$, so that the function $G$ on the positive real axis is the logarithm of the sharp constant divided by $-s$ (Theorem~\CGref{thm:main}). For thermal states the occupation is bracketed by the geometric contrast alone, $1/\mathcal V_1-1<\bar n<\exp(C_g)/(2\mathcal V_1)-1$ (Corollary~\CGref{cor:bracket}), and the geometric and half-period contrasts satisfy the relation \CGeqref{eq:half}, which contains no parameter and which coherent states of mean photon number at least $0.3$ violate (Corollary~\CGref{cor:half}). At high occupation $\mathcal V_1=\frac12\exp(C_g)p_0\,q^{\pi^2/12-3/4}e^{R}$ with $0<R\le\frac{\tau^2}{\pi^2}(\frac52+\frac12\log\frac1\tau)$ (Theorem~\CGref{thm:hot}). A finite range of delays $1\le u\le U$ changes $\log\mathcal V_s$ by at most $U^{-s}\log(2\bar n+1)$ (Proposition~\CGref{prop:trunc}). The integral of the logarithm of the contrast over all delays with the weight $u^{-2}$ is exactly $-\pi^2\bar n$, and the first return separates it into a part within $C_g-\log2$ of $\log p_0$ and a part that carries the linear term (Proposition~\CGref{prop:sum}). The product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$ satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$, with the explicit bound \CGeqref{eq:harm} for its logarithmic rate (Proposition~\CGref{prop:harm}).

As mathematical structure, at complex exponents $G$ is the hot limit of the transform of $\log(V/p_0)$ after the first return, and its zeros are the weights on which that excess has no component (Proposition~\CGref{prop:complex}). Together with the transform $A$ of the delays before the first return it satisfies $G-A=\frac\pi s\cot(\frac{\pi s}2)\zeta$, so that in the strip $0<\operatorname{Re}s<2$ the two transforms coincide at a non-real exponent exactly at the zeros of the Riemann zeta function (Proposition~\CGref{prop:A}). This is a consequence of an explicit factorisation; it gives no information on the location of those zeros, and they are not interpreted as physical critical points.

""")

# ------------------------------------------------------------------ bibliography
rep(r"""\bibitem{Blais2021}""", r"""\bibitem{Blais2004}
A.~Blais, R.-S.~Huang, A.~Wallraff, S.~M.~Girvin and R.~J.~Schoelkopf, Cavity quantum electrodynamics for superconducting electrical circuits: an architecture for quantum computation, \emph{Phys. Rev. A} \textbf{69} (2004), 062320.
\href{https://doi.org/10.1103/PhysRevA.69.062320}{doi:10.1103/PhysRevA.69.062320};
\href{https://arxiv.org/abs/cond-mat/0402216}{arXiv:cond-mat/0402216}.

\bibitem{Blais2021}""")

rep(r"""\bibitem{BorweinStraub2012}""", r"""\bibitem{Boissonneault2009}
M.~Boissonneault, J.~M.~Gambetta and A.~Blais, Dispersive regime of circuit QED: photon-dependent qubit dephasing and relaxation rates, \emph{Phys. Rev. A} \textbf{79} (2009), 013819.
\href{https://doi.org/10.1103/PhysRevA.79.013819}{doi:10.1103/PhysRevA.79.013819};
\href{https://arxiv.org/abs/0810.1336}{arXiv:0810.1336}.

\bibitem{BorweinStraub2012}""")

rep(r"""\bibitem{Glauber1963}""", r"""\bibitem{Feller1968}
W.~Feller, \emph{An Introduction to Probability Theory and Its Applications}, Vol.~I, 3rd ed., Wiley, New York, 1968. No DOI.

\bibitem{Glauber1963}""")

rep(r"""\bibitem{Johnson2010}""", r"""\bibitem{Gleyzes2007}
S.~Gleyzes, S.~Kuhr, C.~Guerlin, J.~Bernu, S.~Del\'eglise, U.~Busk Hoff, M.~Brune, J.-M.~Raimond and S.~Haroche, Quantum jumps of light recording the birth and death of a photon in a cavity, \emph{Nature} \textbf{446} (2007), 297--300.
\href{https://doi.org/10.1038/nature05589}{doi:10.1038/nature05589};
\href{https://arxiv.org/abs/quant-ph/0612031}{arXiv:quant-ph/0612031}.

\bibitem{Guerlin2007}
C.~Guerlin, J.~Bernu, S.~Del\'eglise, C.~Sayrin, S.~Gleyzes, S.~Kuhr, M.~Brune, J.-M.~Raimond and S.~Haroche, Progressive field-state collapse and quantum non-demolition photon counting, \emph{Nature} \textbf{448} (2007), 889--893.
\href{https://doi.org/10.1038/nature06057}{doi:10.1038/nature06057};
\href{https://arxiv.org/abs/0707.3880}{arXiv:0707.3880}.

\bibitem{Haroche2013}
S.~Haroche, Nobel Lecture: Controlling photons in a box and exploring the quantum to classical boundary, \emph{Rev. Mod. Phys.} \textbf{85} (2013), 1083--1102.
\href{https://doi.org/10.1103/RevModPhys.85.1083}{doi:10.1103/RevModPhys.85.1083}.

\bibitem{HarocheRaimond2006}
S.~Haroche and J.-M.~Raimond, \emph{Exploring the Quantum: Atoms, Cavities, and Photons}, Oxford University Press, Oxford, 2006.
\href{https://doi.org/10.1093/acprof:oso/9780198509141.001.0001}{doi:10.1093/acprof:oso/9780198509141.001.0001}.

\bibitem{Johnson2010}""")

rep(r"""\bibitem{Milul2023}""", r"""\bibitem{Kirchmair2013}
G.~Kirchmair, B.~Vlastakis, Z.~Leghtas, S.~E.~Nigg, H.~Paik, E.~Ginossar, M.~Mirrahimi, L.~Frunzio, S.~M.~Girvin and R.~J.~Schoelkopf, Observation of quantum state collapse and revival due to the single-photon Kerr effect, \emph{Nature} \textbf{495} (2013), 205--209.
\href{https://doi.org/10.1038/nature11902}{doi:10.1038/nature11902};
\href{https://arxiv.org/abs/1211.2228}{arXiv:1211.2228}.

\bibitem{Koch2007}
J.~Koch, T.~M.~Yu, J.~Gambetta, A.~A.~Houck, D.~I.~Schuster, J.~Majer, A.~Blais, M.~H.~Devoret, S.~M.~Girvin and R.~J.~Schoelkopf, Charge-insensitive qubit design derived from the Cooper pair box, \emph{Phys. Rev. A} \textbf{76} (2007), 042319.
\href{https://doi.org/10.1103/PhysRevA.76.042319}{doi:10.1103/PhysRevA.76.042319};
\href{https://arxiv.org/abs/cond-mat/0703002}{arXiv:cond-mat/0703002}.

\bibitem{Lee2019}
M.~Lee, K.~Friebe, D.~A.~Fioretto, K.~Sch\"uppert, F.~R.~Ong, D.~Plankensteiner, V.~Torggler, H.~Ritsch, R.~Blatt and T.~E.~Northup, Ion-based quantum sensor for optical cavity photon numbers, \emph{Phys. Rev. Lett.} \textbf{122} (2019), 153603.
\href{https://doi.org/10.1103/PhysRevLett.122.153603}{doi:10.1103/PhysRevLett.122.153603};
\href{https://arxiv.org/abs/1810.13340}{arXiv:1810.13340}.

\bibitem{Milul2023}""")

rep(r"""\bibitem{Rigetti2012}""", r"""\bibitem{Reagor2016}
M.~Reagor, W.~Pfaff, C.~Axline, R.~W.~Heeres, N.~Ofek, K.~Sliwa, E.~Holland, C.~Wang, J.~Blumoff, K.~Chou, M.~J.~Hatridge, L.~Frunzio, M.~H.~Devoret, L.~Jiang and R.~J.~Schoelkopf, Quantum memory with millisecond coherence in circuit QED, \emph{Phys. Rev. B} \textbf{94} (2016), 014506.
\href{https://doi.org/10.1103/PhysRevB.94.014506}{doi:10.1103/PhysRevB.94.014506};
\href{https://arxiv.org/abs/1508.05882}{arXiv:1508.05882}.

\bibitem{Rigetti2012}""")

rep(r"""\bibitem{Schuster2007}""", r"""\bibitem{Royer1977}
A.~Royer, Wigner function as the expectation value of a parity operator, \emph{Phys. Rev. A} \textbf{15} (1977), 449--450.
\href{https://doi.org/10.1103/PhysRevA.15.449}{doi:10.1103/PhysRevA.15.449}.

\bibitem{Schuster2007}""")

rep(r"""\bibitem{WeiLiu2012}""", r"""\bibitem{Vlastakis2013}
B.~Vlastakis, G.~Kirchmair, Z.~Leghtas, S.~E.~Nigg, L.~Frunzio, S.~M.~Girvin, M.~Mirrahimi, M.~H.~Devoret and R.~J.~Schoelkopf, Deterministically encoding quantum information using 100-photon Schr\"odinger cat states, \emph{Science} \textbf{342} (2013), 607--610.
\href{https://doi.org/10.1126/science.1243289}{doi:10.1126/science.1243289}.

\bibitem{WeiLiu2012}""")

open(sys.argv[2], 'w').write(s + '\n\\end{document}\n' + tail)
print('wrote', sys.argv[2])
