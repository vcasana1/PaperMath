#!/usr/bin/env python3
"""Castor_Pollux_I_v2.tex -> Castor_Pollux_I_v3.tex.
Every edit is an exact replacement that must match exactly once; nothing else changes.
Usage: python3 make_v3.py V2.tex V3.tex BUILD.py   (BUILD.py = build.py of the v1 package, for its detex function)"""
import re
import sys

src, dst, build = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src, encoding='utf-8').read()
head, sep, tail = t.partition('\n\\end{document}\n')
assert sep
pre, bd, body = head.partition('\n\\begin{document}\n')
assert bd and '\\end{document}' not in body
bsrc = open(build, encoding='utf-8').read()
exec(bsrc[bsrc.index('def detex'):bsrc.index('tips={}')])          # defines detex(s, cut)
log = []


def rep(old, new, where):
    global body
    n = body.count(old)
    assert n == 1, (where, 'found', n, old[:70])
    body = body.replace(old, new)
    log.append(where)


# ------------------------------------------------------------------ abstract and introduction
rep("Eight figures show the kernels, the moduli of $G$, of an auxiliary function $A$ and of the Riemann zeta function on a rectangle, and the two Gram matrices.",
    "Twelve figures show the kernels, the moduli of $G$, of an auxiliary function $A$ and of the Riemann zeta function on a rectangle, "
    "exponential sums over computed zeros of $G$ and of $A$, and the two Gram matrices.", 'abstract: twelve figures')
rep("Section~\\CGref{sec:fig} contains the figures. Section",
    "Section~\\CGref{sec:fig} contains the figures, the continuation and the real zeros of the auxiliary function $A$ "
    "(Proposition~\\CGref{prop:A}), and exponential sums over computed zeros of $G$ and of $A$. Section", 'introduction: content of the last section')

# ------------------------------------------------------------------ symbol table
rep("$A(s)$ & auxiliary function of the figures & \\CGeqref{eq:A}\\\\\n",
    "$A(s)$ & auxiliary function of the figures & \\CGeqref{eq:A}\\\\\n"
    "$\\Sigma_{2k}$ & $\\sum_{m\\ge1}m^{-2k}$ for the integers $k\\ge1$ & Proposition~\\CGref{prop:A}\\\\\n"
    "$\\widetilde H(s)$ & transform of $\\mathcal K$ on $(0,1)$ & \\CGeqref{eq:Afactor}\\\\\n"
    "$z^G_b,n_G$ & computed zeros of $G$ and their number & Section~\\CGref{sec:fig}\\\\\n"
    "$z^A_b,n_A$ & computed real zeros of $A$ and their number & Section~\\CGref{sec:fig}\\\\\n"
    "$\\mathcal E_G(x),\\mathcal E_A(x)$ & exponential sums over these zeros & \\CGeqref{eq:expsum}\\\\\n", 'symbol table: new rows')

# ------------------------------------------------------------------ how G is evaluated
rep("with the midpoint rule for the integral over $x$ and the Euler--Maclaurin formula for the sum over $n>24$.",
    "with a quadrature rule for the integral over $x$ (the midpoint rule for Figure~\\CGref{fig:Greal}, a Gauss--Legendre rule with $240$ nodes for the surfaces) "
    "and the Euler--Maclaurin formula for the tail of the sum over $n$.", 'figures: evaluation of G')

