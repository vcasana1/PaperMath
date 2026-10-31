D='/tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/build/'
s=open(D+'casanya_ordinal_primes_v45.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))
pre,body=s[:b],s[b:]
G=r'\{\gamma_k\}'
P=[
 (r'For $t>0$ not an imaginary part the Riemann--von Mangoldt formula reads', r'For $t>0$, $t\notin'+G+'$, the Riemann--von Mangoldt formula reads',1),
 (r'At an imaginary part $t$ this paper uses', r'At $t\in'+G+'$ this paper uses',1),
 (r'approximation through values outside $'+G+'$.', r'approximation through $t\notin'+G+'$.',1),
 (r'For $t>0$ not an imaginary part, $S(t)=', r'For $t>0$, $t\notin'+G+'$, $S(t)=',1),
 (r'for $T$ not an imaginary part and have', r'for $T\notin'+G+'$ and have',1),
 (r'Taking sequences of points outside $'+G+'$ tending to each imaginary part $\gamma$', r'Taking sequences in $(0,\infty)\setminus'+G+r'$ tending to each $\gamma\in'+G+'$',1),
 (r'For $t>0$ not an imaginary part, $N(t)=', r'For $t>0$, $t\notin'+G+'$, $N(t)=',1),
 (r'if $T$ is not an imaginary part,', r'if $T\notin'+G+'$,',1),
 (r'holds for $t>0$ not an imaginary part.', r'holds for $t>0$, $t\notin'+G+'$.',1),
 (r'let $T\ge3$ be outside $'+G+'$.', r'let $T\ge3$, $T\notin'+G+'$.',1),
 (r'through values outside $'+G+'$ (at an imaginary part $S(T)=S(T^+)$', r'through $T\notin'+G+r'$ (at $T\in'+G+'$, $S(T)=S(T^+)$',1),
 (r'a limit of values at points outside $'+G+r'$, so the $\limsup$ over points outside $'+G+'$', r'a limit of values at $t\notin'+G+r'$, so the $\limsup$ over $T\notin'+G+'$',1),
 (r'Let $T\ge100$ be outside $'+G+'$.', r'Let $T\ge100$, $T\notin'+G+'$.',1),
 (r'at points $t\ge e$ outside $'+G+'$', r'at $t\ge e$, $t\notin'+G+'$,',1),
 (r'for large $t$ outside $'+G+'$', r'for large $t\notin'+G+'$',1),
 (r'all large $t$ outside $'+G+'$', r'all large $t\notin'+G+'$',1),
 (r'Let $t>\gamma_1$ be outside $'+G+'$ and', r'Let $t>\gamma_1$, $t\notin'+G+'$, and',1),
 (r'Choose $t\to\infty$ outside $'+G+'$ with', r'Choose $t\to\infty$, $t\notin'+G+'$, with',1),
 (r'such that neither $t$ nor $t+h$ is an imaginary part (a null set', r'such that $t,t+h\notin'+G+'$ (a null set',1),
 (r'the convention $S(t)=S(t^+)$ at an imaginary part is adopted', r'the convention $S(t)=S(t^+)$ at $t\in'+G+'$ is adopted',1),
]
for o,n,c in P:
    k=body.count(o); assert k==c,(k,o)
    body=body.replace(o,n)
open(D+'casanya_ordinal_primes_v46.tex','w',encoding='utf-8').write(pre+body)
print('ok')
