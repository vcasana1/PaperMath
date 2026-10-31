# Generates the data tables and the appendices (programs, certificates, exact data) of the Zenodo note from the
# files of numerics/explicit_S_turing. Output: generated_tables.tex, generated_appendix.tex (included by the main file).
import json, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, '../../hybrid_asymptotic')
from flint import arb, acb, ctx
ctx.prec = 256
R_ = '../../'
HYB = R_+'hybrid_asymptotic/'; FAM = R_+'family/'
def A(q): return arb(q.numerator)/q.denominator if isinstance(q, Fr) else arb(q)
def esc(s): return s.replace('\\', '\\textbackslash{}').replace('_', '\\_').replace('%', '\\%').replace('&', '\\&').replace('#', '\\#').replace('{', '\\{').replace('}', '\\}')

# ---------- hybrid data ----------
sol = json.load(open(HYB+'hyb_m10_P.json'))
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(x) for x in sol['B']]; c = [Fr(x) for x in sol['c']]
discs = [(Fr(cc).limit_denominator(10**4), Fr(R).limit_denominator(10**4), Fr(v).limit_denominator(10**4)) for cc, R, v in sol['discs']]
discs = [(cc, min(R, cc-Fr(1, 2)), v) for cc, R, v in discs]
kap = [Fr(x) for x in sol['kappa']]
exec(open(HYB+'certify_hybrid.py').read().split("if __name__=='__main__':")[0].split("sol=json.load")[0])  # helpers A, box
from profile_published import nodes_published
nodes = nodes_published()
PI = arb.pi()
def Jexact(nodes, cc, R):
    tot = arb(0); ccA = A(cc); RA = A(R); lo, hi = cc-R, min(cc+R, Fr(1))
    for (p, ep), (q, eq) in zip(nodes, nodes[1:]):
        a, bq = max(p, lo), min(q, hi)
        if a >= bq: continue
        Bs = (eq-ep)/(q-p); As = ep-Bs*p
        tha = A((a-cc)/R).acos(); thb = A((bq-cc)/R).acos()
        tot += (A(As)+A(Bs)*ccA)*(tha-thb)+A(Bs)*RA*(tha.sin()-thb.sin())
    return tot/PI
J = [Jexact(nodes, cc, R) for cc, R, v in discs]
def fr(x):  # fraction -> tex
    return '%d' % x.numerator if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)
