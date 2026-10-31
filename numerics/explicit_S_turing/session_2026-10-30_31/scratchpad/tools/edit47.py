import re
D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/build/'
s=open(D+'casanya_ordinal_primes_v46.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
log=[]
def rep(o,n,c=1,where='body'):
    global body,pre
    t=body if where=='body' else pre
    k=t.count(o); assert k==c,(k,o[:90])
    t=t.replace(o,n)
    if where=='body': body=t
    else: pre=t
    log.append(o[:60])

# ---- title (user's choice) ----
OLD='Prime-corrected Riemann--von Mangoldt approximation of Riemann zeta imaginary parts and bounds for its argument'
NEW='Bounds for the argument of the Riemann zeta function and a prime-corrected Riemann--von Mangoldt approximation of its zeros'
rep(OLD,NEW,2,'pre') if pre.count(OLD)==2 else None
if OLD in pre: raise SystemExit('title in pre count '+str(pre.count(OLD)))
if OLD in body: rep(OLD,NEW,body.count(OLD))

# ---- A6 + B1 + B2 + T0: intro paragraph 1 ----
rep(r'''The primes enter through $S$. The Euler product writes $\zeta(s)$ as a product of one factor $(1-p^{-s})^{-1}$ for each prime $p$, so that $S(t)$ is, formally, minus the sum over $p$ of the phases $\frac1\pi\arg(1-p^{-1/2-it})$ of these factors; truncated at about $\sqrt t$ primes it approximates $S$ in mean square, unconditionally (Selberg, Tsang, Fujii; see below). The \emph{arithmetic correction} studied here adds this finite prime sum, $\Ph$ in \CGeqref{eq:Euler_phase}, to the main term: the zeros are then approximated by the points $\tau_k^{\mathrm C}$ of the equation $\Nz(t)+\Ph(t)=k-\frac12$ instead of $\Nz(t)=k-\frac12$.''',
r'''The primes enter through $S$. The Euler product writes $\zeta(s)$ as a product of one factor $(1-p^{-s})^{-1}$ for each prime $p$. The \emph{Euler phase of the prime $p$} is $-\frac1\pi\arg(1-p^{-1/2-it})$, the normalized phase of this factor at $s=\frac12+it$, and $S(t)$ is, formally, the sum of the Euler phases of all primes. Truncated at the primes $p\le x$, with $x$ a small power of $t$, this sum approximates $S$ in mean square, unconditionally (Selberg, Tsang, Fujii; see below). Lemma~\CGref{lem:fourth} extends this to about $\sqrt t$ primes. The \emph{arithmetic correction} studied here adds the Euler phases of finitely many primes to the main term ($\Ph_m$ in \CGeqref{eq:Euler_phase}, interpolated as $\Ph$ in \CGeqref{eq:F_def}). The zeros are then approximated by points $\tau_k^{\mathrm C}$ attached to the levels $\Nz+\Ph=k-\frac12$, instead of the roots $\tau_k$ of $\Nz(t)=k-\frac12$.''')

# ---- T0 at (1.10) ----
rep(r'be the phase of the first $m$ Euler factors at $\frac12+it$ (principal argument;',
    r'be the sum of the Euler phases of the first $m$ primes, the Euler phase of the prime $p$ being $-\frac1\pi\arg(1-p^{-1/2-it})$ (principal argument;')

# ---- T1: Euler phases -> of the primes ----
rep(r'where $\Ph$ is defined by finitely many Euler phases.', r'where $\Ph$ is defined by the Euler phases of finitely many primes.')
rep(r'the second concerns its approximation by Euler phases.', r'the second concerns its approximation by the Euler phases of the primes.')
rep(r'The Euler phases of Theorem~\CGref{thm:sublevel} remove', r'The Euler phases of the primes in Theorem~\CGref{thm:sublevel} remove')
rep(r'Then the derivative of the Euler phase is not dominated', r'Then the derivative of the sum of the Euler phases of the primes is not dominated')
rep(r'the unconditional construction by finitely many Euler phases,', r'the unconditional construction by the Euler phases of finitely many primes,')
rep(r'The finite Euler phases of Theorem~\CGref{thm:sublevel} remove', r'The Euler phases of finitely many primes in Theorem~\CGref{thm:sublevel} remove')
rep(r'for the points corrected by the Euler phases:', r'for the points corrected by the Euler phases of the primes:')
# ---- T2 ----
rep('prime-complemented counting function','prime-corrected counting function')

# ---- A1 ----
rep(r'''The certified rounding of the critical constants ($C_1$, $\log(\zeta(c)/\zeta(2c))$, $\log\zeta(\sigma^\sharp)$, $\Lambda(\eB)$, $2\pi\Lambda(\eB)$ and $\Lambda(0)$) is computed in the present appendix, from the closed form by rationals; the decimals printed here are not themselves certified beyond the agreement of the two evaluations.''',
r'''The decimals printed below are $40$-digit floating-point values, not certified by interval arithmetic. The two independent evaluations agree to more than $20$ digits, and every inequality used in the proofs ($C_1<0.09783$, $C_2<0.7214$, $C_3(100)<10.6$, $\log\zeta(\sigma^\sharp)\le1.52499$, $0.096816006\le\Lambda(\eB)\le0.096816007$, $2\pi\Lambda(\eB)\le0.60832$) holds with margin at least $3\cdot10^{-10}$.''')
# ---- A2 ----
rep(r'\footnote{The bound $\log\zeta(\sigma^\sharp)\le1.52499$ computed in Appendix~\CGref{app:code} uses $\zeta(\sigma)\le\sum_{n<N}n^{-\sigma}+(N-\frac12)^{1-\sigma}/(\sigma-1)$, from',
    r'\footnote{Appendix~\CGref{app:code} evaluates $\zeta(\sigma^\sharp)$ directly. The bound $\log\zeta(\sigma^\sharp)\le1.52499$ also follows from $\zeta(\sigma)\le\sum_{n<N}n^{-\sigma}+(N-\frac12)^{1-\sigma}/(\sigma-1)$ with $N=10^4$, which gives $\log\zeta(\sigma^\sharp)\le1.5249836$. This inequality follows from')
# ---- A3 ----
rep(r'and the point $\tau_k$ of \CGeqref{eq:distance_explicit}.', r'and the point $\tau_k$ of \CGeqref{eq:intro_tau}.')
# ---- A5 ----
rep(r"Selberg\'s central limit theorem", r"Selberg's central limit theorem")
# ---- B3 ----
rep(r'uses about $\sqrt t$ primes, tied to the height (imaginary parts of the zeta zeros), and bounds the mean-square error of the approximations $\tau_{k}^{\mathrm C}$ to the imaginary parts, which are increasing and indexed by construction.',
    r'uses about $\sqrt t$ primes at height $t$, a number tied to the height rather than a free parameter, and bounds the mean-square error of approximations $\tau_{k}^{\mathrm C}$ that are increasing and indexed by construction.')
# ---- B4 ----
rep(r'makes no assumption about the real parts or multiplicities of the zeros (i.e., RH).', r'makes no assumption about the real parts of the zeros (RH) or about their multiplicities.')
# ---- B5 ----
rep(r'the version used here is his Theorem~\CGref{thm:known_PL}.)', r'the version used here is his Corollary~3, stated as Theorem~\CGref{thm:known_PL}.)')
# ---- B6 ----
rep(r'the ordinal defect and a recovered simplicity certificate.', r'the ordinal defect and a deterministic certificate for simple critical-line zeros.')
rep(r'The final certificate is included here with a self-contained proof because it applies to any continuous ordinal model.',
    r'The final theorem, a certificate for simple critical-line zeros, holds for any real test function evaluated at the imaginary parts.')
# ---- B7 ----
rep('Further higher-moment and finite Euler-product results are not claimed here.\n','')
# ---- B8 ----
rep(r'Appendix~\CGref{app:code} computes these values (40-digit arithmetic, two independent evaluations) and gives',
    r'Appendix~\CGref{app:code} computes these values with $40$-digit floating-point arithmetic and two independent evaluations, which agree to more than $20$ digits, and gives')
# ---- B10 ----
rep(r'the complete estimate improves upon theirs only beyond the stated crossing height.', r'the complete estimate improves upon theirs only for $\log T>2425.84$.')
# ---- C2 ----
rep(r'how much arithmetic information can bring it within', r'how much arithmetic information can bring them within')
# ---- C3 ----
rep(r'(the number of zeros with that imaginary part).', r'(the number of zeros with that imaginary part, counted with multiplicity).')
# ---- C4 ----
rep(r'by approximation through $t\notin\{\gamma_k\}$.', r'by approximation through points $t\notin\{\gamma_k\}$.')
# ---- C5 ----
rep(r'(An imaginary part equal to $a$ has index', r'(A term $\gamma_k$ equal to $a$ has index')
rep(r'to the first imaginary part beyond $b$,', r'to the first term beyond $b$,')
# ---- C6 ----
rep(r'their convergence to the imaginary parts of $\zeta$ as', r'their convergence to the imaginary parts of the zeros of $\zeta$ as')
# ---- C8 ----
rep(r"by bisection and by Newton's method.", r'by bisection and by the secant method (\texttt{mpmath.findroot}).')
# ---- C10: one-sentence paragraphs and stray \par ----
rep('\n\nThat each of them has exactly one solution is not proved there.', ' That each of them has exactly one solution is not proved there.')
rep('\n\nTheorem~\\CGref{thm:known_PL} gives it with $|\\operatorname{Log}(Q_0+s)|$.', ' Theorem~\\CGref{thm:known_PL} gives it with $|\\operatorname{Log}(Q_0+s)|$.')
rep('\n\\par\nFor $S$, Bellotti and Wong', '\nFor $S$, Bellotti and Wong')
# ---- C11 ----
rep(r'absolute constants and thresholds, not the same at each occurrence, threshold in Corollary~\CGref{cor:proportion}',
    r'absolute constants and thresholds, not the same at each occurrence; $\mathsf A$ is the multiplier of the mean spacing in Corollary~\CGref{cor:proportion}')
# ---- C15 ----
rep(r'We need only (c), which holds for every $|t|\ge3$,', r'On the $1$-line we need only (c), which holds for every $|t|\ge3$,')
# ---- C12: D,B,E -> sans-serif in the proof ----
i=body.index(r'Put $D=\|\delta\|_2$, $B=\|b\|_2$ and $E=\|\varepsilon\|_2$.')
j=body.index(r'\end{proof}',i)
r=body[i:j]
r=r.replace('DB','@@')
r=re.sub(r'(?<![A-Za-z\\])([DBE])(?![A-Za-z])',lambda m:r'\mathsf '+m.group(1),r)
r=r.replace('@@',r'\mathsf D\mathsf B')
body=body[:i]+r+body[j:]
print(r[:400])
open(D+'casanya_ordinal_primes_v47.tex','w',encoding='utf-8').write(pre+body)
print(len(log),'edits ok')