# ------------------------------------------------------------------ Proposition on A
PROP = r"""Thus $G-A$ is the Mellin transform on the whole half-line of $h$ minus its logarithmic part.

\begin{proposition}[Continuation and real zeros of $A$]\label{prop:A}\VCGreviewed{1}
Put $\Sigma_{2k}=\sum_{m\ge1}m^{-2k}$ for the integers $k\ge1$. The function $A$ of \CGeqref{eq:A} extends to a meromorphic function on $\mathbb C$, given by
\begin{equation}\label{eq:Aseries}
A(s)=\frac{\log(2\pi)}{s}+\frac1{s^2}+\sum_{k\ge1}\frac{\Sigma_{2k}}{k\,(2k-s)} .
\end{equation}
Its poles are a double pole at $0$ and a simple pole at each positive even integer. For $\operatorname{Re}s<0$,
\begin{equation}\label{eq:Afactor}
A(s)=-\int_0^1h(u)\,u^{-s-1}\,du=\frac{(s+1)(s+2)}{4\pi^2}\,\widetilde H(s),\qquad\widetilde H(s)=\int_0^1\mathcal K(u)\,u^{-s-3}\,du .
\end{equation}
For real $s$ we have $A(s)>0$ for $s<-2$, $A(-2)=0$, $A(s)<0$ for $-2<s<-1$, $A(-1)=0$, and $A(s)>0$ for $-1<s<0$ and for $0<s<2$. The zeros at $-2$ and $-1$ are simple. For every integer $l\ge1$ the function $A$ has at least one zero in the interval $(2l,2l+2)$.
\end{proposition}

\begin{proof}
Let $0<u<1$. The classical product of Euler, $\sin(\pi u)=\pi u\prod_{m\ge1}(1-u^2/m^2)$, and the series $\log(1-\lambda)=-\sum_{k\ge1}\lambda^k/k$ for $0\le\lambda<1$ give
\begin{equation}\label{eq:logsinc}
-\log\frac{\sin(\pi u)}{\pi u}=\sum_{m\ge1}\sum_{k\ge1}\frac{u^{2k}}{k\,m^{2k}}=\sum_{k\ge1}\frac{\Sigma_{2k}}{k}\,u^{2k},
\end{equation}
where the terms are nonnegative, so that the order of summation is free. Let $\sigma=\operatorname{Re}s<2$. We have $\int_0^1u^{2k-\sigma-1}du=1/(2k-\sigma)$ for all $k\ge1$, and $\sum_{k\ge1}\Sigma_{2k}/(k(2k-\sigma))<\infty$ because $\Sigma_{2k}\le\Sigma_2$. Hence \CGeqref{eq:logsinc} can be integrated termwise against $u^{-s-1}$, and
\begin{equation}\label{eq:Aterm}
-\int_0^1\log\frac{\sin(\pi u)}{\pi u}\,u^{-s-1}\,du=\sum_{k\ge1}\frac{\Sigma_{2k}}{k\,(2k-s)}\qquad(\operatorname{Re}s<2).
\end{equation}
With \CGeqref{eq:A} this is \CGeqref{eq:Aseries} for $0<\operatorname{Re}s<2$. Let $\theta>0$. For $|s|\le\theta$ and $k>\theta$ we have $|2k-s|\ge2k-\theta\ge k$, so the term of index $k$ in \CGeqref{eq:Aseries} has modulus at most $\Sigma_2/k^2$. Hence the series, without its finitely many terms with $k\le\theta$, converges uniformly on $|s|\le\theta$. The right side of \CGeqref{eq:Aseries} is therefore meromorphic on $\mathbb C$, with the principal part $\log(2\pi)/s+1/s^2$ at $0$ and a simple pole of residue $-\Sigma_{2l}/l$ at $2l$ for every integer $l\ge1$. It is the extension of $A$.

Let $\operatorname{Re}s<0$. Then $\int_0^1u^{-s-1}du=-1/s$ and $\int_0^1(\log u)u^{-s-1}du=-1/s^2$, so $\int_0^1\log(2\pi u)u^{-s-1}du=-\log(2\pi)/s-1/s^2$. Since $h(u)=\log(2\pi u)+\log(\sin(\pi u)/(\pi u))$ for $0<u<1$, \CGeqref{eq:Aseries} and \CGeqref{eq:Aterm} give the first equality in \CGeqref{eq:Afactor}. The integral converges absolutely by the bound $|h(u)|\le\log2+|\log(4u)|$ for $0<u\le\frac12$ from the proof of Lemma~\CGref{lem:kernel} and by $h(1-u)=h(u)$.

Let $0<\tau<\frac14$. By \CGeqref{eq:Kprime}, $h=-\mathcal K''/(4\pi^2)$ almost everywhere, with $\mathcal K'$ absolutely continuous. Two integrations by parts, in which $\mathcal K'(1)=\mathcal K(1)=0$ by \CGeqref{eq:Kprops}, give
\begin{equation}\label{eq:Aparts}
\int_\tau^1h(u)\,u^{-s-1}\,du=\frac{\mathcal K'(\tau)\,\tau^{-s-1}}{4\pi^2}+\frac{(s+1)\,\mathcal K(\tau)\,\tau^{-s-2}}{4\pi^2}-\frac{(s+1)(s+2)}{4\pi^2}\int_\tau^1\mathcal K(u)\,u^{-s-3}\,du .
\end{equation}
By \CGeqref{eq:Kprime} and the bound for $|h|$ just quoted, $|\mathcal K'(\tau)|\le4\pi^2\int_0^\tau|h|\le4\pi^2\tau(\log2+|\log(4\tau)|+1)$. By Lemma~\CGref{lem:Klocal}, $0\le\mathcal K(\tau)\le2\pi^2\tau^2(\log\frac1\tau+\frac32)+\pi^4\tau^4/9$. Since $\sigma<0$, the two boundary terms in \CGeqref{eq:Aparts} have modulus at most a constant times $\tau^{-\sigma}(1+\log\frac1\tau)$ and tend to $0$ as $\tau\to0$, and $\mathcal K(u)u^{-\sigma-3}$ is integrable on $(0,1)$. Letting $\tau\to0$ in \CGeqref{eq:Aparts} gives the second equality in \CGeqref{eq:Afactor}, and $\widetilde H$ is holomorphic in $\operatorname{Re}s<0$.

For real $s<0$ we have $\widetilde H(s)>0$, because $\mathcal K>0$ on $(0,1)$ by \CGeqref{eq:Kprops}. By \CGeqref{eq:Afactor} the sign of $A(s)$ is the sign of $(s+1)(s+2)$, and the zeros at $-2$ and $-1$ are simple. For $0<s<2$ every term of \CGeqref{eq:Aseries} is positive. Let $l\ge1$ be an integer. On the interval $(2l,2l+2)$ the function $A$ is real and continuous. As $s$ decreases to $2l$, the term of index $l$ in \CGeqref{eq:Aseries} tends to $-\infty$ and the rest of the right side of \CGeqref{eq:Aseries} stays bounded. As $s$ increases to $2l+2$, the term of index $l+1$ tends to $+\infty$ and the rest of the right side stays bounded. By the intermediate value theorem $A$ vanishes in $(2l,2l+2)$.
\end{proof}

Formula \CGeqref{eq:Afactor} is the counterpart of \CGeqref{eq:factor} for the part of $\mathcal K$ on $(0,1)$."""
rep("Thus $G-A$ is the Mellin transform on the whole half-line of $h$ minus its logarithmic part.", PROP, 'Proposition prop:A with proof')

