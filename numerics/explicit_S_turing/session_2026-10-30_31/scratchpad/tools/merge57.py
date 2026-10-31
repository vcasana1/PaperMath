import sys
base=sys.argv[1]
s=open(base+'.tex',encoding='utf-8').read(); t=open(base+'_tips.tex',encoding='utf-8').read()
a=s.index('% hover texts'); b=s.index('\\makeatother\n',s.index('CGBib@',a))+len('\\makeatother\n')
if not t.endswith('\n'): t+='\n'
s2=s[:a]+t+s[b:]
open(base+'.tex','w',encoding='utf-8').write(s2); print('changed' if s2!=s else 'stable')