with open('generated_tables.tex', 'w') as f:
    # kernel coefficients, hybrid
    f.write('% kernel coefficients of the hybrid (d = 9/10), 12 significant digits; exact binary values in Appendix D\n')
    f.write('\\begin{tabular}{@{}cr@{\\quad}cr@{}}\\toprule $\\iota$ & $c_\\iota$ & $\\iota$ & $c_\\iota$\\\\\\midrule\n')
    Rs = [(b, cc) for b, cc in zip(B, c) if b[0] == 'R']; Is = [(b, cc) for b, cc in zip(B, c) if b[0] == 'I']
    for i in range(10):
        l = '$(\\mathrm R,%d)$ & $%.12g$' % (Rs[i][0][1], float(Rs[i][1]))
        if i < 9: l += ' & $(\\mathrm I,%d)$ & $%.12g$' % (Is[i][0][1], float(Is[i][1]))
        else: l += ' & & '
        f.write(l+'\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
    f.write('%%%%TAB_HYBRID_DISCS\n')
    f.write('\\begin{longtable}{@{}rrrrrrr@{}}\\toprule $k$ & $c_k$ & $R_k$ & $v_k$ & $\\kappa_k$ & $J_k$ & $\\kappa_kJ_k/\\pi$\\\\\\midrule\\endfirsthead\n\\toprule $k$ & $c_k$ & $R_k$ & $v_k$ & $\\kappa_k$ & $J_k$ & $\\kappa_kJ_k/\\pi$\\\\\\midrule\\endhead\n\\bottomrule\\endfoot\n')
    tot = arb(0)
    for k, ((cc, R, v), kk, jj) in enumerate(zip(discs, kap, J), 1):
        tot += A(kk)*jj/PI
        f.write('%d & $%s$ & $%s$ & $%s$ & $%.10g$ & $%s$ & $%s$\\\\\n' % (k, fr(cc), fr(R), fr(v), float(kk), jj.str(8, radius=False), (A(kk)*jj/PI).str(6, radius=False)))
    f.write('\\midrule \\multicolumn{6}{r}{$\\frac1\\pi\\sum_k\\kappa_kJ_k=$} & $%s$\\\\\n' % tot.str(10, radius=False))
    f.write('\\end{longtable}\n')
    CH = A(c[B.index(('R', 1))])/(2*PI)+tot
    f.write('%%%%VALUES\n')
    f.write('\\newcommand{\\CHval}{%s}\n' % CH.str(14, radius=False))
    f.write('\\newcommand{\\CHup}{%s}\n' % CH.upper().str(12, radius=False))
    f.write('\\newcommand{\\CHball}{%s}\n' % CH.str(8))
    f.write('\\newcommand{\\CHkernel}{%s}\n' % (A(c[0])/(2*PI)).str(12, radius=False))
    f.write('\\newcommand{\\CHdiscs}{%s}\n' % tot.str(10, radius=False))
    f.write('\\newcommand{\\Kfive}{%s}\n' % ((2*(A(d)+A(Fr(1, 2)))**5+2*A(d)**5+(2*A(d)+A(Fr(1, 2)))**5+(2*A(d))**5)/5).str(8, radius=False))
    # profile nodes
    f.write('%%%%TAB_NODES\n')
    f.write('\\begin{longtable}{@{}rllr@{}}\\toprule $i$ & $\\varsigma_i$ & $e_i$ & source\\\\\\midrule\\endfirsthead\n\\toprule $i$ & $\\varsigma_i$ & $e_i$ & source\\\\\\midrule\\endhead\n\\bottomrule\\endfoot\n')
    from profile_published import TY, PAIRS, hb
    tyb = set([lo for lo, hi, a, b in TY]+[hi for lo, hi, a, b in TY]); pr = set(l-k for k, l in PAIRS); hbn = {hb(n)[0]: n for n in range(6, 400)}
    for i, (s, e) in enumerate(nodes):
        if s == Fr(1, 2): src = 'Bourgain \\cite[Thm.~5]{Bourgain2017}'
        elif s in hbn: src = 'Heath-Brown \\cite[Thm.~2]{HeathBrown2017}, $n=%d$' % hbn[s]
        elif s in pr: src = 'Tao--Trudgian--Yang \\cite[Thm.~20, Lemma~23]{TaoTrudgianYang2025}'
        elif s in tyb: src = 'Trudgian--Yang \\cite[Thm.~2.4]{TrudgianYang2024}'
        elif s == 1: src = '$\\zeta(1+it)\\ll\\log t$ \\cite[Thm.~3.5]{Titchmarsh1986}'
        else: src = '?'
        if i < len(nodes)-2 and hbn.get(s, 0) > 9:
            if hbn.get(s) == 10: f.write('\\multicolumn{4}{c}{$\\vdots$ \\quad(Heath-Brown nodes $n=10,\\dots,398$)\\quad $\\vdots$}\\\\\n')
            continue
        f.write('%d & $%s$ & $%s$ & %s\\\\\n' % (i, fr(s), fr(e), src))
    f.write('\\end{longtable}\n')
    # line coefficients
    for tag, name in [('L5', 'line5'), ('L20', 'line20'), ('L60', 'line60'), ('L150', 'line150'), ('C400', 'line400'), ('D6000', 'line6000')]:
        p = FAM+'line_%s/sol.json' % tag
        if not os.path.exists(FAM+'line_%s/summary_pp.json' % tag): continue
        s = json.load(open(p)); Bl = [tuple(x) for x in s['B']]; cl = s['c']
        f.write('%%%%%%%%TAB_%s\n' % name)
        f.write('\\begin{tabular}{@{}cr@{\\quad}cr@{}}\\toprule $\\iota$ & $c_\\iota$ & $\\iota$ & $c_\\iota$\\\\\\midrule\n')
        Rs = [(b, cc) for b, cc in zip(Bl, cl) if b[0] == 'R']; Is = [(b, cc) for b, cc in zip(Bl, cl) if b[0] == 'I']
        def g12(x):
            t = '%.12g' % x
            if 'e' in t:
                m_, e_ = t.split('e'); return '%s\\cdot10^{%d}' % (m_, int(e_))
            return t
        for i in range(len(Rs)):
            l = '$(\\mathrm R,%d)$ & $%s$' % (Rs[i][0][1], g12(Rs[i][1]))
            l += (' & $(\\mathrm I,%d)$ & $%s$' % (Is[i][0][1], g12(Is[i][1]))) if i < len(Is) else ' & & '
            f.write(l+'\\\\\n')
        f.write('\\bottomrule\\end{tabular}\n')
print('C_H =', CH.str(16))

# ---------- appendices: programs, certificates, data ----------
def verb(path, title, label=None):
    txt = open(path).read()
    out = '\\subsection*{%s}\n' % title
    if label: out += '\\label{%s}\n' % label
    out += '\\begin{lstlisting}\n'+txt+('\n' if not txt.endswith('\n') else '')+'\\end{lstlisting}\n'
    return out
with open('generated_appendix.tex', 'w') as f:
    f.write('\\section{Programs}\\label{app:code}\n')
    f.write('The programs are written in Python~3 and use \\texttt{python-flint} (Arb ball arithmetic \\cite{Johansson2017}, FLINT \\cite{FLINT}) at $256$ bits, \\texttt{numpy}, \\texttt{scipy} and \\texttt{cvxpy} with the solver Clarabel. The certification programs are those of Sections~\\ref{app:cert_hybrid}--\\ref{app:cert_elem}; the search programs that produced the coefficients are reproduced in Section~\\ref{app:search} for completeness, but no statement of this article depends on them. All files are in the repository cited in Section~\\ref{sec:methods}.\n')
    f.write(verb(HYB+'certify_hybrid.py', '\\texttt{certify\\_hybrid.py}: certification of the kernel inequality (with or without discs) and of $C_{\\rm H}$', 'app:cert_hybrid'))
    f.write(verb(HYB+'profile_published.py', '\\texttt{profile\\_published.py}: the nodes of the profile $\\mathfrak e_{\\rm P}$', 'app:profile'))
    f.write(verb(FAM+'cz_gen_pp.py', '\\texttt{cz\\_gen\\_pp.py}: certification of $C_\\zeta$ (per-prime phase maximum)', 'app:cert_cz'))
    f.write(verb(FAM+'elem_gen.py', '\\texttt{elem\\_gen.py}: certification of $\\sup F_u$, $\\sup F_\\ell$ (modes N and S)', 'app:cert_elem'))
    f.write(verb(FAM+'certify_line_pp.py', '\\texttt{certify\\_line\\_pp.py}: driver for one explicit line', 'app:cert_line'))
    f.write('\\subsection*{Search programs}\\label{app:search}\n')
    for fn, t in [(HYB+'lpm.py', 'lpm.py'), (HYB+'explore_discs.py', 'explore_discs.py'), (FAM+'opt_line.py', 'opt_line.py'), (FAM+'opt_line_pp.py', 'opt_line_pp.py')]:
        f.write(verb(fn, '\\texttt{%s}' % esc(t)))
    f.write('\\section{Outputs of the certification programs}\\label{app:cert}\n')
    f.write(verb(HYB+'cert_m10P.txt', 'Hybrid: \\texttt{certify\\_hybrid.py hyb\\_m10\\_P.json 40}', 'app:out_hybrid'))
    for tag, nm in [('L5', '$\\ell_{5}$'), ('L20', '$\\ell_{20}$'), ('L60', '$\\ell_{60}$'), ('L150', '$\\ell_{150}$'), ('C400', '$\\ell_{400}$'), ('D6000', '$\\ell_{6000}$')]:
        if not os.path.exists(FAM+'line_%s/summary_pp.json' % tag): continue
        for fn, t in [('cert_kernel.txt', 'kernel inequality'), ('cert_czeta_pp.txt', '$C_\\zeta$'), ('cert_elem.txt', 'elementary part, mode N'), ('cert_elem_S.txt', 'elementary part, mode S')]:
            f.write(verb(FAM+'line_%s/%s' % (tag, fn), 'Line %s: %s' % (nm, t)))
    f.write('\\section{Exact data}\\label{app:data}\n')
    f.write('The following files hold the coefficients as exact binary floating-point numbers (the decimal strings are the shortest that round-trip), the disc data before rounding to rationals (the certificate rounds $c_k,R_k,v_k$ to denominators $\\le10^4$ and then replaces $R_k$ by $\\min(R_k,c_k-\\frac12)$, as in \\texttt{certify\\_hybrid.py}), and the parameters $d$, $m$, $\\eta$.\n')
    def jverb(path, title):
        s = json.load(open(path)); txt = json.dumps(s, indent=1)
        return '\\subsection*{%s}\n\\begin{lstlisting}\n%s\n\\end{lstlisting}\n' % (title, txt)
    f.write(jverb(HYB+'hyb_m10_P.json', '\\texttt{hyb\\_m10\\_P.json} (hybrid)'))
    for tag, nm in [('L5', '$\\ell_{5}$'), ('L20', '$\\ell_{20}$'), ('L60', '$\\ell_{60}$'), ('L150', '$\\ell_{150}$'), ('C400', '$\\ell_{400}$'), ('D6000', '$\\ell_{6000}$')]:
        if os.path.exists(FAM+'line_%s/summary_pp.json' % tag): f.write(jverb(FAM+'line_%s/sol.json' % tag, '\\texttt{line\\_%s/sol.json} (line %s)' % (tag, nm)))
print('done')
