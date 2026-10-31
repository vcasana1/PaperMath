D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/'
s=open(D+'out/casanya_ordinal_primes_v55.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
n=0
def rep(o,new,c=1):
    global body,n
    k=body.count(o); assert k==c,(k,o[:120])
    body=body.replace(o,new); n+=1
AMB=r'\CGcite{Amberger2025}'; BW6=r'\CGcite{BellottiWong2026}'
# 1 abstract
rep(r'''Its leading coefficient is smaller than that of Bellotti--Wong, while the complete bound is smaller only for $\log T>2425.8385\ldots$.
\end{abstract}''',
r'''Its leading coefficient is smaller than that of the bound of Bellotti--Wong (2025) obtained by Backlund's method, whose complete bound it improves only for $\log T>2425.8385\ldots$. The bound of Turing type of Bellotti--Wong (2026), with leading coefficient $0.0946$ and no $\log\log T$ term, is smaller than both estimates above, and that of Amberger (2025), with leading coefficient $0.097$, is smaller than the explicit one.
\end{abstract}''')
# 2 introduction
rep(r'''The leading coefficient is smaller than Bellotti--Wong's; the complete estimate improves upon theirs only for $\log T>2425.8385\ldots$.''',
r'''The leading coefficient is smaller than that of Bellotti and Wong \CGcite{BellottiWong2025}, obtained by Backlund's method; the complete estimate improves upon theirs only for $\log T>2425.8385\ldots$. The estimates of Turing type of Amberger '''+AMB+r''' and of Bellotti and Wong '''+BW6+r''' are smaller (Section~\CGref{subsec:literature}).''')
# 3 claim after Theorem 1.3
rep(r'''Among the explicit unconditional bounds compared in Table~\CGref{tab:records}, the coefficient $0.09783$ is the smallest leading coefficient in a bound of the form $|S(T)|\le A_1\log T+A_2\log\log T+A_3$ for all $T\ge e$.''',
r'''Among the bounds obtained by Backlund's method in Table~\CGref{tab:records}, the coefficient $0.09783$ is the smallest leading coefficient. The bounds of Turing type of Amberger \CGcite[Cor.~2.2]{Amberger2025} and of Bellotti and Wong \CGcite[Cor.~1.3]{BellottiWong2026} have the smaller leading coefficients $0.097$ and $0.0946$.''')
# 4 previous values
rep(r'''and $0.10076$ (Bellotti and Wong \CGcite{BellottiWong2025}). Table~\CGref{tab:records} lists the whole history, from von Mangoldt \CGcite{VonMangoldt1905}.''',
r'''and $0.10076$ (Bellotti and Wong \CGcite{BellottiWong2025}). By a method of Turing type, Amberger \CGcite[Cor.~2.2]{Amberger2025} obtained $0.097$ and Bellotti and Wong \CGcite[Cor.~1.3]{BellottiWong2026} obtained $0.0946$ (Section~\CGref{subsec:literature}). Table~\CGref{tab:records} lists the whole history, from von Mangoldt \CGcite{VonMangoldt1905}.''')
# 5 after Corollary 1.4
rep(r'''\end{enumerate}
\end{corollary}

Now, for the localization by primes''',
r'''\end{enumerate}
\end{corollary}

By Proposition~\CGref{prop:distance_sharp}, $\limsup_k|\tau_k-\gamma_k|=2\pi\mathfrak a$. The bound $\mathfrak a\le0.0946$ that follows from \CGcite[Cor.~1.3]{BellottiWong2026} therefore gives $\limsup_k|\tau_k-\gamma_k|\le2\pi\cdot0.0946=0.5943\ldots$, smaller than the bound in (a).

Now, for the localization by primes''')
# 6 literature
rep(r'''and by Bellotti and Wong to $0.10076$ \CGcite[Cor.~1.5]{BellottiWong2025}.''',
r'''and by Bellotti and Wong to $0.10076$ \CGcite[Cor.~1.5]{BellottiWong2025}.

A different method, of Turing type \CGcite{Turing1953}, uses no bound for $\zeta$ inside the critical strip and gives smaller values. Amberger \CGcite[Thm.~2.1, Cor.~2.2]{Amberger2025} obtains $|N(T)-\frac T{2\pi}\log\frac T{2\pi e}|\le0.097\log T+5.081$ for $T\ge1$. Bellotti and Wong \CGcite[Cor.~1.3]{BellottiWong2026}, with an additional parameter, obtain $0.0946\log T+5.746$ and $0.097\log T+4.954$ for $T\ge1$, and state that the constant term of \CGcite{Amberger2025} relies on a sign convention that may require verification \CGcite[\S1, footnote~1]{BellottiWong2026}. Since $|S(T)|\le|N(T)-\frac T{2\pi}\log\frac T{2\pi e}|+\frac78+|\varpi(T)|/\pi$, the first of these gives $|S(T)|\le0.0946\log T+6.691$ for $T\ge e$ (Lemma~\CGref{lem:varpi}), which is smaller than \CGeqref{eq:explicit_S} for every $T\ge e$, and $\mathfrak a\le0.0946$, which is smaller than the bound of Corollary~\CGref{cor:bourgain}. Both works are preprints.''')
# 7 table rows and caption
rep(r'''2025 & Bellotti, Wong \CGcite{BellottiWong2025} & $0.10076$ & $0.24460$ & $8.08344$ & $T\ge e$\\
''',r'''2025 & Bellotti, Wong \CGcite{BellottiWong2025} & $0.10076$ & $0.24460$ & $8.08344$ & $T\ge e$\\
2025 & Amberger \CGcite{Amberger2025} & $0.097$ & $0$ & $5.081$ & $T\ge1$\\
2026 & Bellotti, Wong \CGcite{BellottiWong2026} & $0.0946$ & $0$ & $5.746$ & $T\ge1$\\
''')
rep(r'''The rows up to 2025 are those of \CGcite[Table~1]{BellottiWong2025}, with the year of publication,''',
r'''The rows from von Mangoldt to Bellotti--Wong (2025) are those of \CGcite[Table~1]{BellottiWong2025}, with the year of publication,''')
rep(r'''The last row follows from \CGeqref{eq:explicit_S},''',
r'''The rows of Amberger and of Bellotti--Wong (2026) are preprints obtained by a method of Turing type: \CGcite[Cor.~2.2]{Amberger2025} (arXiv v4; v1 states $3.962$), whose constant term is questioned in \CGcite[\S1, footnote~1]{BellottiWong2026}, and \CGcite[Cor.~1.3]{BellottiWong2026}, which also gives $(0.097,0,4.954)$. The last row follows from \CGeqref{eq:explicit_S},''')
# 8 conclusion
rep(r'''it improves the complete estimate of
Bellotti--Wong only beyond the stated crossing height.''',
r'''it improves the complete estimate of
Bellotti--Wong \CGcite{BellottiWong2025} only beyond the stated crossing height.
Both estimates are larger than the bound of Turing type of
Bellotti--Wong \CGcite{BellottiWong2026} (Section~\CGref{subsec:literature}).''')
rep(r'''the explicit bound of Theorem~\CGref{thm:explicit} improves on Bellotti--Wong only for $\log T>2425.8385\ldots$, as it trades the constant term for the leading coefficient (for comparison,''',
r'''the explicit bound of Theorem~\CGref{thm:explicit} improves on the bound of Bellotti--Wong \CGcite{BellottiWong2025} obtained by Backlund's method only for $\log T>2425.8385\ldots$, as it trades the constant term for the leading coefficient, and it does not improve on the bounds of Turing type of \CGcite{Amberger2025} and \CGcite{BellottiWong2026} (for comparison,''')
# 9 sources table (appendix)
rep(r'''the other rows as listed in \CGcite{BellottiWong2025}, Table~1 & normalization''',
r'''the other rows up to 2025 as listed in \CGcite{BellottiWong2025}, Table~1; \CGcite{Amberger2025}, Cor.~2.2; \CGcite{BellottiWong2026}, Cor.~1.3 and \S1, footnote~1 & normalization''')
rep(r'''\CGcite{BellottiWong2025}, Cor.~1.5 and Table~1 & $0.111$ in the preprint of Trudgian, $0.112$ in its published version (as listed in both tables); $0.110$; $0.1038$; $0.10076$\\''',
r'''\CGcite{BellottiWong2025}, Cor.~1.5 and Table~1; \CGcite{Amberger2025}, Thm.~2.1, Cor.~2.2; \CGcite{BellottiWong2026}, Cor.~1.3 & $0.111$ in the preprint of Trudgian, $0.112$ in its published version (as listed in both tables); $0.110$; $0.1038$; $0.10076$; $0.097$ (Turing type); $0.0946$ (Turing type)\\''')
# 10 bibliography
rep(r'''\bibitem{Backlund1918}''', r'''\bibitem{Amberger2025} V. S. G. Amberger, Estimating the number of zeros of Dedekind zeta-functions, preprint, arXiv:2510.27444 (v1 2025), statements numbered as in v4, \href{https://doi.org/10.48550/arXiv.2510.27444}{doi:10.48550/arXiv.2510.27444}.

\bibitem{Backlund1918}''')
rep(r'''\bibitem{BennettEtAl2021}''', r'''\bibitem{BellottiWong2026} C. Bellotti and P.-J. Wong, Counting zeros of Artin $L$-functions, preprint, arXiv:2606.31441v1, 2026, \href{https://doi.org/10.48550/arXiv.2606.31441}{doi:10.48550/arXiv.2606.31441}.

\bibitem{BennettEtAl2021}''')
import re
k=body.index(r'\bibitem{Trudgian2014}'); k2=body.index(r'\bibitem',k+5)
body=body[:k2]+r'''\bibitem{Turing1953} A. M. Turing, Some calculations of the Riemann zeta-function, \textit{Proc. London Math. Soc. (3)} \textbf{3} (1953) 99--117, \href{https://doi.org/10.1112/plms/s3-3.1.99}{doi:10.1112/plms/s3-3.1.99}.

'''+body[k2:]
print('next bibitem after Turing:',body[k2+len('\\bibitem{Turing1953}')+200:k2+400][:60])
open(D+'b57/casanya_ordinal_primes_v57.tex','w',encoding='utf-8').write(pre+body)
print(n,'edits ok')
