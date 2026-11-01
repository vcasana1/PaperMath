# Build the Mathematics of Computation version of the article from the Zenodo-note source (../zenodo_note/body.tex).
#   python3 build_mcom.py vN
# Produces, in this folder:
#   casanya_turing_jensen_mcom_vN.pdf / _l.tex / .txt           the article, class mcom-l (AMS author package), Appendix A only
#   casanya_turing_jensen_mcom_supplement_vN.pdf / .tex / .txt   the supplement: programs, certificate outputs, input data
# The mathematical text is identical to the Zenodo note; only the preamble, the top matter, the abstract (macros expanded),
# the references to the appendices (now to the supplement) and the Data availability paragraph change.
import re, subprocess, sys, os, shutil
V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'zenodo_note') + os.sep
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
base = 'casanya_turing_jensen_mcom_%s' % V; supp = 'casanya_turing_jensen_mcom_supplement_%s' % V

def inline(s):
    def rep(m):
        fn = m.group(1); fn = fn if fn.endswith('.tex') else fn + '.tex'
        return '%% ---- inlined from %s ----\n' % fn + open(SRC + fn).read()
    return re.sub(r'\\input\{([^}]*)\}', rep, s)

body = open(SRC + 'body.tex').read()
values = open(SRC + 'generated_values.tex').read()
macros = dict(re.findall(r'\\newcommand\{\\([A-Za-z]+)\}\{([^{}]*)\}', values))

def cut(s, start, end, must=True):
    i = s.find(start); j = s.find(end, i) + len(end)
    assert (i >= 0 and j > i) or not must, (start, end)
    return s[:i] + s[j:] if i >= 0 else s

# ---------------- preamble ----------------
s = body
s = s.replace('\\documentclass[11pt,reqno]{amsart}', '\\documentclass{mcom-l}')
s = cut(s, '% ---------- hover previews', '\\input{tips.tex}\n')                       # tooltips (pdfcomment)
s = cut(s, '\\hypersetup{', '\n}\n')                                                    # boxed links, bookmarks, pdf metadata
s = cut(s, '% back-references in the bibliography', '\\fi}\n')
s = cut(s, '% in \\cite[note]{key} the note is linked too', '\\makeatother\n')
for pkg in ['\\usepackage{geometry}\n', '\\usepackage{listings}\n', '\\usepackage{bookmark}\n', '\\usepackage{pdfcomment}\n']:
    assert s.count(pkg) == 1, pkg; s = s.replace(pkg, '')
s = s.replace('\\usepackage[pagebackref=true]{hyperref}', '\\usepackage[hyphens]{url}\n\\usepackage{xr-hyper}\n\\usepackage{hyperref}\n\\externaldocument[S-]{%s}' % supp)
s = s.replace('\\geometry{margin=1in}\n', '')
s = s.replace('\\setcounter{tocdepth}{2}\n', '')
s = re.sub(r'\\lstset\{[^\n]*\}\n', '', s)
s = s.replace('\\CGeqref{', '\\eqref{').replace('\\CGref{', '\\ref{')
s = s.replace('\\input{generated_values.tex}', '\\input{generated_values.tex}\n\\hypersetup{colorlinks=false,pdfborder={0 0 1},linkbordercolor={1 0 0},citebordercolor={0 0.3 1},urlbordercolor={0 0.6 0.6},pdftitle={Explicit and asymptotic estimates for the zero-counting function of the Riemann zeta-function},pdfauthor={Victor Casana-Giner}}')
s = inline(s).replace('\\input{tips.tex}', '')
s = s.replace('\\CGeqref{', '\\eqref{').replace('\\CGref{', '\\ref{')
# top matter
s = s.replace('\\email{\\href{mailto:vcasana1@alumno.uned.es}{vcasana1@alumno.uned.es}}', '\\email{vcasana1@alumno.uned.es}')
s = s.replace('\\date{1 November 2026}', '\\date{}')
s = s.replace('\\maketitle\n\\tableofcontents\n', '\\maketitle\n')
# abstract: expand the numerical macros (the AMS wants a self-contained abstract)
i = s.index('\\begin{abstract}'); j = s.index('\\end{abstract}')
ab = s[i:j]
for k, v in sorted(macros.items(), key=lambda kv: -len(kv[0])):
    ab = ab.replace('\\' + k + '\\ldots', v + '\\ldots').replace('\\' + k + ' ', v + ' ').replace('\\' + k, v)
