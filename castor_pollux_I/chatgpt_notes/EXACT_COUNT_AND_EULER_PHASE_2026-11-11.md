# Castor–Pollux: exact intersection-counting criteria and Euler phase (11 November 2026)

**RESEARCH WORKING NOTES, NOT A VERIFIED GLOBAL ZERO-COUNT FORMULA.** Keep the exact winding-number identity separate from the still-open task of proving a uniform analytic count for every height. The branch carrying these notes is separate from Claude's \`castor-pollux-I\`; no author-approved source is edited.

## 1. Counting function and names

Use the manuscript's notation \`G\`, \`A\`, \`H\`, \`\mathcal K\`, \`\mathcal B\`, \`\Omega\` and reserve \`Q\` for Proposition 7.1. Let
$$
D(s)=G(s)-A(s)
=-\frac{(s+1)(s+2)}{4\pi^2}\Omega(s),\qquad
\Omega(s)=\int_0^\infty\mathcal B(u)u^{-s-3}\,du
$$
for $0<\Re s<2$.

For $T>0$, denote by $N_{GA}(T)$ the number of solutions to $D(s)=0$ with $0<\Re s<1$ and $0<\Im s\le T$, **counted with multiplicity**. Similarly $N_{GA}^{1/2}(T)$ is the multiplicity-weighted central count. A definition using only the cardinality of distinct $t$ values is **not** a multiplicity count when multiple zeros exist.

Assuming an analytic proof of the reflection equation for $D$, intersections off the central line occur in equal-multiplicity reflected pairs. Consequently
$$N_{GA}(T)-N_{GA}^{1/2}(T)=2N_{GA}^{+}(T)\in2\mathbb Z_{\ge0},$$
where $N_{GA}^{+}(T)$ counts the ones with $1/2<\Re s<1$. This defect is nondecreasing. Proving it is $<2$ for all $T$ (or along a sequence tending to infinity) is therefore equivalent to having no off-central intersections. By itself, this says nothing about simplicity of central intersections.

## 2. An exact finite-height contour reduction

Let $N\ge2$ be an integer and let $\kappa=\Sigma_3=\int_0^1\mathcal K(v)\,dv$. Set
$$
\Omega_N(s)=
\frac{4\pi^2A(s)}{(s+1)(s+2)}
+\int_1^N\mathcal K(u)u^{-s-3}\,du
+\frac{\kappa N^{-s-2}}{s+2}.
$$
Equivalently the middle integral is $\sum_{n=1}^{N-1}H_n(s)$.

**Tail lemma (independent calculation, needs audit of constants before manuscript use).**
Since $\int_0^1(\mathcal K-\kappa)\,dv=0$ and
$\int_0^1(v-1/2)(\mathcal K-\kappa)\,dv=0$, Taylor's formula with $|\mathcal K-\kappa|\le\kappa$ gives, for $\sigma=\Re s>-2$,
$$
\left|
\int_N^\infty\mathcal K(u)u^{-s-3}\,du
-\frac{\kappa N^{-s-2}}{s+2}
\right|
\le
\frac{\kappa |(s+3)(s+4)|}
{24(\sigma+4)(N-1)^{\sigma+4}}.
$$
In particular, for $0<\sigma<1$ and $|t|\le T$,
$$
|\Omega(s)-\Omega_N(s)|
\le \varepsilon_N(T),\qquad
\varepsilon_N(T)=
\frac{\kappa\sqrt{(T^2+16)(T^2+25)}}{96(N-1)^4}.
$$
This is a **uniform approximation for a fixed finite height**, not a universal positive lower bound for $|\Omega|$.

