# Check a_U(n) = lambda(n) b_U(n), b_U(n) = #{t | a : ab/U <= t <= U/b} for n = a b^2, (a,b)=1 squarefree; else 0.
import math
from sympy import factorint, divisors
def mu(n):
    f=factorint(n); return 0 if any(e>1 for e in f.values()) else (-1)**len(f)
def lam(n): return (-1)**sum(factorint(n).values())
for U in [7,20,45]:
    X=U*U+0.5; bad=0; tot=0
    for n in range(1,int(X)+1):
        aU=sum(mu(d)*mu(n//d) for d in divisors(n) if d<=U and n//d<=U)
        f=factorint(n)
        if any(e>2 for e in f.values()): b=0
        else:
            a=math.prod(p for p,e in f.items() if e==1); bb=math.prod(p for p,e in f.items() if e==2)
            b=sum(1 for t in divisors(a) if a*bb/U<=t<=U/bb)
        tot+=1; bad+=(aU!=lam(n)*b)
    print(f"U={U}: n<=U^2 checked={tot}, mismatches={bad}")
