# Shared helpers of the certification programs (python-flint / Arb ball arithmetic at 256 bits).
#   A(q)            exact ball of a Fraction or of an integer (floats are refused)
#   box(lo, hi)     ball containing the interval [lo, hi]
#   exact(x)        the rational value of an exact (zero-radius) arb
#   up_str(x, n)    decimal string with n significant digits that is >= every point of the ball x (directed rounding)
#   down_str(x, n)  decimal string with n significant digits that is <= every point of the ball x
#   provenance(...) lines with the SHA-256 of the input and program files and the library versions, for the record
# The .str() method of arb rounds to the nearest decimal, so it must not be used to print an upper or lower bound;
# every bound printed or written to a JSON file by the certification programs goes through up_str / down_str.
import hashlib, os, sys, platform
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
import flint
from flint import arb, ctx
ctx.prec = 256

def A(q):
    # exact ball of a Fraction or an integer; floats are refused, so that no binary approximation of a decimal enters silently
    if isinstance(q, Fr): return arb(q.numerator)/arb(q.denominator)
    assert isinstance(q, int), 'A() takes a Fraction or an integer, got %r' % (q,)
    return arb(q)

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

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh: h.update(fh.read())
    return h.hexdigest()

def provenance(*paths):
    # one line per file (name and SHA-256), then the versions of Python and python-flint and the working precision
    lines = ['%s sha256 %s' % (os.path.basename(p), sha256(p)) for p in paths]
    lines.append('python %s, python-flint %s, precision %d bits' % (platform.python_version(), getattr(flint, '__version__', '?'), ctx.prec))
    return '\n'.join(lines)

if __name__ == '__main__':
    x = arb(1)/3
    print(x.str(12, radius=False), up_str(x, 12), down_str(x, 12))
    y = -arb(1)/7
    print(y.str(12, radius=False), up_str(y, 12), down_str(y, 12))
