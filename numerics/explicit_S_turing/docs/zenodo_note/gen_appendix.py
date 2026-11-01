# Build script of the note (not part of the article's programs). Generates, from the files of numerics/explicit_S_turing:
#   generated_tables.tex    tables of the hybrid kernel, discs and profile nodes, kernel tables of the six lines, and the macros
#                           \CHval, \CHup, \CHball, \CHkernel, \CHdiscs, \Kfive and the certificate statistics (boxes, times)
#   generated_appendix.tex  the appendices: programs, outputs of the certification programs, exact data
import json, os, re, sys
from fractions import Fraction as Fr
R_ = '../../'; HYB = R_+'hybrid_asymptotic/'; FAM = R_+'family/'
sys.path.insert(0, HYB)
from flint import arb
from certutil import A, up_str, down_str, exact, sha256
from profile_published import nodes_published, TY, PAIRS, hb
PI = arb.pi()
LINES = [('L5', '$\\ell_{5}$', 'line5', 'Five'), ('L20', '$\\ell_{20}$', 'line20', 'Twenty'), ('L60', '$\\ell_{60}$', 'line60', 'Sixty'), ('L150', '$\\ell_{150}$', 'line150', 'OneFifty'), ('C400', '$\\ell_{400}$', 'line400', 'FourH'), ('D6000', '$\\ell_{6000}$', 'line6000', 'B')]
HYBJSON = 'hyb_m10_P.json'; HYBCERT = 'cert_m10P.txt'

def esc(s): return s.replace('\\', '\\textbackslash{}').replace('_', '\\_').replace('%', '\\%').replace('&', '\\&').replace('#', '\\#').replace('{', '\\{').replace('}', '\\}')
def gexp(t):   # 1.2e-5 -> 1.2\cdot10^{-5}
    t = t.strip()
    if 'e' in t:
        m_, e_ = t.split('e'); return '%s\\cdot10^{%d}' % (m_, int(e_))
    return t
def fr(x): return '%d' % x.numerator if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)
def g12(x): return gexp('%.12g' % x)
def f3(n): return '{:,}'.format(int(n)).replace(',', '\\,')

# ---------- hybrid data (same reading and rounding as certify_hybrid.py) ----------
sol = json.load(open(HYB+HYBJSON))
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(x) for x in sol['B']]; c = [Fr(x) for x in sol['c']]
discs = [(Fr(cc).limit_denominator(10**4), Fr(R).limit_denominator(10**4), Fr(v).limit_denominator(10**4)) for cc, R, v in sol['discs']]
discs = [(cc, min(R, cc-Fr(1, 2)), v) for cc, R, v in discs]
kap = [Fr(x) for x in sol['kappa']]
assert B[0] == ('R', 1) and len(c) == len(B) and len(kap) == len(discs)
nodes = nodes_published()
def Jexact(nodes, cc, R):   # as in certify_hybrid.py
    tot = arb(0); ccA = A(cc); RA = A(R); lo, hi = cc-R, min(cc+R, Fr(1))
    for (p, ep), (q, eq) in zip(nodes, nodes[1:]):
        a, bq = max(p, lo), min(q, hi)
        if a >= bq: continue
        Bs = (eq-ep)/(q-p); As = ep-Bs*p
        tha = A((a-cc)/R).acos(); thb = A((bq-cc)/R).acos()
        tot += (A(As)+A(Bs)*ccA)*(tha-thb)+A(Bs)*RA*(tha.sin()-thb.sin())
    return tot/PI
J = [Jexact(nodes, cc, R) for cc, R, v in discs]
cert = open(HYB+HYBCERT).read()
assert 'all certified' in cert
def check_provenance(certtext, folder):
    # every file named in the provenance lines of a certificate must be the file published here, byte for byte
    for name, h in re.findall(r'^(\S+) sha256 ([0-9a-f]{64})$', certtext, re.M):
        for cand in (folder+name, HYB+name, FAM+name):
            if os.path.exists(cand): break
        else: raise SystemExit('provenance: file %s not found' % name)
        assert sha256(cand) == h, 'provenance mismatch for %s (certificate %s)' % (name, folder)
