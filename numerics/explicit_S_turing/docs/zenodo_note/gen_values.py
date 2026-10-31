# Generates generated_values.tex (macros with the certified constants, breakpoints and gaps, computed in exact rational
# arithmetic), generated_linetable.tex (rows of Table tab:lines) and generated_datatables.tex (Appendix A), from the
# certified summaries and the output of gen_appendix.py.
import json, os, re, math
from fractions import Fraction as Fr
FAM = '../../family/'
LINES = [('L5', 'Five'), ('L20', 'Twenty'), ('L60', 'Sixty'), ('L150', 'OneFifty'), ('C400', 'FourH'), ('D6000', 'B')]
NAMES = {'L5': '\\ell_{5}', 'L20': '\\ell_{20}', 'L60': '\\ell_{60}', 'L150': '\\ell_{150}', 'C400': '\\ell_{400}', 'D6000': '\\ell_{6000}'}
rows = []; macros = []
for tag, mac in LINES:
    s = json.load(open(FAM+'line_%s/summary_pp.json' % tag)); sol = json.load(open(FAM+'line_%s/sol.json' % tag))
    cz = s['Czeta_pp_upper']; supN = s.get('Fsup_N', s.get('Fsup_upper')); supS = float(json.load(open(FAM+'line_%s/sol_elemS.json' % tag))['Fsup_upper'])
    A1 = s['A1']; A3N = s['A3_N']; A3S = s['A3_S']
    # consistency checks (rounding up to 3 decimals)
    import math
    assert float(A3N) == math.ceil((cz+supN)*1000-1e-9)/1000 or float(A3N) >= cz+supN, (tag, A3N, cz+supN)
    assert float(A3S) >= cz+supS and float(A3S)-(cz+supS) < 1e-3+1e-9, (tag, A3S, cz+supS)
    assert float(A1) >= sol['C1'] and float(A1)-sol['C1'] < 1e-5
    rows.append((tag, sol['d'], max(j for _, j in sol['B']), A1, cz, supN, A3N, supS, A3S))
    for k, v in [('Aone', A1), ('AthreeN', A3N), ('AthreeS', A3S)]: macros.append('\\newcommand{\\Line%s%s}{%s}' % (mac, k, v))
with open('generated_linetable.tex', 'w') as f:
    for tag, d, m, A1, cz, supN, A3N, supS, A3S in rows:
        up = lambda x: math.ceil(x*1e8)/1e8
        f.write('$%s$ & $%s$ & $%d$ & $%s$ & $%.8f$ & $%.8f$ & $%s$ & $%.8f$ & $%s$\\\\\n' % (NAMES[tag], ('%g' % d), m, A1, up(cz), up(supN), A3N, up(supS), A3S))
# envelope breakpoints and gaps, exact
mine = [(Fr(A1), Fr(A3N)) for tag, d, m, A1, cz, supN, A3N, supS, A3S in rows]
def env(lines, L): return min(a*L+b for a, b in lines)
def breakpoints(lines):
    pts = set([Fr(0)])
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            (a1, b1), (a2, b2) = lines[i], lines[j]
            if a1 != a2:
                L = (b2-b1)/(a1-a2)
                if L > 0: pts.add(L)
    return sorted(pts)
# active intervals of my lines
bps = breakpoints(mine); act = []
for i in range(len(bps)):
    L = bps[i]; Lr = bps[i+1] if i+1 < len(bps) else bps[i]+1
    mid = (L+Lr)/2
    k = min(range(len(mine)), key=lambda k: mine[k][0]*mid+mine[k][1]); act.append((L, k))
# merge
segs = []
for L, k in act:
    if segs and segs[-1][1] == k: continue
    segs.append((L, k))