# ------------------------------------------------------------------ surfaces
rep("Figures~\\CGref{fig:Gsurf}, \\CGref{fig:Asurf} and~\\CGref{fig:GAsurf} show $\\log_{10}$ of the moduli of $G$, $A$ and $G-A$ on the rectangle $0.05\\le\\operatorname{Re}s\\le1.95$, $1\\le\\operatorname{Im}s\\le40$, on a grid of $39\\times157$ points. "
    "Figure~\\CGref{fig:zetasurf} shows, on the same grid, the modulus of the Riemann zeta function $\\zeta(s)$, which is not used anywhere else in this note. "
    "On that grid the computed values satisfy $|G(s)-A(s)-\\frac\\pi s\\cot(\\frac{\\pi s}2)\\zeta(s)|\\le9.1\\cdot10^{-7}$.",
    "Figures~\\CGref{fig:Gsurf}, \\CGref{fig:Asurf} and~\\CGref{fig:GAsurf} show $-\\log_{10}$ of the moduli of $G$, $A$ and $G-A$ on the rectangle $0.05\\le\\operatorname{Re}s\\le1.95$, $1\\le\\operatorname{Im}s\\le40$, so that a zero is a peak. "
    "The grid has $253\\times889$ points. Its steps are $0.01$ in $\\operatorname{Re}s$ and $0.05$ in $\\operatorname{Im}s$, and it is refined near the six zeros of $G$ of Table~\\CGref{tab:rouche} and near the six points $\\frac12+it$ of Figure~\\CGref{fig:zeromap}, which are grid points. "
    "The plotted values are clipped at $6$, that is, where the modulus is below $10^{-6}$. At the six zeros of $G$ the computed values of $|G|$ are between $4.1\\cdot10^{-12}$ and $2.8\\cdot10^{-11}$. "
    "On this rectangle $A$ has no peak. Figure~\\CGref{fig:Areal} shows $-\\log_{10}|A(s)|$ for $-3.5\\le\\operatorname{Re}s\\le9.5$ and $|\\operatorname{Im}s|\\le2$, computed from \\CGeqref{eq:Aseries}. "
    "Its peaks are the real zeros of Proposition~\\CGref{prop:A} at $-2$ and $-1$ and the computed zeros $3.0428$, $5.0981$, $7.1478$ and $9.1892$, and its pits are the poles at $0,2,4,6,8$. "
    "Figure~\\CGref{fig:zetasurf} shows, on the grid of Figure~\\CGref{fig:Gsurf}, $-\\log_{10}$ of the modulus of the Riemann zeta function $\\zeta(s)$, which is not used anywhere else in this note. "
    "On that grid the computed values satisfy $|G(s)-A(s)-\\frac\\pi s\\cot(\\frac{\\pi s}2)\\zeta(s)|\\le1.2\\cdot10^{-11}$.",
    'figures: surfaces on the fine grid')