assert '\\Line' not in ab and '\\CH' not in ab, ab
s = s[:i] + ab + s[j:]
# references to the appendices B-D, which become the supplement
s = s.replace('are reproduced after the bibliography (Appendices~\\ref{app:code}--\\ref{app:data})', 'are reproduced in the Supplement to this article (Sections~\\ref{S-app:code}--\\ref{S-app:data})')
s = s.replace('Appendices~\\ref{app:code}--\\ref{app:data}', 'Sections~\\ref{S-app:code}--\\ref{S-app:data} of the Supplement')
s = s.replace('Appendices~\\ref{app:code}--\\ref{app:cert}', 'Sections~\\ref{S-app:code}--\\ref{S-app:cert} of the Supplement')
s = s.replace('(Appendix~\\ref{app:data})', '(Section~\\ref{S-app:data} of the Supplement)').replace('(Appendix~\\ref{app:profile})', '(Section~\\ref{S-app:profile} of the Supplement)')
for lab in ['app:cert_cz', 'app:cert_elem', 'app:cert_hybrid', 'app:cert', 'app:data', 'app:out_hybrid', 'app:out_kernel_only', 'app:search', 'app:code', 'app:profile', 'app:certutil', 'app:cert_line']:
    s = s.replace('Appendix~\\ref{%s}' % lab, 'Section~\\ref{S-%s} of the Supplement' % lab)
# data availability
old_da = s[s.index('\\subsection*{Data availability}'):s.index('% ---- inlined from ai_declaration.tex ----')]
new_da = ('\\subsection*{Data availability}\nThe programs, the coefficient files and the outputs of all certificates are reproduced in the Supplement to this article '
          '(Sections~\\ref{S-app:code}--\\ref{S-app:data}) and are available, together with the Supplement and the archive of the computations, at '
          '\\url{https://github.com/vcasana1/PaperMath/tree/explicit-S-turing/numerics/explicit_S_turing} and at Zenodo, '
          '\\href{https://doi.org/10.5281/zenodo.23858827}{doi:10.5281/zenodo.23858827}.\n\n')
s = s.replace(old_da, new_da)
# structure: Appendix A before the bibliography (AMS convention), no supplement material in the article
tail = s[s.index('\\clearpage\n\\appendix'):]
s = s[:s.index('\\clearpage\n\\appendix')]
bib_start = s.index('\\begin{thebibliography}')
appendixA = '\\appendix\n\\section{Data tables}\\label{app:tables}\n' + open(SRC + 'generated_datatables.tex').read().replace('Appendix~\\ref{app:data}', 'Section~\\ref{S-app:data} of the Supplement').replace('Appendix~\\ref{app:profile}', 'Section~\\ref{S-app:profile} of the Supplement') + '\n\n'
s = s[:bib_start] + appendixA + '\\bibliographystyle{amsplain}\n' + s[bib_start:] + '\n\\end{document}\n'
assert 'ref{app:' not in s.replace('ref{app:tables}', '').replace('ref{S-app:', ''), re.findall(r'ref\{app:[a-z_]*\}', s)
s = s.replace('\\appsub', '\\mcomappsub')
s = s.replace('\\newcommand{\\mcomappsub}[1]{\\par\\medskip\\noindent\\textbf{#1}\\par\\nobreak\\smallskip}', '\\newcommand{\\mcomappsub}[1]{\\par\\medskip\\noindent\\textbf{#1}\\par\\nobreak\\smallskip}')
article = s
from mcom_overrides import OVERRIDES
for o, n in OVERRIDES:
    assert article.count(o) == 1, ('override not found exactly once', o[:60], article.count(o))
    article = article.replace(o, n)
# close the groups opened around the two small-font tables
parts = article.split('\\begingroup\\footnotesize')
for i in range(1, len(parts)):
    j = parts[i].index('\\end{longtable}') + len('\\end{longtable}')
    parts[i] = parts[i][:j] + '\\endgroup' + parts[i][j:]
article = '\\begingroup\\footnotesize'.join(parts)
assert '\\input{' not in article and 'CGref' not in article and 'pdftooltip' not in article

# ---------------- supplement ----------------
pre = body[:body.index('\\title[')]
pre = pre.replace('\\documentclass[11pt,reqno]{amsart}', '\\documentclass{amsart}')
pre = cut(pre, '% ---------- hover previews', '\\input{tips.tex}\n')
pre = cut(pre, '\\hypersetup{', '\n}\n')
pre = cut(pre, '% back-references in the bibliography', '\\fi}\n')
pre = cut(pre, '% in \\cite[note]{key} the note is linked too', '\\makeatother\n')
for pkg in ['\\usepackage{bookmark}\n', '\\usepackage{pdfcomment}\n']:
    pre = pre.replace(pkg, '')
