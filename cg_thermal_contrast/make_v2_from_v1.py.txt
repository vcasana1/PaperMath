"""Apply the corrections of the referee report (12 Nov 2026) to Cg_Thermal_Contrast_v1.tex -> v2.
Not applied, by order of the author: certification of the zeros (the mathematics is not touched)."""
import re
src = open('Cg_Thermal_Contrast_v1_received.tex').read()
head, tail = src.split('\n\\end{document}\n', 1)
s = head


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# ------------------------------------------------------------------ tips of new labels, renumbered theorem
rep(r"\expandafter\gdef\csname CGTip@thm:hot\endcsname{Theorem 4.3: expansion", r"\expandafter\gdef\csname CGTip@thm:hot\endcsname{Theorem 4.4: expansion")
rep(r"\expandafter\gdef\csname CGTip@fig:bound\endcsname",
    r"\expandafter\gdef\csname CGTip@cor:half\endcsname{Corollary 4.3: relation without parameters between the geometric contrast and the half-period contrast of a thermal state.}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:half\endcsname{2 V(1/2)/(1 + V(1/2)) < V\_1 < (exp(C\_g)/2) 2 V(1/2)/(1 + V(1/2)).}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:coh\endcsname{Coherent state of mean nu: (1 + exp(-2 nu))/(2 exp(-2 nu)) exp(-nu (1 - c\_1(1))) = exp(nu c\_1(1)) cosh(nu).}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:VsU\endcsname{V\_(s,U) = exp((s/(1 - U\textasciicircum{}(-s))) int\_1\textasciicircum{}U log V(u) u\textasciicircum{}(-s-1) du): geometric contrast over 1 <= u <= U.}" "\n"
    r"\expandafter\gdef\csname CGTip@prop:trunc\endcsname{Proposition 4.5: effect of a finite range of delays on the geometric contrast.}" "\n"
    r"\expandafter\gdef\csname CGTip@eq:trunc\endcsname{|log V\_(s,U) - log V\_s| <= L U\textasciicircum{}(-s), L = log(2 nbar + 1).}" "\n"
    r"\expandafter\gdef\csname CGTip@fig:bound\endcsname")
rep(r"pdfkeywords={dispersive coupling, thermal photons,", r"pdfkeywords={circuit quantum electrodynamics, dispersive coupling, thermal photons,")

# ------------------------------------------------------------------ review marks hidden in the PDF
# review marks removed by order of the author
s = re.sub(r'\\VCGreviewed\{\d+\}', '', s)
m0 = s.index('% CorrectVCG review marks:')
m1 = s.index('\\makeatother\n', m0) + len('\\makeatother\n')
s = s[:m0] + s[m1:]

