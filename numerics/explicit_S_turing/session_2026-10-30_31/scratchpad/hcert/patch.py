s=open('lpm.py').read()
old="""        for b in bfine:
            Ar,Fr_=rows(d,B,discs,np.full_like(tfine,b),tfine,eta); v=Fr_-Ar@x; worst=max(worst,v.max())"""
new="""        used=[k for k in range(len(discs)) if x[len(B)+k]>0]
        dU=[discs[k] for k in used]; xU=np.concatenate([x[:len(B)],x[len(B)+np.array(used,dtype=int)]]) if used else x[:len(B)]
        for b in bfine:
            Ar,Fr_=rows(d,B,dU,np.full_like(tfine,b),tfine,eta) if used else (np.array([F(d+b,tfine,k,j)+F(d-b,tfine,k,j) for (k,j) in B]).T, f(b,tfine,d)+eta/(1+tfine**2))
            v=Fr_-Ar@xU; worst=max(worst,v.max())"""
assert s.count(old)==1; s=s.replace(old,new); open('lpm.py','w').write(s); print('patched')