pre = pre.replace('\\usepackage[pagebackref=true]{hyperref}', '\\usepackage[hyphens]{url}\n\\usepackage{xr-hyper}\n\\usepackage{hyperref}\n\\externaldocument[M-]{%s}' % base)
pre = pre.replace('\\geometry{margin=1in}\n', '\\geometry{margin=1in}\n')
pre = pre.replace('\\setcounter{tocdepth}{2}\n', '')
pre = pre.replace('\\newcommand{\\appsub}[1]{\\par\\medskip\\noindent\\textbf{#1}\\par\\nobreak\\smallskip}', '\\newcommand{\\appsub}[1]{\\subsection{#1}}')
pre += ('\\hypersetup{colorlinks=false,pdfborder={0 0 1},linkbordercolor={1 0 0},citebordercolor={0 0.3 1},urlbordercolor={0 0.6 0.6},'
        'pdftitle={Supplement to: Explicit and asymptotic estimates for the zero-counting function of the Riemann zeta-function},pdfauthor={Victor Casana-Giner}}\n'
        '\\renewcommand{\\thesection}{S\\arabic{section}}\n')
app = open(SRC + 'generated_appendix.tex').read()
app = app.replace('\\clearpage\n', '').replace('Remark~\\ref{rem:infimum}', 'Remark~\\ref{M-rem:infimum} of the article')
app = app.replace('Section~\\ref{sec:methods}', 'Section~\\ref{M-sec:methods} of the article').replace('Table~\\ref{tab:hybrid_discs}', 'Table~\\ref{M-tab:hybrid_discs} of the article')
app = app.replace('\\appsub{', '\\appsub{')
# bibliography of the supplement: the entries cited in it, copied from the article
bibblock = body[body.index('\\begin{thebibliography}{99}'):body.index('\\end{thebibliography}') + len('\\end{thebibliography}')]
cited = sorted(set(re.findall(r'\\cite\{([A-Za-z0-9]+)\}', app)))
items = re.findall(r'(\\bibitem\{([A-Za-z0-9]+)\}.*?)(?=\n\n\\bibitem|\n\n\\end\{thebibliography\})', bibblock, re.S)
keep = [t for t, k in items if k in cited]
assert len(keep) == len(cited), (cited, [k for t, k in items])
supplement = (pre + '\\title[Supplement: estimates for $N(T)$]{Supplement to: Explicit and asymptotic estimates for the zero-counting function of the Riemann zeta-function}\n'
              '\\author{V\\\'ictor Casa\\~na-Giner}\n\\address{Universidad Nacional de Educaci\\\'on a Distancia, Madrid, Spain}\n\\email{vcasana1@alumno.uned.es}\n'
              '\\begin{document}\n\\begin{abstract}\nThis supplement reproduces the programs, the outputs of the $25$ certificates and the input data of the certificates of the article '
              '\\emph{Explicit and asymptotic estimates for the zero-counting function of the Riemann zeta-function}. Section and equation numbers without the prefix S refer to the article. '
              'The same files are available at \\url{https://github.com/vcasana1/PaperMath/tree/explicit-S-turing/numerics/explicit_S_turing} and at Zenodo, \\href{https://doi.org/10.5281/zenodo.23858827}{doi:10.5281/zenodo.23858827}.\n\\end{abstract}\n\\maketitle\n\\tableofcontents\n\n'
              + app + '\n\\begin{thebibliography}{99}\n\n' + '\n\n'.join(keep) + '\n\n\\end{thebibliography}\n\\end{document}\n')
supplement = inline(supplement)
assert '\\input{' not in supplement and 'CGref' not in supplement

open(base + '_l.tex', 'w').write(article); open(base + '.txt', 'w').write(article)
open(supp + '.tex', 'w').write(supplement); open(supp + '.txt', 'w').write(supplement)
os.makedirs('build', exist_ok=True)
for fn in [base + '_l.tex', supp + '.tex', 'mcom-l.cls']: shutil.copy(fn, 'build/' + fn)
def latex(job, src):
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-jobname', job, src], cwd='build', capture_output=True, text=True, errors='replace')
    if r.returncode != 0: print(r.stdout[-4000:]); sys.exit(1)
# cross references between the two documents need alternating runs
for i in range(3):
    latex(supp, supp + '.tex'); latex(base, base + '_l.tex')
latex(supp, supp + '.tex'); latex(base, base + '_l.tex')
for job in (base, supp):
    shutil.copy('build/' + job + '.pdf', job + '.pdf')
    log = open('build/' + job + '.log', errors='replace').read()
    print(job, '| pages:', re.search(r'Output written on .* \((\d+) pages', log).group(1),
          '| undefined refs:', len(re.findall(r"Reference `[^']*' on page", log)), '| undefined cites:', len(re.findall(r"Citation `[^']*' on page", log)),
          '| overfull hboxes:', len(re.findall(r'Overfull \\hbox', log)))
    for m in re.findall(r"(?:Reference|Citation) `([^']*)' on page", log)[:20]: print('  undefined:', m)
