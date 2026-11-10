#!/usr/bin/env python3
"""Castor_Pollux_I_v3.tex -> Castor_Pollux_I_v4.tex: the surfaces are drawn on a linear scale with the vertical axis inverted.
Every edit is an exact replacement that must match exactly once; nothing else changes.
Usage: python3 make_v4.py V3.tex V4.tex BUILD.py"""
import re
import sys

src, dst, build = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src, encoding='utf-8').read()
head, sep, tail = t.partition('\n\\end{document}\n')
pre, bd, body = head.partition('\n\\begin{document}\n')
assert sep and bd
bsrc = open(build, encoding='utf-8').read()
exec(bsrc[bsrc.index('def detex'):bsrc.index('tips={}')])
log = []


def rep(old, new, where):
    global body
    assert body.count(old) == 1, (where, body.count(old), old[:70])
    body = body.replace(old, new)
    log.append(where)


rep(r"show $-\log_{10}$ of the moduli of $G$, $A$ and $G-A$ on the rectangle $0.05\le\operatorname{Re}s\le1.95$, $1\le\operatorname{Im}s\le40$, so that a zero is a peak. ",
    r"show the moduli of $G$, $A$ and $G-A$ on the rectangle $0.05\le\operatorname{Re}s\le1.95$, $1\le\operatorname{Im}s\le40$, on a linear scale. "
    r"The vertical axis is inverted, with the value $0$ at the top, so that a zero is a peak whose tip is at $0$, where the red points are. ", 'surfaces: linear scale, inverted axis')
rep(r"The plotted values are clipped at $6$, that is, where the modulus is below $10^{-6}$. ",
    r"In Figure~\CGref{fig:GAsurf} the values above $0.6$ are clipped. ", 'surfaces: clipping')
rep(r"On this rectangle $A$ has no peak. Figure~\CGref{fig:Areal} shows $-\log_{10}|A(s)|$ for $-3.5\le\operatorname{Re}s\le9.5$ and $|\operatorname{Im}s|\le2$, computed from \CGeqref{eq:Aseries}. ",
    r"On this rectangle the surface of $|A|$ does not reach $0$. Figure~\CGref{fig:Areal} shows $|A(s)|$ in the same way for $-3.5\le\operatorname{Re}s\le9.5$ and $|\operatorname{Im}s|\le2$, computed from \CGeqref{eq:Aseries} and clipped above $1.5$. ",
    'surfaces: A near the real axis')
rep(r"shows, on the grid of Figure~\CGref{fig:Gsurf}, $-\log_{10}$ of the modulus of the Riemann zeta function $\zeta(s)$, which",
    r"shows in the same way, on the grid of Figure~\CGref{fig:Gsurf}, the modulus of the Riemann zeta function $\zeta(s)$, clipped above $1.5$, which", 'surfaces: zeta')
rep(r"\caption{$-\log_{10}|G(s)|$, clipped at $6$. The peaks are the six zeros of $G$ of Table~\CGref{tab:rouche}.}\label{fig:Gsurf}",
    r"\caption{$|G(s)|$ on a linear scale, with the vertical axis inverted. The red points, at the value $0$, are the six zeros of $G$ of Table~\CGref{tab:rouche}.}\label{fig:Gsurf}", 'caption fig:Gsurf')
rep(r"\caption{$-\log_{10}|A(s)|$ on the rectangle of Figure~\CGref{fig:Gsurf}.}\label{fig:Asurf}",
    r"\caption{$|A(s)|$ on the rectangle of Figure~\CGref{fig:Gsurf}, with the vertical axis inverted.}\label{fig:Asurf}", 'caption fig:Asurf')
rep(r"\caption{$-\log_{10}|A(s)|$ near the real axis, clipped to $[-2,6]$. The peaks are real zeros of $A$ and the pits are its poles at $0,2,4,6,8$.}\label{fig:Areal}",
    r"\caption{$|A(s)|$ near the real axis, clipped above $1.5$, with the vertical axis inverted. The red points, at the value $0$, are real zeros of $A$. The pits are its poles at $0,2,4,6,8$.}\label{fig:Areal}", 'caption fig:Areal')
rep(r"\caption{$-\log_{10}|G(s)-A(s)|$, clipped at $6$. The peaks are at the six points $\frac12+it$ of Figure~\CGref{fig:zeromap}.}\label{fig:GAsurf}",
    r"\caption{$|G(s)-A(s)|$, clipped above $0.6$, with the vertical axis inverted. The red points, at the value $0$, are the six points $\frac12+it$ of Figure~\CGref{fig:zeromap}.}\label{fig:GAsurf}", 'caption fig:GAsurf')
rep(r"\caption{$-\log_{10}|\zeta(s)|$, clipped at $6$. The peaks are the first six nontrivial zeros of $\zeta$.}\label{fig:zetasurf}",
    r"\caption{$|\zeta(s)|$, clipped above $1.5$, with the vertical axis inverted. The red points, at the value $0$, are the first six nontrivial zeros of $\zeta$.}\label{fig:zetasurf}", 'caption fig:zetasurf')

tips = {}
for m in re.finditer(r'\\caption\{(.*?)\}\\label\{([^}]+)\}', body, re.S):
    tips[m.group(2)] = 'Figure: ' + detex(m.group(1))
changed = ['fig:Gsurf', 'fig:Asurf', 'fig:Areal', 'fig:GAsurf', 'fig:zetasurf']
lines = pre.split('\n')
n = 0
for k, ln in enumerate(lines):
    for lab in changed:
        if ln.startswith('\\expandafter\\gdef\\csname CGTip@%s\\endcsname{' % lab):
            lines[k] = '\\expandafter\\gdef\\csname CGTip@%s\\endcsname{%s}' % (lab, tips[lab]); n += 1
assert n == len(changed)
pre = '\n'.join(lines)
assert 'log_{10}' not in body.split('\\section{Figures}')[1].replace('log10', '')
open(dst, 'w', encoding='utf-8').write(pre + bd + body + sep + tail)
for w in log:
    print('  1  ' + w)
print('edits in the body: %d; tooltips rewritten: %d' % (len(log), n))
