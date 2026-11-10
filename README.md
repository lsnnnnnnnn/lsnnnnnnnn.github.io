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
- `blog/`: research notes and existing posts

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
