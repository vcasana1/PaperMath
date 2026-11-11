# Castor–Pollux: independent analytic research notes (11 November 2026)

**STATUS: RESEARCH WORKING NOTES — NOT A REVIEWED PAPER OR A CERTIFICATE.**
This file records analytic derivations from the ChatGPT discussion after the v4 handoff. They are **not** incorporated into the author-approved manuscript. In particular, none of the proposed global zero-location or counting claims is proved here. Recheck any new formula, constants, and domains before publication. No numerical computations were run for these notes.

**Isolation:** this file was added only to the branch \`chatgpt-castor-pollux-20261111-notes\`. Do not merge automatically, overwrite Claude's \`castor-pollux-I\` branch, or edit the v5 source in place.

**Current authoritative manuscript:** \`castor_pollux_I/Castor_Pollux_I_v5.tex\` on \`castor-pollux-I\` (sha256 \`39d73e583d5e5fb016f6ea76bfa15a197f2a80359a9996457ba55d9f07ff5ea7\`). The v4 archive is already preserved under \`previous_versions/\`. Work below uses the **v5** symbols, not the transient symbols from the discussion.

## 1. Notation and analytic foundations

Let
$$
h(u)=\log|2\sin(\pi u)|,\qquad
\mathcal K(u)=\sum_{m\ge1}\frac{1-\cos(2\pi m u)}{m^3}\ge0,
\qquad \kappa=\Sigma_3=\sum_{m\ge1}m^{-3}.
$$
For $\Re s>-2$ define
$$H(s)=\int_1^\infty\mathcal K(u)u^{-s-3}\,du.$$
The v5 auxiliary $A(s)$ and $G(s)$ satisfy
$$G(s)=-\frac{(s+1)(s+2)}{4\pi^2}H(s).$$

Following v5, set $\ell(u)=\log(\pi u/|\sin(\pi u)|)$, $\mathfrak b=\log(2\pi)-3/2$, and
$$
\mathcal B(u)=4\pi^2\int_0^u (u-v)\ell(v)\,dv.
$$
It is positive and convex, and can be expressed piecewise as
$$
\mathcal B(u)=
\begin{cases}
R(u),&0<u<1,\\
\mathcal K(u)+2\pi^2u^2(\log u+\mathfrak b),&u>1,
\end{cases}
$$
where
$$R(u)=-4\pi^2\int_0^u (u-v)\log\frac{\sin(\pi v)}{\pi v}\,dv.$$
For $0<\Re s<2$,
$$
\Omega(s)=\int_0^\infty\mathcal B(u)u^{-s-3}\,du,\quad
G(s)-A(s)=-\frac{(s+1)(s+2)}{4\pi^2}\Omega(s).
$$
Thus the intersections of $G$ and $A$ in that band are exactly the zeros of $\Omega$. The existence, positivity, inversion inequality and elementary exclusion region are already addressed in **v5 §16**; they are not new claims here. The symbol $Q$ remains reserved for the manuscript's specific remainder in Proposition 7.1.

## 2. Proposed complete localization of the zeros of A (new argument; audit before insertion)

Set $\Sigma_{2k}=\sum_{m\ge1}m^{-2k}$ and
$$
d_k=\frac{2\Sigma_{2k}}{k(2k+1)(2k+2)},\qquad
b_k=(2k)^2d_k=\frac{8k\Sigma_{2k}}{(2k+1)(2k+2)}>0.
$$
From the local series for $\mathcal K$, and $\mathcal K(1)=\mathcal K'(1)=0$,
$$
\mathcal K(u)=2\pi^2u^2\left[-\log u-\mathfrak b+\sum_{k\ge1}d_k u^{2k}\right]\quad(0<u<1),
$$
$$\sum_{k\ge1}d_k=\mathfrak b,\qquad\sum_{k\ge1}2k\,d_k=1.$$
To avoid collision with the manuscript's $Q$, define, **only in this note,**
$$
\mathscr J(v)=\frac{e^{2v}}{2\pi^2}\mathcal K(e^{-v})
=v-\sum_{k\ge1}d_k(1-e^{-2kv}),\quad v\ge0.
$$
Then $\mathscr J(0)=\mathscr J'(0)=0$ and
$$\mathscr J''(v)=\sum_{k\ge1}b_k e^{-2kv}>0.$$
Let
$$
\mathscr P(s)=\sum_{k\ge1}\frac{b_k}{2k-s}.
$$
Two integrations by parts for $\Re s<0$, followed by meromorphic continuation, yield
$$
A(s)=\frac{(s+1)(s+2)}{2s^2}\mathscr P(s).
$$
For $s=\sigma+it$, $t>0$,
$$
\Im\mathscr P(s)
=t\sum_{k\ge1}\frac{b_k}{(2k-\sigma)^2+t^2}>0.
$$
For real $x<2$, $\mathscr P(x)>0$. Between consecutive poles,
$$\mathscr P'(x)=\sum_{k\ge1}\frac{b_k}{(2k-x)^2}>0.$$
Thus **candidate theorem:** all zeros of $A$ are real and simple; they consist of $-2,-1$ and exactly one zero in each $(2k,2k+2)$, $k\ge1$. This strengthens v5's partial statement. The proposed proof is algebraic and does not use any external zero-location theorem. It should receive a dedicated mathematical audit before incorporation.

## 3. Joint evaluation of the infinitely many periods

Define for $y>0$ the positive series
$$
\mathcal S(y)=\sum_{m\ge1}\frac1{m(y^2+4\pi^2m^2)}.
$$
Integration of the Fourier series of $\mathcal K$ over one period gives
$$
\int_0^1\mathcal K(v)e^{-yv}\,dv
=\frac{4\pi^2(1-e^{-y})}{y}\,\mathcal S(y).
$$
Using the Euler gamma integral for $u^{-s-3}$, and summing the geometric series of period shifts,
$$
H(s)=\frac{4\pi^2}{\Gamma(s+3)}
\int_0^\infty y^{s+1}e^{-y}\mathcal S(y)\,dy
\qquad(\Re s>-2).
$$
Consequently
$$
G(s)=-\frac1{\Gamma(s+1)}
\int_0^\infty y^{s+1}e^{-y}\mathcal S(y)\,dy.
$$
The latter is understood by analytic continuation at removable exceptional parameters. For $j\ge0$,
$$
(-1)^j\left(\frac{d}{d(y^2)}\right)^j\mathcal S(y)
=j!\sum_{m\ge1}\frac1{m(y^2+4\pi^2m^2)^{j+1}}>0.
$$
Also $0<4\pi^2\mathcal S(y)<\kappa$, so for real $\sigma>-2$,
$$0<H(\sigma)<\frac{\kappa}{\sigma+2}.$$

For real $\sigma>0$, the inequalities $\mathcal S'(y)<0$ and
$\frac d{dy}(y^2\mathcal S(y))>0$ compare the log-mean of the probability density proportional to $y^{\sigma+1}e^{-y}\mathcal S(y)$ with gamma densities. Writing $\psi=\Gamma'/\Gamma$ yields the candidate strict estimate
$$
-\frac1{\sigma}-\frac1{\sigma+1}-\frac1{\sigma+2}
<
\frac{H'(\sigma)}{H(\sigma)}
<
-\frac1{\sigma+2}.
$$
This does **not** by itself control the complex phase of $H$ at arbitrary height.

## 4. Neighboring-period phase restrictions

For $n\ge1$, set
$$H_n(s)=\int_n^{n+1}\mathcal K(u)u^{-s-3}\,du.$$
For $s=\sigma+it$, $t>0$,
$$
H_n(s)\overline{H_{n+1}(s)}
=\int_0^1\int_0^1
\frac{\mathcal K(v)\mathcal K(w)e^{it\theta_n(v,w)}}
{(n+v)^{\sigma+3}(n+1+w)^{\sigma+3}}\,dv\,dw,
$$
where $\theta_n(v,w)=\log((n+1+w)/(n+v))$ lies strictly between $0$ and $\log((n+2)/n)$ almost everywhere.

Therefore
$$
t\log\frac{n+2}{n}<\pi
\Longrightarrow
\Im\bigl(H_n(s)\overline{H_{n+1}(s)}\bigr)>0,
$$
and if $t\log((n+2)/n)<\pi/2$, its real part is positive as well. This forbids cancellation of a **pair** of adjacent period contributions for sufficiently large $n$ but does not forbid cancellation among all periods.

## 5. Positive-kernel constants

The original product constant $C$ satisfies
$$
G(1)=\log2-C,\qquad
C=\log2+\frac{3}{2\pi^2}H(1)
=\log2+\int_0^\infty y^2e^{-y}\mathcal S(y)\,dy.
$$
In particular, $\log2<C<\log2+\kappa/(2\pi^2)$.
From the manuscript's digamma-remainder representation for $G$,
$$Q(1)=C+\log\pi.$$
The independent direct-normalization derivation, recorded in the counting notes, also implies the **candidate** identities
$$
G(1)-A(1)=-\frac{\pi^2}{2},\quad
A(1)=\frac{\pi^2}{2}+\log2-C,\quad
\Omega(1)=\frac{\pi^4}{3}.
$$
These endpoint formulas should be checked before reuse.

## 6. Non-solutions and cautions

Positivity, $C^1$ regularity, and the inversion inequality for $\mathcal B$ are not sufficient on their own to put the complex zeros of a Mellin transform on any prescribed vertical line. The explicit two-harmonic counterexample in v5 §16 already exhibits this failure.

No proof is claimed of the exact equality between the total number of intersections of $G,A$ and the number on any given vertical line. A finite-height winding-number certificate is not a uniform-in-$T$ theorem about zero location.

**Next task:** seek a structural phase / winding estimate that exploits the exact periodic coefficients beyond positivity, then audit the new formulas above only; do not reopen the frozen v1–v5 results without a relevant modification.
