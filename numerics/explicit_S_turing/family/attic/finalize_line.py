import json, sys, math
D=sys.argv[1]; sol=D+'/sol.json'; r=json.load(open(sol))
k=open(D+'/cert_kernel.txt').read(); assert 'all certified' in k
cz=float(json.load(open(sol.replace('.json','_cz.json')))['Czeta_upper']); e=json.load(open(sol.replace('.json','_elem.json')))
fs=float(e['Fsup_upper']); A1=e['A1']; A3=math.ceil((cz+fs)*1e3)/1e3
json.dump({'A1':A1,'A3':'%.3f'%A3,'Czeta_upper':cz,'Fsup_upper':fs,'d':r['d'],'B':r['B'],'Lstar':r['Lstar']},open(D+'/summary.json','w'),indent=1)
print('LINE %s CERTIFIED: |N(T)-main| <= %s log T + %.3f  (T>=1)'%(D,A1,A3))
