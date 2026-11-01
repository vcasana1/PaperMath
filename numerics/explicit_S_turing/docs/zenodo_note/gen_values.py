# Build script of the note (not part of the article's programs). Generates, in exact rational / decimal arithmetic:
#   generated_values.tex     macros \Line<name>Aone, \Line<name>AthreeN, \Line<name>AthreeS (the certified constants), the
#                            envelope breakpoints \LineBreak{A..E} (decimal, truncated) and ...frac (exact), the minimal gaps
#                            \GapBW, \GapAmb (truncated) with their positions, plus every macro of generated_tables.tex
#   generated_linetable.tex  rows of the table of the six lines
#   generated_datatables.tex the data tables of Appendix A
import json, math
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_CEILING, localcontext
FAM = '../../family/'
LINES = [('L5', 'Five'), ('L20', 'Twenty'), ('L60', 'Sixty'), ('L150', 'OneFifty'), ('C400', 'FourH'), ('D6000', 'B')]
NAMES = {'L5': '\\ell_{5}', 'L20': '\\ell_{20}', 'L60': '\\ell_{60}', 'L150': '\\ell_{150}', 'C400': '\\ell_{400}', 'D6000': '\\ell_{6000}'}
TABKEY = {'L5': 'line5', 'L20': 'line20', 'L60': 'line60', 'L150': 'line150', 'C400': 'line400', 'D6000': 'line6000'}
def ceil_dec(x, places): return x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_CEILING)
rows = []; macros = []
with localcontext() as dc:
    dc.prec = 60
    for tag, mac in LINES:
        s = json.load(open(FAM+'line_%s/summary_pp.json' % tag)); sol = json.load(open(FAM+'line_%s/sol.json' % tag))
        cz = Decimal(s['Czeta_pp_upper']); supN = Decimal(s['Fsup_N']); supS = Decimal(s['Fsup_S'])
        A1 = Decimal(s['A1']); A3N = Decimal(s['A3_N']); A3S = Decimal(s['A3_S'])
        # the certified decimals are upper bounds; the constants of the theorem are their sums rounded upwards
        assert A3N == ceil_dec(cz+supN, 3) and A3S == ceil_dec(cz+supS, 3), tag
        assert A1 >= Decimal(repr(sol['C1'])) and A1-Decimal(repr(sol['C1'])) < Decimal('0.00001'), tag
        # and the kernel certificate prints C_1 = c_R1/(2 pi) rounded upwards to 12 digits, which must not exceed A1
        cert = open(FAM+'line_%s/cert_kernel.txt' % tag).read().strip().splitlines()[-1]
        C1cert = Decimal(cert.split('C <')[1].split()[0]); assert C1cert <= A1, (tag, C1cert, A1)
        rows.append((tag, sol['d'], max(j for _, j in sol['B']), A1, cz, supN, A3N, supS, A3S))
        for k, v in [('Aone', A1), ('AthreeN', A3N), ('AthreeS', A3S)]: macros.append('\\newcommand{\\Line%s%s}{%s}' % (mac, k, v))
    with open('generated_linetable.tex', 'w') as f:
        for tag, d, m, A1, cz, supN, A3N, supS, A3S in rows:
            f.write('$%s$ & $%s$ & $%d$ & $%s$ & $%s$ & $%s$ & $%s$ & $%s$ & $%s$\\\\\n' % (NAMES[tag], ('%g' % d), m, A1, ceil_dec(cz, 8), ceil_dec(supN, 8), A3N, ceil_dec(supS, 8), A3S))
# envelope breakpoints and gaps, exact
mine = [(Fr(str(A1)), Fr(str(A3N))) for tag, d, m, A1, cz, supN, A3N, supS, A3S in rows]
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
bps = breakpoints(mine); act = []
for i in range(len(bps)):
    L = bps[i]; Lr = bps[i+1] if i+1 < len(bps) else bps[i]+1
    mid = (L+Lr)/2
    act.append((L, min(range(len(mine)), key=lambda k: mine[k][0]*mid+mine[k][1])))
segs = []
for L, k in act:
    if segs and segs[-1][1] == k: continue
    segs.append((L, k))