rep("At the $39\\times157$ grid points the computed values satisfy $|A(s)|\\ge0.072$", "At the $253\\times889$ grid points the computed values satisfy $|A(s)|\\ge0.072$", 'figures: grid of the zero map')
rep("At those six points the computed value of $|G-A|$ is below $10^{-11}$.", "At those six points the computed value of $|G-A|$ is at most $1.1\\cdot10^{-11}$.", 'figures: |G-A| at the six points')

# ------------------------------------------------------------------ exponential sums
EXP = r"""Of its $100$ entries, $52$ are negative.

The last three figures concern exponential sums over computed zeros. In the rectangle $-1.5\le\operatorname{Re}s\le3$, $0.2\le\operatorname{Im}s\le200$ a numerical search finds $n_G=79$ zeros $z^G_1,\dots,z^G_{n_G}$ of $G$, and the computed variation of the argument of $G$ along the boundary of this rectangle corresponds to $79$ zeros. Their real parts lie between $0.1036$ and $1.1274$, and the six with the smallest imaginary parts are the zeros of Table~\CGref{tab:rouche}. For $A$ the same search finds no zero with $-60\le\operatorname{Re}s\le201$ and $0.2\le\operatorname{Im}s\le200$, and exactly one zero in each interval $(2l,2l+2)$ with $1\le l\le99$. With $-2$ and $-1$ this gives $n_A=101$ real zeros $z^A_1,\dots,z^A_{n_A}$ of $A$ in $[-60,200]$. These counts are computed and not proved. For real $x$ put
\begin{equation}\label{eq:expsum}
\mathcal E_G(x)=\frac1{n_G}\sum_{b=1}^{n_G}e^{ix\operatorname{Im}z^G_b},\qquad\mathcal E_A(x)=\frac1{n_A}\sum_{b=1}^{n_A}e^{ixz^A_b}.
\end{equation}
For $G$ the frequencies are the imaginary parts of the zeros. For $A$ the zeros found are real, so their imaginary parts vanish, and the frequencies are the zeros themselves. Figure~\CGref{fig:expsum3d} shows the two curves $x\mapsto\mathcal E_G(x)$ and $x\mapsto\mathcal E_A(x)$ for $0\le x\le2\pi$, with $x$ on the vertical axis. Figure~\CGref{fig:expsumplane} shows the same curves in the complex plane, and the two sets of zeros with their centroids, which are $\frac1{n_G}\sum_bz^G_b=0.45923+119.21486\,i$ and $\frac1{n_A}\sum_bz^A_b=99.44250$. The means $\frac1{2\pi}\int_0^{2\pi}\mathcal E_G(x)\,dx=-0.00029+0.00188\,i$ and $\frac1{2\pi}\int_0^{2\pi}\mathcal E_A(x)\,dx=0.00151+0.00423\,i$ are the dashed lines of Figure~\CGref{fig:expsum3d}.

Figure~\CGref{fig:expsummod} shows the moduli. The mean of $|\mathcal E_G(x)|$ over $0\le x\le2\pi$ is $0.0847$. For the integers $2\le n\le31$, the value $|\mathcal E_G(\log n)|$ lies between $0.152$ and $0.254$ for the eleven primes, between $0.090$ and $0.189$ for the prime powers $4,8,9,16,25,27$, and between $0.020$ and $0.124$ for the other thirteen integers. At the eleven primes $p\le31$ the real part of $\mathcal E_G(\log p)$ is negative, between $-0.161$ and $-0.030$. The modulus $|\mathcal E_A(x)|$ equals $0.926$ at $x=\pi$ and $0.784$ at $x=2\pi$, and it is below $0.074$ for $0.3\le x\le2\pi-0.2$ with $|x-\pi|\ge0.2$. The zeros $z^A_b$ other than $-2$ and $-1$ lie in consecutive intervals of length $2$. All the statements of the last two paragraphs are numerical observations for the listed zeros."""
rep("Of its $100$ entries, $52$ are negative.", EXP, 'figures: exponential sums over computed zeros')

