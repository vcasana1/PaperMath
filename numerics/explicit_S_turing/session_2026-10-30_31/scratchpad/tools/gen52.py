"""gen_tips.py -- generates <base>_tips.tex, the texts of the hover tooltips for \\CGref, \\CGeqref and \\CGcite.
Usage: python3 -I gen_tips.py base   (reads base.tex and base.aux, after two pdflatex runs)."""
import re, sys

base = sys.argv[1]
src = open(base + '.tex', encoding='utf-8').read()
aux = open(base + '.aux', encoding='utf-8').read()


bibnum = dict(re.findall(r'\\bibcite\{([^}]*)\}\{([^}]*)\}', aux))

def _bracket(x, i):
    """x[i]=='[': return (content, index after the matching ']'), respecting nested {} and []."""
    d, j = 0, i
    while j < len(x):
        ch = x[j]
        if ch in '[{': d += 1
        elif ch in ']}': d -= 1
        if d == 0: return x[i+1:j], j+1
        j += 1
    return x[i+1:], len(x)

def cites(x):
    out, i = [], 0
    while True:
        k = x.find('\\CGcite', i)
        if k < 0: out.append(x[i:]); return ''.join(out)
        out.append(x[i:k]); j = k + len('\\CGcite')
        opt = ''
        if j < len(x) and x[j] == '[': opt, j = _bracket(x, j)
        if j < len(x) and x[j] == '{':
            keys, j = _bracket(x, j)
            nums = ', '.join(bibnum.get(s.strip(), s.strip()) for s in keys.split(','))
            out.append('[' + nums + (', ' + opt if opt else '') + ']')
        i = j

def _arg(x, i):
    while i < len(x) and x[i] in ' \n\t': i += 1
    if i >= len(x): return '', i
    if x[i] == '{':
        d, j = 0, i
        while j < len(x):
            d += (x[j] == '{') - (x[j] == '}')
            if d == 0: break
            j += 1
        return x[i+1:j], j+1
    if x[i] == '\\':
        m = re.match(r'\\[A-Za-z]+', x[i:])
        if m: return m.group(0), i + len(m.group(0))
        return x[i:i+2], i+2
    return x[i], i+1

def fracs(x):
    while True:
        m = re.search(r'\\[td]?frac(?![A-Za-z])', x)
        if not m: return x
        a, i = _arg(x, m.end()); b, j = _arg(x, i)
        par = lambda u: u if re.fullmatch(r'[\w.\\]+', u) else '(' + u + ')'
        x = x[:m.start()] + par(a) + '/' + par(b) + ' ' + x[j:]

