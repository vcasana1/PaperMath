# Redraws the figure of J_terms_v2.csv as a vector EPS file (no new computation).
import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows=list(csv.DictReader(open("J_terms_v2.csv")))
ts=sorted({float(r["t"]) for r in rows})
fig,axs=plt.subplots(1,3,figsize=(15,4.6))
for ax,t in zip(axs,ts):
    R=[r for r in rows if float(r["t"])==t]
    sg=[float(r["sigma"]) for r in R]
    for key,lab,m in [("abs_T1",r"$|T_1|$","o"),("abs_T2",r"$|T_2|$","s"),("abs_T3",r"$|T_3|$","^"),("abs_J",r"$|J|=|T_1+T_2+T_3|$","*")]:
        ax.semilogy(sg,[float(r[key]) for r in R],marker=m,label=lab)
    ax.set_title(f"t = {t:.4f}"); ax.set_xlabel(r"$\sigma$"); ax.grid(alpha=.3)
axs[0].set_ylabel("absolute value"); axs[0].legend(fontsize=9)
fig.suptitle(r"The three terms of $J(s)=\int_0^\infty Q(u)\,u^{-s-3}\,du$, $s=\sigma+it$")
fig.tight_layout(); fig.savefig("fig_J_terms_v4.eps")
print("saved fig_J_terms_v4.eps")