# ------------------------------------------------------------------ captions and new figure environments
rep("\\caption{$\\log_{10}|G(s)|$.}\\label{fig:Gsurf}",
    "\\caption{$-\\log_{10}|G(s)|$, clipped at $6$. The peaks are the six zeros of $G$ of Table~\\CGref{tab:rouche}.}\\label{fig:Gsurf}", 'caption fig:Gsurf')
rep("\\caption{$\\log_{10}|A(s)|$.}\\label{fig:Asurf}\n\\end{figure}\n",
    "\\caption{$-\\log_{10}|A(s)|$ on the rectangle of Figure~\\CGref{fig:Gsurf}.}\\label{fig:Asurf}\n\\end{figure}\n\n"
    "\\begin{figure}[ht]\n\\centering\n\\includegraphics[width=0.95\\textwidth]{fig_A_real_surface.png}\n"
    "\\caption{$-\\log_{10}|A(s)|$ near the real axis, clipped to $[-2,6]$. The peaks are real zeros of $A$ and the pits are its poles at $0,2,4,6,8$.}\\label{fig:Areal}\n\\end{figure}\n",
    'caption fig:Asurf; new figure fig:Areal')
rep("\\caption{$\\log_{10}|G(s)-A(s)|$.}\\label{fig:GAsurf}",
    "\\caption{$-\\log_{10}|G(s)-A(s)|$, clipped at $6$. The peaks are at the six points $\\frac12+it$ of Figure~\\CGref{fig:zeromap}.}\\label{fig:GAsurf}", 'caption fig:GAsurf')
