import re
v3=open('../logsine_product_constant_v3.tex').read()
pre=v3[:v3.index(r'\begin{document}')]
pre='\n'.join(l for l in pre.split('\n') if not l.startswith(r'\expandafter\gdef\csname CGTip@'))
body=open('body1.tex').read()+'\n\n'+open('body2.tex').read()+open('body3.tex').read()
def detex(s, cut=330):
    s=re.sub(r'\\label\{[^}]*\}','',s); s=re.sub(r'\\VCGreviewed\{\d\}','',s)
    s=re.sub(r'\\CGeqref\{([^}]*)\}',r'(\1)',s); s=re.sub(r'\\CGref\{([^}]*)\}',r'\1',s)
    s=re.sub(r'\\(begin|end)\{[a-z*]+\}','',s)
    for a,b in [(r'\qquad',' ; '),(r'\quad',' '),(r'\,',' '),(r'\ ',' '),(r'\!',''),(r'\;',' '),(r'\\',' ; '),('&',''),(r'\left',''),(r'\right',''),
                (r'\Bigl',''),(r'\Bigr',''),(r'\bigl',''),(r'\bigr',''),(r'\displaystyle',''),(r'\substack',''),(r'\operatorname',''),(r'\mathcal',''),(r'\mathsf',''),
                (r'\mathfrak',''),(r'\mathbb',''),(r'\mathbf',''),(r'\widehat','hat '),(r'\overline','conj '),(r'\tfrac',r'\frac'),(r'\ge','>='),(r'\le','<='),(r'\ne','!='),
                (r'\infty','infinity'),(r'\cdot','*'),(r'\mid',' | '),(r'\nmid',' not| '),(r'\vee',' v '),(r'\to','->'),(r'\mapsto','->'),(r'\notin',' not in '),(r'\in',' in '),
                (r'\ldots','...'),(r'\dots','...'),(r'\lfloor','floor('),(r'\rfloor',')'),(r'\{','('),(r'\}',')'),(r'\%','percent')]:
        s=s.replace(a,b)
    for _ in range(6): s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'(\1)/(\2)',s)
    s=re.sub(r'\\frac(\d)(\d)',r'\1/\2',s); s=re.sub(r'\\frac\s*([A-Za-z\\]+?)\s*(\d)',r'\1/\2',s); s=s.replace(r'\frac','frac ')
    s=re.sub(r'\\([A-Za-z]+)',r'\1',s)
    s=s.replace('{','(').replace('}',')').replace('$','').replace('~',' ').replace('#','')
    s=re.sub(r'\s+',' ',s).strip()
    s=s[:cut]
    s=s.replace('^',r'\textasciicircum{}').replace('_',r'\_')
    return s
tips={}
for m in re.finditer(r'\\begin\{equation\}\\label\{([^}]+)\}(.*?)\\end\{equation\}',body,re.S): tips[m.group(1)]='Equation: '+detex(m.group(2))
for m in re.finditer(r'\\section\{(.*?)\}\\label\{([^}]+)\}',body): tips[m.group(2)]='Section: '+detex(m.group(1))
for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition)\}\[(.*?)\]\\label\{([^}]+)\}(.*?)\\end\{\1\}',body,re.S):
    tips[m.group(3)]=m.group(1).capitalize()+' - '+detex(m.group(2))+': '+detex(m.group(4),260)
for m in re.finditer(r'\\caption\{(.*?)\}\\label\{([^}]+)\}',body,re.S): tips[m.group(2)]=('Table: ' if m.group(2).startswith('tab') else 'Figure: ')+detex(m.group(1))
labels=re.findall(r'\\label\{([^}]+)\}',body)
assert len(labels)==len(set(labels)), [l for l in labels if labels.count(l)>1]
missing=set(labels)-set(tips); assert not missing, missing
tiplines='\n'.join(r'\expandafter\gdef\csname CGTip@%s\endcsname{%s}'%(k,tips[k]) for k in labels)
pre=pre.replace('% one line per label:','% one line per label:\n'+tiplines)
pre=pre.replace(r'\usepackage{pdfcomment}',r'\usepackage{pdfcomment}'+'\n'+r'\usepackage{graphicx}')
pre=re.sub(r'pdftitle=\{[^}]*\}','pdftitle={Castor and Pollux I: the log-sine transform G and the Gram matrix of the factors of a sine product}',pre)
pre=re.sub(r'pdfsubject=\{[^}]*\}','pdfsubject={Products of sines; Mellin transforms; gcd matrices}',pre)
pre=re.sub(r'pdfkeywords=\{[^}]*\}','pdfkeywords={products of sines, log-sine function, Mellin transform, positive kernel, gcd matrices, Jordan totient, Gram matrix, digamma function}',pre)
open('tmp.tex','w').write(pre+body)
print(len(labels),'labels')
