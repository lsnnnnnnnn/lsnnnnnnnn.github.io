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
- `cv.qmd` and `assets/Shengen_Li_CV.pdf`: CV page and downloadable PDF
- `blog/`: research notes and existing posts

Replace the PDF at the same path when updating the CV. Publication statuses and current roles are maintained manually; the September 2026 refresh follows the supplied CV.

The design uses local assets, system fonts, and Quarto’s built-in navigation and search. No additional JavaScript packages or build tools are required.
