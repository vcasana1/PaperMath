# Best known upper bound for mu(sigma), 1/2 <= sigma <= 1: ANTEDB (Tao-Trudgian-Yang), Table 6.2 of
# https://teorth.github.io/expdb/blueprint/zeta-growth-chapter.html  (Trudgian-Yang Thm 2.4-2.6; Tao-Trudgian-Yang
# arXiv:2501.16779 Thm 5.22, 5.23, Cor 6.8; Heath-Brown 2017 exponent pairs, Thm 6.14).  Exact rational nodes.
from fractions import Fraction as Fr
PIECES = [  # (lo, hi, a, b): mu <= a - b*sigma on [lo, hi]
 (Fr(1,2), Fr(88225,153852), Fr(31,84), Fr(3,7)),
 (Fr(88225,153852), Fr(521,796), Fr(220633,620612), Fr(62831,155153)),
 (Fr(521,796), Fr(53141,76066), Fr(1333,3825), Fr(1508,3825)),
 (Fr(53141,76066), Fr(454,641), Fr(405,1202), Fr(227,601)),
 (Fr(454,641), Fr(1744,2411), Fr(779,2590), Fr(423,1295)),
 (Fr(1744,2411), Fr(951057,1298878), Fr(179,622), Fr(96,311)),
 (Fr(951057,1298878), Fr(1389,1736), Fr(157319,560830), Fr(251324,841245)),
 (Fr(1389,1736), Fr(587779,702192), Fr(2841,10316), Fr(754,2579)),
 (Fr(587779,702192), Fr(7441,8695), Fr(1691,6554), Fr(890,3277)),
 (Fr(7441,8695), Fr(277,300), Fr(29,130), Fr(3,13))]
def hb(n): return 1-Fr(3*n*n-3*n+2, n*(n-1)**2*(n+2)), Fr(2, (n-1)**2*(n+2))
def nodes_tty(nmax=400):
    nd = [(lo, a-b*lo) for lo, hi, a, b in PIECES]+[(PIECES[-1][1], PIECES[-1][2]-PIECES[-1][3]*PIECES[-1][1])]
    # Heath-Brown nodes sigma_n (n >= 7) beyond 277/300; the segment 277/300 -> sigma_7 is the line through both
    # (convexity of mu; both endpoints are proved bounds)
    for n in range(7, nmax): nd.append(hb(n))
    nd.append((Fr(1), Fr(0)))
    return nd
if __name__ == '__main__':
    nd = nodes_tty(12)
    for s, e in nd: print(float(s), float(e))
    # continuity check of the pieces
    for (l1,h1,a1,b1),(l2,h2,a2,b2) in zip(PIECES,PIECES[1:]): print('jump at %.5f: %.2e'%(float(h1), float((a1-b1*h1)-(a2-b2*h1))))
