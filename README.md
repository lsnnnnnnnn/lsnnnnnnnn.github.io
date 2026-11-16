# Sheng’en Li’s personal website

A Quarto website published on GitHub Pages at https://lsnnnnnnnn.github.io.

## Update the site

Edit the `.qmd` source pages and `styles.css`, then run:

```sh
quarto render
```

Commit both the source changes and the generated `docs/` directory. GitHub Pages serves the `main` branch’s `docs/` directory.

- `index.qmd`: home and selected research
- `publications.qmd`: publications and manuscripts, with separate review statuses
- `projects.qmd`: research experience (keeps the existing URL)
- `about.qmd`: education, industry experience, service, and skills
- `assets/Shengen_Li_CV.pdf`: CV linked directly from the navigation
- `assets/profile.jpg`: small homepage portrait
- `blog/index.qmd`: Research Notes; dated articles are listed automatically
- `tools.qmd`: Reader First and the L2 factor-capacity tool, with usage links and release status

The original test post is retained as a draft and excluded from the published Notes listing.

The homepage keeps CV, GitHub, and Email below the profile photo. Tools replaces Software in the navigation; `software.html` redirects to `tools.html`. Reader First is maintained in [its own repository](https://github.com/lsnnnnnnnn/reader-first), with installation instructions and bilingual examples. The downloadable archive mirrors that release. Notes navigation includes a version parameter so visitors reload the updated covers and dates.

Replace the PDF at the same path when updating the CV. Publication statuses and current roles are maintained manually; the November 2026 refresh follows the supplied revised CV.

The design uses local assets, system fonts, and Quarto’s built-in navigation and search. No additional JavaScript packages or build tools are required.

## Research previews

The home page uses compact research previews linking to the corresponding section of `projects.qmd`. The Research page pairs fuller descriptions with clickable figures. The research list uses aligned image and text columns, with distinct title, metadata, and summary typography. WebP assets live in `assets/research/`; `_quarto.yml` copies them to the published site.

| Asset | Original source |
| --- | --- |
| `reachability-system.webp` | Supplied *Reachability Analysis of Neural-Network Controlled Systems* slides, slide 33, image93.png; Xiangru Zhong (2025-02-13) |
| `copf-framework.webp` | COPF, protocol schematic (Figure 3); [paper, Appendix B](https://arxiv.org/abs/2606.00700); rendered from the existing `copf_protocol.pdf` crop |
| `decaf-gad-architecture.webp` | DECAF-GAD, Figure 2, PDF page 4; [paper](https://arxiv.org/abs/2508.10785) |
| `audit-refine-framework.webp` | Supplied `PPIDM_Pi.pdf`, Figure 1, page 5 |
| `history-alarm-controls.webp` | Supplied `sw.pdf`, Figure 1.1, PDF page 9 |

The November 2026 descriptions and linked CV follow the supplied revised CV and manuscripts. The ECG paper is listed as submitted to Artificial Intelligence in Medicine; the time-series project is undergraduate Signature Work. Full unpublished manuscripts are not hosted.

The typography follows the compact academic style of [Juntang Wang’s site](https://www.qqgjyx.com/): Palatino/Georgia body text with system sans-serif headings. The stylesheet is included with a version query in `_quarto.yml`; update that query with future visual releases to refresh cached CSS.

The November 11 update adds research notes grounded in the supplied Signature Work manuscript and the author's description of the L2 factor-capacity engine. The software page describes the current 10% participation / 100% same-day completion criterion and labels the open-source release as in preparation. No company market data, source code, or sample results are published with this update.

The November 14 update links Notes and Software from the homepage introduction and adds a note on the author's Reader First writing skill. The paper that inspired it is credited in small text beside the discussion; editing examples come from the skill itself. `assets/skills/reader-first.zip` contains a snapshot of the skill instructions, examples, research basis, agent metadata, and icon. Refresh this archive when publishing changes to the skill.

The November 16 Reader First revision adds the author-supplied *When AI stacks nouns* comic, created with Codex using [baoyu-comic](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-comic), and Figure 7 from Clark, Martin, and Mahowald, [arXiv:2610.29162v1](https://arxiv.org/abs/2610.29162v1). The paper figure is reproduced from the [original SVG](https://arxiv.org/html/2610.29162v1/summary_transfer_figure.svg) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Both files are stored in `assets/notes/reader-first/` and credited beside the images. The note includes English and Chinese revision comparisons; the per-note “All research notes” footer links have been removed.

The November 16 structured-dependence note explores an XOR counterexample, forest-cover bounds, source cancellation, and a block-moment interface for COMET. Three analytical SVG figures and their reproducible NumPy/Matplotlib script are stored in `assets/notes/structured-dependence/`. Run `python assets/notes/structured-dependence/generate_figures.py` to redraw them before `quarto render`. The figures use exact formulas, not simulated results.

