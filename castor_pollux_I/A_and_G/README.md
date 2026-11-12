# A and G, each on its own (v1, 2026-11-12)

Results about A and G separately, without using G - A.

- `certify_ImA_v1.py`: ball-arithmetic (python-flint 0.9.0, 80 bits) certificate that Im A > 0 on
  B1 = [-38.2, 2] x [5, 40.2] and B2 = [2, 8.4] x [5, 8.4]. Outside these boxes, Im A > 0 for t >= 5
  follows analytically (integral comparison for sigma <= 2, |s-2| >= 40.1; Binet bound for sigma >= 2, |s| >= 8.33).
  Output: `certify_ImA_v1_output.txt`.
- `G_zero_free_v1.py`: for sigma > 1, G = B + C D with B = A + C, C = (pi/s) cot(pi s/2), D = sum_{n>=2} n^{-s};
  G(s) != 0 whenever sum_{n>=2} n^{-sigma} < |B/C|. Computes sigma_G(t) for 10 <= t <= 300 and compares with the
  zeros of G (all 137 lie to the left, minimum margin 0.576). Output: `G_zero_free_v1_output.txt`,
  figure `fig_G_zero_free_v1.png`.

The `.py.txt` files are text copies of the scripts.