print('active:', [(float(L), rows[k][0]) for L, k in segs])
assert [k for L, k in segs] == list(range(len(mine))), 'unexpected envelope order'
brk = [L for L, k in segs][1:]
for nm, L in zip(['A', 'B', 'C', 'D', 'E'], brk):
    macros.append('\\newcommand{\\LineBreak%s}{%s}' % (nm, ('%.6f' % (math.floor(float(L)*1e6)/1e6))))
    macros.append('\\newcommand{\\LineBreak%sfrac}{\\tfrac{%d}{%d}}' % (nm, L.numerator, L.denominator))
BW = [(Fr('0.0946'), Fr('5.746')), (Fr('0.097'), Fr('4.954'))]
AMB = [(Fr('0.097'), Fr('4.807')), (Fr('0.1'), Fr('4.140')), (Fr('0.12'), Fr('2.830')), (Fr('0.14'), Fr('2.306')), (Fr('0.16'), Fr('2.027')), (Fr('0.18'), Fr('1.847')), (Fr('0.2'), Fr('1.722'))]
for nm, other in [('BW', BW), ('Amb', AMB)]:
    assert min(a for a, b in other) > min(a for a, b in mine)
    pts = sorted(set(breakpoints(mine)+breakpoints(other)+[Fr(0)]))
    g, L = min((env(other, L)-env(mine, L), L) for L in pts)
    assert g > 0
    print(nm, 'min gap', float(g), 'at L =', float(L))
    macros.append('\\newcommand{\\Gap%s}{%.3f}' % (nm, math.floor(g*1000)/1000))
    macros.append('\\newcommand{\\Gap%sat}{%.2f}' % (nm, float(L)))
# single-line comparisons of Corollary 2.2 (checked exactly)
a400, b400 = mine[4]; a6000, b6000 = mine[5]
assert a400 < Fr('0.0946') and b400 < Fr('5.746') and a6000 < Fr('0.0946') and b6000 < Fr('5.746')
assert b400 > Fr('4.954') and b6000 > Fr('4.954')
macros.append('\\newcommand{\\CrossFourH}{%.3f}' % (math.floor(float((b400-Fr('4.954'))/(Fr('0.097')-a400))*1000)/1000))
macros.append('\\newcommand{\\CrossB}{%.3f}' % (math.floor(float((b6000-Fr('4.954'))/(Fr('0.097')-a6000))*1000)/1000))
# macros of generated_tables.tex (hybrid values, box counts, times, kernel-only optima)
for line in open('generated_tables.tex').read().splitlines():
    if line.startswith('\\newcommand'): macros.append(line)
open('generated_values.tex', 'w').write('\n'.join(macros)+'\n')
# data tables for Appendix A
T = open('generated_tables.tex').read()
parts = T.split('%%%%')
head = parts[0].split('\n', 1)[1]
sec = {}
for p in parts[1:]:
    name, body = p.split('\n', 1); sec[name] = body
out = ['\\begin{table}[ht]\\centering\\small\n'+head+'\\caption{Coefficients $c_\\iota$ of the hybrid kernel ($d=\\frac9{10}$, $m=10$), to twelve significant digits; the full-precision decimal strings of the binary coefficients are in Appendix~\\ref{app:data}.}\\label{tab:hybrid_kernel}\\end{table}\n',
       '\\small\n\\begin{center}\n'+sec['TAB_HYBRID_DISCS']+'\\end{center}\n', '\\begin{center}\n'+sec['TAB_NODES']+'\\end{center}\n\\normalsize\n']
for tag, mac in LINES:
    d = [r for r in rows if r[0] == tag][0][1]; m = [r for r in rows if r[0] == tag][0][2]
    out.append('\\begin{table}[ht]\\centering\\small\n'+sec['TAB_'+TABKEY[tag]]+'\\caption{Coefficients of the kernel of the line $%s$ ($d=%g$, $m=%d$), to twelve significant digits.}\\label{tab:kernel_%s}\\end{table}\n' % (NAMES[tag], d, m, tag))
open('generated_datatables.tex', 'w').write('\n'.join(out))
print('ok')