# ------------------------------------------------------------------ abstract
a0 = s.index("\\begin{abstract}")
a1 = s.index("\\end{abstract}")
s = s[:a0] + r"""\begin{abstract}
A two-level probe coupled dispersively to a cavity mode in a thermal state with mean occupation $\bar n$ has the well-known Ramsey contrast $V(u)=(1+4\bar n(\bar n+1)\sin^2\pi u)^{-1/2}$, where $u$ is the delay in units of the period of the dispersive phase. The contrast returns to $1$ at every integer $u$, and at the half period it equals $1/(2\bar n+1)$, which already gives the occupation exactly in this ideal model. This note does not propose a new measurement. It establishes exact properties of a global functional of the known contrast, its geometric mean after the first return with a power weight, $\mathcal V_s=\exp\big(s\int_1^\infty\log V(u)\,u^{-s-1}du\big)$, $s>0$. The main result is a two-sided bound that holds for every positive occupation: $p_0<\mathcal V_s<e^{-sG(s)}\,p_0$, where $p_0=1/(\bar n+1)$ is the probability that the mode is empty and $G(s)=\int_1^\infty\log|2\sin\pi u|\,u^{-s-1}du$. Both constants are the best possible. For the weight $u^{-2}$ the upper constant is $e^{C_g}/2=1.05195\ldots$, with $C_g=-\int_1^\infty\log|\sin\pi u|\,u^{-2}du=0.743794\ldots$ Hence the geometric contrast after the first return equals the vacuum probability within $5.2$ per cent at every positive temperature. Together with the half-period contrast it gives a relation without parameters that every thermal state satisfies and that coherent states of mean photon number at least $0.3$ violate. Five further results are proved. The expansion $\mathcal V_1=\tfrac12e^{C_g}\,p_0\,(1-p_0)^{\pi^2/12-3/4}e^{R}$ holds with an explicit bound for $R$. A finite range of delays $1\le u\le U$ changes $\log\mathcal V_s$ by at most $U^{-s}\log(2\bar n+1)$. The integral of $\log V$ over all delays with the weight $u^{-2}$ equals $-\pi^2\bar n$. The product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$, $1\le k<N$, satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$. The companion transform $A$, which collects the delays before the first return of $\log|2\sin\pi u|$ relative to its short-time form $\log(2\pi u)$, satisfies $G(s)-A(s)=\frac\pi s\cot(\frac{\pi s}2)\,\zeta(s)$, so that in the strip $0<\operatorname{Re}s<2$ the non-real solutions of $G=A$ are the zeros of the Riemann zeta function. The functions $G$ and $A$ are shown with their computed zeros. All statements concern the ideal model without damping.
""" + s[a1:]
rep(r"\keywords{dispersive coupling; thermal photons;", r"\keywords{circuit quantum electrodynamics; dispersive coupling; thermal photons;")

