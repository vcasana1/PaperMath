import re
D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/build/'
s=open(D+'casanya_ordinal_primes_v44.tex',encoding='utf-8').read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(s.count(o),o[:70]); s=s.replace(o,n)

# ---- 1. intro rewrite (first two paragraphs) ----
i=s.index('The main result of this paper constructs a strictly increasing sequence of approximate ordinates')
j=s.index('The other results concern the argument $S(T)$')
new=r'''The imaginary parts $\gamma_k$ of the nontrivial zeros of the Riemann zeta function are located only on average by the Riemann--von Mangoldt formula: the points $\tau_k$ defined by $\Nz(\tau_k)=k-\frac12$ \CGeqref{eq:intro_tau}, where $\Nz$ is the smooth main term of the zero-counting function, discard the oscillating term $S(t)=\frac1\pi\arg\zeta(\frac12+it)$. The primes enter through $S$. The Euler product writes $\zeta(s)$ as a product of one factor $(1-p^{-s})^{-1}$ for each prime $p$, so that $S(t)$ is, formally, minus the sum over $p$ of the phases $\frac1\pi\arg(1-p^{-1/2-it})$ of these factors; truncated at about $\sqrt t$ primes it approximates $S$ in mean square, unconditionally (Selberg, Tsang, Fujii; see below). The \emph{arithmetic correction} studied here adds this finite prime sum, $\Ph$ in \CGeqref{eq:Euler_phase}, to the main term: the zeros are then approximated by the points $\tau_k^{\mathrm C}$ of the equation $\Nz(t)+\Ph(t)=k-\frac12$ instead of $\Nz(t)=k-\frac12$.

The main result constructs the strictly increasing sequence $\tau_k^{\mathrm C}$ through the sublevel measures \CGeqref{eq:xk_def} of $\Nz+\Ph$, where $\Ph$ is defined by finitely many Euler phases. Unconditionally, the root-mean-square error of $\tau_k^{\mathrm C}$ with respect to $\gamma_k$ on dyadic blocks is $O(1/\log T)$, a bounded multiple of the mean zero spacing (Theorem~\CGref{thm:sublevel}). The key technical feature is the sublevel-set definition: it remains valid even when the prime-corrected counting function $\Nz+\Ph$ is not monotone, where the equation $\Nz+\Ph=k-\frac12$ may have no unique root.

An exact defect identity supplies an independent comparison. Without RH, the uncorrected points $\tau_k$ differ from the $\gamma_k$ by root-mean-square $\sqrt{2\log\log T}/\log T\,(1+o(1))$, the factor $\log\log T$ coming from Selberg's mean square of $S$. Thus the arithmetic correction removes the factor $\log\log T$ from the proved mean-square upper order. Further consequences proved below describe the arithmetic correction itself and the defect of the ordinal equation when evaluated at the actual imaginary parts $\gamma_k$.

'''
s=s[:i]+new+s[j:]

# ---- 2. ordinates ----
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))+len('\\makeatother\n')
pre,tips,post=s[:a],s[a:b],s[b:]
s=post
pairs=[
 ('$e_i$ for the ordinates','$e_i$ for the second coordinates'),
 ('(zeta imaginary ordinates)','(imaginary parts of the zeta zeros)'),
 ('positive imaginary ordinates','positive imaginary parts'),
 ('original Riemann--von Mangoldt ordinates and the actual ordinates','points $\\tau_k$ of the Riemann--von Mangoldt equation and the actual imaginary parts $\\gamma_k$'),
 ('uncorrected Riemann--von Mangoldt ordinates','uncorrected Riemann--von Mangoldt points $\\tau_k$'),
 ('the actual ordinates','the actual imaginary parts $\\gamma_k$'),
 ('We define the corrected ordinates by','We define the corrected points by'),
 ('increasing sublevel-defined ordinates','increasing sublevel-defined approximations of the imaginary parts'),
 ('error of ordinates $\\tau_{k}^{\\mathrm C}$ that are increasing and indexed by construction','error of the approximations $\\tau_{k}^{\\mathrm C}$ to the imaginary parts, which are increasing and indexed by construction'),
 ('Distance from \\texorpdfstring{$\\tau_k$}{tau_k} to the ordinates','Distance from \\texorpdfstring{$\\tau_k$}{tau_k} to the imaginary parts'),
 ('[Distance to the ordinates]','[Distance to the imaginary parts]'),
 ('at non-ordinates $t\\ge e$','at points $t\\ge e$ outside $\\{\\gamma_k\\}$'),
 ('large non-ordinates $t$','large $t$ outside $\\{\\gamma_k\\}$'),
 ('Choose non-ordinates $t\\to\\infty$','Choose $t\\to\\infty$ outside $\\{\\gamma_k\\}$'),
 ('be a non-ordinate','be outside $\\{\\gamma_k\\}$'),
 ('through non-ordinates','through values outside $\\{\\gamma_k\\}$'),
 ('tending to each ordinate','tending to each imaginary part'),
]
for o,n in pairs:
    c=s.count(o); assert c>=1,o
    s=s.replace(o,n)
s=s.replace('non-ordinates','points outside $\\{\\gamma_k\\}$').replace('non-ordinate','point outside $\\{\\gamma_k\\}$')
s=re.sub(r'\bordinates\b','imaginary parts',s); s=re.sub(r'\bordinate\b','imaginary part',s)
assert not re.search(r'\bordinate',s,re.I)
s=pre+tips+s
open(D+'casanya_ordinal_primes_v45.tex','w',encoding='utf-8').write(s)
print('ok')
