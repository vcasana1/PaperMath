# Journal-specific re-breaking of displays and tables for the 30pc text width of the AMS class (mcom-l).
# Each pair (old, new) must occur exactly once in the article text; the mathematics is unchanged, only line breaks,
# the grouping of displayed formulas and the font size of two long tables.  Applied by build_mcom.py after inlining.
OVERRIDES = [
# abstract
(r"""\[
\Bigl|N(T)-\frac T{2\pi}\log\frac T{2\pi e}\Bigr|\le0.08382\log T+5.326,\qquad |S(T)|\le0.08382\log T+4.444,
\]""",
 r"""\[
\Bigl|N(T)-\frac T{2\pi}\log\frac T{2\pi e}\Bigr|\le0.08382\log T+5.326,\quad |S(T)|\le0.08382\log T+4.444,
\]"""),
# breakpoints: two per row
(r"""L_1&=\LineBreakAfrac=\LineBreakA\ldots,&\quad L_2&=\LineBreakBfrac=\LineBreakB\ldots,&\quad L_3&=\LineBreakCfrac=\LineBreakC\ldots,\\
L_4&=\LineBreakDfrac=\LineBreakD\ldots,&\quad L_5&=\LineBreakEfrac=\LineBreakE\ldots""",
 r"""L_1&=\LineBreakAfrac=\LineBreakA\ldots,&\quad L_2&=\LineBreakBfrac=\LineBreakB\ldots,\\
L_3&=\LineBreakCfrac=\LineBreakC\ldots,&\quad L_4&=\LineBreakDfrac=\LineBreakD\ldots,\\
L_5&=\LineBreakEfrac=\LineBreakE\ldots"""),
# single line
(r"""\bigl|N(T)-\main(T)\bigr|\le\LineBAone\log T+\LineBAthreeN,\qquad |S(T)|\le\LineBAone\log T+\LineBAthreeS\qquad(T\ge1).
\label{eq:single_line}""",
 r"""\bigl|N(T)-\main(T)\bigr|\le\LineBAone\log T+\LineBAthreeN,\quad |S(T)|\le\LineBAone\log T+\LineBAthreeS\quad(T\ge1).
\label{eq:single_line}"""),
# G_def
(r"""F_{\mathrm R,j}(x,t)=\Rp(x+it)^{-j},\quad F_{\mathrm I,j}(x,t)=-\Ip(x+it)^{-j},\quad G_\iota(b,t)=F_\iota(d+b,t)+F_\iota(d-b,t)\ \ (|b|<d).
\label{eq:G_def}""",
 r"""\begin{gathered}
F_{\mathrm R,j}(x,t)=\Rp(x+it)^{-j},\qquad F_{\mathrm I,j}(x,t)=-\Ip(x+it)^{-j},\\
G_\iota(b,t)=F_\iota(d+b,t)+F_\iota(d-b,t)\qquad(|b|<d).
\end{gathered}
\label{eq:G_def}"""),
# D_def
(r"""D_1(s)=\frac1s+\frac1{s-1}-\frac12\log\pi+\frac12\dg\Bigl(\frac s2\Bigr),\qquad
D_j(s)=\frac1{s^j}+\frac1{(s-1)^j}+\frac{(-1)^{j-1}}{(j-1)!\,2^j}\dg^{(j-1)}\Bigl(\frac s2\Bigr)\quad(j\ge2),
\label{eq:D_def}""",
 r"""\begin{gathered}
D_1(s)=\frac1s+\frac1{s-1}-\frac12\log\pi+\frac12\dg\Bigl(\frac s2\Bigr),\\
D_j(s)=\frac1{s^j}+\frac1{(s-1)^j}+\frac{(-1)^{j-1}}{(j-1)!\,2^j}\dg^{(j-1)}\Bigl(\frac s2\Bigr)\quad(j\ge2),
\end{gathered}
\label{eq:D_def}"""),
# A_def
(r"""\mathcal A(s)=\arg s+\arg(s-1)-\frac T2\log\pi+\Ip\Lo\Gamma\Bigl(\frac s2\Bigr),\qquad\arg s=\arctan\frac T\sigma,\quad\arg(s-1)=\arctan\frac T{\sigma-1},
\label{eq:A_def}""",
 r"""\begin{gathered}
\mathcal A(s)=\arg s+\arg(s-1)-\frac T2\log\pi+\Ip\Lo\Gamma\Bigl(\frac s2\Bigr),\\
\arg s=\arctan\frac T\sigma,\qquad\arg(s-1)=\arctan\frac T{\sigma-1},
\end{gathered}
\label{eq:A_def}"""),
# twosided: each inequality on two lines
(r"""N(T)-\main(T)&\le\mathcal E_u(T)+\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\bigl(a(\log n)\cos(T\log n)+b(\log n)\sin(T\log n)\bigr),\\
N(T)-\main(T)&\ge\mathcal E_\ell(T)+\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\bigl(-a(\log n)\cos(T\log n)+b(\log n)\sin(T\log n)\bigr),""",
 r"""N(T)-\main(T)&\le\mathcal E_u(T)+\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\bigl(a(\log n)\cos(T\log n)\\
&\hspace{10em}+b(\log n)\sin(T\log n)\bigr),\\
N(T)-\main(T)&\ge\mathcal E_\ell(T)+\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\bigl(-a(\log n)\cos(T\log n)\\
&\hspace{10em}+b(\log n)\sin(T\log n)\bigr),"""),
(r"first line of \eqref{eq:twosided}", r"upper bound in \eqref{eq:twosided}"),
(r"gives the second line of \eqref{eq:twosided}", r"gives the lower bound in \eqref{eq:twosided}"),
# argxi_comb
(r"""\frac1\pi\bigl(2\arg\xi(s_1)-\arg\xi(s_2)\bigr)=\frac1\pi\bigl(2\mathcal A(s_1)-\mathcal A(s_2)\bigr)+\frac1\pi\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\frac{e^{-d\log n}-2}{\log n}\sin(T\log n).
\label{eq:argxi_comb}""",
 r"""\begin{split}
\frac1\pi\bigl(2\arg\xi(s_1)-\arg\xi(s_2)\bigr)&=\frac1\pi\bigl(2\mathcal A(s_1)-\mathcal A(s_2)\bigr)\\
&\quad+\frac1\pi\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\frac{e^{-d\log n}-2}{\log n}\sin(T\log n).
\end{split}
\label{eq:argxi_comb}"""),
# Q(L) displayed
(r"""so, with $Q(L)=\sum_{(\mathrm I,j)}c_{\mathrm I,j}L^{j-1}/(j-1)!=\frac{e^{-dL}-2}L-\pi b(L)$, the inner sum over $\iota$ is""",
 r"""so, with
\[
Q(L)=\sum_{(\mathrm I,j)}c_{\mathrm I,j}\frac{L^{j-1}}{(j-1)!}=\frac{e^{-dL}-2}L-\pi b(L),
\]
the inner sum over $\iota$ is"""),
# multline in the proof of the two-sided estimate
(r"""\begin{multline*}
-\frac1\pi\sum_\iota\varepsilon_{\mathrm X}c_\iota\Phi_{\mathrm X}(D_j(s_1))+\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\bigl(-a(\log n)\cos(T\log n)+b(\log n)\sin(T\log n)\bigr)\\
-\frac1\pi\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\frac{e^{-d\log n}-2}{\log n}\sin(T\log n).
\end{multline*}""",
 r"""\begin{multline*}
-\frac1\pi\sum_\iota\varepsilon_{\mathrm X}c_\iota\Phi_{\mathrm X}(D_j(s_1))+\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\bigl(-a(\log n)\cos(T\log n)\\
+b(\log n)\sin(T\log n)\bigr)-\frac1\pi\sum_{n\ge2}\Lambda(n)n^{-\sigma_1}\frac{e^{-d\log n}-2}{\log n}\sin(T\log n).
\end{multline*}"""),
# Lemma M_p item
(r"""\item $M_p\le\sum_{k\ge1}H_{p,k}$; more precisely, for every $K\ge1$, $M_p\le\max_x\sum_{k\le K}\lambda_k(a_k\cos kx+b_k\sin kx)+\sum_{k>K}H_{p,k}$;""",
 r"""\item $M_p\le\sum_{k\ge1}H_{p,k}$; more precisely, for every $K\ge1$,
\[
M_p\le\max_x\sum_{k\le K}\lambda_k(a_k\cos kx+b_k\sin kx)+\sum_{k>K}H_{p,k};
\]"""),
(r"""\[
\max_x\sum_{k\le K}\lambda_k(a_k\cos kx+b_k\sin kx)\le\max_{0\le i<\mathsf M}\sum_{k\le K}\lambda_k(a_k\cos kx_i+b_k\sin kx_i)+\frac\pi{\mathsf M}\sum_{k\le K}kH_{p,k}.
\]""",
 r"""\begin{multline*}
\max_x\sum_{k\le K}\lambda_k(a_k\cos kx+b_k\sin kx)\\
\le\max_{0\le i<\mathsf M}\sum_{k\le K}\lambda_k(a_k\cos kx_i+b_k\sin kx_i)+\frac\pi{\mathsf M}\sum_{k\le K}kH_{p,k}.
\end{multline*}"""),
# tail lemma
(r"""\[
\sum_{n>N_0}\Lambda(n)g(n)\le\sum_{n>N_0}\Lambda(n)G(n)=\int_0^{\infty}\sum_{\substack{n>N_0\\ G(n)>y}}\Lambda(n)\,dy\le\int_0^{G(N_0)}\bigl(1.03883X_y-\psi(N_0)\bigr)dy .
\]""",
 r"""\begin{multline*}
\sum_{n>N_0}\Lambda(n)g(n)\le\sum_{n>N_0}\Lambda(n)G(n)=\int_0^{\infty}\sum_{\substack{n>N_0\\ G(n)>y}}\Lambda(n)\,dy\\
\le\int_0^{G(N_0)}\bigl(1.03883X_y-\psi(N_0)\bigr)dy .
\end{multline*}"""),
# num/low
(r"""\mathrm{num}(u)=u\sum_{i\ge1}iq_iu^{D-i}+d\,u^{D+1}+2u^{D+2},\qquad
\mathrm{low}(u)=|\mathsf p_D|-\sum_{i<D}|\mathsf p_i|u^{D-i}-\varepsilon_Pu^{D+1},""",
 r"""\begin{gathered}
\mathrm{num}(u)=u\sum_{i\ge1}iq_iu^{D-i}+d\,u^{D+1}+2u^{D+2},\\
\mathrm{low}(u)=|\mathsf p_D|-\sum_{i<D}|\mathsf p_i|u^{D-i}-\varepsilon_Pu^{D+1},
\end{gathered}"""),
# C_zeta definition
(r"""C_\zeta=\sum_{p\le P_0}\min\Bigl(\max_{i<\mathsf M}\sum_{k:\,p^k\le N_0}\lambda_k(a_k\cos kx_i+b_k\sin kx_i)&+\frac\pi{\mathsf M}\sum_{k:\,p^k\le N_0}kH_{p,k},\ \sum_{k:\,p^k\le N_0}H_{p,k}\Bigr)\\
&+\sum_{\substack{P_0<p\le N_0\\ p^k\le N_0}}H_{p,k}+\mathrm{Tail},""",
 r"""C_\zeta=\sum_{p\le P_0}\min\Bigl(&\max_{i<\mathsf M}\sum_{k:\,p^k\le N_0}\lambda_k(a_k\cos kx_i+b_k\sin kx_i)+\frac\pi{\mathsf M}\sum_{k:\,p^k\le N_0}kH_{p,k},\\
&\sum_{k:\,p^k\le N_0}H_{p,k}\Bigr)+\sum_{\substack{P_0<p\le N_0\\ p^k\le N_0}}H_{p,k}+\mathrm{Tail},"""),
# K_def
(r"""\mathsf K&=\frac1\pi\Bigl(4d+\frac{\sigma_1^2}2+\frac{\sigma_2(\sigma_2-1)}2+1+\frac{\sigma_2^2}2+\sigma_1(\sigma_1-1)\Bigr)+\frac{|c_{\mathrm R,1}|}{\pi T_0}\Bigl((2\sigma_1-1)+\frac{\sigma_1^2}4+\frac83\Bigr)\\
&\quad+\frac{T_0}\pi\sum_{\substack{\iota=(\mathrm X,j)\in\mathcal B\\ j\ge2}}|c_\iota|\Bigl(\frac2{T_0^{\,j}}+\frac1{(j-1)!\,2^j}\Bigl[(j-2)!\Bigl(\frac2{T_0}\Bigr)^{j-1}+\frac{(j-1)!}2\Bigl(\frac2{T_0}\Bigr)^{j}+j!\,\frac4{3T_0}\Bigl(\frac4{T_0}\Bigr)^{j}\Bigr]\Bigr).""",
 r"""\mathsf K&=\frac1\pi\Bigl(4d+\frac{\sigma_1^2}2+\frac{\sigma_2(\sigma_2-1)}2+1+\frac{\sigma_2^2}2+\sigma_1(\sigma_1-1)\Bigr)\\
&\quad+\frac{|c_{\mathrm R,1}|}{\pi T_0}\Bigl((2\sigma_1-1)+\frac{\sigma_1^2}4+\frac83\Bigr)\\
&\quad+\frac{T_0}\pi\sum_{\substack{\iota=(\mathrm X,j)\in\mathcal B\\ j\ge2}}|c_\iota|\Bigl(\frac2{T_0^{\,j}}+\frac1{(j-1)!\,2^j}\Bigl[(j-2)!\Bigl(\frac2{T_0}\Bigr)^{j-1}\\
&\hspace{8em}+\frac{(j-1)!}2\Bigl(\frac2{T_0}\Bigr)^{j}+j!\,\frac4{3T_0}\Bigl(\frac4{T_0}\Bigr)^{j}\Bigr]\Bigr)."""),
# A(s) expansion
(r"""\mathcal A(s)=\pi+\frac T2\log\frac T{2\pi}-\frac T2+\frac{(\sigma-1)\pi}4+\delta_\sigma,\quad
\delta_\sigma=-\theta_\sigma-\frac{\sigma-1}2\arctan\frac\sigma T+\frac T4\log\Bigl(1+\frac{\sigma^2}{T^2}\Bigr)+\Ip\mathcal R(z),""",
 r"""\begin{gathered}
\mathcal A(s)=\pi+\frac T2\log\frac T{2\pi}-\frac T2+\frac{(\sigma-1)\pi}4+\delta_\sigma,\\
\delta_\sigma=-\theta_\sigma-\frac{\sigma-1}2\arctan\frac\sigma T+\frac T4\log\Bigl(1+\frac{\sigma^2}{T^2}\Bigr)+\Ip\mathcal R(z),
\end{gathered}"""),
# Re D_1
(r"""\Rp D_1(s_1)=\frac12\log\frac T{2\pi}+\delta_1,\qquad\delta_1=\frac12\Rp\frac1{s_1}+\Rp\frac1{s_1-1}+\frac14\log\Bigl(1+\frac{\sigma_1^2}{T^2}\Bigr)+\frac12\Rp\mathcal R'(z_1),""",
 r"""\begin{gathered}
\Rp D_1(s_1)=\frac12\log\frac T{2\pi}+\delta_1,\\
\delta_1=\frac12\Rp\frac1{s_1}+\Rp\frac1{s_1-1}+\frac14\log\Bigl(1+\frac{\sigma_1^2}{T^2}\Bigr)+\frac12\Rp\mathcal R'(z_1),
\end{gathered}"""),
# U_tail
(r"""t^2U(b,t)=c_{\mathrm R,1}\Bigl(\frac{d+b}{1+(d+b)^2u^2}+\frac{d-b}{1+(d-b)^2u^2}\Bigr)+\sum_{\substack{\iota\in\mathcal B\\ j\ge2}}c_\iota\sum_{x=d\pm b}\Phi_{\mathrm X}\Bigl(u^{j-2}(xu+i)^{-j}\Bigr),
\label{eq:U_tail}""",
 r"""\begin{split}
t^2U(b,t)&=c_{\mathrm R,1}\Bigl(\frac{d+b}{1+(d+b)^2u^2}+\frac{d-b}{1+(d-b)^2u^2}\Bigr)\\
&\quad+\sum_{\substack{\iota\in\mathcal B\\ j\ge2}}c_\iota\sum_{x=d\pm b}\Phi_{\mathrm X}\Bigl(u^{j-2}(xu+i)^{-j}\Bigr),
\end{split}
\label{eq:U_tail}"""),
# interpolation
(r"""\[
|\mathcal Z(s)|\le\bigl(A_i|Q+s|^{1+e_i+\varepsilon}\bigr)^{\frac{\varsigma_{i+1}-\sigma}{\varsigma_{i+1}-\varsigma_i}}\bigl(B_i|Q+s|^{1+e_{i+1}+\varepsilon}\bigr)^{\frac{\sigma-\varsigma_i}{\varsigma_{i+1}-\varsigma_i}}\le\max(A_i,B_i)\,|Q+s|^{1+\mathfrak e(\sigma)+\varepsilon},
\]""",
 r"""\begin{multline*}
|\mathcal Z(s)|\le\bigl(A_i|Q+s|^{1+e_i+\varepsilon}\bigr)^{\frac{\varsigma_{i+1}-\sigma}{\varsigma_{i+1}-\varsigma_i}}\bigl(B_i|Q+s|^{1+e_{i+1}+\varepsilon}\bigr)^{\frac{\sigma-\varsigma_i}{\varsigma_{i+1}-\varsigma_i}}\\
\le\max(A_i,B_i)\,|Q+s|^{1+\mathfrak e(\sigma)+\varepsilon},
\end{multline*}"""),
# Trudgian-Yang breakpoints: allow line breaks after the commas
(r"""$\varsigma\in\{\frac{88225}{153852},\frac{521}{796},\frac{53141}{76066},\frac{3620}{5119},\frac{52209}{69128},\frac{1389}{1736},\frac{134765}{163248},\frac{18193}{21906},\frac{249}{280},\frac{277}{300}\}$""",
 r"""$\varsigma\in\{\frac{88225}{153852},\allowbreak\frac{521}{796},\allowbreak\frac{53141}{76066},\allowbreak\frac{3620}{5119},\allowbreak\frac{52209}{69128},\allowbreak\frac{1389}{1736},\allowbreak\frac{134765}{163248},\allowbreak\frac{18193}{21906},\allowbreak\frac{249}{280},\allowbreak\frac{277}{300}\}$"""),
# asymptotic main term: shorter wording of the bound on the sum
(r"""since $|\sum_{n\ge2}\frac{\Lambda(n)}{\log n}n^{-\sigma}\sin(T\log n)|\le\log\zeta(\sigma)$.""",
 r"""since the sum in \eqref{eq:argxi} is bounded in modulus by $\log\zeta(\sigma)$."""),
# the two long tables of Appendix A in a smaller font
(r"""\begin{longtable}{@{}rrrrrrr@{}}""", r"""\begingroup\footnotesize\setlength{\tabcolsep}{4pt}\begin{longtable}{@{}rrrrrrr@{}}"""),
(r"""\begin{longtable}{@{}rllr@{}}""", r"""\begingroup\footnotesize\setlength{\tabcolsep}{4pt}\begin{longtable}{@{}rllr@{}}"""),
# table of the six lines (nine columns): smaller font
(r"""\begin{tabular}{@{}lcccccccc@{}}""", r"""\footnotesize\setlength{\tabcolsep}{3.5pt}\begin{tabular}{@{}lcccccccc@{}}"""),
]
