D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/'
s=open(D+'b51/casanya_ordinal_primes_v51.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
n=0
def rep(o,new,c=1):
    global body,n
    k=body.count(o); assert k==c,(k,o[:110])
    body=body.replace(o,new); n+=1

# A2: one-sided limits as a lemma
rep(r'''All bounds for $|S(T)|$ in this article are proved first for $T\notin\{\gamma_k\}$ and have right sides continuous in $T$. Taking sequences in $(0,\infty)\setminus\{\gamma_k\}$ tending to each $\gamma\in\{\gamma_k\}$ from either side yields the same bounds for $S(\gamma^-)$ and $S(\gamma^+)$.''',
r'''\begin{lemma}\label{lem:onesided}
Let $B$ be a continuous function on an open interval $J\subset(0,\infty)$. If $|S(t)|\le B(t)$ for every $t\in J\setminus\{\gamma_k\}$, then $|S(\gamma^-)|\le B(\gamma)$ and $|S(\gamma^+)|\le B(\gamma)$ for every $\gamma\in J\cap\{\gamma_k\}$.
\end{lemma}

\begin{proof}
The set $\{\gamma_k\}$ has no accumulation point in $(0,\infty)$, and the one-sided limits $S(\gamma^\pm)$ exist. Take $t_n\to\gamma$ from the left (from the right) with $t_n\in J\setminus\{\gamma_k\}$. Then $|S(t_n)|\le B(t_n)$, and $n\to\infty$ gives the claim, since $B$ is continuous at $\gamma$.
\end{proof}

All bounds for $|S(T)|$ in this article are proved first for $T\notin\{\gamma_k\}$ and have right sides continuous in $T$, so Lemma~\CGref{lem:onesided} gives the same bounds for $S(\gamma^-)$ and $S(\gamma^+)$.''')
# A3: equivalence wording
rep(r'In particular Corollary~\CGref{cor:distance}(a) is equivalent to Corollary~\CGref{cor:bourgain},',
    r'In particular the bound $\limsup_k|\tau_k-\gamma_k|\le2\pi\Lambda(\eB)$ of Corollary~\CGref{cor:distance}(a) is equivalent, through this identity, to the bound $\mathfrak a\le\Lambda(\eB)$ of Corollary~\CGref{cor:bourgain},')
# A5: maximal lemma step
rep(r"The remaining part $D-D''$ is $<\Theta/2$, so $(\M D)_\ell\ge\Theta$ implies $(\M D'')_\ell\ge\Theta/2$,",
    r"Every term of the remaining part $D-D''$ is $<\Theta/2$, so every average of $D-D''$ over an interval of indices is $<\Theta/2$, that is, $\M(D-D'')<\Theta/2$. Since $\M$ is subadditive, $(\M D)_\ell\ge\Theta$ implies $(\M D'')_\ell\ge\Theta/2$,")
# A7: q_f terminology
rep(r'''q_f(t)=\bigl|\lfloor f(t)+\tfrac12\rfloor-N(t)\bigr| .
\label{eq:disp_21}
\end{equation}
Then''', r'''q_f(t)=\bigl|\lfloor f(t)+\tfrac12\rfloor-N(t)\bigr| .
\label{eq:disp_21}
\end{equation}
Here $q_f$ is the integer discrepancy between the levels of $f$ and of $N$, not the continuous error $f-N$; note that $q_f\le|f-N|+\frac12$. Then''')
# A8: dyadic cover
rep(r'These ranges cover $[2/L_T,1]\ni D_\ell$, because $2^{j+2}/L_T>1$ for the largest such $j$, and',
    r'The largest such $j$ is $J=\lfloor\log_2(L_T/2)\rfloor$, and $2^{J+1}>L_T/2$ gives $2^{J+2}/L_T>1$, so these ranges cover $[2/L_T,1]\ni D_\ell$; moreover')
# A9: absolute constants in Lemma 7.6
rep(r'''\ll U^{1/4}.
\label{eq:disp_26}
\end{equation}
\end{proof}''', r'''\ll U^{1/4}.
\label{eq:disp_26}
\end{equation}
Since $\mathsf k=2$ and $\alpha_{\rm F}=\frac15$ are fixed, and $m\in\{m_j,m_{j+1}\}$ enters only through $m\le\sqrt{2U}$, all the implied constants are absolute.
\end{proof}''')
# A10: scope of iff
rep(r'It is $O(U)$ if and only if $m\ll\sqrt U$, and the same holds for $\mathscr D_2^2$.',
    r'With this expansion and this direct application of Theorem~\CGref{thm:known_MV}, it is $O(U)$ exactly when $m=O(\sqrt U)$, and the same holds for $\mathscr D_2^2$.')
# A11: dyadic Selberg
rep(r'Subtracting the integrals over $[0,2T]$ and $[0,T]$, and using $\log\log2T-\log\log T=O(1/\log T)$,',
    r'Write $\int_0^XS^2\,dt=\frac{X}{2\pi^2}\log\log X+R(X)$ with $R(X)=o(X\log\log X)$. Subtracting the integrals over $[0,2T]$ and $[0,T]$, using $R(2T)-R(T)=o(T\log\log T)$ and $\log\log2T-\log\log T=O(1/\log T)$,')
# A12: higher moments as a proposition
rep(r'''With $F=\Nz$ and the higher moments of Theorem~\CGref{thm:known_selberg}, the identity \CGeqref{eq:identity_general} gives in the same way $\langle s_k^{2j}\rangle_{\Kc_T}\sim\frac{(2j)!}{j!(2\pi)^{2j}}(\log\log T)^j$ for every fixed $j\ge1$. Only the case $j=1$ is used here.

The proof is by induction on $j$,''', r'''With $F=\Nz$ and the higher moments of Theorem~\CGref{thm:known_selberg}, the identity \CGeqref{eq:identity_general} gives in the same way all the even moments of $s_k$ (Proposition~\CGref{prop:higher_moments}). Only the case $j=1$ is used here.
\end{remark}

\begin{proposition}[Higher moments of $s_k$]\label{prop:higher_moments}
For every fixed integer $j\ge1$, $\langle s_k^{2j}\rangle_{\Kc_T}\sim\frac{(2j)!}{j!(2\pi)^{2j}}(\log\log T)^j$ as $T\to\infty$.
\end{proposition}

\begin{proof}
The proof is by induction on $j$,''')
rep(r'''dividing by $\#\Kc_T$ gives the claim.
\end{remark}''', r'''dividing by $\#\Kc_T$ gives the claim.
\end{proof}''')
rep(r'and with every $\mathsf k$ in Remark~\CGref{rem:meansquare_comparison}.', r'and with every $\mathsf k$ in Proposition~\CGref{prop:higher_moments}.')
rep(r'every $\mathsf k$ in Remark~\CGref{rem:meansquare_comparison}\\', r'every $\mathsf k$ in Proposition~\CGref{prop:higher_moments}\\')
# A13: Theorem 8.1 for absolutely continuous F
rep(r'let $F$ be a real $C^1$ function on an open interval containing $[\gamma_{k_1},\gamma_{k_2}]$,',
    r'let $F$ be a real absolutely continuous function on a compact interval containing $[\gamma_{k_1},\gamma_{k_2}]$,')
rep(r'''and $F$, $F'$ are continuous. The integrand is bounded and piecewise continuous, hence Riemann integrable.''',
    r'''$F$ is bounded, and $F'$ is integrable. Hence the integrand is integrable.''')
rep(r'''The function $t\mapsto-(k-F(t))^{2j+1}/(2j+1)$ is $C^1$ with derivative $(k-F(t))^{2j}F'(t)$, by the chain rule, and no monotonicity of $F$ is needed. Hence''',
    r'''The function $t\mapsto-(k-F(t))^{2j+1}/(2j+1)$ is absolutely continuous, as the composition of the $C^1$ function $x\mapsto-(k-x)^{2j+1}/(2j+1)$ with $F$, and its derivative is $(k-F(t))^{2j}F'(t)$ almost everywhere; no monotonicity of $F$ is needed. By the fundamental theorem of calculus for absolutely continuous functions,''')
rep(r'''For an absolutely continuous real function $F$ on a compact interval,
the composition $t\mapsto(k-F(t))^{2j+1}$ is absolutely continuous
and has derivative $-(2j+1)(k-F(t))^{2j}F'(t)$ almost everywhere.
Thus the proof of Theorem~\CGref{thm:identity} applies to such $F$
by the fundamental theorem for absolutely continuous functions,
including degenerate intervals between repeated imaginary parts.
The function''', r'''Theorem~\CGref{thm:identity} applies to absolutely continuous $F$.
The function''')
rep(r'rests on an exact identity, valid for every $C^1$ function $F$,', r'rests on an exact identity, valid for every absolutely continuous function $F$,')
rep(r'& $C^1$ model of $N$,', r'& absolutely continuous model of $N$,')
# A14: uniformity in Lemma 9.2
rep(r'''Finally, $\Nz'(t)=(2\pi)^{-1}\log(t/2\pi)=O(\log T)$ on''',
    r'''All these bounds hold uniformly for $m\in\{m_j,m_{j+1}\}$, since only $m\le\sqrt{2U}$ is used.
Finally, $\Nz'(t)=(2\pi)^{-1}\log(t/2\pi)=O(\log T)$ on''')
# A15: scope of the certificate in the statement
rep(r'''\ge\#\mathcal K_T-\sum_{k\in\mathcal K_T}(2v_k)^{2j}.
\label{eq:recovered_simple_certificate}
\end{equation}''', r'''\ge\#\mathcal K_T-\sum_{k\in\mathcal K_T}(2v_k)^{2j}.
\label{eq:recovered_simple_certificate}
\end{equation}
The right side is positive only if the defects $v_k$ are individually small; the bounds of this article do not achieve this (Remark~\CGref{rem:certificate_scope}).''')
# B1: tau_1
rep(r'The uncorrected sequence $\tau_k$ is the case $\Ph=0$.', r'The uncorrected sequence $\tau_k$ is, for $k\ge2$, the case $\Ph=0$.')
# B2: Remark quantile
rep(r'at the half-integer levels, the midpoints between the levels at which $N$ jumps.',
    r'at the half-integer levels, the thresholds between consecutive integer counting levels (with multiplicities, $N$ may skip levels).')
rep(r'The right side has no counterpart that we know of: one factor is a moment of the gaps between the atoms of $\mathsf m_N$, the other a moment of the pointwise difference $f-N$.',
    r'The right side has no counterpart known to the author: one factor is a moment of the gaps $D_\ell$, which are, up to the truncation at $a$ and $b$, the masses of the atoms of $\mathsf m_N$ (the atoms themselves sit at the integers $\ell$), the other a moment of the pointwise difference $f-N$.')
# B3: monotonicity wording
rep(r'Many primes give bounded error but not monotonicity.', r'Many primes give bounded error without establishing monotonicity.')
rep(r"Then the derivative of the sum of the Euler phases of the primes is not dominated by $\Nz'$:",
    r"Then the derivative of the sum of the Euler phases of the primes is not negligible relative to $\Nz'$ in mean square:")
# impersonal voice
rep(r'On the $1$-line we need only (c),', r'On the $1$-line only (c) is needed,')
open(D+'b52/casanya_ordinal_primes_v52.tex','w',encoding='utf-8').write(pre+body)
print(n,'edits ok')
