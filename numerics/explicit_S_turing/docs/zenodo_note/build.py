# Inline all \input files into one self-contained .tex, write the .txt copy, compile to a PDF with a different name.
import re, subprocess, sys, os, shutil
V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
base = 'casanya_turing_jensen_%s' % V
src = open('body.tex').read()
def inline(s):
    def rep(m):
        fn = m.group(1); fn = fn if fn.endswith('.tex') else fn+'.tex'
        return '%% ---- inlined from %s ----\n' % fn + open(fn).read()
    return re.sub(r'\\input\{([^}]*)\}', rep, s)
out = inline(inline(src))
open(base+'_l.tex', 'w').write(out); open(base+'.txt', 'w').write(out)
os.makedirs('build', exist_ok=True); shutil.copy(base+'_l.tex', 'build/'+base+'_l.tex')
for i in range(3):
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-jobname', base, base+'_l.tex'], cwd='build', capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:]); sys.exit(1)
shutil.copy('build/'+base+'.pdf', base+'.pdf')
log = open('build/'+base+'.log').read()
print('pages:', re.search(r'Output written on .* \((\d+) pages', log).group(1))
print('undefined refs:', len(re.findall(r'Reference `[^\']*\' on page', log)), ' undefined cites:', len(re.findall(r'Citation `[^\']*\' on page', log)))
print('overfull hboxes:', len(re.findall(r'Overfull \\hbox', log)))
for m in re.findall(r'Reference `([^\']*)\' on page', log)[:20]: print('  undefined:', m)
for m in re.findall(r'Citation `([^\']*)\' on page', log)[:20]: print('  undefined cite:', m)