rep("\\caption{$\\log_{10}|\\zeta(s)|$.}\\label{fig:zetasurf}",
    "\\caption{$-\\log_{10}|\\zeta(s)|$, clipped at $6$. The peaks are the first six nontrivial zeros of $\\zeta$.}\\label{fig:zetasurf}", 'caption fig:zetasurf')
rep("\\begin{figure}[ht]\n\\centering\n\\includegraphics[width=0.98\\textwidth]{fig_gram.png}",
    "\\begin{figure}[ht]\n\\centering\n\\includegraphics[width=0.55\\textwidth]{fig_expsum_3d.png}\n"
    "\\caption{The exponential sums $\\mathcal E_G(x)$ and $\\mathcal E_A(x)$ of \\CGeqref{eq:expsum} for $0\\le x\\le2\\pi$. The variable $x$ is the vertical axis. The dashed lines are the means of the two curves.}\\label{fig:expsum3d}\n\\end{figure}\n\n"
    "\\begin{figure}[ht]\n\\centering\n\\includegraphics[width=0.98\\textwidth]{fig_expsum_plane.png}\n"
    "\\caption{Left: the curves $\\mathcal E_G$ and $\\mathcal E_A$ in the complex plane. Right: the $79$ computed zeros of $G$ and the $101$ computed real zeros of $A$, with their centroids.}\\label{fig:expsumplane}\n\\end{figure}\n\n"
    "\\begin{figure}[ht]\n\\centering\n\\includegraphics[width=0.95\\textwidth]{fig_expsum_modulus.png}\n"
    "\\caption{Top: $|\\mathcal E_G(x)|$ for $0.3\\le x\\le4.2$, with vertical lines at $x=\\log n$ for the prime powers $n\\le66$. Bottom: $|\\mathcal E_G(x)|$ and $|\\mathcal E_A(x)|$ for $0\\le x\\le2\\pi$.}\\label{fig:expsummod}\n\\end{figure}\n\n"
    "\\begin{figure}[ht]\n\\centering\n\\includegraphics[width=0.98\\textwidth]{fig_gram.png}",
    'new figures: exponential sums')

# ------------------------------------------------------------------ tooltips
tips = {}
for m in re.finditer(r'\\begin\{equation\}\\label\{([^}]+)\}(.*?)\\end\{equation\}', body, re.S):
    tips[m.group(1)] = 'Equation: ' + detex(m.group(2))
for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition)\}\[(.*?)\]\\label\{([^}]+)\}(.*?)\\end\{\1\}', body, re.S):
    tips[m.group(3)] = m.group(1).capitalize() + ' - ' + detex(m.group(2)) + ': ' + detex(m.group(4), 260)
for m in re.finditer(r'\\caption\{(.*?)\}\\label\{([^}]+)\}', body, re.S):
    tips[m.group(2)] = ('Table: ' if m.group(2).startswith('tab') else 'Figure: ') + detex(m.group(1))


def clean(s):
    return s.replace(' in t\\_', ' int\\_').replace('in t\\_', 'int\\_').replace('=()frac', '=frac')


new_labels = ['prop:A', 'eq:Aseries', 'eq:Afactor', 'eq:logsinc', 'eq:Aterm', 'eq:Aparts', 'eq:expsum',
              'fig:Areal', 'fig:expsum3d', 'fig:expsumplane', 'fig:expsummod']
changed = ['fig:Gsurf', 'fig:Asurf', 'fig:GAsurf', 'fig:zetasurf']
lines = pre.split('\n')
n_changed = 0
for k, ln in enumerate(lines):
    for lab in changed:
        if ln.startswith('\\expandafter\\gdef\\csname CGTip@%s\\endcsname{' % lab):
            lines[k] = '\\expandafter\\gdef\\csname CGTip@%s\\endcsname{%s}' % (lab, clean(tips[lab]))
            n_changed += 1
assert n_changed == len(changed)
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
print('edits in the body: %d; tooltips rewritten: %d, added: %d; labels: %d' % (len(log), n_changed, len(new_labels), len(labels)))
