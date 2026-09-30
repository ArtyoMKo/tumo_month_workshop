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
| `slide_cards()` | Offset cards (green block behind a white card). 2 columns up to 4 cards, 3 for 5–6; a short last row is centred |
| `slide_content()` | Small label + big title one side, bullets on a panel the other |
| `slide_big()` | One sentence, large — the point to remember |
| `slide_roadmap()` | All 8 milestones on a track, grouped into phases |
| `slide_progress()` | Opens a lesson: done / today / still ahead |

`panel_side="left"` flips `slide_content`, so consecutive slides can alternate.

## The roadmap and progress slides

Both read one list, `LESSONS`, at the top of the script — so they cannot drift apart, and
renaming a lesson updates every deck on the next run.

```python
LESSONS = [
    (1, "Setup",         "Your first AI call, and system prompts"),
    (2, "Why AI lies",   "Hallucination, and why pasting everything fails"),
    ...
]
PHASES = [("Explore", 1, 5), ("Build", 6, 6), ("Finish", 7, 8)]
```

- `slide_roadmap()` — the whole course. Labels alternate above and below the track so
  eight of them fit. Pass `highlight=5` to mark "you are here".
- `slide_progress(today=5)` — put this second in every lesson's deck. Same track in
  miniature along the top, then three columns: **You already know** (green, the topics
  from earlier lessons), **Today** (blue, given the most room), **Still ahead** (grey).

States are colour-coded consistently: green = done, blue = today, white outline = ahead.

## Unverified

**"Level 3" on the cover is a guess.** It was copied from the template filename and the
AI Music Workshop deck. Nobody has confirmed what level this workshop is — check with
TUMO and change `slide_cover(prs, "AI", level=...)` if it is wrong.

## Known gaps

- **No images.** TUMO's decks lean on screenshots; every one here is text on colour.
  Screenshots of the terminal and VS Code would carry a lot of these slides.
- **Unreviewed rendering.** These were written through a library, not looked at. Expect
  to nudge spacing.
- **Poppins must be installed** or PowerPoint substitutes a fallback.
