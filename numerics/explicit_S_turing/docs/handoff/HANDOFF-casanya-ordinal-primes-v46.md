# HANDOFF — casanya_ordinal_primes v46 (2026-10-30)

Paper: "Prime-corrected Riemann--von Mangoldt approximation of Riemann zeta imaginary parts and bounds for its argument", V. Casaña-Giner (UNED, Madrid, Spain; vcasana1@alumno.uned.es).
Input: casanya_ordinal_primes_v41.tex (user's, untouched). Claude produced v42–v46 on copies; each delivered as .tex/.txt/.pdf/.zip + diff.
Session scratchpad: /tmp/claude-0/-home-claude/fd3d3839-ef37-5333-8273-1fc922053f5c/scratchpad/{build,out,tools}
(build/code = Python programs of Appendix A; tools/gen_inline.py = inline tooltip generator; stub/ = local stubs for datetime2/soul so pdfcomment compiles in the cloud container; NOT in the zip).

## RULE: ask ALWAYS before changing anything. Literal substitutions on a copy, new version number, show diff.

## Done (v41 → v46)
- v42: no version number in \date; author block (UNED, Madrid, Spain, email, ORCID; pdfauthor with accents); labels with clock/envelope renamed (thm:asymptotic, cor:distance, sec:distance, rem:bare_point, subsec:tau_intro, eq:intro_tau, eq:asymptotic_formula, eq:distance_explicit, subsec:proof_asymptotic, prop:distance_sharp, cor:identity_distance, eq:identity_distance); Lean appendix + all Lean/GitHub/earlier-manuscript references removed (bib AlpogeFurmanZeta23, CasanaPaperMath2026 deleted); Data availability = programs reproduced in Appendix A; 48 unnumbered displays numbered (eq:disp_NN; abstract untouched; two \qedhere removed); Trudgian double cite split; arXiv DOIs for BellottiWong, Bourgain, Kargin, LeClair2016; tooltips inline in preamble (no external tips file); .py comments cleaned (no file names, no "clock", no stale numbering in comments).
- v43: records table: \midrule above last row removed; last row "Casa\~na-Giner [This work]".
- v44: new title (above).
- v45: intro paragraphs 1–3 rewritten (primes via Euler product phases, arithmetic correction = adding Φ to N0); "ordinate(s)" removed everywhere → "imaginary part(s)" (γ_k), "points τ_k", profile node heights → "second coordinates".
- v46: heavy "not an imaginary part" → compact t∉{γ_k} (20 places).

## Independent review of v46 — PROPOSALS, NOT APPLIED (awaiting user's decision)
(A) definite errors
- A1 L1595: leftover from Lean deletion: "...computed in the present appendix, from the closed form by rationals; the decimals printed here are not themselves certified..." — program does no rational bounding. Proposed: decimals are 40-digit floating point, two evaluations agree to >20 digits, all inequalities used hold with margin ≥3e-10 (smallest Λ(e_B)−0.096816006 = 3.2e-10); not interval-certified.
- A2 L930 footnote: "The bound log ζ(σ#)≤1.52499 computed in Appendix A uses ζ(σ)≤Σ..." — program uses mpmath.zeta directly; inequality belonged to Lean. Reword ("Appendix A evaluates ζ(σ#) numerically; a rigorous bound ... follows from ...") or delete footnote.
- A3 L1611: "the point τ_k of \CGeqref{eq:distance_explicit}" → \CGeqref{eq:intro_tau} (error already in v41).
- A4 constantes_v5.py print strings/outputs: "explicit nodes (4.3)" should be (4.5); "closed form (5.3)" should be (5.9). Fix strings + re-run, or remove numbers.
- A5 L1676 bib Fazzari: "Selberg\'s" renders as accent → "Selberg's".
- A6 L279 (new intro): Selberg/Tsang/Fujii prove the mean-square approximation for p≤x, x a small power of t; the extension to ~√t primes is the paper's Lemma (lem:fourth). Reword accordingly.
(B) likely problems
- B1 L279 sign wording: phase of (1−p^{-s})^{-1} is −arg(1−p^{-s}); say "S is formally the sum of the normalized phases −(1/π)arg(1−p^{-1/2-it})".
- B2 L279: Φ is defined in eq:F_def (Φ_m in eq:Euler_phase); and "points of the equation N0+Φ=k−1/2" contradicts sublevel definition → "points attached to the levels N0+Φ=k−1/2".
- B3 L301: "tied to the height (imaginary parts of the zeta zeros)" damaged by script → "at height t, a number tied to the height rather than a free parameter, and bounds the mean-square error of approximations τ_k^C that are increasing and indexed by construction".
- B4 L434: "real parts or multiplicities of the zeros (i.e., RH)" → "real parts of the zeros (RH) or about their multiplicities".
- B5 L441: "his Theorem~\CGref{thm:known_PL}" prints this paper's number as Fiori's → "his Corollary 3, stated as Theorem~\CGref{thm:known_PL}".
- B6 L524 "a recovered simplicity certificate" → "a deterministic certificate for simple critical-line zeros"; L1282 "The final certificate is included here with a self-contained proof because it applies to any continuous ordinal model." → antecedent lost.
- B7 L1545 "Further higher-moment and finite Euler-product results are not claimed here." vague leftover → delete or make specific.
- B8 L899, 917–919, C3(100)<10.6 (margin 0.0014): constants now rest on floating-point evaluation (Lean bounds removed); state so (see A1).
- B9 23 labels have no tooltip (thm:known_*, sec:distance, sec:meansquare, subsec:proof_*, rem:varpi_weak, tab:records, eq:C1_value, eq:backlund_conditions, eq:explicit_assembled, eq:hinge_integrals, eq:identity_one_gap, eq:selberg_dyadic, eq:varpi_weak) → hover shows raw label; generator skips them. Also 10 tips contain unresolved "[label]" strings.
- B10 L285 "only beyond the stated crossing height" (not yet stated) → "only for log T>2425.84".
(C) style: title "its" ambiguous; L316 "bring it"→"bring them"; L543 add "counted with multiplicity"; L309 "through points t∉{γ_k}"; L1043 "a term γ_k equal to a"/"first term beyond b" (Thm 7.3 general sequence); L495 "imaginary parts of ζ"→"of the zeros of ζ"; L1553 "prime-complemented"→"prime-corrected"; L1591 Newton→findroot (secant); L457 "[This work]" looks like a citation (user chose it); one-sentence paragraphs L493, L811, stray \par L364; L596 notation table "threshold"; L1329–1330 D,B,E reuse symbols; casanya_method output "x_k" vs τ_k^C; Kargin/Korolev/Gonek/LeClair described twice; L620 "(c) only on the 1-line".
Checked OK: all constants consistent (0.0968160063, 0.6083129, 0.09783, 0.7214, 10.6, 10.7, 10.2, 11.55, 2425.84, 933.47, 1.87781, C3(100)=10.5986…); all labels resolve; no Lean/GitHub left; all 42 bibitems cited; compile clean.

## Added by user (2026-10-30) — terminology, to apply in v47 (PENDING, ordered by user)
- T0 Define the term ONCE, in the introduction and at (1.10): "the Euler phase of the prime $p$, $-\frac1\pi\arg(1-p^{-1/2-it})$" — and always use it that way.
- T1 In the 11 occurrences of "Euler phase(s)" in the body: "prime phases" or "Euler phases of the primes" (e.g. "defined by the Euler phases of finitely many primes"), so each occurrence links to the title. (User has not yet chosen between the two forms.)
- T2 "prime-complemented" (1 occurrence, ~L1553) → "prime-corrected", to match the title.
- Title: user asked for title PROPOSALS before any change (no title change without his choice).

## v47 DONE (2026-10-30) — user: "usa este [título 4] y corrige todo lo que has dicho"
- Title: "Bounds for the argument of the Riemann zeta function and a prime-corrected Riemann--von Mangoldt approximation of its zeros" (\title + pdftitle).
- Applied: A1–A6, B1–B10, T0–T2 (form chosen: "Euler phases of the primes"; T0 defined in intro and at (1.10)), C2–C8, C10–C13, C15.
- A2: bound log ζ(σ#) ≤ 1.5249836 checked with N=10^4 in the footnote inequality (mpmath, 30 digits).
- A4: constantes_v5.py + output: "(4.3)"→"(4.5)", "(5.3)"→"(5.9)" edited by hand in both (only label text; cannot rerun identically: header prints Python 3.13.17).
- C13: casanya_method.py prints tauC_k instead of x_k; RE-RUN, numbers identical.
- B9: new generator tools/gen47.py (balanced-brace newlabel parser, tables, \texorpdfstring, refs resolved to numbers): 206 tooltips, 0 missing, 0 unresolved.
- NOT applied (need user): C9 "[This work]" (his own choice), C14 trimming duplicated literature descriptions (deletes content), C16 ISBNs; C' vs "not the same at each occurrence" in notation table left as is.
- Files: scratchpad/b47 (build), scratchpad/out (deliverables), scratchpad/c47 (code v47).

## Certification (2026-10-30, IN PROGRESS — NOT yet in the paper; user will first send a list of corrections)
- User: "ve certificando y prepara ese material para incorporarlo donde se deba, pero aún no"; "con un número elevado de decimales"; "certifica TODO lo del paper, hasta si es externo y aquí lo usas".
- scratchpad/cert/constants_arb.py (+ constants_arb_output.txt): python-flint 0.9.0 Arb, 1100 bits, 100 digits printed. ALL CHECKS PASSED: Λ(e_B)=0.0968160063238489656… (closed form = rigorous Arb integration), margin above 0.096816006 = 3.2385e-10; 2πΛ(e_B)=0.60831290843…; Λ(0)=0.0786252790902…, 2πΛ(0)=0.494017198352…; C_1=0.0978292318785179…<0.09783; C_2=0.72134647976617…<0.7214; log ζ(σ#)=1.52498355868919…<1.52499; log(ζ(c)/ζ(2c))=12.6246665092014…; χ=1.00691797810…, K_1=2.71660628886…, K=2.73539971168…<2.74; E/(2π)=0.000540539646…<0.00055; C_3(100)=10.5986023483…<10.6 (exact-difference version 10.5985454733…); crossing BW log T=2425.8385801225889… (sign structure certified on [1,∞)); crossing Yang log t=933.46789604929….
- Full inventory of every numerical claim (own + arithmetic on external constants) being produced in scratchpad/cert/inventory.md and paper_numerics_arb.py.
- DONE: scratchpad/cert/paper_numerics_arb.py (+_output.txt, exit 0) and inventory.md: 62 substantive items, 112 asserts pass on whole Arb balls (256 bits, 40 digits printed). External constants recorded as quoted.
- FAILURES (stated numbers with "…" that are rounded UP, not truncated) — to add to the correction list, NOT applied:
  F1 L974 "640δ#−112=48.0008…" true 48.00079999984… → "48.0007…" (only >0 is used; certified)
  F2 L314, 409, 1628 "log T>2425.8386…" true 2425.83858012258894… → "2425.8385…" (or 2425.83858…)
  F3 L330 (my v47 B10 edit) and L1622 "only for log T>2425.84" is false on (2425.8386,2425.84] → "for log T>2425.8385…" / "2425.83…"
  F4 L1628 "log t=933.47…" true 933.46789604929… → "933.4679…" (statement "as soon as log t>933.5" is correct)
- Printing digits for the appendix: proposed 20 (user asked how many a normal paper uses; awaiting answer).

## v48 DONE (2026-10-30) — user: "corrige todo lo del paper relativo a anexos y certificados ya"; 20 digits printed, 256 bits internal
- Text always says certified (ball arithmetic): proof Cor 1.2, (5.10), footnote log ζ(σ#)=1.5249835586…; Appendix A: mpmath program = floating point, certified by last program; new paragraph + \lstinputlisting code/certify_arb.py and its output (python-flint 0.9.0, FLINT 3.6.0, 256 bits, 20 digits, 61 checks/136 conditions, exit 0, refs by paper numbering); Arb cited also for the 1.878 program.
- F1–F4 applied with truncation convention: 48.0007…, 2425.8385… (abstract, 1.2, conclusion, App. A), 933.4678….
- Bib: Johansson2017 (IEEE Trans. Comput. 66 (2017) 1281–1292, doi:10.1109/TC.2017.2690633), FLINT (version 3.6.0, flintlib.org). Practice checked: Bellotti–Wong (Math. Comp.) "We used the ARB ball arithmetic package [Joh17]".
- 47 pages, 208 tooltips, 0 missing. Note: the old mpmath output still prints "crossing ... 2425.8386" (nstr rounding, program output, not text).
- Certification sources: scratchpad/cert/{constants_arb.py, paper_numerics_arb.py (audit), inventory.md, certify_arb.py}. Not uploaded to GitHub (no GitHub in this session).

## v49 DONE (2026-10-30) — user's list of 12 review items (ChatGPT cross-review of v46), "solo lo necesario y suficiente"
- Applied (11 literal replacements, only in the affected sentences): 1 Yang Thm 3.3(b) stated as published + used only m=4..9 with constant 2 per Rem 4.5(ii); 3 real-part step for Montgomery–Vaughan (∫P² ≪ X absorbed); 4 "strictly increasing" (F continuous); 5 excursion effect stated precisely (levels between min and max on I); 6 "In the present argument, the number of primes…"; 7 conclusion: removes loglog T from the proved upper bound, no asymptotic claimed; 8 split 0.10076→0.10073687 (disc limit, 0.0000231…) and →0.09782899 (reflection, 0.0029078…), "essentially"; 9 full induction proof for higher moments of s_k in Remark meansquare_comparison (+ Selberg note "every k"); 10 Kargin enumeration caveat in intro.
- Already fixed earlier: item 2 (v47, "points attached to the levels"), item 11 (v47/v48: 208 tooltips, none missing).
- Item 12 NOT applied: reviewer says user asked "[Present work]", but the user wrote "Casaña-Giner [This work]" in this chat; kept.
- 48 pages, compile clean.

## v50 FINAL (2026-10-30) — "versión final completa con declaración IA"
- Applied review-of-v49 items 1–11, 13 (Kargin ref→1.2 and window N≤k≤N+⌊N^θ⌋−1; A_ε'≥2 in Cor 1.2 proof; Im-part step in §1.3 item 1 with P=Σ_{X<p<Y}p^{-1/2-it}; levels min<k−1/2≤max; Remark 4.2 0.53 also for |ϖ|/π<1/2; remainder <1e-6 of split; App. B rows Selberg (every k, Rem 8.5) and MV (§1.3, Lemma 9.2); local symbols: Gonek paragraph, Section 9; explicit Ψ_j coefficients; bookmarks \texorpdfstring; "in root-mean-square").
- AI Declaration (after Data availability): Claude (Anthropic) Fable 5.1, Opus 5.5, Sonnet 5.5; ChatGPT (OpenAI) Astra 6; Microsoft 365 Copilot (GPT-5 reasoning) only reviewed drafts, not Python/Lean 4; Python of App. A and Lean 4 formalization "written with Claude" (Lean not presented); user's earlier request "solo Fable 5.1" declined as inaccurate, user accepted neutral listing. Then "Mathematical software" section (Python 3.13, mpmath 1.4.1, numpy, python-flint 0.9.0 / Arb / FLINT 3.6.0).
- 48 pages; 208 tooltips; compile clean. Journal: user weighing IJNT vs Transactions LMS (TLMS SJR 2025 0.280 Q3; IJNT Journal Metrics Q3, JCR IF 0.674 (2020)). For submission: \CGplaintrue switch gives copy without pdfcomment; World Scientific may require its template at final stage; ~10 pages of code listings could go to supplementary material.

## v51 (2026-10-30): Theorem 3.3(b) restated as used: 4<=m<=9, 1.546 for |t|>=T_m (Yang §3.2), 1.878 for 3<=|t|<=T_m (§3.1 corrected, Rem 4.5(ii)), hence 2 for |t|>=3; Yang's Thm 1.1 general claim only quoted. Appendix B row updated.

## v52 (2026-10-30): two external reviews of v50 (Copilot 15 points; second reviewer 5 points)
- Applied: new Lemma 2.1 (one-sided limits S(γ±)); Prop 6.2 "equivalent" restricted to the two bounds; maximal lemma M(D−D'')<Θ/2 + subadditivity; q_f = integer level discrepancy, q_f≤|f−N|+1/2; Lemma 7.5 J=⌊log2(L_T/2)⌋; Lemma 7.6 constants absolute; MV "exactly when m=O(√U)" for this expansion; dyadic Selberg with R(2T)−R(T)=o(T loglogT); higher moments now Proposition 8.6 with proof (Remark 8.5 shortened); Theorem 8.1 for absolutely continuous F (proof adjusted; Thm 9.3 proof simplified; intro + notation table updated); Lemma 9.2 uniform in m; Thm 9.5 scope sentence in statement; Remark 7.7 "for k≥2" (N_0(0+)=7/8); Remark 7.4 atoms at integers, D_ℓ are masses; monotonicity item 2 wording; impersonal "only (c) is needed", "known to the author".
- Not applied: transfer-theorem equivalence N(t)<k−1/2 ⇔ t<γ_k is exact with right-continuous N (reviewer wrong); listings missing = reviewers read only the .tex (zip has code/).
- Tooltip generator tools/gen52.py: citations → bibliography numbers, balanced optional titles, newline-safe \frac; 210 tooltips. Numbering of all existing labels unchanged (new: lem:onesided 2.1, prop:higher_moments 8.6).

## v53 (2026-10-30): user angry that plain author-year citations were left (they came from v41): all citations now \CGcite (line 'previous values', Selberg/Tsang/Fujii, Selberg mean square, Mertens' theorem -> Thm ref); bibliography in World Scientific/IJNT style (initials spaced, 'and' before last author, journal italic, volume bold, books italic with (Publisher, City, Year)); fixed false inequality 0.09783-0.09782899...=0.0000010... (was '<1e-6', it is 1.0045e-6); Thm 9.5 sentence: positivity iff sum (2v_k)^{2j} < #K_T (collective). ws-ijnt.cls not obtainable from the container (worldscientific.com blocked). 49 pages.

## v54 (2026-10-30): only change: intro 'O(1/log T), at most a bounded multiple of the mean zero spacing' (no ≍ claimed). Rule from user: corrected error has only an upper bound; never write ≍ nor 'reduces by a factor loglogT'. Checked: all other mentions say 'from the proved upper bound/order'.

## v55 (2026-10-30): submission system rejects zips with subfolders. Only change: the 8 \lstinputlisting paths code/xxx -> xxx; zip is flat (tex + 4 .py + 4 outputs, no PDF, no folders). PDF text identical to v54. Build dir scratchpad/b55flat. Rule: submission zips must be flat.

## v56 (2026-10-30): journal system could not process the v55 PDF (692 pdfcomment /Widget tooltip annotations without AcroForm, built with local datetime2/soul stubs). v56 = submission copy: \CGplaintrue (no pdfcomment/tooltips; hyperlinks and backrefs kept), \pdfminorversion=4 \pdfobjcompresslevel=0; compiled with real packages only, PDF 1.4, qpdf clean, 918 links, 0 widgets; flat zip. Content identical. v55 remains the copy with hover.
