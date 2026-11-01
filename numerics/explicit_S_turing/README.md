# Explicit and asymptotic bounds for S(T): Turing–Amberger–Bellotti–Wong kernels and Jensen discs

V. Casaña-Giner. Numerical certificates in Arb ball arithmetic (python-flint 0.9.0, 256 bits). Not Lean files; not
imported by the Lake project. The article is `docs/zenodo_note/` (latest `casanya_turing_jensen_vN`); deposited at Zenodo, doi:10.5281/zenodo.23858827 (v9, 1 Nov 2026).

Notation: `N(T)` counts zeros with `0 < γ ≤ T`; `main(T) = (T/2π) log(T/2πe)`; `a = limsup |S(T)|/log T`.

## Results (all certified)

| statement | where |
|---|---|
| `|N(T) − main(T)| ≤ min_k (A1_k log T + A3N_k)`, `|S(T)| ≤ min_k (A1_k log T + A3S_k)` for all `T ≥ 1`, six lines; last line `0.08382 log T + 5.326` / `0.08382 log T + 4.444` | `family/line_*/summary_pp.json` |
| `a ≤ C_H < 0.0748596142711` (hybrid: kernel + 90 Jensen discs, published-source profile e_P) | `hybrid_asymptotic/hyb_m10_P.json`, `cert_m10P.txt` |

## Programs of the article

Certification (rigorous): `hybrid_asymptotic/certutil.py` (helpers, directed decimal rounding, provenance),
`certify_hybrid.py` (kernel inequality with or without discs, and C_H), `profile_published.py` (the profile e_P),
`family/cz_gen_pp.py` (Euler-product constant with the per-prime phase maximum), `family/elem_gen.py` (elementary part,
modes N and S), `family/certify_line_pp.py` (driver of one line).
Search (floating point, not used in any proof): `hybrid_asymptotic/lpcommon.py`, `explore_discs.py` (hybrid LP),
`kernel_only.py` (Remark on the infimum), `family/opt_line.py` (SOCP of one line), `family/sweepC.py`, `sweepD.py`.

Every certificate starts with the SHA-256 of its input and of the programs that produced it; the build of the note
(`docs/zenodo_note/gen_appendix.py`) checks these digests against the files it reproduces.

## Running everything

    ./run_certificates.sh [JOBS]      # all 25 certificates in parallel (JOBS processes, default = cores)
    python3 rerun/finalize.py         # install the new certificates, recompute the summaries, check the constants
    cd docs/zenodo_note && python3 gen_appendix.py && python3 gen_values.py && python3 build.py vN

Requirements: `pip install python-flint==0.9.0 numpy` for the certificates, plus `scipy cvxpy clarabel` for the search
programs. CPU times on a 2-vCPU machine: l6000 kernel 59 min, l400 38 min, hybrid 14 min, the rest a few minutes each.

## Other folders

`hybrid_explicit/`: exploration of an explicit hybrid for all T (open question of the note). `turing_backlund/`,
`explicit_allT_BWkernels/`: earlier experiments (Backlund scan; Bellotti–Wong kernels certified for all T ≥ 1).
`rerun/`: the lane scripts of the 1 Nov 2026 rerun and `finalize.py`. `*/attic/`: superseded programs and data, kept for
the record (READMEs inside). `session_2026-10-30_31/`: copy of the session scratchpad. `docs/handoff/`: handoff notes.
