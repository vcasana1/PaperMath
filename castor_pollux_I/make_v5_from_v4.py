#!/usr/bin/env python3
"""Castor and Pollux I: v4 -> v5.
New Sections 'The difference G-A', 'A positive convex kernel for G-A', 'The difference G-A and the Riemann zeta
function' and 'Conclusions' (text in v5_new_sections.tex), two renamings that removed clashes of letters
(p^a -> p^k in the Jordan totient paragraph, a_b -> theta_b in the proof of Corollary cor:partial), and the updates of
abstract, introduction, notation, figures paragraph and bibliography that the new sections require.
Every edit is an exact replacement that must match exactly once; nothing else changes.
Usage: python3 make_v5.py V4.tex V5.tex BUILD.py NEW_SECTIONS.tex"""
import re
import sys

src, dst, build, newsec = sys.argv[1:5]
t = open(src, encoding='utf-8').read()
head, sep, tail = t.partition('\n\\end{document}\n')
pre, bd, body = head.partition('\n\\begin{document}\n')
assert sep and bd
bsrc = open(build, encoding='utf-8').read()
exec(bsrc[bsrc.index('def detex'):bsrc.index('tips={}')])
new = open(newsec, encoding='utf-8').read()
log = []


def rep(old, new_, where, part='body'):
    global body, pre
    s = body if part == 'body' else pre
    assert s.count(old) == 1, (where, s.count(old), old[:70])
    s = s.replace(old, new_)
    if part == 'body':
        body = s
    else:
        pre = s
    log.append(where)


# ---------------------------------------------------------------- clashes of letters
rep(r"for a prime power $p^a$ with $a\ge1$ we have $\sum_{b=0}^{a}J_2(p^b)=1+\sum_{b=1}^{a}(p^{2b}-p^{2b-2})=p^{2a}$",
    r"for a prime power $p^k$ with $k\ge1$ we have $\sum_{b=0}^{k}J_2(p^b)=1+\sum_{b=1}^{k}(p^{2b}-p^{2b-2})=p^{2k}$",
    'J_2 paragraph: exponent a -> k (a is j v k)')
rep(r"Since $\prod_b(1-a_b)\ge1-\sum_ba_b$ for numbers $a_b\in[0,1]$",
    r"Since $\prod_b(1-\theta_b)\ge1-\sum_b\theta_b$ for numbers $\theta_b\in[0,1]$",
    'proof of cor:partial: a_b -> theta_b')
rep(r"The letters $u,x,v,\tau,\lambda,\theta$ denote real variables.",
    r"The letters $u,x,y,v,\tau,\lambda,\theta$ denote real variables.", 'notation: y is a real variable')

# ---------------------------------------------------------------- front matter
rep(r"\subjclass[2020]{11A05; 11C20; 42A16; 33B15; 30C15; 44A15}",
    r"\subjclass[2020]{11A05; 11C20; 42A16; 33B15; 30C15; 44A15; 11M06; 11M26}", 'subjclass')
rep(r"Gram matrix; digamma function}",
    r"Gram matrix; digamma function; Riemann hypothesis}", 'keywords')
rep(r"pdfkeywords={products of sines, log-sine function, Mellin transform, positive kernel, gcd matrices, Jordan totient, Gram matrix, digamma function}",
    r"pdfkeywords={products of sines, log-sine function, Mellin transform, positive kernel, gcd matrices, Jordan totient, Gram matrix, digamma function, Riemann hypothesis}",
    'pdfkeywords', part='pre')
rep(r"The proofs use the Fourier series of $h$, Parseval's identity and integration by parts, together with the Cauchy--Schwarz inequality, Rouch\'e's theorem and standard real and complex analysis. Twelve figures",
    r"We then study the difference $G-A$, where $A$ is an explicit auxiliary function, using only $h$. On the strip $0<\operatorname{Re}s<2$, $G-A$ is minus the Mellin transform of the positive function $\log(\pi u/|\sin(\pi u)|)$, and, after the factor $-(s+1)(s+2)/(4\pi^2)$, the Mellin transform of an explicit positive convex kernel that satisfies a strict inversion inequality. This gives the bound $|G-A|\le A(\operatorname{Re}s)-G(\operatorname{Re}s)$, a decomposition through the digamma function, a region without solutions of $G=A$ around the real axis, and the decay of the transform. We prove analytically that $A(s)\ne0$ for $0\le\operatorname{Re}s\le1$ and $|\operatorname{Im}s|\ge9$. A positive periodic kernel with two harmonics shows that positivity and periodicity alone do not place the solutions of $G=A$ on $\operatorname{Re}s=\frac12$. Finally, through the functional equation of the Riemann zeta function, $G(s)-A(s)=\frac\pi s\cot(\frac{\pi s}2)\zeta(s)$, so that the statement that every non-real solution of $G(s)=A(s)$ has real part $\frac12$ is equivalent to the Riemann hypothesis. "
    r"The proofs use the Fourier series of $h$, Parseval's identity and integration by parts, together with the Cauchy--Schwarz inequality, Rouch\'e's theorem and standard real and complex analysis, and, in one section only, cited results on the zeta and gamma functions. Twelve figures",
    'abstract')