Consider a closed rectangle
$$\mathcal R=[a,b]\times i[0,T],
\qquad 0<a<1/2<b<1,$$
whose boundary contains no zero. Partition the oriented boundary into $z_0,z_1,\ldots,z_m=z_0$ with maximal segment length $\ell$. If $L_N$ is a valid upper bound for $|\Omega_N'|$ on $\mathcal R$ and
$$
|\Omega_N(z_j)|>\varepsilon_N(T)+L_N\ell
\quad\text{for every }j,
$$
then the original boundary image and the polygon through $\Omega_N(z_j)$ are homotopic in $\mathbb C\setminus\{0\}$. Hence
$$
N_{\mathcal R}(G,A)
=\operatorname{Wind}(\Omega_N(z_0),\ldots,\Omega_N(z_m);0)
\in\mathbb Z_{\ge0}.
$$
**This is an exact, integer certificate conditional on verification of strict numerical or analytic inequalities**; it is not an evaluated count for arbitrary $T$.

A candidate derivative bound on the rectangle is
$$
\begin{aligned}
L_N={}&2\pi^2\left(\frac2{a^3}+\frac{\mathfrak b}{a^2}\right)
+\int_0^1R(u)|\log u|u^{-b-3}\,du\\
&+\int_1^N\mathcal K(u)(\log u)u^{-a-3}\,du\\
&+\kappa N^{-a-2}
\left(\frac{\log N}{a+2}+\frac1{(a+2)^2}\right),
\end{aligned}
$$
where $\mathfrak b=\log(2\pi)-3/2$ and $R$ is the $(0,1)$ part of $\mathcal B$. Check the bound with the chosen rectangle before using it in a certificate. No contours have been evaluated here.

For $T$ coinciding with an intersection height, a slightly higher contour must be used to include boundary zeros; multiplicities and the full interior must be tracked. To cover the entire open strip, take a limit of rectangles with $a\downarrow0$, rather than presupposing a zero-free boundary at $\sigma=1$.

## 3. Fourth-order correction from the exact Fourier coefficients

The additional exact moment
$$
\int_0^1(\mathcal K(v)-\kappa)(v-\tfrac12)^2\,dv
=-\frac{\Sigma_5}{2\pi^2}
$$
yields the proposed expansion
$$
\begin{aligned}
H_n(s)
={}&\kappa\int_n^{n+1}u^{-s-3}\,du\\
&-\frac{\Sigma_5}{4\pi^2}(s+3)(s+4)
(n+\tfrac12)^{-s-5}+E_n(s),
\end{aligned}
$$
$$
|E_n(s)|\le
\frac{\kappa|(s+3)(s+4)(s+5)(s+6)|}
{1920\,n^{\sigma+7}}.
$$
Summing $n\ge N$ gives an accelerated tail formula with error at most
$$
\frac{\kappa|(s+3)(s+4)(s+5)(s+6)|}
{1920(\sigma+6)(N-1)^{\sigma+6}}.
$$
This is a **candidate error improvement**, not a measured implementation.

## 4. Intrinsic candidate functional equation from h (independent source route)

The following calculation is intended as an independent proof that does not import a functional equation from any other special function. It uses **the classical sine product and integer power series**, so it must **not** be described as avoiding the integer Dirichlet-series structure entirely.

For $0<\Re s<2$,
$$
D(s)=\int_0^\infty
\log\left|\frac{\sin(\pi u)}{\pi u}\right|u^{-s-1}\,du.
$$
For $1<\Re s<2$, the Euler sine product and the elementary integral
$$
\int_0^\infty\log|1-v^2|v^{-s-1}\,dv
=\frac{\pi}{s}\cot\frac{\pi s}{2}
$$
give
$$
D(s)=\frac{\pi}{s}\cot\frac{\pi s}{2}\sum_{n\ge1}n^{-s}.
$$
On the other hand, for $-2<\Re s<0$, the Fourier representation of $\mathcal K$ gives
$$
D(s)=-\frac{(s+1)(s+2)}{4\pi^2}
\int_0^\infty\mathcal K(u)u^{-s-3}\,du
$$
and hence
$$
D(s)=
\frac{\pi(2\pi)^s}{2s\Gamma(s)\sin(\pi s/2)}
\sum_{n\ge1}n^{s-1}.
$$
Define
$$
\Lambda_D(s)=
\frac{s}{\pi}\tan\frac{\pi s}{2}
\frac{\Gamma(s/2)}{\pi^{s/2}}D(s).
$$
Gamma reflection and duplication turn the second representation into the first with $s$ replaced by $1-s$, on the shared region $-1<\Re s<0$. The intended conclusion is
$$\Lambda_D(s)=\Lambda_D(1-s)$$
by meromorphic continuation. **Audit the interchange of sums/integrals, continuation, and all removable singularities before treating this sketch as a paper-level proof.** The standard equation imported in v5 §17 is a separate established route.

