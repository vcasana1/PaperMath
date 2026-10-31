import re
D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/'
s=open(D+'b52/casanya_ordinal_primes_v52.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
def rep(o,new,c=1):
    global body
    k=body.count(o); assert k==c,(k,o[:110])
    body=body.replace(o,new)

# ---------- citations in the text that were plain author-year ----------
rep(r'The previous values are $0.112$ (Trudgian, 2014), $0.110$ (Platt and Trudgian, 2015), $0.1038$ (Hasanalizade, Shen and Wong, 2022) and $0.10076$ (Bellotti and Wong, 2025). Table~\CGref{tab:records} lists the whole history, from von Mangoldt (1905).',
    r'The previous values are $0.112$ (Trudgian \CGcite{Trudgian2014}), $0.110$ (Platt and Trudgian \CGcite{PlattTrudgian2015}), $0.1038$ (Hasanalizade, Shen and Wong \CGcite{HasanalizadeShenWong2022}) and $0.10076$ (Bellotti and Wong \CGcite{BellottiWong2025}). Table~\CGref{tab:records} lists the whole history, from von Mangoldt \CGcite{VonMangoldt1905}.')
rep(r'unconditionally (Selberg, Tsang, Fujii; see below).',
    r'unconditionally (Selberg \CGcite{Selberg1946a}, Tsang \CGcite{Tsang1984}, Fujii \CGcite{Fujii1974}; see below).')
rep(r"the factor $\log\log T$ coming from Selberg's mean square of $S$.",
    r"the factor $\log\log T$ coming from Selberg's mean square of $S$ \CGcite{Selberg1946a}.")
rep(r"=O(1)$ by Mertens' theorem.", r"=O(1)$ by Mertens' theorem (Theorem~\CGref{thm:known_mertens}).")

rep(r'(the remaining $0.09783-0.09782899\ldots<10^{-6}$ is the cost of fixed $c,R$ and of rounding)',
    r'(the remaining $0.09783-0.09782899\ldots=0.0000010\ldots$ is the cost of fixed $c,R$ and of rounding)')
rep(r'The right side is positive only if the defects $v_k$ are individually small; the bounds of this article do not achieve this (Remark~\CGref{rem:certificate_scope}).',
    r'The right side is positive exactly when $\sum_{k\in\mathcal K_T}(2v_k)^{2j}<\#\mathcal K_T$, a condition on the defects $v_k$ as a whole; the bounds of this article do not achieve it (Remark~\CGref{rem:certificate_scope}).')

# ---------- bibliography in World Scientific (IJNT) style ----------
i=body.index('\\begin{thebibliography}'); j=body.index('\\end{thebibliography}')
bib=body[i:j]
def initials(x):
    # "R.J." -> "R. J.", "F.W.J." -> "F. W. J."; keep hyphenated "P.-J."
    return re.sub(r'([A-Z])\.(?=[A-Z])', r'\1. ', x)
# number of authors at the start of each entry (comma separated)
nauth={'Backlund1918':1,'Bellotti2024':1,'BellottiWong2025':2,'BennettEtAl2021':4,'Bourgain2017':1,'FazzariGerspachMinelli2025':3,
'FrancaLeClair2015':2,'Fiori2025':1,'Fujii1974':1,'Fujii1981':1,'Gonek2012':1,'Grossmann1913':1,'HardyLittlewoodPolya1934':3,
'HasanalizadeShenWong2021':3,'HasanalizadeShenWong2022':3,'HiaryLeongYang2024':3,'HiaryPatelYang2024':3,'Ivic1985':1,'Johansson2017':1,
'Kargin2013':1,'Korolev2012':1,'LeClair2016':1,'Leong2024':1,'LiebLoss2001':2,'Mertens1874':1,'MontgomeryVaughan1974':2,'Patel2022':1,
'PatelYang2023':2,'Platt2017':1,'PlattTrudgian2015':2,'Rademacher1959':1,'Revers2026':1,'Riesz1932':1,'Rosser1941':1,'Selberg1946a':1,
'Tenenbaum2015':1,'Titchmarsh1986':1,'Trudgian2012':1,'Trudgian2014':1,'Tsang1984':1,'VonMangoldt1905':1,'Yang2024':1}
# journal name and volume as they appear (journal articles only)
jv={'Backlund1918':('Acta Math.','41'),'Bellotti2024':('J. Math. Anal. Appl.','536'),'BennettEtAl2021':('Math. Comp.','90'),
'Bourgain2017':('J. Amer. Math. Soc.','30'),'FrancaLeClair2015':('Commun. Number Theory Phys.','9'),'Fujii1974':('Trans. Amer. Math. Soc.','196'),
'Fujii1981':('Trans. Amer. Math. Soc.','267'),'Gonek2012':('Trans. Amer. Math. Soc.','364'),'HasanalizadeShenWong2021':('Math. Comp.','91'),
'HasanalizadeShenWong2022':('J. Number Theory','235'),'HiaryLeongYang2024':('Funct. Approx. Comment. Math.','73'),
'HiaryPatelYang2024':('J. Number Theory','256'),'Johansson2017':('IEEE Trans. Comput.','66'),'Kargin2013':('Probab. Theory Related Fields','157'),
'Korolev2012':('Publ. Inst. Math. (Beograd) (N.S.)','92(106)'),'LeClair2016':('Symmetry','13'),'Mertens1874':('J. Reine Angew. Math.','78'),
'MontgomeryVaughan1974':('J. Lond. Math. Soc. (2)','8'),'Patel2022':('Indag. Math.','33'),'PatelYang2023':('J. Number Theory','262'),
'Platt2017':('Math. Comp.','86'),'PlattTrudgian2015':('J. Number Theory','147'),'Rademacher1959':('Math. Z.','72'),
'Riesz1932':('J. London Math. Soc.','7'),'Rosser1941':('Amer. J. Math.','63'),'Selberg1946a':('Arch. Math. Naturvid.','48 (5)'),
'Trudgian2012':('Math. Comp.','81'),'Trudgian2014':('J. Number Theory','134'),'VonMangoldt1905':('Math. Ann.','60'),
'Yang2024':('J. Math. Anal. Appl.','534')}
books={
'HardyLittlewoodPolya1934':(r'Inequalities, first ed., Cambridge University Press, Cambridge, 1934.', r'\textit{Inequalities}, 1st edn. (Cambridge University Press, Cambridge, 1934).'),
'Ivic1985':(r'The Riemann Zeta-Function, Wiley, New York, 1985; reprinted by Dover, Mineola, NY, 2003.', r'\textit{The Riemann Zeta-Function} (Wiley, New York, 1985); reprinted (Dover, Mineola, NY, 2003).'),
'LiebLoss2001':(r'Analysis, second ed., Grad. Stud. Math. 14, Amer. Math. Soc., Providence, RI, 2001,', r'\textit{Analysis}, 2nd edn., Graduate Studies in Mathematics, Vol.~14 (American Mathematical Society, Providence, RI, 2001),'),
'Tenenbaum2015':(r'Introduction to Analytic and Probabilistic Number Theory, third ed., Grad. Stud. Math. 163, Amer. Math. Soc., Providence, RI, 2015,', r'\textit{Introduction to Analytic and Probabilistic Number Theory}, 3rd edn., Graduate Studies in Mathematics, Vol.~163 (American Mathematical Society, Providence, RI, 2015),'),
'Titchmarsh1986':(r'The Theory of the Riemann Zeta-Function, second ed., revised by D.R. Heath-Brown, Clarendon Press, Oxford, 1986.', r'\textit{The Theory of the Riemann Zeta-Function}, 2nd edn., revised by D. R. Heath-Brown (Clarendon Press, Oxford, 1986).'),
'Grossmann1913':(r'doctoral thesis, Georg-August-Universit\"at G\"ottingen, 1913.', r'Ph.D. thesis, Georg-August-Universit\"at G\"ottingen (1913).'),
'Tsang1984':(r'Ph.D. thesis, Princeton University, 1984;', r'Ph.D. thesis, Princeton University (1984);'),
}
entries=re.split(r'(?=\\bibitem\{)',bib)
out=[entries[0]]
for e in entries[1:]:
    key=re.match(r'\\bibitem\{([^}]*)\}',e).group(1)
    head='\\bibitem{%s} '%key
    txt=e[len(head):]
    if key in nauth:
        parts=txt.split(', ')
        k=nauth[key]
        auth=[initials(p) for p in parts[:k]]
        a_str=auth[0] if k==1 else (', '.join(auth[:-1])+' and '+auth[-1])
        txt=a_str+', '+', '.join(parts[k:])
    if key in jv:
        jn,vol=jv[key]
        o=jn+' '+vol+' ('
        assert txt.count(o)>=1,(key,o)
        txt=txt.replace(o,r'\textit{'+jn+r'} \textbf{'+vol+'} (',1)
    if key in books:
        o,n=books[key]; assert o in txt,(key,o); txt=txt.replace(o,n)
    out.append(head+txt)
body=body[:i]+''.join(out)+body[j:]
open(D+'b53/casanya_ordinal_primes_v53.tex','w',encoding='utf-8').write(pre+body)
print('ok')
