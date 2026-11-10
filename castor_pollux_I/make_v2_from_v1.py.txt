#!/usr/bin/env python3
"""Castor_Pollux_I_v1.tex -> Castor_Pollux_I_v2.tex.
Every edit is an exact replacement that must match exactly once; nothing else changes.
Usage: python3 make_v2.py V1.tex V2.tex"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
head, sep, tail = t.partition('\n\\end{document}\n')      # the real one, not the mentions in comments
assert sep, 'no \\end{document}'
pre, bd, body = head.partition('\n\\begin{document}\n')
assert bd and '\\end{document}' not in body
log = []


def rep(old, new, where, count=1):
    global body
    n = body.count(old)
    assert n == count, (where, 'expected', count, 'found', n, old[:60])
    body = body.replace(old, new)
    log.append((where, n))


# ---------------------------------------------------------------- 1. abstract
rep("All proofs use only the Fourier series of $h$, Parseval's identity and integration by parts. Seven figures show",
    "The proofs use the Fourier series of $h$, Parseval's identity and integration by parts, together with the "
    "Cauchy--Schwarz inequality, Rouch\\'e's theorem and standard real and complex analysis. Eight figures show",
    'abstract: scope of the techniques; eight figures')

# ---------------------------------------------------------------- 2. the letter i
rep("The letters $i,j,k,l,m,n,d,r$ denote integers, except that $i$ is the imaginary unit in exponentials and in $\\sigma+it$.",
    "The letter $i$ always denotes the imaginary unit. The letters $b,j,k,l,m,n,d,r$ denote integers.",
    'notation: i reserved for the imaginary unit')
rep("$s,\\sigma,t$ & complex variable, its real and imaginary parts & Section~\\CGref{sec:notation}\\\\\n",
    "$s,\\sigma,t$ & complex variable, its real and imaginary parts & Section~\\CGref{sec:notation}\\\\\n"
    "$i$ & imaginary unit & Section~\\CGref{sec:notation}\\\\\n",
    'symbol table: row for i')
rep("$x_i$ & quadrature nodes $(i+\\frac12)/\\mathsf L$", "$x_b$ & quadrature nodes $(b+\\frac12)/\\mathsf L$", 'symbol table: nodes')
rep("harmonic number $\\sum_{i\\le n}1/i$", "harmonic number $\\sum_{b\\le n}1/b$", 'symbol table: har')
rep("If $\\sigma_i+it_i$, $i\\ge1$, are zeros of $G$ with $\\sigma_i\\to+\\infty$, then $|t_i|/\\sigma_i\\to+\\infty$.",
    "If $\\sigma_b+it_b$, $b\\ge1$, are zeros of $G$ with $\\sigma_b\\to+\\infty$, then $|t_b|/\\sigma_b\\to+\\infty$.",
    'cor:angular: index')
rep("If $|t_i|/\\sigma_i$ stayed bounded", "If $|t_b|/\\sigma_b$ stayed bounded", 'cor:angular proof: index')
rep("$x_i=(i+\\frac12)/\\mathsf L$ for $0\\le i\\le\\mathsf L-1$", "$x_b=(b+\\frac12)/\\mathsf L$ for $0\\le b\\le\\mathsf L-1$", 'def:trunc: index')
rep("\\sum_{i=0}^{\\mathsf L-1}\\mathcal K_{\\mathsf M}(x_i)\\,(n+x_i)^{-s-3}", "\\sum_{b=0}^{\\mathsf L-1}\\mathcal K_{\\mathsf M}(x_b)\\,(n+x_b)^{-s-3}", 'eq:HMNL: index')
rep("\\sum_{i=0}^{\\mathsf L-1}\\chi(x_i)", "\\sum_{b=0}^{\\mathsf L-1}\\chi(x_b)", 'eq:midpoint: index')
rep("centred at $x_i$, Taylor's formula gives $|\\chi(x)-\\chi(x_i)-\\chi'(x_i)(x-x_i)|\\le\\frac12\\sup|\\chi''|(x-x_i)^2$, the linear term integrates to $0$, and $\\int(x-x_i)^2dx",
    "centred at $x_b$, Taylor's formula gives $|\\chi(x)-\\chi(x_b)-\\chi'(x_b)(x-x_b)|\\le\\frac12\\sup|\\chi''|(x-x_b)^2$, the linear term integrates to $0$, and $\\int(x-x_b)^2dx",
    'midpoint rule text: index')
rep("\\sum_{i=0}^{a}J_2(p^i)=1+\\sum_{i=1}^{a}(p^{2i}-p^{2i-2})=p^{2a}", "\\sum_{b=0}^{a}J_2(p^b)=1+\\sum_{b=1}^{a}(p^{2b}-p^{2b-2})=p^{2a}", 'J_2 prime powers: index')
rep("\\operatorname{har}(n)=\\sum_{i=1}^{n}1/i$", "\\operatorname{har}(n)=\\sum_{b=1}^{n}1/b$", 'cor:partial proof: har')
rep("are $k=di$ with $1\\le i\\le\\lfloor K/d\\rfloor$", "are $k=db$ with $1\\le b\\le\\lfloor K/d\\rfloor$", 'cor:partial proof: multiples')
rep("Since $\\prod_i(1-a_i)\\ge1-\\sum_ia_i$ for numbers $a_i\\in[0,1]$", "Since $\\prod_b(1-a_b)\\ge1-\\sum_ba_b$ for numbers $a_b\\in[0,1]$", 'cor:partial proof: product')
rep("\\sum_{i\\ge0}(a+iL)^{-2\\sigma-1}", "\\sum_{b\\ge0}(a+bL)^{-2\\sigma-1}", 'prop:bound proof: index')

# ---------------------------------------------------------------- 3. Rouche: certified
rep("The sums $\\eta_0$ and $\\eta_1$ were evaluated in double precision arithmetic, and the rounding errors of these two finite sums are not bounded here. "
    "With that reservation, the inequality holds at the six points, so each disc $|s-s_0|<10^{-2}$ contains exactly one zero of $G$. ",
    "The six centres are the decimal numbers printed in the table, taken as exact rational numbers. "
    "The finite sums $\\eta_0$ and $\\eta_1$, the bounds $E_0$ and $E_1$ and the two sides of \\CGeqref{eq:rouche} were enclosed in ball arithmetic "
    "with the library Arb \\cite{Johansson2017}, at a precision of $128$ bits. In this arithmetic every operation returns a midpoint and a radius "
    "such that the ball contains the exact result, so the rounding errors are inside the radii. The radii of the real and imaginary parts of "
    "$\\eta_0$ and $\\eta_1$ are below $10^{-32}$. At each of the six points the upper bound of the left side of \\CGeqref{eq:rouche} is smaller "
    "than the lower bound of the right side, and the left side is less than $0.47$ times the right side. By Proposition~\\CGref{prop:rouche}, "
    "each disc $|s-s_0|<10^{-2}$ contains exactly one zero of $G$, and this zero is simple. The entries of Table~\\CGref{tab:rouche} are the "
    "enclosures rounded to the digits shown. ",
    'Rouche test: ball arithmetic certificate')

# ---------------------------------------------------------------- 4. lem:T, sign of r'
rep("Summing over $l\\ge0$ and using the formula for $\\psi(\\alpha)-\\psi(\\beta)$ stated after \\CGeqref{eq:psi} gives \\CGeqref{eq:Tclosed}.",
    "Summing over $l\\ge0$ and using the formula for $\\psi(\\alpha)-\\psi(\\beta)$ stated after \\CGeqref{eq:psi} gives \\CGeqref{eq:Tclosed}. "
    "This holds for both signs of $r'$. Each term $1/(l+\\beta)-1/(l+\\alpha)$ has the sign of $\\alpha-\\beta$, which is the sign of $r'$. "
    "Hence in \\CGeqref{eq:Tclosed} the difference $\\psi(m_*/j')-\\psi(n_*/k')$ and the denominator $2r'$ change sign together, and $T_{jk}(r)>0$.",
    "lem:T proof: both signs of r'")

# ---------------------------------------------------------------- 5. numerical comparison
rep("Table~\\CGref{tab:check} compares the two sides of \\CGeqref{eq:weighted} in four cases. The left side",
    "Table~\\CGref{tab:check} compares the two sides of \\CGeqref{eq:weighted} in four cases. It is a numerical check and is not used in any proof. The left side",
    'numerical comparison: status')
rep("with $X=j\\vee k+150\\,[j,k]$. The right side was computed with the terms $r\\le20000$ of the series, using \\CGeqref{eq:Tclosed} for $T_{jk}(\\pm r)$.",
    "with $X=j\\vee k+150\\,[j,k]$. In the four cases of the table this bound equals $4.1\\cdot10^{-7}$, $1.5\\cdot10^{-7}$, $2.5\\cdot10^{-5}$ and "
    "$1.4\\cdot10^{-4}$, rounded up. The right side was computed with the terms $r\\le20000$ of the series, using \\CGeqref{eq:Tclosed} for $T_{jk}(\\pm r)$. "
    "The error of the quadrature and the tail $r>20000$ of the series are not bounded here.",
    'numerical comparison: what is and is not bounded')
rep("The two computations agree to seven decimal places in the four cases.",
    "The two computed values differ by at most $1.3\\cdot10^{-8}$ in the four cases.",
    'numerical comparison: observed difference')

# ---------------------------------------------------------------- 6. G/A
rep("and the arcs of the curve $\\operatorname{Im}(G/A)=0$ on which $0<\\operatorname{Re}(G/A)<1$. At those six points the computed value of $|G-A|$ is below $10^{-11}$. "
    "Each arc joins a zero of $G$, where $G/A=0$, to one of those points, where $G/A=1$.",
    "and the arcs of the curve $\\operatorname{Im}(G/A)=0$ on which $0<\\operatorname{Re}(G/A)<1$. The quotient $G/A$ is formed only at points where $A(s)\\ne0$. "
    "At the $39\\times157$ grid points the computed values satisfy $|A(s)|\\ge0.072$, and the arcs are the level lines drawn from the grid values. "
    "That $A$ has no zero in the whole rectangle is not proved in this note. At those six points the computed value of $|G-A|$ is below $10^{-11}$. "
    "In the computed figure each arc joins a zero of $G$, where $G/A=0$, to one of those points, where $G/A=1$. This pairing is a numerical observation "
    "for these six zeros. It is not proved, and no correspondence between the zeros of $G$ and the points with $G=A$ is claimed.",
    'figures: A nonzero, pairing is an observation')
rep("\\caption{Zeros of $G$, points with $G=A$, and the arcs of $\\operatorname{Im}(G/A)=0$ with $0<\\operatorname{Re}(G/A)<1$.}\\label{fig:zeromap}",
    "\\caption{Computed zeros of $G$, computed points with $G=A$, and the computed arcs of $\\operatorname{Im}(G/A)=0$ with $0<\\operatorname{Re}(G/A)<1$, "
    "at points where $A\\ne0$. The pairing shown by the arcs is a numerical observation.}\\label{fig:zeromap}",
    'fig:zeromap caption')

# ---------------------------------------------------------------- 7. bibliography
rep("\\begin{thebibliography}{9}\n\n\\bibitem{Smith1875}",
    "\\begin{thebibliography}{9}\n\n\\bibitem{Johansson2017}\n"
    "F.~Johansson, Arb: efficient arbitrary-precision midpoint-radius interval arithmetic, \\emph{IEEE Trans. Comput.} \\textbf{66} (2017), no.~8, 1281--1292.\n"
    "\\href{https://doi.org/10.1109/TC.2017.2690633}{doi:10.1109/TC.2017.2690633}.\n\n\\bibitem{Smith1875}",
    'bibliography: Arb')

# ---------------------------------------------------------------- 8. tooltips (preamble)
plog = []


def prep(old, new, where, count=1):
    global pre
    n = pre.count(old)
    assert n == count, (where, 'expected', count, 'found', n, old[:60])
    pre = pre.replace(old, new)
    plog.append((where, n))


# changed statements
prep("If sigma\\_i+it\\_i, i>=1, are zeros of G with sigma\\_i->+infinity, then |t\\_i|/sigma\\_i->+infinity.",
     "If sigma\\_b+it\\_b, b>=1, are zeros of G with sigma\\_b->+infinity, then |t\\_b|/sigma\\_b->+infinity.", 'tip cor:angular')
prep("x\\_i=(i+1/2)/ L for 0<= i<= L-1", "x\\_b=(b+1/2)/ L for 0<= b<= L-1", 'tip def:trunc (1)')
prep("sum\\_(i=0)\\textasciicircum{}( L-1) K\\_( M)(x\\_i) (n+x\\_i)\\textasciicircum{}(-s-3).",
     "sum\\_(b=0)\\textasciicircum{}( L-1) K\\_( M)(x\\_b) (n+x\\_b)\\textasciicircum{}(-s-3).", 'tip eq:HMNL')
prep("sum\\_(i=0)\\textasciicircum{}( L-1) K\\_( M)(x\\_i) (n+x\\_i)\\textasciicircum{}(-s}",
     "sum\\_(b=0)\\textasciicircum{}( L-1) K\\_( M)(x\\_b) (n+x\\_b)\\textasciicircum{}(-s}", 'tip def:trunc (2)')
prep("sum\\_(i=0)\\textasciicircum{}( L-1)chi(x\\_i)|", "sum\\_(b=0)\\textasciicircum{}( L-1)chi(x\\_b)|", 'tip eq:midpoint')
prep("Figure: Zeros of G, points with G=A, and the arcs of (Im)(G/A)=0 with 0<(Re)(G/A)<1.",
     "Figure: Computed zeros of G, computed points with G=A, and the computed arcs of (Im)(G/A)=0 with 0<(Re)(G/A)<1, at points where A!=0. "
     "The pairing shown by the arcs is a numerical observation.", 'tip fig:zeromap')
# readability: "\int" had been rendered as "in t"; aligned displays had left "()"
n_int = len(re.findall(r'(?m)^\\expandafter\\gdef\\csname CGTip@.*in t\\_', pre))
lines = pre.split('\n')
c_int = c_par = 0
for k, ln in enumerate(lines):
    if ln.startswith('\\expandafter\\gdef\\csname CGTip@'):
        a = ln.count(' in t\\_')
        ln2 = ln.replace(' in t\\_', ' int\\_')
        a2 = ln2.count('in t\\_')
        ln2 = ln2.replace('in t\\_', 'int\\_')
        b = ln2.count('=()frac')
        ln2 = ln2.replace('=()frac', '=frac')
        c_int += a + a2
        c_par += b
        lines[k] = ln2
pre = '\n'.join(lines)
plog.append(('tips: "in t_" -> "int_"', c_int))
plog.append(('tips: "=()frac" -> "=frac"', c_par))
assert 'in t\\_' not in pre

open(dst, 'w', encoding='utf-8').write(pre + bd + body + sep + tail)
for w, n in log + plog:
    print('%3d  %s' % (n, w))
print('edits in the body: %d; in the tooltips: %d' % (len(log), len(plog)))