Define the completed function
$$\mathcal X(s)=\frac{s(s-1)}2\Lambda_D(s).$$
Then the candidate reflection is $\mathcal X(s)=\mathcal X(1-s)$. Because the original integral coefficients are real, $\mathcal X(\bar s)=\overline{\mathcal X(s)}$ and $\mathcal X(1/2+it)$ is real. These are properties of the **difference**, not separate symmetries of $G$ or $A$.

## 5. The Euler–Mascheroni phase and its first moment

Using $\Omega$ from v5 and $\mathcal X$ above, write
$$\mathcal X(s)=E(s)\Omega(s),$$
where
$$
E(s)=
-\frac{s^2(s-1)(s+1)(s+2)}{8\pi^3}
\tan\frac{\pi s}{2}\,
\frac{\Gamma(s/2)}{\pi^{s/2}}.
$$
Set $\vartheta(t)=\arg E(1/2+it)$ continuously, with $\vartheta(0)=0$ (since $E(1/2)>0$). Then the candidate reflection implies
$$e^{i\vartheta(t)}\Omega(1/2+it)\in\mathbb R.$$
Logarithmic differentiation gives the exact elementary-special-function identity
$$
\begin{aligned}
\vartheta'(t)={}&
\frac1{2(t^2+1/4)}
+\frac3{2(t^2+9/4)}
+\frac5{2(t^2+25/4)}\\
&+\frac{\pi}{\cosh(\pi t)}
+\frac12\Re\psi(1/4+it/2)
-\frac12\log\pi.
\end{aligned}
$$
Let $\gamma$ denote Euler's constant. Using
$\psi(1/4)=-\gamma-\pi/2-3\log2$ yields
$$
\vartheta'(0)=
\frac{46}{15}+\frac{3\pi}{4}
-\frac{\gamma}{2}
-\frac32\log2-\frac12\log\pi.
$$
In terms of the positive kernel $\mathcal B$, the intended moment identity is
$$
\frac{\int_0^\infty\mathcal B(u)u^{-7/2}\log u\,du}
{\int_0^\infty\mathcal B(u)u^{-7/2}\,du}
=\vartheta'(0).
$$
This requires the reflection-derived phase assertion and should be audited before inclusion in v5.

Let $w(x)=e^{-5x/2}\mathcal B(e^x)$. The corresponding real oscillatory expression is
$$
\mathcal X(1/2+it)=|E(1/2+it)|
\int_{\mathbb R}w(x)\cos(tx-\vartheta(t))\,dx.
$$
It may count *sign changes*, not every central zero with multiplicity. If $V_{GA}(T)$ counts central sign changes, then
$$
V_{GA}(T)\le N_{GA}^{1/2}(T)\le N_{GA}(T).
$$
Equality $N_{GA}^{1/2}(T)=N_{GA}(T)$ concerns location. Equality $V_{GA}(T)=N_{GA}(T)$ also imposes simplicity. A counting theorem for **all** $T$ is not provided by these identities.

## 6. Open global theorem

The unresolved task is an exact identity, for every $T$, between the **total integer count** and the **central multiplicity count**, not merely an asymptotic count or numerical checks at finitely many heights. It is *not* settled by an exact polygonal certificate at an arbitrary but fixed $T$.

No code, numerics, or existing theorem in the manuscript was changed by this note.
