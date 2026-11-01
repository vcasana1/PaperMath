import json, math, sys, glob
rs=[json.loads(l) for f in glob.glob('sweep*.jsonl') for l in open(f)]
BW=lambda L: min(0.0946*L+5.746, 0.097*L+4.954)
best={}
for r in rs:
    L=r['Lstar']
    if L not in best or r['val']<best[L]['val']: best[L]=r
for L in sorted(best):
    r=best[L]; print('L*=%6g best: %.5f L + %.4f  (d=%.2f m=%s) val=%.3f  BW=%.3f'%(L,r['C1'],r['A3_est'],r['d'],max(j for _,j in r['B']),r['val'],BW(L)))
# envelope check on grid
Lg=[0.0]+[x*0.5 for x in range(1,60000)]
worst=min(BW(L)-min(r['C1']*L+r['A3_est'] for r in rs) for L in Lg)
print('min over L in [0,30000] of BW - envelope(all candidates) =',round(worst,4))
