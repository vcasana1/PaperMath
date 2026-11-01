# Shared helpers of the certification programs (python-flint / Arb ball arithmetic at 256 bits).
#   A(q)            exact ball of a Fraction or of a Python number
#   box(lo, hi)     ball containing the interval [lo, hi]
#   exact(x)        the rational value of an exact (zero-radius) arb
#   up_str(x, n)    decimal string with n significant digits that is >= every point of the ball x (directed rounding)
#   down_str(x, n)  decimal string with n significant digits that is <= every point of the ball x
# The .str() method of arb rounds to the nearest decimal, so it must not be used to print an upper or lower bound;
# every bound printed or written to a JSON file by the certification programs goes through up_str / down_str.
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from flint import arb, ctx
ctx.prec = 256

def A(q):
    return arb(q.numerator)/arb(q.denominator) if isinstance(q, Fr) else arb(q)

def box(lo, hi):
    return A(lo).union(A(hi))

def exact(x):
    assert x.is_exact() and x.is_finite(), x
    m, e = x.man_exp()
    return Fr(int(m))*Fr(2)**int(e)

def _dir_str(q, n, rounding):
    with localcontext() as c:
        c.prec = n; c.rounding = rounding
        dec = Decimal(q.numerator)/Decimal(q.denominator)      # correctly rounded to n significant digits
    return format(dec, 'f')

def up_str(x, n):
    u = exact(x.upper()); s = _dir_str(u, n, ROUND_CEILING)
    assert Fr(s) >= u, (s, u)
    return s

def down_str(x, n):
    l = exact(x.lower()); s = _dir_str(l, n, ROUND_FLOOR)
    assert Fr(s) <= l, (s, l)
    return s

if __name__ == '__main__':
    x = arb(1)/3
    print(x.str(12, radius=False), up_str(x, 12), down_str(x, 12))
    y = -arb(1)/7
    print(y.str(12, radius=False), up_str(y, 12), down_str(y, 12))
