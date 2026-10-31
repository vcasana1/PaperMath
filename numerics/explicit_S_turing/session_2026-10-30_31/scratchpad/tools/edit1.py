import re,sys
P='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/build/casanya_ordinal_primes_v42.tex'
s=open(P,encoding='utf-8').read()
def rep(old,new,count=1):
    global s
    n=s.count(old)
    assert n==count,(n,old[:80])
    s=s.replace(old,new)

# a) tips line / date / author
rep(r'\InputIfFileExists{casanya_ordinal_primes_v41_tips.tex}{}{}'+'\n','%%TIPS%%\n')
rep(r'\date{Version 41 --- 30 October 2026}',r'\date{30 October 2026}')
rep(r'pdfauthor={Victor Casana-Giner}',r'pdfauthor={Víctor Casaña-Giner}')
rep(r'\author{V\'ictor Casa\~na-Giner\thanks{Independent researcher, Spain. ORCID \href{https://orcid.org/0000-0002-8252-2608}{0000-0002-8252-2608}.}}',
    r'\author{V\'ictor Casa\~na-Giner\thanks{Universidad Nacional de Educaci\'on a Distancia, Madrid, Spain. Email: \href{mailto:vcasana1@alumno.uned.es}{vcasana1@alumno.uned.es}. ORCID \href{https://orcid.org/0000-0002-8252-2608}{0000-0002-8252-2608}.}}')

# e) Lean removal: body
rep(r'; Appendix~\CGref{app:lean} describes the formal verification in Lean~4 of Theorem~\CGref{thm:explicit} and of Section~\CGref{sec:sublevel}, with the results of the literature that they use as explicit hypotheses;',';')
rep(r'Bounding each of these values by rationals, Appendix~\CGref{app:lean} proves $0.096816006',r'Appendix~\CGref{app:code} computes these values (40-digit arithmetic, two independent evaluations) and gives $0.096816006')
rep(r'(Appendix~\CGref{app:code}; Appendix~\CGref{app:lean} bounds each term by rationals) gives',r'(Appendix~\CGref{app:code}) gives')
rep(r'The certified bound $\log\zeta(\sigma^\sharp)\le1.52499$ of Appendix~\CGref{app:lean} uses',r'The bound $\log\zeta(\sigma^\sharp)\le1.52499$ computed in Appendix~\CGref{app:code} uses')
# conclusion
rep('''The constants of Theorem~\\CGref{thm:explicit}, and the proofs of
Theorems~\\CGref{thm:explicit} and~\\CGref{thm:sublevel} and of
Corollary~\\CGref{cor:proportion}, are verified in Lean~4, with the results
of the literature entering as explicit hypotheses
(Appendix~\\CGref{app:lean}). Those external results themselves are not
formalized, and neither is Section~\\CGref{sec:meansquare} or the added
consequences of Section~\\CGref{sec:additional}.

''','')
rep(r'is the Lean proof of Appendix~\CGref{app:lean}, which bounds each term of the closed form',r'is computed in the present appendix, from the closed form')
# Appendix B
i=s.index(r'\section{Formal verification in Lean 4}\label{app:lean}')
j=s.index(r'\section{Correspondence with the sources}\label{app:sources}')
s=s[:i]+s[j:]
# data availability
i=s.index(r'\section*{Data availability}')
j=s.index('%======',i)
s=s[:i]+r'''\section*{Data availability}
The programs of Appendix~\CGref{app:code} and their outputs are reproduced in that appendix. No other data were used.

'''+s[j:]
# bib entries
for key in ['AlpogeFurmanZeta23','CasanaPaperMath2026']:
    m=re.search(r'\\bibitem\{'+key+r'\}.*?\n\n',s,re.S); assert m
    s=s[:m.start()]+s[m.end():]

# f) earlier manuscripts
rep(r'The final certificate is recovered from an earlier manuscript by the author, \emph{A computable prime-corrected Riemann--von Mangoldt sequence}, in its analytic version 14; it is included here with a self-contained proof because it applies to any continuous ordinal model.',
    r'The final certificate is included here with a self-contained proof because it applies to any continuous ordinal model.')
i=s.index(r'Theorem~\CGref{thm:recovered_simple_certificate} was already proved in the author')
j=s.index('It is a certificate, not an unconditional',i)
s=s[:i]+s[j:]
rep('''The further higher-moment and finite Euler-product results of that
manuscript, and the resonance and iteration results of
\\texttt{ordinal\\_prime\\_cutoff\\_v17}, retain their original hypotheses
and proof chains. They are not claimed here without those chains.
''','''Further higher-moment and finite Euler-product results are not claimed here.
''')
rep('''Theorem~\\CGref{thm:recovered_simple_certificate}, recovered from an
earlier manuscript, gives''','''Theorem~\\CGref{thm:recovered_simple_certificate} gives''')

# Appendix A texts: program names
rep(r'(the program \texttt{yang\_smallt\_arb.py} of Appendix~\CGref{app:code})',r'(the interval-arithmetic program of Appendix~\CGref{app:code})')

# h) points of first review
rep(r'(Trudgian \CGcite{Trudgian2012,Trudgian2014}, Bellotti and Wong',r'(Trudgian \CGcite{Trudgian2012}, \CGcite{Trudgian2014}; Bellotti and Wong')
# arXiv DOIs
for a,v in [('2412.15470','v2'),('1408.5794','v2'),('1203.5309','v2'),('1601.00914','v1')]:
    old='arXiv:%s%s'%(a,v)
    assert old in s,old
for old,new in [
 (r'statements numbered as in arXiv:2412.15470v2, \href{https://doi.org/10.1090/mcom/4133}',r'statements numbered as in arXiv:2412.15470v2 (\href{https://doi.org/10.48550/arXiv.2412.15470}{doi:10.48550/arXiv.2412.15470}), \href{https://doi.org/10.1090/mcom/4133}'),
 (r'theorems numbered as in arXiv:1408.5794v2, \href',r'theorems numbered as in arXiv:1408.5794v2 (\href{https://doi.org/10.48550/arXiv.1408.5794}{doi:10.48550/arXiv.1408.5794}), \href'),
 (r'theorems numbered as in arXiv:1203.5309v2, \href',r'theorems numbered as in arXiv:1203.5309v2 (\href{https://doi.org/10.48550/arXiv.1203.5309}{doi:10.48550/arXiv.1203.5309}), \href'),
 (r'arXiv:1601.00914v1, 2016, cited',r'arXiv:1601.00914v1 (\href{https://doi.org/10.48550/arXiv.1601.00914}{doi:10.48550/arXiv.1601.00914}), 2016, cited'),
]: rep(old,new)

# b) labels
M={'subsec:clock_intro':'subsec:tau_intro','eq:intro_clock':'eq:intro_tau','thm:envelope':'thm:asymptotic','eq:envelope_formula':'eq:asymptotic_formula',
'cor:clock':'cor:distance','eq:clock_explicit':'eq:distance_explicit','subsec:proof_envelope':'subsec:proof_asymptotic','sec:clock':'sec:distance',
'prop:clock_sharp':'prop:distance_sharp','rem:bare_clock':'rem:bare_point','cor:identity_clock':'cor:identity_distance','eq:identity_clock':'eq:identity_distance',
'eq:S_envelope_eta':'eq:S_asymptotic_eta','eq:a_envelope_eta':'eq:a_asymptotic_eta','eq:clock_lower':'eq:distance_lower'}
for a,b in M.items():
    s=re.sub(r'(?<=[{,])'+re.escape(a)+r'(?=[},])',b,s)
open(P,'w',encoding='utf-8').write(s)
print('ok')
