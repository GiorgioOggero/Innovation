# SEO corrections — 11 November 2026

Working branch: `seo-multilingue-20261111`.
Based on `Multilingue_con_Book` at `582d754`.
`Sito_multilingue` remains unchanged.

## Included

- Homepage canonical is `https://giorgiooggero.github.io/Innovation/`; internal homepage links and sitemap match it.
- Self-referencing canonicals and unique translated titles/descriptions on every generated page.
- Static English pages at the existing URLs; Italian, Arabic, German, Spanish and Chinese pages under their language folders. Reciprocal `hreflang` and `x-default` links.
- 32 canonical pages: five pages in six languages plus the existing English/Italian privacy text. Other privacy language buttons lead to the English page; no untranslated privacy content is advertised through hreflang.
- Existing visible main text and visual assets retained. Language controls are crawlable anchors styled like the original buttons. The URL controls the language, without localStorage overriding it.
- Clean UTF-8 XML sitemap with absolute canonical URLs and no speculative modification dates. `sitemaps.xml` is an alias for the historically submitted spelling.
- `.nojekyll` for plain static publishing, and `noindex` on the existing error document.

## Validate and maintain

Edit the multilingual source files in `tools/seo/templates/*.html.in`, then run:

```sh
python tools/seo/build.py
python tools/seo/check.py
node --check assets/js/script.js
git diff --check
```

Requires Python 3 with lxml. The check validates 32 pages, descriptions, canonical consistency, reciprocal language annotations, XML, JSON-LD and unchanged main copy. It reports 12 image files already absent in the upstream source, rather than treating them as new regressions. The upstream CV links also refer to filenames not present in this branch; these are separate pre-existing content issues.

## Publication still required

Push this new branch and configure GitHub Pages to deploy from it, leaving `Sito_multilingue` intact. Check the rendered desktop/mobile site and language navigation after deployment; a live visual comparison has not yet been possible.

Then resubmit `/Innovation/sitemap.xml` in Search Console and verify a successful fetch. The original XML already returned HTTP 200 publicly, so the existing Search Console fetch failure cannot be honestly marked resolved until Google accepts the deployed sitemap. A project-level robots.txt would not control crawling: that file belongs at the host root and is not added here.

The prior six indexing requests were accepted. Resubmit changed canonical pages as necessary after publication; Google determines indexing and may take time to refresh the reports.