check_provenance(cert, HYB)
for tag, nm, name, mac in LINES:
    for fn in ('cert_kernel.txt', 'cert_czeta_pp.txt', 'cert_elem.txt', 'cert_elem_S.txt'):
        check_provenance(open(FAM+'line_%s/%s' % (tag, fn)).read(), FAM+'line_%s/' % tag)

with open('generated_tables.tex', 'w') as f:
    # kernel coefficients of the hybrid
    f.write('% kernel coefficients of the hybrid, 12 significant digits; full-precision decimal strings of the binary coefficients in the data appendix\n')
    f.write('\\begin{tabular}{@{}cr@{\\quad}cr@{}}\\toprule $\\iota$ & $c_\\iota$ & $\\iota$ & $c_\\iota$\\\\\\midrule\n')
    Rs = [(b, cc) for b, cc in zip(B, c) if b[0] == 'R']; Is = [(b, cc) for b, cc in zip(B, c) if b[0] == 'I']
    for i in range(len(Rs)):
        l = '$(\\mathrm R,%d)$ & $%s$' % (Rs[i][0][1], g12(float(Rs[i][1])))
        l += (' & $(\\mathrm I,%d)$ & $%s$' % (Is[i][0][1], g12(float(Is[i][1])))) if i < len(Is) else ' & & '
        f.write(l+'\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
    # discs
    f.write('%%%%TAB_HYBRID_DISCS\n')
    f.write('\\begin{longtable}{@{}rrrrrrr@{}}\\caption{The $%d$ disc data $(c_k,R_k,v_k)$ (rational, as used in the certificate), the weights $\\kappa_k$ (ten significant digits; the full-precision decimal strings of the binary floating-point weights are in Appendix~\\ref{app:data}). The rationals $c_k,R_k,v_k$ are the data used in the certificate: a centre such as $\\log3$ in the search grid of Section~\\ref{subsec:optimisation} appears here as its rounding to denominator $\\le10^4$, not as a symbolic value, $J_k=J(\\mathfrak e_{\\rm P};c_k,R_k)$ and the contributions $\\kappa_kJ_k/\\pi$ to $C_{\\rm H}$.}\\label{tab:hybrid_discs}\\\\\n\\toprule $k$ & $c_k$ & $R_k$ & $v_k$ & $\\kappa_k$ & $J_k$ & $\\kappa_kJ_k/\\pi$\\\\\\midrule\\endfirsthead\n\\toprule $k$ & $c_k$ & $R_k$ & $v_k$ & $\\kappa_k$ & $J_k$ & $\\kappa_kJ_k/\\pi$\\\\\\midrule\\endhead\n\\bottomrule\\endfoot\n' % len(discs))
    tot = arb(0)
    for k, ((cc, R, v), kk, jj) in enumerate(zip(discs, kap, J), 1):
        tot += A(kk)*jj/PI
        f.write('%d & $%s$ & $%s$ & $%s$ & $%s$ & $%s$ & $%s$\\\\\n' % (k, fr(cc), fr(R), fr(v), gexp('%.10g' % float(kk)), gexp(jj.str(8, radius=False)), gexp((A(kk)*jj/PI).str(6, radius=False))))
    f.write('\\midrule \\multicolumn{6}{r}{$\\frac1\\pi\\sum_k\\kappa_kJ_k=$} & $%s$\\\\\n' % tot.str(10, radius=False))
    f.write('\\end{longtable}\n')
    CH = A(c[0])/(2*PI)+tot
    f.write('%%%%VALUES\n')
    # truncated (not rounded) decimal expansion: common prefix of the lower and upper bounds of the ball, 16 decimals
    lo_ = CH.lower().str(24, radius=False); hi_ = CH.upper().str(24, radius=False); trunc_ = lo_[:18]
    assert hi_.startswith(trunc_) and lo_.startswith(trunc_), (lo_, hi_)
    f.write('\\newcommand{\\CHval}{%s}\n' % trunc_)
    chup = up_str(CH, 12); f.write('\\newcommand{\\CHup}{%s}\n' % chup)
    assert ('C < '+chup) in cert, 'the certificate prints a different upper bound'
    lo20, up20 = down_str(CH, 20), up_str(CH, 20)
    assert ('[%s, %s]' % (lo20, up20)) in cert, 'the certificate prints a different enclosure of C_H'
    f.write('\\newcommand{\\CHball}{[%s,\\ %s]}\n' % (lo20, up20))
    f.write('\\newcommand{\\CHkernel}{%s}\n' % down_str(A(c[0])/(2*PI), 12))   # truncated (rounded down): the text appends dots
    f.write('\\newcommand{\\CHdiscs}{%s}\n' % down_str(tot, 12))
    f.write('\\newcommand{\\Kfive}{%s}\n' % ((2*(A(d)+A(Fr(1, 2)))**5+2*A(d)**5+(2*A(d)+A(Fr(1, 2)))**5+(2*A(d))**5)/5).str(8, radius=False))
    f.write('\\newcommand{\\HybNdiscs}{%d}\n' % len(discs))
    mx = max(R+abs(v) for cc, R, v in discs)                     # exact rational maximum of R_k+|v_k| over the certified disc data
    f.write('\\newcommand{\\HybMaxRv}{%s}\n' % ('\\tfrac{%d}{%d}' % (mx.numerator, mx.denominator) if mx.denominator != 1 else str(mx.numerator)))
    f.write('\\newcommand{\\HybMaxRvDec}{%s}\n' % format(float(mx), '.4g'))
    # certificate statistics: boxes and times
    def stats(txt):
        pos = re.search(r't in \(0,T1\]: certified, boxes (\d+)', txt).group(1); neg = re.search(r't in \[-T1,0\): certified, boxes (\d+)', txt).group(1)
        tail = re.search(r'\|t\|>=T1: certified, boxes (\d+)', txt).group(1); tm = re.search(r'time (\d+)s', txt).group(1)
        return pos, neg, tail, tm
    pos, neg, tail, tm = stats(cert)
    f.write('\\newcommand{\\HybBoxesPos}{%s}\n\\newcommand{\\HybBoxesNeg}{%s}\n\\newcommand{\\HybBoxesTail}{%s}\n\\newcommand{\\HybTime}{%s}\n' % (f3(pos), f3(neg), f3(tail), tm))
    czt = []; elt = []
    for tag, nm, name, mac in LINES:
        pos, neg, tail, tm = stats(open(FAM+'line_%s/cert_kernel.txt' % tag).read())
        tcz = int(re.search(r'time (\d+)s', open(FAM+'line_%s/cert_czeta_pp.txt' % tag).read()).group(1))
        tel = max(int(re.search(r'time (\d+)s', open(FAM+'line_%s/%s' % (tag, fn)).read()).group(1)) for fn in ('cert_elem.txt', 'cert_elem_S.txt'))
        czt.append(tcz); elt.append(tel)
        f.write('\\newcommand{\\line%sBoxesPos}{%s}\n\\newcommand{\\line%sBoxesNeg}{%s}\n\\newcommand{\\line%sBoxesTail}{%s}\n\\newcommand{\\line%sTime}{%s}\n' % (mac, f3(pos), mac, f3(neg), mac, f3(tail), mac, tm))
    f.write('\\newcommand{\\CzTimeMin}{%d}\n\\newcommand{\\CzTimeMax}{%d}\n\\newcommand{\\ElemTimeMin}{%d}\n\\newcommand{\\ElemTimeMax}{%d}\n' % (min(czt), max(czt), min(elt), max(elt)))
    # grid values of the hybrid linear programme quoted in the Methods section (search outputs, not certified)
    for log, mac in [('explore_B.log', 'HybGridB'), ('explore_P0.log', 'HybGridPzero'), ('explore_P.log', 'HybGridP')]:
        m_ = re.search(r'ndiscs=(\d+) C\(grid\)=([\d.]+) kernel=[\d.]+ worst violation=\S+ it=\d+ used=(\d+)', open(HYB+log).read())
        f.write('\\newcommand{\\%s}{%.5f}\n\\newcommand{\\%sUsed}{%s}\n\\newcommand{\\%sCand}{%s}\n' % (mac, float(m_.group(2)), mac, m_.group(3), mac, f3(m_.group(1))))
    # kernel-only optima for the Remark on the infimum
    ko = open(HYB+'kernel_only.txt').read()
    vals = {}
    # only runs whose cutting planes converged (residual violation on the fine grid below 1e-5) are quoted
    for m_, d_, kind, v, viol in re.findall(r'm=(\d+) d=([\d.]+) (all beta|constraint at beta=1/2 only) C1\(grid\)=([\d.]+) worst violation=(\S+)', ko):
        if float(viol) < 1e-5:
            key = (int(m_), kind == 'all beta'); vals[key] = min(vals.get(key, 9), float(v))
    for m_ in (4, 10, 20, 40):
        if (m_, True) in vals: f.write('\\newcommand{\\KernelOnly%s}{%.5f}\n' % ({4: 'Four', 10: 'Ten', 20: 'Twenty', 40: 'Forty'}[m_], vals[(m_, True)]))
    for m_ in (4, 10, 20):
        if (m_, False) in vals: f.write('\\newcommand{\\KernelOnlyRH%s}{%.5f}\n' % ({4: 'Four', 10: 'Ten', 20: 'Twenty'}[m_], vals[(m_, False)]))
    # profile nodes
    f.write('%%%%TAB_NODES\n')
    f.write('\\begin{longtable}{@{}rllr@{}}\\caption{The vertices $(\\varsigma_i,e_i)$ of the profile $\\mathfrak e_{\\rm P}$ of Lemma~\\ref{lem:profile}, and the source of the bound $\\mu(\\varsigma_i)\\le e_i$. The Heath-Brown vertices $n=10,\\dots,398$ are omitted from the table; they are generated by \\texttt{profile\\_published.py} (Appendix~\\ref{app:profile}).}\\label{tab:nodes}\\\\\n\\toprule $i$ & $\\varsigma_i$ & $e_i$ & source\\\\\\midrule\\endfirsthead\n\\toprule $i$ & $\\varsigma_i$ & $e_i$ & source\\\\\\midrule\\endhead\n\\bottomrule\\endfoot\n')
    tyb = set([lo for lo, hi, a, b in TY]+[hi for lo, hi, a, b in TY]); pr = set(l-k for k, l in PAIRS); hbn = {hb(n)[0]: n for n in range(6, 400)}
    for i, (s, e) in enumerate(nodes):
        if s == Fr(1, 2): src = 'Bourgain \\cite[Thm.~5]{Bourgain2017}'
        elif s in hbn: src = 'Heath-Brown \\cite[Thm.~2]{HeathBrown2017}, $n=%d$' % hbn[s]
        elif s in pr: src = 'Tao--Trudgian--Yang \\cite[Thm.~20, Lemma~23]{TaoTrudgianYang2025}'
        elif s in tyb: src = 'Trudgian--Yang \\cite[Thm.~2.4]{TrudgianYang2024}'
        elif s == 1: src = '$\\zeta(1+it)\\ll\\log t$ \\cite[Thm.~3.5]{Titchmarsh1986}'
        else: raise SystemExit('node of unknown origin: %s' % s)
        if i < len(nodes)-2 and hbn.get(s, 0) > 9:
            if hbn.get(s) == 10: f.write('\\multicolumn{4}{c}{$\\vdots$ \\quad(Heath-Brown nodes $n=10,\\dots,398$)\\quad $\\vdots$}\\\\\n')
            continue
        f.write('%d & $%s$ & $%s$ & %s\\\\\n' % (i, fr(s), fr(e), src))
    f.write('\\end{longtable}\n')
    # kernel coefficients of the six lines
    for tag, nm, name, mac in LINES:
        s = json.load(open(FAM+'line_%s/sol.json' % tag)); Bl = [tuple(x) for x in s['B']]; cl = s['c']
        f.write('%%%%%%%%TAB_%s\n' % name)
        f.write('\\begin{tabular}{@{}cr@{\\quad}cr@{}}\\toprule $\\iota$ & $c_\\iota$ & $\\iota$ & $c_\\iota$\\\\\\midrule\n')
        Rs = [(b, cc) for b, cc in zip(Bl, cl) if b[0] == 'R']; Is = [(b, cc) for b, cc in zip(Bl, cl) if b[0] == 'I']
        for i in range(len(Rs)):
            l = '$(\\mathrm R,%d)$ & $%s$' % (Rs[i][0][1], g12(Rs[i][1]))
            l += (' & $(\\mathrm I,%d)$ & $%s$' % (Is[i][0][1], g12(Is[i][1]))) if i < len(Is) else ' & & '
            f.write(l+'\\\\\n')
        f.write('\\bottomrule\\end{tabular}\n')
print('C_H =', CH.str(16), ' upper', chup)

# ---------- appendices: programs, certificates, data ----------
def jfmt(s, width=92):
    out = ['{']; keys = list(s.keys())
    for ki, k in enumerate(keys):
        v = s[k]; comma = ',' if ki < len(keys)-1 else ''
        if isinstance(v, list) and v and isinstance(v[0], list):
            out.append(' "%s": [' % k)
            for ii, x in enumerate(v): out.append('  '+json.dumps(x)+(',' if ii < len(v)-1 else ''))
            out.append(' ]'+comma)
        elif isinstance(v, list):
            items = [json.dumps(x) for x in v]; cur = ' "%s": [' % k
            for ii, it in enumerate(items):
                piece = it+(', ' if ii < len(items)-1 else '')
                if len(cur)+len(piece) > width: out.append(cur.rstrip()); cur = '  '
                cur += piece
            out.append(cur+']'+comma)
        else: out.append(' "%s": %s%s' % (k, json.dumps(v), comma))
    out.append('}')
    return '\n'.join(out)
def verb(path, title, label=None):
    txt = open(path).read()
    out = '\\appsub{%s}\n' % title
    if label: out += '\\label{%s}\n' % label
    return out+'\\begin{lstlisting}\n'+txt+('\n' if not txt.endswith('\n') else '')+'\\end{lstlisting}\n'
def jverb(path, title):
    return '\\appsub{%s}\n\\begin{lstlisting}\n%s\n\\end{lstlisting}\n' % (title, jfmt(json.load(open(path))))
with open('generated_appendix.tex', 'w') as f:
    f.write('\\section{Programs}\\label{app:code}\n')
    f.write('The programs are written in Python~3 and use \\texttt{python-flint} (Arb ball arithmetic \\cite{Johansson2017}, FLINT \\cite{FLINT}) at $256$ bits, \\texttt{numpy}, \\texttt{scipy}, \\texttt{cvxpy} with the solver Clarabel, and \\texttt{mpmath} (in \\texttt{opt\\_line.py} only). '
            'The certification programs are those of Sections~\\ref{app:certutil}--\\ref{app:cert_line}; every bound they print or write to a file is converted to decimal with directed rounding (\\texttt{up\\_str} in \\texttt{certutil.py}), so that the printed decimal is itself a valid bound. Each certificate begins with the SHA-256 digests of its input file and of the programs that produced it, and the versions of Python and \\texttt{python-flint}; the build script of this note checks that these digests are those of the files reproduced in Appendices~\\ref{app:code} and~\\ref{app:data}. '
            'The search programs that produced the coefficients are reproduced in Section~\\ref{app:search} for completeness, but no statement of this article depends on them. '
            'All files are in the repository cited in Section~\\ref{sec:methods}, in the folders \\texttt{hybrid\\_asymptotic/} and \\texttt{family/}; the deposited archive is flat, and the programs locate their helper modules in either layout.\n')
    f.write(verb(HYB+'certutil.py', '\\texttt{certutil.py}: shared helpers, directed decimal rounding of bounds', 'app:certutil'))
    f.write(verb(HYB+'certify_hybrid.py', '\\texttt{certify\\_hybrid.py}: certification of the kernel inequality (with or without discs) and of $C_{\\rm H}$', 'app:cert_hybrid'))
    f.write(verb(HYB+'profile_published.py', '\\texttt{profile\\_published.py}: the nodes of the profile $\\mathfrak e_{\\rm P}$', 'app:profile'))
    f.write(verb(FAM+'cz_gen_pp.py', '\\texttt{cz\\_gen\\_pp.py}: certification of $C_\\zeta$ (per-prime phase maximum)', 'app:cert_cz'))
    f.write(verb(FAM+'elem_gen.py', '\\texttt{elem\\_gen.py}: certification of $\\sup F_u$, $\\sup F_\\ell$ (modes N and S)', 'app:cert_elem'))
    f.write(verb(FAM+'certify_line_pp.py', '\\texttt{certify\\_line\\_pp.py}: driver for one explicit line', 'app:cert_line'))
    f.write('\\appsub{Search programs}\\label{app:search}\n')
    for fn, t in [(HYB+'lpcommon.py', 'lpcommon.py: helpers of the search programs'), (HYB+'explore_discs.py', 'explore_discs.py: the hybrid linear programme'),
                  (HYB+'kernel_only.py', 'kernel_only.py: kernel-only optima (Remark on the infimum)'), (FAM+'opt_line.py', 'opt_line.py: the second-order cone programme of one explicit line')]:
        f.write(verb(fn, '\\texttt{%s}' % esc(t)))
    f.write('\\clearpage\n\\section{Outputs of the certification programs}\\label{app:cert}\n')
    f.write('Each output begins with the SHA-256 digests of its input file and of the programs that produced it. Only the plain decimal numbers printed after \\texttt{<} or \\texttt{<=} (without a radius) are produced by directed decimal rounding (\\texttt{up\\_str} of \\texttt{certutil.py}) and are asserted as bounds; every display of the form \\texttt{[m +/- r]} is a ball printed with the standard \\texttt{str} of \\texttt{python-flint}, which rounds the midpoint to nearest, and is diagnostic only (for the final value of $C_{\\rm H}$ the certificate also prints its radius, as a ball enclosing the radius, and a twenty-digit enclosure obtained by directed rounding). The running times printed at the end of the lines are informative only and depend on the machine; they are not part of the certified data. There are $1+6\\cdot4=25$ certificates: one for the hybrid inequality and four (kernel inequality, $C_\\zeta$, elementary part in modes N and S) for each of the six lines.\n')
    f.write(verb(HYB+HYBCERT, 'Hybrid: \\texttt{certify\\_hybrid.py %s 40}' % esc(HYBJSON), 'app:out_hybrid'))
    for tag, nm, name, mac in LINES:
        for fn, t in [('cert_kernel.txt', 'kernel inequality'), ('cert_czeta_pp.txt', '$C_\\zeta$'), ('cert_elem.txt', 'elementary part, mode N'), ('cert_elem_S.txt', 'elementary part, mode S')]:
            f.write(verb(FAM+'line_%s/%s' % (tag, fn), 'Line %s: %s' % (nm, t)))
    ko_lines = []   # the file is reproduced unchanged; runs whose cutting planes did not converge (residual >= 1e-5) are marked
    for ln in open(HYB+'kernel_only.txt').read().splitlines():
        mv = re.search(r'worst violation=(\S+)', ln)
        ko_lines.append(ln+('   # NOT CONVERGED (not quoted)' if mv and float(mv.group(1)) >= 1e-5 else ''))
    f.write('\\appsub{Grid optima of \\texttt{kernel\\_only.py} (Remark~\\ref{rem:infimum}; not certified)}\\label{app:out_kernel_only}\n'
            'Lines marked \\texttt{NOT CONVERGED} are runs whose cutting-plane iteration stopped with a residual violation $\\ge10^{-5}$ on the fine grid; they are not quoted in the text. The marks are added here; the file \\texttt{kernel\\_only.txt} is unchanged.\n'
            '\\begin{lstlisting}\n'+'\n'.join(ko_lines)+'\n\\end{lstlisting}\n')
    f.write('\\clearpage\n\\section{Input data of the certificates}\\label{app:data}\n')
    f.write('The following files hold the coefficients as decimal strings that round-trip to the binary floating-point numbers produced by the optimiser (the certifiers convert them to exact rationals), the disc data before rounding to rationals (the certificate rounds $c_k,R_k,v_k$ to denominators $\\le10^4$ and then replaces $R_k$ by $\\min(R_k,c_k-\\frac12)$, as in \\texttt{certify\\_hybrid.py}), and the parameters of the search. The fields \\texttt{J\\_grid} and \\texttt{C\\_grid\\_objective} are the floating-point values of the search programme and are not used by the certificates, which recompute $J_k$ and $C_{\\rm H}$ exactly; they are kept so that the file is the unaltered output of the search (its digest is part of the provenance lines of the certificate). The rational disc data actually certified are those of Table~\\ref{tab:hybrid_discs}, obtained from the decimal values below by the two lines of \\texttt{certify\\_hybrid.py} quoted in Appendix~\\ref{app:cert_hybrid}.\n')
    f.write(jverb(HYB+HYBJSON, '\\texttt{%s} (hybrid)' % esc(HYBJSON)))
    # machine-readable copy of the rational disc data and exact weights actually used by the certificate (derived by this
    # script from hyb_m10_P.json exactly as certify_hybrid.py does; not an input of any certificate)
    rat = {'source': HYBJSON, 'd': [d.numerator, d.denominator],
           'discs': [{'k': k+1, 'c': [cc.numerator, cc.denominator], 'R': [R.numerator, R.denominator], 'v': [v.numerator, v.denominator],
                      'kappa': [kap[k].numerator, kap[k].denominator]} for k, (cc, R, v) in enumerate(discs)]}
    json.dump(rat, open('hyb_m10_P_discs_rational.json', 'w'), indent=1)
    f.write('\\appsub{\\texttt{hyb\\_m10\\_P\\_discs\\_rational.json} (derived)}\nThe rational disc data $(c_k,R_k,v_k)$ and the exact weights $\\kappa_k$ used by the certificate, as pairs (numerator, denominator), obtained from \\texttt{%s} by the conversions of \\texttt{certify\\_hybrid.py}; the file is generated by \\texttt{gen\\_appendix.py} and is not an input of any certificate. Its first lines are\n\\begin{lstlisting}\n%s\n\\end{lstlisting}\n' % (esc(HYBJSON), '\n'.join(open('hyb_m10_P_discs_rational.json').read().splitlines()[:12])+'\n...'))
    for tag, nm, name, mac in LINES: f.write(jverb(FAM+'line_%s/sol.json' % tag, '\\texttt{line\\_%s/sol.json} (line %s)' % (tag, nm)))
print('done')
