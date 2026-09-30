# Slides

`build_slides.py` generates the deck from TUMO's own template, so theme, masters, fonts
and slide size come from TUMO rather than from us.

```bash
python build_slides.py          # needs: pip install python-pptx
```

## The visual language

Lifted by inspecting the existing *AI Music Workshop* decks, not invented:

| | |
|---|---|
| Slide size | 20 × 11.25 in |
| Brand blue | `#3627FC` — all headings |
| Accent green | `#31C59E` — the offset shadow behind task cards |
| Panel grey | `#F3F3F3` — full-height side panel |
| Body grey | `#666666` on white, `#434343` on cards |
| Fonts | Poppins ExtraBold (headings) · Medium (labels) · SemiBold (emphasis) · Poppins (body) |
| Sizes | 60 cover · 50–54 titles · 32–36 card headings · 31 labels · 18 body |

## Slide types available

| Function | Shape |
|---|---|
| `slide_cover()` | "AI / Workshop:" + Level 3 |
| `slide_title()` | Big title + subtitle |
| `slide_overview()` | Title left, body on a full-height grey panel right |
| `slide_cards()` | 2×2 offset cards (green block behind a white card) |
| `slide_content()` | Small label + big title one side, bullets on a panel the other |
| `slide_big()` | One sentence, large — the point to remember |

`panel_side="left"` flips `slide_content`, so consecutive slides can alternate.

## Known gaps

- **No images.** TUMO's decks lean on screenshots; every one here is text on colour.
  Screenshots of the terminal and VS Code would carry a lot of these slides.
- **Unreviewed rendering.** These were written through a library, not looked at. Expect
  to nudge spacing.
- **Poppins must be installed** or PowerPoint substitutes a fallback.
