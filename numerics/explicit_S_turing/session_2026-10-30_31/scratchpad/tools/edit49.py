D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/'
s=open(D+'b48/casanya_ordinal_primes_v48.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
n=0
def rep(o,new,c=1):
    global body,n
    k=body.count(o); assert k==c,(k,o[:100])
    body=body.replace(o,new); n+=1

# 1. Yang's published bound vs the bound used here
rep(r'\CGcite[Thm.~1.1]{Yang2024} (see Remark~\CGref{rem:robust}(ii));',
    r'\CGcite[Thm.~1.1]{Yang2024}, as stated there. Its proof for $3\le|t|\le T_m$ needs the correction described in Remark~\CGref{rem:robust}(ii), and this article uses (b) only for $4\le m\le9$ and with constant $2$, which that remark establishes;')

# 3. real part in the Montgomery--Vaughan step
rep(r'''is $\frac{1}{2\pi^2}\sum_{p\le X}\frac{\log^2p}{p}(1+O(\frac{p}{T}))\asymp\log^2X\asymp\log^2T$ for $2\le X\le T$ with $\log X\asymp\log T$, the order of $\Nz'(T)^2$.''',
    r'''is $\frac{1}{2\pi^2}\sum_{p\le X}\frac{\log^2p}{p}(1+O(\frac{p}{T}))\asymp\log^2X\asymp\log^2T$ for $2\le X\le T$ with $\log X\asymp\log T$, the order of $\Nz'(T)^2$. (With $P(t)=\sum_{p\le X}p^{-1/2}\log p\,p^{-it}$, the cosine sum is $\operatorname{Re}P$ and $(\operatorname{Re}P)^2=\frac12|P|^2+\frac12\operatorname{Re}P^2$. Theorem~\CGref{thm:known_MV} gives the mean of $|P|^2$, and $|\int_T^{2T}P(t)^2\,dt|\le\frac2{\log4}\bigl(\sum_{p\le X}p^{-1/2}\log p\bigr)^2\ll X$, since $|\int_T^{2T}(pq)^{-it}\,dt|\le2/\log(pq)$. Divided by $T$, this is absorbed in the remainder $\sum_{p\le X}\frac{\log^2p}{p}O(\frac pT)\gg\frac XT$.)''')

# 4. strict monotonicity
rep(r'If $\Fc$ were increasing on $[2\pi,\infty)$, then for $k\ge2$ the equation $\Fc(t)=k-\frac12$ would have exactly one solution,',
    r'If $\Fc$, which is continuous, were strictly increasing on $[2\pi,\infty)$, then for $k\ge2$ the equation $\Fc(t)=k-\frac12$ would have exactly one solution,')

# 5. effect of an excursion, stated precisely
rep(r'A non-monotone excursion of $\Fc$ moves only the nearby $\tau_{k}^{\mathrm C}$, and Theorem~\CGref{thm:transfer}',
    r'If $\Fc$ is replaced on a bounded interval $I$ by another function with the same minimum and maximum on $I$, then $\tau_{k}^{\mathrm C}$ changes only for the levels $k-\frac12$ between these two values: for the other levels $\meas(I\cap\{\Fc<k-\frac12\})$ is $0$ or $|I|$ in both cases. Theorem~\CGref{thm:transfer}')

# 6. scope of the prime budget
rep(r'The number of primes is dictated by the fourth moment. In the proof above,',
    r'In the present argument, the number of primes is dictated by the fourth moment. In the proof above,')

# 7. conclusion: scope
rep('''$2\\log\\log T/\\log^2T\\,(1+o(1))$. The arithmetic correction removes the
divergent factor.''', '''$2\\log\\log T/\\log^2T\\,(1+o(1))$. The arithmetic correction removes the
divergent factor $\\log\\log T$ from the proved upper bound of the mean square,
which is $O(1/\\log^2T)$ for the corrected points; no asymptotic of the corrected
error is claimed.''')

# 8. share of the reflection in the improvement
rep(r'The improvement in the leading coefficient from $0.10076$ to $0.09783$ is entirely due to the reflected profile.',
    r'Of the reduction of the leading coefficient from $0.10076$ to $0.09783$, the limit $c,R\to1$ accounts for $0.10076-0.10073687\ldots=0.0000231\ldots$ and the reflected profile for $0.10073687\ldots-0.09782899\ldots=0.0029078\ldots$. The improvement is thus essentially due to the reflected profile.')
rep('''The improved leading coefficient comes from pointwise reflection by the''','''The improved leading coefficient comes essentially from pointwise reflection by the''')

# 9. higher moments of s_k: complete argument
rep(r'With $F=\Nz$ and the higher moments of Theorem~\CGref{thm:known_selberg}, the identity \CGeqref{eq:identity_general} gives in the same way $\langle s_k^{2j}\rangle_{\Kc_T}\sim\frac{(2j)!}{j!(2\pi)^{2j}}(\log\log T)^j$ for every fixed $j$, by induction on $j$ through the lower-degree terms of $\Psi_j$. Only the case $j=1$ is used here.',
    r'''With $F=\Nz$ and the higher moments of Theorem~\CGref{thm:known_selberg}, the identity \CGeqref{eq:identity_general} gives in the same way $\langle s_k^{2j}\rangle_{\Kc_T}\sim\frac{(2j)!}{j!(2\pi)^{2j}}(\log\log T)^j$ for every fixed $j\ge1$. Only the case $j=1$ is used here.

The proof is by induction on $j$, the case $j=1$ being Proposition~\CGref{prop:s_meansquare}. Take $k_1=N(T)$ and $k_2=N(2T)+1$, so that the sum in \CGeqref{eq:identity_general} runs over $\Kc_T$, and $u_k=s_k$. The boundary terms are $O(\log^{2j+1}T)$, because $s_k\ll\log\gamma_k$ by Lemma~\CGref{lem:s_bounds}. On the left side, the intervals $[\gamma_{k_1},T]$ and $[2T,\gamma_{k_2}]$ have length $o(1)$ by Theorem~\CGref{thm:known_basic}, and the integrand is $O(\log^{2j+1}T)$ there. On $[T,2T]$, $\lL(t)=\lL(T)(1+O(1/\log T))$ and $G=S+\varpi/\pi$ with $|\varpi|/\pi\le0.53/(\pi t)$ (Lemma~\CGref{lem:varpi}). By Hölder's inequality and Theorem~\CGref{thm:known_selberg}, $\int_T^{2T}|S|^{2j-i}t^{-i}\,dt\ll T^{1-i}(\log\log T)^{j-i/2}$ for $1\le i\le2j$, so $\int_T^{2T}G^{2j}\,dt=\int_T^{2T}S^{2j}\,dt+o(T)$. Theorem~\CGref{thm:known_selberg} at $2T$ and at $T$ gives $\int_T^{2T}S^{2j}\,dt\sim\frac{(2j)!}{j!(2\pi)^{2j}}T(\log\log T)^j$. Hence the left side of \CGeqref{eq:identity_general} is $\lL(T)\,T\,\frac{(2j)!}{j!(2\pi)^{2j}}(\log\log T)^j(1+o(1))$. On the right side, $\Psi_j(s_k)=s_k^{2j}+\sum_{l=0}^{j-1}c_{j,l}s_k^{2l}$ by \CGeqref{eq:Psi_def}, and the induction hypothesis gives $\sum_{k\in\Kc_T}s_k^{2l}\ll\#\Kc_T(\log\log T)^l=o(\#\Kc_T(\log\log T)^j)$ for $l<j$. Since $\#\Kc_T=T\lL(T)(1+O(1/\log T))$ (proof of Proposition~\CGref{prop:s_meansquare}), dividing by $\#\Kc_T$ gives the claim.''')
rep(r'with $\mathsf k=1$, in the dyadic form \CGeqref{eq:selberg_dyadic} (Proposition~\CGref{prop:s_meansquare}), and with $\mathsf k=2$ in Remark~\CGref{rem:bare_point}.',
    r'with $\mathsf k=1$, in the dyadic form \CGeqref{eq:selberg_dyadic} (Proposition~\CGref{prop:s_meansquare}), with $\mathsf k=2$ in Remark~\CGref{rem:bare_point}, and with every $\mathsf k$ in Remark~\CGref{rem:meansquare_comparison}.')

# 10. Kargin's enumeration (clarity)
rep(r'and proves, without RH, that $\gamma_k-t_k$, suitably normalized, is asymptotically Gaussian,',
    r'and proves, without RH, that $\gamma_k-t_k$, suitably normalized, is asymptotically Gaussian (for his enumeration of the zeros, which agrees with the one used here when RH holds; see Section~\CGref{subsec:literature}),')

open(D+'b49/casanya_ordinal_primes_v49.tex','w',encoding='utf-8').write(pre+body)
print(n,'edits ok')
