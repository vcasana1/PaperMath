D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/'
s=open(D+'b49/casanya_ordinal_primes_v49.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
n=0
def rep(o,new,c=1):
    global body,n
    k=body.count(o); assert k==c,(k,o[:100])
    body=body.replace(o,new); n+=1

# 1 Kargin cross-reference
rep(r'agrees with the one used here when RH holds; see Section~\CGref{subsec:literature}),', r'agrees with the one used here when RH holds; see Section~\CGref{subsec:results}),')
# 2 Kargin window
rep(r'uniform in a window $N<k\le N+N^{\theta}$,', r'uniform in a window $N\le k\le N+\lfloor N^{\theta}\rfloor-1$,')
# 3 constant A >= 2
rep(r"there is a constant $A_{\varepsilon'}\ge1$ with", r"there is a constant $A_{\varepsilon'}\ge2$ with")
# 4 imaginary part step
rep(r'and Theorem~\CGref{thm:known_MV} for the primes in $(X,Y)$). This tends to infinity',
    r'and Theorem~\CGref{thm:known_MV} for the primes in $(X,Y)$, with $(\operatorname{Im}P)^2=\frac12|P|^2-\frac12\operatorname{Re}P^2$ and $\int_T^{2T}P^2\,dt$ treated as in item~2). This tends to infinity')
# 5 levels
rep(r'changes only for the levels $k-\frac12$ between these two values:', r'changes only for the levels $k-\frac12$ with $\min_I\Fc<k-\frac12\le\max_I\Fc$:')
# 6 Remark on 0.53
rep(r'The explicit constant $0.53$ is needed only for \CGeqref{eq:explicit_N}.',
    r'The explicit constant $0.53$ is needed only for \CGeqref{eq:explicit_N} and for the inequalities $|\varpi|/\pi<\frac12$ of Section~\CGref{subsec:tau_intro} and Remark~\CGref{rem:bare_point}.')
# 7 remainder of the split
rep(r'and the reflected profile for $0.10073687\ldots-0.09782899\ldots=0.0029078\ldots$.',
    r'and the reflected profile for $0.10073687\ldots-0.09782899\ldots=0.0029078\ldots$ (the remaining $0.09783-0.09782899\ldots<10^{-6}$ is the cost of fixed $c,R$ and of rounding).')
# 8 Appendix B rows
rep(r'$\mathsf k=2$ in Remark~\CGref{rem:bare_point}\\', r'$\mathsf k=2$ in Remark~\CGref{rem:bare_point}, every $\mathsf k$ in Remark~\CGref{rem:meansquare_comparison}\\')
rep(r'applied to $\mathscr D_1^2$ and, as a Dirichlet polynomial in $v^2$, to $\mathscr D_2^2$\\',
    r'applied to $\mathscr D_1^2$ and, as a Dirichlet polynomial in $v^2$, to $\mathscr D_2^2$; also in Section~\CGref{subsec:literature} and Lemma~\CGref{lem:additional_derivative}\\')
# 9, 10 local symbols
rep(r'(Section~\CGref{sec:external}, two paragraphs of Section~\CGref{subsec:literature},',
    r'(the paragraph on Gonek in Section~\CGref{sec:intro}, Section~\CGref{sec:external}, two paragraphs of Section~\CGref{subsec:literature},')
rep(r'Section~\CGref{sec:meansquare}, and Theorem~\CGref{thm:recovered_simple_certificate}).',
    r'Section~\CGref{sec:meansquare}, Section~\CGref{sec:additional}, and Theorem~\CGref{thm:recovered_simple_certificate}).')
rep(r'\sum_{l=0}^{j-1}c_{j,l}s_k^{2l}', r'\sum_{l=0}^{j-1}\binom{2j+1}{2l}\frac{4^{l-j}}{2j+1}s_k^{2l}')
# 11 bookmarks
rep(r'\section{A disc-based estimate for $S(T)$}', r'\section{A disc-based estimate for \texorpdfstring{$S(T)$}{S(T)}}')
rep(r'\section{Distance from \texorpdfstring{$\tau_k$}{tau_k} to the imaginary parts}', r'\section{Distance from \texorpdfstring{$\tau_k$}{tau\_k} to the imaginary parts}')
# 13 root-mean-square
rep(r'how much arithmetic information can bring them within a bounded number of mean spacings', r'how much arithmetic information can bring them, in root-mean-square, within a bounded number of mean spacings')
# AI declaration + mathematical software after Data availability
decl=open(D+'tools/ai_declaration.tex',encoding='utf-8').read()
rep('The programs of Appendix~\\CGref{app:code} and their outputs are reproduced in that appendix. No other data were used.\n\n',
    'The programs of Appendix~\\CGref{app:code} and their outputs are reproduced in that appendix. No other data were used.\n\n'+decl)
open(D+'b50/casanya_ordinal_primes_v50.tex','w',encoding='utf-8').write(pre+body)
print(n,'edits ok')