rep(r"and exponential sums over computed zeros of $G$ and of $A$. Section~\CGref{sec:notation} lists every symbol of the note with its single meaning.",
    r"and exponential sums over computed zeros of $G$ and of $A$. Section~\CGref{sec:GA} writes $G-A$ as minus the Mellin transform of the positive function $\log(\pi u/|\sin(\pi u)|)$ (Proposition~\CGref{prop:GAbound}) and through the digamma function (Proposition~\CGref{prop:GAdigamma}), and proves that $A(s)\ne0$ for $0\le\operatorname{Re}s\le1$ and $|\operatorname{Im}s|\ge9$ (Theorem~\CGref{thm:Anonzero}). Section~\CGref{sec:B} writes $G-A$ through the Mellin transform of a positive convex kernel (Proposition~\CGref{prop:B}), proves an inversion inequality for it (Proposition~\CGref{prop:Binv}), a region without solutions of $G=A$ around the real axis (Theorem~\CGref{thm:GAexcl}) and a decay bound (Proposition~\CGref{prop:Omegadecay}), and gives a positive kernel with two harmonics for which the counterpart of $G-A$ vanishes at points with real part $\frac34$ (Proposition~\CGref{prop:Ksharp}). These two sections do not use the Riemann zeta function. Section~\CGref{sec:zeta} introduces it and proves that $G(s)-A(s)=\frac\pi s\cot(\frac{\pi s}2)\zeta(s)$ (Proposition~\CGref{prop:zeta}), so that the condition that every non-real solution of $G=A$ has real part $\frac12$ is the Riemann hypothesis (Corollary~\CGref{cor:RH}). Section~\CGref{sec:concl} states the conclusions: what is characterized without $\zeta$, why the introduction of $\zeta$ does not lead further, and whether and where $G$ and $A$ intersect. Section~\CGref{sec:notation} lists every symbol of the note with its single meaning.",
    'introduction')

# ---------------------------------------------------------------- symbol table
rep(r"$\zeta(s)$ & Riemann zeta function, used only in Section~\CGref{sec:fig} & Section~\CGref{sec:fig}\\",
    r"$\zeta(s)$ & Riemann zeta function, used only in Sections~\CGref{sec:fig}, \CGref{sec:zeta} and~\CGref{sec:concl} & Section~\CGref{sec:fig}\\" "\n"
    r"$\ell(u)$ & $\log(\pi u/|\sin(\pi u)|)$, $u>0$ & \CGeqref{eq:ell}\\" "\n"
    r"$q_0(u),Q_0(s)$ & remainder on $(0,1)$ and its transform & \CGeqref{eq:q0}, \CGeqref{eq:Q0series}\\" "\n"
    r"$\mathcal Q(t),\mathfrak r_k$ & upper bound for $\operatorname{Re}(sA(s))$, real part of $s/(2k-s)$ & Theorem~\CGref{thm:Anonzero}\\" "\n"
    r"$\mathfrak b$ & $\log(2\pi)-\frac32$ & Section~\CGref{sec:B}\\" "\n"
    r"$\mathcal B(u),\Omega(s)$ & positive convex kernel of $G-A$ and its Mellin transform & \CGeqref{eq:Bdef}\\" "\n"
    r"$\upsilon_\sigma(v),\upsilon^\pm_\sigma(v)$ & weights of $\Omega$ in the variable $v=\log u$ & \CGeqref{eq:upsilon}\\" "\n"
    r"$\mathcal M_j(\sigma)$ & moments of $\mathcal B$, $j=0,1,2$ & Theorem~\CGref{thm:GAexcl}\\" "\n"
    r"$\mathcal K^\sharp,H^\sharp,\widetilde H^\sharp,G^\sharp,A^\sharp,\mathfrak c_n$ & kernel with two harmonics and its counterparts of $H,\widetilde H,G,A$; Taylor coefficients & \CGeqref{eq:Ksharp}\\" "\n"
    r"$\mathcal C(s)$ & $\int_0^\infty(1-\cos y)y^{-s-3}dy$ & \CGeqref{eq:Cdef}\\" "\n"
    r"$\Gamma(s)$ & Euler's gamma function, used only in Section~\CGref{sec:zeta} & Section~\CGref{sec:zeta}\\" "\n"
    r"$N(T),N_0(T)$ & number of zeros of $\zeta$ up to height $T$, main term plus $\frac78$ & \CGeqref{eq:NT}\\" "\n"
    r"$\tau_k,W$ & solutions of $N_0(\tau_k)=k-\frac12$, inverse of $w\mapsto we^w$ & \CGeqref{eq:tauk}\\",
    'symbol table')