print('active:', [(float(L), rows[k][0]) for L, k in segs])
assert [k for L, k in segs] == list(range(len(mine))), 'unexpected envelope order'
brk = [L for L, k in segs][1:]
for nm, L in zip(['A', 'B', 'C', 'D', 'E'], brk): macros.append('\\newcommand{\\LineBreak%s}{%.1f}' % (nm, float(L)))
BW = [(Fr('0.0946'), Fr('5.746')), (Fr('0.097'), Fr('4.954'))]
AMB = [(Fr('0.097'), Fr('4.807')), (Fr('0.1'), Fr('4.140')), (Fr('0.12'), Fr('2.830')), (Fr('0.14'), Fr('2.306')), (Fr('0.16'), Fr('2.027')), (Fr('0.18'), Fr('1.847')), (Fr('0.2'), Fr('1.722'))]
import math
for nm, other in [('BW', BW), ('Amb', AMB)]:
    assert min(a for a, b in other) > min(a for a, b in mine)
    pts = sorted(set(breakpoints(mine)+breakpoints(other)+[Fr(0)]))
    gaps = [(env(other, L)-env(mine, L), L) for L in pts]
    g, L = min(gaps)
    print(nm, 'min gap', float(g), 'at L =', float(L))
    macros.append('\\newcommand{\\Gap%s}{%.3f}' % (nm, math.floor(float(g)*1000)/1000))
    macros.append('\\newcommand{\\Gap%sat}{%.2f}' % (nm, float(L)))
# hybrid values and box counts
vals = open('generated_tables.tex').read()
for line in vals.splitlines():
    if line.startswith('\\newcommand'): macros.append(line)
cert = open('../../hybrid_asymptotic/cert_m10P.txt').read()
pos = re.search(r't in \(0,T1\]: certified, boxes (\d+)', cert).group(1); neg = re.search(r't in \[-T1,0\): certified, boxes (\d+)', cert).group(1); tail = re.search(r'\|t\|>=T1: certified, boxes (\d+)', cert).group(1)
f3 = lambda n: '{:,}'.format(int(n)).replace(',', '\\,')
macros += ['\\newcommand{\\HybBoxesPos}{%s}' % f3(pos), '\\newcommand{\\HybBoxesNeg}{%s}' % f3(neg), '\\newcommand{\\HybBoxesTail}{%s}' % f3(tail)]
assert 'all certified' in cert
open('generated_values.tex', 'w').write('\n'.join(macros)+'\n')
# data tables for Appendix A
T = open('generated_tables.tex').read()
parts = re.split(r'%%%%(\w+)\n', T)
sec = {parts[i]: parts[i+1] for i in range(1, len(parts), 2)}
head = parts[0].split('\n', 1)[1]  # hybrid kernel table (after comment line)
out = []
out.append('\\begin{table}[ht]\\centering\\small\n'+head+'\\caption{Coefficients $c_\\iota$ of the hybrid kernel ($d=\\frac9{10}$, $m=10$), to twelve significant digits; the exact binary values are in Appendix~\\ref{app:data}.}\\label{tab:hybrid_kernel}\\end{table}\n')
out.append('\\small\n\\begin{center}\n'+sec['TAB_HYBRID_DISCS']+'\\end{center}\n\\begin{table}[ht]\\caption{The $85$ disc data $(c_k,R_k,v_k)$ (rational, as used in the certificate), the weights $\\kappa_k$ (ten significant digits; exact binary values in Appendix~\\ref{app:data}), $J_k=J(\\mathfrak e_{\\rm P};c_k,R_k)$ and the contributions $\\kappa_kJ_k/\\pi$ to $C_{\\rm H}$. The centres include $\\log3$ and $\\log5$ rounded to denominators $\\le10^4$.}\\label{tab:hybrid_discs}\\end{table}\n')
out.append('\\begin{center}\n'+sec['TAB_NODES']+'\\end{center}\n\\begin{table}[ht]\\caption{The vertices $(\\varsigma_i,e_i)$ of the profile $\\mathfrak e_{\\rm P}$ of Lemma~\\ref{lem:profile}, and the source of the bound $\\mu(\\varsigma_i)\\le e_i$. The Heath-Brown vertices $n=10,\\dots,398$ are omitted from the table; they are generated by \\texttt{profile\\_published.py} (Appendix~\\ref{app:profile}).}\\label{tab:nodes}\\end{table}\n')
for tag, mac in LINES:
    key = 'TAB_line'+{'L5': '5', 'L20': '20', 'L60': '60', 'L150': '150', 'C400': '400', 'D6000': '6000'}[tag]
    d = [r for r in rows if r[0] == tag][0][1]; m = [r for r in rows if r[0] == tag][0][2]
    out.append('\\begin{table}[ht]\\centering\\small\n'+sec[key]+'\\caption{Coefficients of the kernel of the line $%s$ ($d=%g$, $m=%d$), to twelve significant digits.}\\label{tab:kernel_%s}\\end{table}\n' % (NAMES[tag], d, m, tag))
open('generated_datatables.tex', 'w').write('\n'.join(out))
print('ok')
