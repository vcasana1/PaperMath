import sys; sys.path.insert(0, '..')
from lst_common import *
for nb in [0.05, 1.0, 20.0]:
    for U in [2, 20]:
        base = float(log_VU(nb, U))
        row = []
        for rho in [0.0, 1e-6, 1e-5, 1e-4, 1e-3]:
            lv = log_VU_damped(nb, rho, U)
            est = invert_VU(lv, U)
            row.append('%.2e:%+.4f' % (rho, est/nb-1))
        print('nbar', nb, 'U', U, 'exact', base, ' | ', '  '.join(row))