# ------------------------------------------------------------------ introduction
i0 = s.index("\\section{Introduction}\\label{sec:intro}")
i1 = s.index("\\begin{table}[!htb]\n\\caption{Notation.}")
INTRO = r"""\section{Introduction}\label{sec:intro}

In a superconducting quantum processor each qubit is read out through a microwave resonator, and a few thermal photons left in that resonator are enough to dephase the qubit \cite{Rigetti2012,Sears2012}. The interaction responsible is dispersive: the transition frequency of the qubit shifts by a fixed amount for every photon in the mode \cite{Blais2021}. The same interaction turns the qubit into a probe of the photon statistics. This note is about one exact property of that probe when the mode is thermal. It does not introduce a new method of measurement, and we first state what is known.

Two families of methods are established. The first works in the frequency domain. When the shift per photon exceeds all linewidths, the transition of the qubit splits into one line for each photon number. This was predicted in \cite{Gambetta2006} and observed in \cite{Schuster2007}, where the strengths of the lines distinguished a coherent field from a thermal one. A pulse that is selective on one line maps a chosen photon number onto the state of the qubit \cite{Johnson2010}, and Rabi oscillations driven on the separate lines are used to determine the occupation of the mode \cite{Sears2012}.

The second family works in the time domain and is older. Brune et al.\ proposed a quantum non-demolition measurement of small photon numbers by the phase-sensitive detection of atoms coupled dispersively to the field \cite{Brune1990}. A Ramsey sequence on the dispersively coupled probe is the usual form of this measurement: each photon number gives a different phase of the probe \cite{Johnson2010}. With a delay of half the period of the dispersive phase, the Ramsey sequence maps the photon-number parity of a cavity onto the qubit \cite{Sun2014}. The coherence of the probe after a delay is the characteristic function of the photon number. For a thermal mode in contact with a bath it is known in closed form: the result is due to Dykman and Krivoglaz \cite{DykmanKrivoglaz1987} and was derived again, including a drive, by Clerk and Utami \cite{ClerkUtami2007}. Its long-time limit gives the dephasing rate that is used to interpret coherence times \cite{Rigetti2012}, and Ramsey experiments with injected thermal photons test it quantitatively \cite{Sears2012}. Thermal and coherent photon noise have been distinguished through the noise spectrum seen by the qubit \cite{Yan2018}, and a superconducting circuit has been used as a primary thermometer of the thermal occupation of propagating microwave modes \cite{Scigliuzzo2020}. More generally, the coherence of a probe is a partition function of the system to which it is coupled, continued to a complex parameter \cite{WeiLiu2012}, and such functions and their zeros have been measured \cite{Peng2015}.

In a mode without damping the photon number is constant during the sequence, and the contrast of a thermal state is the elementary closed form \CGeqref{eq:V}, the case without damping of \cite{DykmanKrivoglaz1987,ClerkUtami2007}. It is periodic in the delay and returns to $1$ at every multiple of the period $\pi/\chi$ of the dispersive phase, where $2\chi$ is the shift of the transition frequency per photon; we call these instants the returns. At the half period the contrast is the modulus of the mean parity, $1/(2\bar n+1)$, where $\bar n$ is the mean occupation. In this ideal model a single Ramsey delay therefore determines $\bar n$ exactly.

Nothing in the preceding paragraphs is new here: neither the Ramsey method, nor the contrast of a thermal mode, nor the fact that this contrast determines the occupation. This note does not propose a better estimator of $\bar n$ than the half-period contrast. Its subject is a global functional of the known contrast, and its results are exact statements about that functional: best constants, a sum rule and the structure of a Mellin transform.

The objective is to determine how the contrast accumulated after the first return depends on the occupation of the mode, when it is averaged geometrically over the delay with a power weight, and to find the best constants in that dependence.

The answer is Theorem~\CGref{thm:main}. For every exponent $s>0$ of the weight and every positive occupation, the geometric contrast $\mathcal V_s$ lies strictly between the probability $p_0$ that the mode is empty and $e^{-sG(s)}p_0$, and neither constant can be improved. Here $G$ is the transform \CGeqref{eq:G} of $\log|2\sin\pi u|$ on $[1,\infty)$. For the weight $u^{-2}$ the upper constant is $e^{C_g}/2$, where $C_g$ is the log-sine constant \CGeqref{eq:Cg}. Corollary~\CGref{cor:bracket} turns the bound into a bracket for the occupation. Corollary~\CGref{cor:half} combines the bound with the half-period contrast into a relation between two measured quantities that holds for every thermal state and fails for coherent states of mean photon number at least $0.3$. Theorem~\CGref{thm:hot} gives the expansion of $\mathcal V_1$ at high temperature with an explicit remainder. Proposition~\CGref{prop:trunc} bounds the effect of a finite range of delays. Proposition~\CGref{prop:sum} shows that the integral of $\log V$ over all delays with the weight $u^{-2}$ is exactly $-\pi^2\bar n$. Proposition~\CGref{prop:harm} shows that the product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$ satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$. Section~\CGref{sec:GA} treats the function $G$ at complex exponents together with the companion transform $A$ of \CGeqref{eq:A}, which collects the delays before the first return, proves the identity \CGeqref{eq:GAzeta} that links them to the Riemann zeta function, and shows both functions with their computed zeros.

On the mathematical side, the classical log-sine integrals are integrals of powers of $\log|2\sin(\theta/2)|$ against powers of $\theta$ over a finite interval, and their evaluation in terms of zeta values and polylogarithms has a long history \cite{Lewin1981,BorweinStraub2012}. The function $G$ is of a different kind: it is a Mellin transform of $\log|2\sin\pi u|$ over the half-line $[1,\infty)$, and $C_g$ is $\log2$ minus its value at $s=1$. Mellin transforms over a half-line that represent the Riemann zeta function in the critical strip are classical \cite[Chapter~II]{Titchmarsh1986}, and the identity \CGeqref{eq:GAzeta} is of this type. We do not claim it as new; we prove it and use the way in which the first return splits it into $G$ and $A$. The sum rule \CGeqref{eq:sumrule} is an elementary consequence of the Dirichlet integral. To our knowledge the bound \CGeqref{eq:bound} and the role of $C_g$ as its sharp constant have not been stated before.

All statements are theorems about the ideal model \CGeqref{eq:H}: a single mode without damping, a probe without intrinsic dephasing, and a dispersive shift that is exactly linear in the photon number. The returns of the contrast to $1$ rest on these three idealisations. The effect of damping on the contrast is contained in the closed form of \cite{DykmanKrivoglaz1987,ClerkUtami2007} and is not treated here. The geometric contrast is an integral over unbounded delays, and Proposition~\CGref{prop:trunc} gives the error of a finite range. It averages the logarithm of the contrast and therefore gives weight to the delays where the contrast is small, down to $1/(2\bar n+1)$, where a measured contrast is most affected by noise. No experimental advantage over the existing methods is claimed.

The proofs are elementary and self-contained. Three classical formulas are quoted from \cite{DLMF}: the product for the sine, the partial fractions of the cotangent and the Dirichlet integral. The figures and tables are computed in double precision or in multiple precision arithmetic and illustrate the statements; the scripts that produce them accompany the note. Table~\CGref{tab:notation} lists the notation.

"""
s = s[:i0] + INTRO + s[i1:]

