// MathJax v3 configuration for the jansky docs.
//
// Prose pages go through pymdownx.arithmatex (generic mode), which emits
// \(...\) / \[...\]. The course notebooks, however, are rendered by
// mkdocs-jupyter and emit raw single-dollar math ($...$) straight from the
// notebook source. We therefore enable BOTH delimiter styles so the chapters'
// inline maths renders instead of showing literal dollar signs.
//
// This object must be defined before tex-mml-chtml.js loads (it is listed first
// in mkdocs.yml `extra_javascript`).
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true,
    tags: "ams"
  }
};