# ---------------------------------------------------------------- figures section
rep(r"the modulus of the Riemann zeta function $\zeta(s)$, clipped above $1.5$, which is not used anywhere else in this note.",
    r"the modulus of the Riemann zeta function $\zeta(s)$, clipped above $1.5$, which is used elsewhere only in Sections~\CGref{sec:zeta} and~\CGref{sec:concl}.",
    'figures: zeta used in Section zeta')
rep(r"This relation is not proved and not used in this note.",
    r"This relation is proved in Proposition~\CGref{prop:zeta}.", 'figures: relation proved')
rep(r"That $A$ has no zero in the whole rectangle is not proved in this note.",
    r"That $A$ has no zero for $0.05\le\operatorname{Re}s\le1$ and $9\le\operatorname{Im}s\le40$ is Theorem~\CGref{thm:Anonzero}. On the rest of the rectangle it is not proved in this note.",
    'figures: A nonzero partly proved')

# ---------------------------------------------------------------- new sections and bibliography
rep("\\clearpage\n\\begin{thebibliography}{9}\n",
    new.rstrip('\n') + "\n\n\\clearpage\n\\begin{thebibliography}{9}\n", 'new sections')
rep(r"""\href{https://doi.org/10.1112/plms/s1-7.1.208}{doi:10.1112/plms/s1-7.1.208}.
""",
    r"""\href{https://doi.org/10.1112/plms/s1-7.1.208}{doi:10.1112/plms/s1-7.1.208}.

\bibitem{Titchmarsh1939}
E.~C.~Titchmarsh, \emph{The Theory of Functions}, 2nd ed., Oxford University Press, Oxford, 1939. No DOI.

\bibitem{Titchmarsh1986}
E.~C.~Titchmarsh, \emph{The Theory of the Riemann Zeta-Function}, 2nd ed., revised by D.~R.~Heath-Brown, Clarendon Press, Oxford, 1986. No DOI.
""", 'bibliography')

# ---------------------------------------------------------------- tooltips
tips = {}
for m in re.finditer(r'\\begin\{equation\}\\label\{([^}]+)\}(.*?)\\end\{equation\}', body, re.S):
    tips[m.group(1)] = 'Equation: ' + detex(m.group(2))
for m in re.finditer(r'\\section\{(.*?)\}\\label\{([^}]+)\}', body):
    tips[m.group(2)] = 'Section: ' + detex(m.group(1))
for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark)\}\[(.*?)\]\\label\{([^}]+)\}(.*?)\\end\{\1\}', body, re.S):
    tips[m.group(3)] = m.group(1).capitalize() + ' - ' + detex(m.group(2)) + ': ' + detex(m.group(4), 260)


def clean(s):
    return s.replace(' in t\\_', ' int\\_').replace('in t\\_', 'int\\_').replace('=()frac', '=frac')


new_labels = re.findall(r'\\label\{([^}]+)\}', new)
lines = pre.split('\n')
idx = [k for k, ln in enumerate(lines) if ln.startswith('\\expandafter\\gdef\\csname CGTip@fig:gram\\endcsname{')]
assert len(idx) == 1
lines[idx[0] + 1:idx[0] + 1] = ['\\expandafter\\gdef\\csname CGTip@%s\\endcsname{%s}' % (lab, clean(tips[lab])) for lab in new_labels]
pre = '\n'.join(lines)
labels = re.findall(r'\\label\{([^}]+)\}', body)
assert len(labels) == len(set(labels)), [l for l in labels if labels.count(l) > 1]
missing = [l for l in labels if ('CGTip@%s\\endcsname' % l) not in pre]
assert not missing, missing

open(dst, 'w', encoding='utf-8').write(pre + bd + body + sep + tail)
for w in log:
    print('  1  ' + w)
print('edits: %d; tooltips added: %d; labels: %d' % (len(log), len(new_labels), len(labels)))