# ------------------------------------------------------------------ notation table
rep(r"$\omega_c$, $\omega_p$, $\chi$ & frequencies of the mode and of the probe, dispersive shift per photon\\",
    r"$\omega_c$, $\omega_p$, $\chi$ & frequencies of the mode and of the probe, dispersive coupling; the transition frequency of the probe shifts by $2\chi$ per photon\\")
rep(r"$R(\tau)$ & remainder of the expansion \CGeqref{eq:hot}\\",
    r"$R(\tau)$ & remainder of the expansion \CGeqref{eq:hot}\\" "\n"
    r"$\mathcal V_{s,U}$, $U$ & geometric contrast over the finite range $1\le u\le U$, \CGeqref{eq:VsU}\\" "\n"
    r"$\nu$ & mean photon number of a coherent state, \CGeqref{eq:coh}\\")
rep(r"$v$, $w$, $B_1$, $B_2$; $z$ &", r"$v$, $w$, $B_1$, $B_2$, $X_1$, $X_2$; $z$ &")

# ------------------------------------------------------------------ section 2: convention for chi
rep(r"have energies that differ by $\omega_p+2\chi n$. After a time $t$",
    r"have energies that differ by $\omega_p+2\chi n$, so that the transition frequency of the probe shifts by $2\chi$ per photon. After a time $t$")

# ------------------------------------------------------------------ section 4: half-period contrast, corollary, coherent state
rep(r"For $\bar n=20$, $\mathcal V_1=0.0499291$ and \CGeqref{eq:bracket} reads $19.03<\bar n<20.07$.",
    r"""For $\bar n=20$, $\mathcal V_1=0.0499291$ and \CGeqref{eq:bracket} reads $19.03<\bar n<20.07$.

In the ideal model the occupation is also given exactly by a single delay. By Proposition~\CGref{prop:contrast}, $V(\frac12)=1/(2\bar n+1)$, which is the modulus of the mean parity $\sum_{n\ge0}(-1)^np_n$, so that $\bar n=\frac12\big(1/V(\frac12)-1\big)$. As an estimator of $\bar n$ the bracket \CGeqref{eq:bracket} is therefore not an improvement on the half-period contrast. What the geometric contrast adds is a second number, and Theorem~\CGref{thm:main} fixes its relation to the first.

\begin{corollary}\label{cor:half}
For every $\bar n>0$,
\begin{equation}\label{eq:half}
\frac{2\,V(\frac12)}{1+V(\frac12)}<\mathcal V_1<\frac{e^{C_g}}2\cdot\frac{2\,V(\frac12)}{1+V(\frac12)} .
\end{equation}
\end{corollary}

\begin{proof}
By Proposition~\CGref{prop:contrast}, $V(\frac12)=1/(2\bar n+1)$, so $2V(\frac12)/(1+V(\frac12))=2/(2\bar n+2)=p_0$. Substitute this in \CGeqref{eq:boundCg}.
\end{proof}

The relation \CGeqref{eq:half} contains no parameter and holds for every thermal state, so that a pair of values that violates it is not the pair of a thermal state in the model \CGeqref{eq:H}. Other states do violate it. For a coherent state of mean photon number $\nu>0$ the photon number has the Poisson probabilities $e^{-\nu}\nu^n/n!$, the sum in \CGeqref{eq:D} is $\exp\big(\nu(e^{-2\pi iu}-1)\big)$, and its modulus is $\exp\big(\nu(\cos2\pi u-1)\big)$. The half-period contrast is $e^{-2\nu}$, and by \CGeqref{eq:cm} the geometric contrast of order $1$ after the first return is $\exp\big(-\nu(1-c_1(1))\big)$. The quotient of the middle term of \CGeqref{eq:half} by its left term is then
\begin{equation}\label{eq:coh}
\frac{1+e^{-2\nu}}{2\,e^{-2\nu}}\,e^{-\nu(1-c_1(1))}=e^{\nu\,c_1(1)}\cosh\nu .
\end{equation}
It is increasing in $\nu$. With the computed value $c_1(1)=0.0409047$ it equals $1.0582$ at $\nu=0.3$, which is above $\frac12e^{C_g}=1.0520$. Every coherent state with $\nu\ge0.3$ therefore violates the upper inequality of \CGeqref{eq:half}.""")

