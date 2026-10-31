D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/'
s=open(D+'b47/casanya_ordinal_primes_v47.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
n=0
def rep(o,new,c=1):
    global body,n
    k=body.count(o); assert k==c,(k,o[:100])
    body=body.replace(o,new); n+=1

# ---- F1-F4: truncated digits ----
rep(r'the complete bound is smaller only for $\log T>2425.8386\ldots$.', r'the complete bound is smaller only for $\log T>2425.8385\ldots$.')
rep(r'the complete estimate improves upon theirs only for $\log T>2425.84$.', r'the complete estimate improves upon theirs only for $\log T>2425.8385\ldots$.')
rep(r'is the smaller of the two exactly when $\log T>2425.8386\ldots$.', r'is the smaller of the two exactly when $\log T>2425.8385\ldots$.')
rep(r'$640\delta^\sharp-112=48.0008\ldots>0$', r'$640\delta^\sharp-112=48.0007\ldots>0$')
rep(r'improves on Bellotti--Wong only for $\log T>2425.84$,', r'improves on Bellotti--Wong only for $\log T>2425.8385\ldots$,')
rep(r'the crossing point $\log T=2425.8386\ldots$ with', r'the crossing point $\log T=2425.8385\ldots$ with')
rep(r'the crossing point $\log t=933.47\ldots$ with', r'the crossing point $\log t=933.4678\ldots$ with')

# ---- certified wording in the body ----
rep(r'Appendix~\CGref{app:code} computes these values with $40$-digit floating-point arithmetic and two independent evaluations, which agree to more than $20$ digits, and gives',
    r'The certified ball-arithmetic computation of Appendix~\CGref{app:code} gives')
rep(r'\footnote{Appendix~\CGref{app:code} evaluates $\zeta(\sigma^\sharp)$ directly. The bound $\log\zeta(\sigma^\sharp)\le1.52499$ also follows from',
    r'\footnote{Appendix~\CGref{app:code} certifies $\log\zeta(\sigma^\sharp)=1.5249835586\ldots$ by ball arithmetic. The bound $\log\zeta(\sigma^\sharp)\le1.52499$ also follows from')
rep(r'Evaluating it (Appendix~\CGref{app:code}) gives', r'Evaluating it with certified ball arithmetic (Appendix~\CGref{app:code}) gives')

# ---- Appendix A ----
rep(r'with \CGcite[(4.29)]{Yang2024} are computed by the following program (Python~3.13.17 with \texttt{mpmath}~1.4.1, working precision $40$ decimal digits).',
    r'with \CGcite[(4.29)]{Yang2024} are computed in floating point by the following program (Python~3.13.17 with \texttt{mpmath}~1.4.1, working precision $40$ decimal digits), and certified by the last program of this appendix.')
rep(r'''The decimals printed below are $40$-digit floating-point values, not certified by interval arithmetic. The two independent evaluations agree to more than $20$ digits, and every inequality used in the proofs ($C_1<0.09783$, $C_2<0.7214$, $C_3(100)<10.6$, $\log\zeta(\sigma^\sharp)\le1.52499$, $0.096816006\le\Lambda(\eB)\le0.096816007$, $2\pi\Lambda(\eB)\le0.60832$) holds with margin at least $3\cdot10^{-10}$. The output follows the program.''',
    r'''The decimals printed by this program are floating-point values. Every constant and every numerical inequality used in the proofs is certified by the ball-arithmetic program at the end of this appendix. The output follows the program.''')
rep(r'(Python~3.13.17 with \texttt{python-flint}~0.9.0, Arb ball arithmetic at $120$ bits with outward rounding, so that every printed value is an upper bound).',
    r'(Python~3.13.17 with \texttt{python-flint}~0.9.0, Arb ball arithmetic \CGcite{Johansson2017} at $120$ bits with outward rounding, so that every printed value is an upper bound).')
rep(r'''\lstinputlisting[language={}]{code/casanya_method_output.txt}
''', r'''\lstinputlisting[language={}]{code/casanya_method_output.txt}

All constants and numerical inequalities of this article are certified by the following program. It uses the ball arithmetic of Arb \CGcite{Johansson2017}, through \texttt{python-flint}~0.9.0 (FLINT~3.6.0 \CGcite{FLINT}), with working precision $256$ bits. Every quantity is a ball $[m\pm r]$ that contains the exact value, all operations round outward, and every inequality is checked by an assertion on the whole ball.

The angular integrals are computed both by the closed form \CGeqref{eq:hinge_integrals} and by rigorous integration (\texttt{acb.integral}) on the arcs where the integrand is analytic. Statements valid on a range of $t$ are certified by monotonicity together with balls at the endpoints, or by covering the range with balls. The values are printed with $20$ significant digits.

\lstinputlisting{code/certify_arb.py}

\lstinputlisting[language={}]{code/certify_arb_output.txt}
''')

# ---- bibliography ----
rep(r'''\bibitem{Fujii1974}''', r'''\bibitem{FLINT} The FLINT team, FLINT: Fast Library for Number Theory, version 3.6.0, \url{https://flintlib.org}.

\bibitem{Fujii1974}''')
rep(r'''\bibitem{Kargin2013}''', r'''\bibitem{Johansson2017} F. Johansson, Arb: efficient arbitrary-precision midpoint-radius interval arithmetic, IEEE Trans. Comput. 66 (2017) 1281--1292, \href{https://doi.org/10.1109/TC.2017.2690633}{doi:10.1109/TC.2017.2690633}.

\bibitem{Kargin2013}''')
open(D+'b48/casanya_ordinal_primes_v48.tex','w',encoding='utf-8').write(pre+body)
print(n,'edits ok')
