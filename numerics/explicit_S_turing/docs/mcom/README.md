# Mathematics of Computation version

Built from the Zenodo-note source `../zenodo_note/body.tex` by `build_mcom.py vN` (same mathematical text, same
certificates and data). Differences from the note:

- class `mcom-l` with its default left equation numbers (AMS author package, `mcom-l.cls` and the template/README are the AMS files), default layout, no
  `geometry`, no tooltips (`pdfcomment`), no back-references; `hyperref` kept with boxed links; no table of contents;
  `\date{}` empty (the AMS fills "Received by the editor");
- abstract with the numerical macros expanded (self-contained);
- Appendix A (data tables) before the bibliography, AMS convention; Appendices B–D of the note (programs, outputs of the
  25 certificates, input data) become the **Supplement** `casanya_turing_jensen_mcom_supplement_vN.pdf`, sections S1–S3,
  cross-referenced from the article with `xr-hyper`;
- displays and tables re-broken for the 30pc text width (`mcom_overrides.py`; each override is asserted to occur once);
- bibliography: manual `thebibliography` with `\bibliographystyle{amsplain}` as in the AMS sample; DOIs kept as links.

Outputs: `casanya_turing_jensen_mcom_vN.{pdf,_l.tex,.txt}` (article, 31 pp.) and
`casanya_turing_jensen_mcom_supplement_vN.{pdf,.tex,.txt}` (supplement, 23 pp.). Submit the article PDF, the
supplement PDF and the flat archive of the Zenodo note (programs, certificates, data) as supplementary files.