# ------------------------------------------------------------------ section 4: remainder not sharp; finite range of delays
rep(r"Table~\CGref{tab:values} gives the exact value of $\mathcal V_1$ from \CGeqref{eq:exact}, the ratio $\mathcal V_1/p_0$, the remainder $R(\tau)$ and its bound \CGeqref{eq:Rbound}.",
    r"Table~\CGref{tab:values} gives the exact value of $\mathcal V_1$ from \CGeqref{eq:exact}, the ratio $\mathcal V_1/p_0$, the remainder $R(\tau)$ and its bound \CGeqref{eq:Rbound}. The bound \CGeqref{eq:Rbound} is not sharp: in the table the remainder is smaller than the bound by a factor between $2.9$ and $6$.")
rep("\\section{The sum rule and the harmonic delays}\\label{sec:sum}",
    r"""A measured sequence of contrasts covers a finite range of delays. For real $U>1$ and $s>0$ let
\begin{equation}\label{eq:VsU}
\mathcal V_{s,U}=\exp\Big(\frac{s}{1-U^{-s}}\int_1^U\log V(u)\,u^{-s-1}\,du\Big),
\end{equation}
the geometric mean of the contrast over $1\le u\le U$ with the normalised weight.

\begin{proposition}\label{prop:trunc}
Let $\bar n>0$, $L=\log(2\bar n+1)$, $s>0$ and $U>1$. Then
\begin{equation}\label{eq:trunc}
\big|\log\mathcal V_{s,U}-\log\mathcal V_s\big|\le L\,U^{-s} .
\end{equation}
\end{proposition}

\begin{proof}
Put $X_1=s\int_1^U\log V(u)\,u^{-s-1}du$ and $X_2=s\int_U^\infty\log V(u)\,u^{-s-1}du$, so that $\log\mathcal V_s=X_1+X_2$ and $\log\mathcal V_{s,U}=X_1/(1-U^{-s})$. By Proposition~\CGref{prop:contrast}, $-L\le\log V(u)\le0$. Since $s\int_1^Uu^{-s-1}du=1-U^{-s}$ and $s\int_U^\infty u^{-s-1}du=U^{-s}$, we have $-L(1-U^{-s})\le X_1\le0$ and $-L\,U^{-s}\le X_2\le0$. The difference $\log\mathcal V_{s,U}-\log\mathcal V_s=X_1U^{-s}/(1-U^{-s})-X_2$ is thus the sum of a number in $[-L\,U^{-s},0]$ and a number in $[0,L\,U^{-s}]$.
\end{proof}

The bound \CGeqref{eq:trunc} uses only the range of $\log V$ and is not sharp: for $\bar n=20$, $s=1$ and $U=20$ it gives $0.186$, while the computed difference is $0.0025$.

\section{The sum rule and the harmonic delays}\label{sec:sum}""")

# ------------------------------------------------------------------ section 5
rep(r"a series of terms that are all $\le0$, so it may be integrated term by term.",
    r"a series of terms that are all $\le0$, so by Tonelli's theorem it may be integrated term by term.")