def detex(x, n=320):
    x = re.sub(r'%.*', '', x)
    x = re.sub(r'\\texorpdfstring\{((?:[^{}]|\{[^{}]*\})*)\}\{[^{}]*\}', r'\1', x)
    x = re.sub(r'\\label\{[^}]*\}', '', x)
    x = re.sub(r'\\CGeqref\{([^}]*)\}', lambda m: '(' + labels[m.group(1)][0] + ')' if m.group(1) in labels else '[' + m.group(1) + ']', x)
    x = re.sub(r'\\CGref\{([^}]*)\}', lambda m: labels[m.group(1)][0] if m.group(1) in labels else '[' + m.group(1) + ']', x)
    x = cites(x)
    x = re.sub(r'\\eqref\{([^}]*)\}', lambda m: '(' + labels[m.group(1)][0] + ')' if m.group(1) in labels else '[' + m.group(1) + ']', x)
    x = re.sub(r'\\ref\{([^}]*)\}', lambda m: labels[m.group(1)][0] if m.group(1) in labels else '[' + m.group(1) + ']', x)
    x = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', x)
    x = re.sub(r'\\url\{([^}]*)\}', r'\1', x)
    x = fracs(x)
    x = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', x)
    x = re.sub(r'\\(?:mathrm|mathcal|mathfrak|operatorname|textbf|emph|text|mathbf|textit)\{([^{}]*)\}', r'\1', x)
    x = re.sub(r'\\(?:qquad|quad|bigl|bigr|Bigl|Bigr|biggl|biggr|left|right|displaystyle|nobreak|,|;|!)', ' ', x)
    x = re.sub(r'\\S(?![A-Za-z])', 'Sec. ', x)
    rep = {r'\notin': ' not in ', r'\le': '<=', r'\ge': '>=', r'\ll': '<<', r'\to': '->', r'\infty': 'inf', r'\cdot': '*',
           r'\sum': 'sum', r'\int': 'int', r'\log': 'log', r'\limsup': 'limsup', r'\sup': 'sup'}
    rep = {k: (v + ' ' if v.isalpha() else v) for k, v in rep.items()}
    for a, b in rep.items():
        x = x.replace(a, b)
    x = re.sub(r'\\([A-Za-z]+)', r'\1', x)
    x = x.replace('{', '').replace('}', '').replace('$', '').replace('~', ' ').replace('&', ' ')
    x = x.replace('\\\\', ' ').replace('\\', '')
    x = re.sub(r'\s+', ' ', x).strip()
    if len(x) > n: x = x[:n].rsplit(' ', 1)[0] + ' ...'
    return x.replace('#', 'no.').replace('%', 'pct').replace('^', '\\textasciicircum{}').replace('_', '\\_')

labels = {}
def _groups(x, i, n):
    out = []
    for _ in range(n):
        g, i = _arg(x, i); out.append(g)
    return out
for m in re.finditer(r'\\newlabel\{([^}]*)\}\{', aux):
    g = _groups(aux, m.end(), 5)
    if len(g) < 4: continue
    kind = g[3].split('.')[0]
    labels[m.group(1)] = (g[0], g[1], kind)

envs = r'theorem|proposition|lemma|corollary|definition|remark'
out = ['% hover texts (equations, statements, references)', r'\makeatletter']
for key, (num, page, kind) in labels.items():
    pos = src.find(r'\label{%s}' % key)
    if pos < 0: continue
    if kind == 'equation':
        b = src.rfind(r'\begin{', 0, pos); e = src.find(r'\end{', pos)
        body = src[src.find('}', b) + 1:e]
        tip = f'Eq. ({num}), p. {page}: ' + detex(body)
    elif kind == 'table':
        c = src.rfind(r'\caption{', 0, pos)
        cap, _ = _arg(src, c + len(r'\caption'))
        tip = f'Table {num} (p. {page}): ' + detex(cap)
    elif kind in ('section', 'subsection', 'appendix'):
        line = src[src.rfind('\n', 0, pos) + 1:pos]
        ms = re.search(r'\\(?:sub)*section\*?', line)
        title = detex(_arg(line, ms.end())[0]) if ms else ''
        tip = f'Section {num}: {title} (p. {page})'
    else:
        m = None
        for mm in re.finditer(r'\\begin\{(' + envs + r')\}', src[:pos]): m = mm
        if not m: continue
        env = m.group(1); e = src.find(r'\end{%s}' % env, pos)
        body = src[m.end():e]
        bs = body.lstrip(); opt = None
        if bs.startswith('['):
            o, e2 = _bracket(bs, 0); opt = o.strip('{}'); body = bs[e2:]
        name = env.capitalize() + f' {num}' + (f' ({detex(opt, 120)})' if opt else '')
        tip = f'{name} (p. {page}): ' + detex(body)
    out.append(r'\expandafter\gdef\csname CGTip@%s\endcsname{%s}' % (key, tip))
for m in re.finditer(r'\\bibitem\{([^}]*)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})', src, re.S):
    out.append(r'\expandafter\gdef\csname CGBib@%s\endcsname{%s}' % (m.group(1), detex(m.group(2), 400)))
out.append(r'\makeatother')
open(base + '_tips.tex', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out) - 3, 'tooltips')
