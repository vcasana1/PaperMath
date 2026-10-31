# Upper bound for mu(sigma) on [1/2,1] from published sources only, as a piecewise linear function through nodes
# (sigma_i, e_i) with mu(sigma_i) <= e_i a theorem in each case:
#  - 1/2: 13/84 (Bourgain 2017, Thm 5);
#  - breakpoints of Trudgian-Yang, Toward optimal exponent pairs, arXiv:2306.05599v3, Thm 2.4 (pieces are continuous);
#  - l-k for the exponent pairs (k,l) of Tao-Trudgian-Yang, arXiv:2501.16779v1, Thm 20, via Lemma 23 (mu(l-k) <= k);
#  - Heath-Brown 2017 (Proc. Steklov Inst. Math. 296), Thm 2: pairs (2/((n-1)^2(n+2)), 1-(3n-2)/(n(n-1)(n+2))+eps), n >= 3,
#    giving mu(sigma_n) <= mu_n, sigma_n = 1-(3n^2-3n+2)/(n(n-1)^2(n+2)), mu_n = 2/((n-1)^2(n+2)) (continuity of mu), 6 <= n <= 399;
#  - (1, 0) (zeta(1+it) << log t).
# The profile is the lower convex hull of these points (nodes above a chord of two others are dropped: the chord is a
# valid bound by the Phragmen-Lindelof interpolation lemma, and smaller).
from fractions import Fraction as Fr
TY = [(Fr(1,2),Fr(88225,153852),Fr(31,84),Fr(3,7)),(Fr(88225,153852),Fr(521,796),Fr(220633,620612),Fr(62831,155153)),
 (Fr(521,796),Fr(53141,76066),Fr(1333,3825),Fr(1508,3825)),(Fr(53141,76066),Fr(3620,5119),Fr(405,1202),Fr(227,601)),
 (Fr(3620,5119),Fr(52209,69128),Fr(49318855,170145110),Fr(52938216,170145110)),(Fr(52209,69128),Fr(1389,1736),Fr(471957,1682490),Fr(502648,1682490)),
 (Fr(1389,1736),Fr(134765,163248),Fr(2841,10316),Fr(3016,10316)),(Fr(134765,163248),Fr(18193,21906),Fr(859,3214),Fr(908,3214)),
 (Fr(18193,21906),Fr(249,280),Fr(5*8707,180277),Fr(5*9067,180277)),(Fr(249,280),Fr(277,300),Fr(29,130),Fr(30,130))]
PAIRS = [(Fr(89,1282),Fr(997,1282)),(Fr(652397,9713986),Fr(7599781,9713986)),(Fr(10769,351096),Fr(609317,702192)),(Fr(89,3478),Fr(15327,17390))]
def hb(n): return 1-Fr(3*n*n-3*n+2, n*(n-1)**2*(n+2)), Fr(2, (n-1)**2*(n+2))
def raw_nodes(nmax=400):
    for (l1,h1,a1,b1),(l2,h2,a2,b2) in zip(TY,TY[1:]): assert a1-b1*h1 == a2-b2*h1
    nodes = {}
    for lo,hi,a,b in TY: nodes[lo] = a-b*lo; nodes[hi] = a-b*hi
    for k,l in PAIRS: nodes[l-k] = min(nodes.get(l-k, Fr(1)), k)
    for n in range(6, nmax): s,m = hb(n); nodes[s] = min(nodes.get(s, Fr(1)), m)
    nodes[Fr(1)] = Fr(0)
    return sorted(nodes.items())
def nodes_published(nmax=400):
    P = raw_nodes(nmax); hull = []
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    for p in P:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0: hull.pop()
        hull.append(p)
    return hull
if __name__ == '__main__':
    H = nodes_published()
    print(len(H), 'nodes; first ones:')
    for s,e in H[:14]: print('  sigma = %-20s  e = %-18s  (%.6f, %.6f)' % (s, e, s, e))