rep(r"The geometric contrast is also the rate of decay of a product.",
    r"The logarithm of the geometric contrast is also the logarithmic rate of decay of a product.")
rep(r"independent modes with dispersive shifts $\chi/k$,", r"independent modes with dispersive couplings $\chi/k$,")

# ------------------------------------------------------------------ section 6
rep(r"By Proposition~\CGref{prop:A}(c) the two coincide at a non-real exponent of the strip exactly at the zeros of $\zeta$.",
    r"By Proposition~\CGref{prop:A}(c) the two coincide at a non-real exponent of the strip exactly at the zeros of $\zeta$. This equivalence is a consequence of the explicit factor in \CGeqref{eq:GAzeta} and gives no information on the location of those zeros. The identity \CGeqref{eq:GAzeta} is a Mellin representation of $\zeta$ of the classical type \cite[Chapter~II]{Titchmarsh1986}.")

# ------------------------------------------------------------------ conclusions
c0 = s.index("\\section{Conclusions}\\label{sec:concl}")
c1 = s.index("\\begin{thebibliography}")
CONCL = r"""\section{Conclusions}\label{sec:concl}

The main conclusion is the bound \CGeqref{eq:boundCg}. For a two-level probe coupled dispersively to a thermal mode, the geometric mean of the Ramsey contrast after the first return, taken with the weight $u^{-2}$, satisfies $p_0<\mathcal V_1<\frac12e^{C_g}\,p_0$ for every positive occupation, where $p_0$ is the probability that the mode is empty and $C_g=0.743794\ldots$ is the log-sine constant \CGeqref{eq:Cg}. The two constants $1$ and $\frac12e^{C_g}=1.05195\ldots$ cannot be improved. The log-sine constant is thus the sharp constant of a functional of the ideal contrast that can in principle be estimated from a sequence of Ramsey measurements: no thermal state gives a ratio $\mathcal V_1/p_0$ above $\frac12e^{C_g}$, and every smaller constant is exceeded at a sufficiently high temperature.

Seven further conclusions follow from the same analysis. The bound holds for every power weight $u^{-s-1}$ with $s>0$, with the sharp constant $e^{-sG(s)}$, so that the function $G$ on the positive real axis is the logarithm of the sharp constant divided by $-s$ (Theorem~\CGref{thm:main}). The occupation is bracketed by the geometric contrast alone, $1/\mathcal V_1-1<\bar n<e^{C_g}/(2\mathcal V_1)-1$, with no fitted quantity (Corollary~\CGref{cor:bracket}). The geometric contrast and the half-period contrast of a thermal state satisfy the relation \CGeqref{eq:half}, which contains no parameter and which coherent states of mean photon number at least $0.3$ violate (Corollary~\CGref{cor:half}). At high temperature $\mathcal V_1=\frac12e^{C_g}p_0\,q^{\pi^2/12-3/4}e^{R}$ with $0<R\le\frac{\tau^2}{\pi^2}(\frac52+\frac12\log\frac1\tau)$ (Theorem~\CGref{thm:hot}). A finite range of delays $1\le u\le U$ changes $\log\mathcal V_s$ by at most $U^{-s}\log(2\bar n+1)$ (Proposition~\CGref{prop:trunc}). The integral of the logarithm of the contrast over all delays with the weight $u^{-2}$ is exactly $-\pi^2\bar n$, and the first return separates it into a part within $C_g-\log2$ of $\log p_0$ and a part that carries the linear term (Proposition~\CGref{prop:sum}). The product $\mathcal P(N)$ of the contrasts at the harmonic delays $N/k$ satisfies $\mathcal P(N)^{1/N}\to\mathcal V_1$, with the explicit bound \CGeqref{eq:harm} for its logarithmic rate (Proposition~\CGref{prop:harm}).

At complex exponents $G$ is the hot limit of the transform of $\log(V/p_0)$ after the first return, and its zeros are the weights on which that excess has no component (Proposition~\CGref{prop:complex}). Together with the transform $A$ of the delays before the first return it satisfies $G-A=\frac\pi s\cot(\frac{\pi s}2)\zeta$, so that in the strip $0<\operatorname{Re}s<2$ the two transforms coincide at a non-real exponent exactly at the zeros of the Riemann zeta function (Proposition~\CGref{prop:A}). This is a consequence of an explicit factorisation and gives no information on the location of those zeros.

These statements concern the ideal model \CGeqref{eq:H}, without damping of the mode, without intrinsic dephasing of the probe and with a shift that is exactly linear in the photon number. In that model the half-period contrast already gives the occupation exactly, so the bound is not a better estimator of $\bar n$. What the note adds to the known contrast is an exact statement about the whole sequence of contrasts after the first return, the identification of the log-sine constant as its sharp constant, and the relation \CGeqref{eq:half} as a test of the thermal hypothesis that contains no parameter.

"""
s = s[:c0] + CONCL + s[c1:]

# ------------------------------------------------------------------ bibliography
rep(r"\bibitem{ClerkUtami2007}",
    r"""\bibitem{BorweinStraub2012}
J.~M.~Borwein and A.~Straub, Log-sine evaluations of Mahler measures, \emph{J. Aust. Math. Soc.} \textbf{92} (2012), 15--36.
\href{https://doi.org/10.1017/S1446788712000067}{doi:10.1017/S1446788712000067};
\href{https://arxiv.org/abs/1103.3893}{arXiv:1103.3893}.

\bibitem{Brune1990}
M.~Brune, S.~Haroche, V.~Lefevre, J.~M.~Raimond and N.~Zagury, Quantum nondemolition measurement of small photon numbers by Rydberg-atom phase-sensitive detection, \emph{Phys. Rev. Lett.} \textbf{65} (1990), 976--979.
\href{https://doi.org/10.1103/PhysRevLett.65.976}{doi:10.1103/PhysRevLett.65.976}.

\bibitem{ClerkUtami2007}""")
rep(r"\bibitem{Sears2012}",
    r"""\bibitem{Scigliuzzo2020}
M.~Scigliuzzo, A.~Bengtsson, J.-C.~Besse, A.~Wallraff, P.~Delsing and S.~Gasparinetti, Primary thermometry of propagating microwaves in the quantum regime, \emph{Phys. Rev. X} \textbf{10} (2020), 041054.
\href{https://doi.org/10.1103/PhysRevX.10.041054}{doi:10.1103/PhysRevX.10.041054};
\href{https://arxiv.org/abs/2003.13522}{arXiv:2003.13522}.

\bibitem{Sears2012}""")
rep(r"\bibitem{WeiLiu2012}",
    r"""\bibitem{Sun2014}
L.~Sun, A.~Petrenko, Z.~Leghtas, B.~Vlastakis, G.~Kirchmair, K.~M.~Sliwa, A.~Narla, M.~Hatridge, S.~Shankar, J.~Blumoff, L.~Frunzio, M.~Mirrahimi, M.~H.~Devoret and R.~J.~Schoelkopf, Tracking photon jumps with repeated quantum non-demolition parity measurements, \emph{Nature} \textbf{511} (2014), 444--448.
\href{https://doi.org/10.1038/nature13436}{doi:10.1038/nature13436};
\href{https://arxiv.org/abs/1311.2534}{arXiv:1311.2534}.


\bibitem{WeiLiu2012}""")
rep(r"\end{thebibliography}",
    r"""\bibitem{Yan2018}
F.~Yan, D.~Campbell, P.~Krantz, M.~Kjaergaard, D.~Kim, J.~L.~Yoder, D.~Hover, A.~Sears, A.~J.~Kerman, T.~P.~Orlando, S.~Gustavsson and W.~D.~Oliver, Distinguishing coherent and thermal photon noise in a circuit quantum electrodynamical system, \emph{Phys. Rev. Lett.} \textbf{120} (2018), 260504.
\href{https://doi.org/10.1103/PhysRevLett.120.260504}{doi:10.1103/PhysRevLett.120.260504}.

\end{thebibliography}""")
open('Cg_Thermal_Contrast_v2.tex', 'w').write(s + '\n\\end{document}\n' + tail)
print('wrote v2')
