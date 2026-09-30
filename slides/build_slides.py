"""
build_slides.py - generate TUMO workshop slides from the official template.

    python build_slides.py

Reads the TUMO template (so theme, masters and slide size come from TUMO, not from us),
strips its example slides, and rebuilds the deck for our workshop using the same visual
language as the existing AI Music Workshop deck.

Everything about the look lives in the constants below. Change those, re-run, done.
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
TEMPLATE = HERE.parent / "tmp" / "Workshop Level 3_3D Modeling.pptx"
OUTPUT = HERE / "Lesson 1 - Setup and Your First AI Call.pptx"

# ---------------------------------------------------------------------------
# The TUMO visual language, lifted from the existing workshop decks
# ---------------------------------------------------------------------------
BLUE = RGBColor(0x36, 0x27, 0xFC)      # brand blue - headings
GREEN = RGBColor(0x31, 0xC5, 0x9E)     # accent - the offset card shadow
PANEL = RGBColor(0xF3, 0xF3, 0xF3)     # light grey full-height panel
GREY = RGBColor(0x66, 0x66, 0x66)      # body text on white
DARK = RGBColor(0x43, 0x43, 0x43)      # body text on cards
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

BOLD = "Poppins ExtraBold"             # headings
MEDIUM = "Poppins Medium"              # small labels
SEMI = "Poppins SemiBold"              # emphasised body
BODY = "Poppins"                       # body

W, H = 20.0, 11.25                     # slide size in inches (16:9 at TUMO's scale)


def blank_slide(prs):
    """Add a slide on the BLANK layout - we place everything ourselves, as TUMO's own decks do."""
    return prs.slides.add_slide(prs.slide_layouts[10])


def rect(slide, left, top, width, height, colour):
    """A solid colour block. Used for the grey side panel and the green card shadows."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = colour
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def text(slide, left, top, width, height, lines, size, font=BODY, colour=GREY,
         align=PP_ALIGN.LEFT, spacing=None):
    """
    Place a text box. `lines` is a string or a list of strings, one per paragraph.

    Everything is a free text box rather than a layout placeholder, because that is how
    TUMO's own decks are built - they come out of Google Slides.
    """
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    for i, line in enumerate([lines] if isinstance(lines, str) else lines):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.alignment = align
        if spacing:
            para.space_after = Pt(spacing)
        run = para.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.name = font
        run.font.color.rgb = colour
    return box


# ---------------------------------------------------------------------------
# Slide types - each mirrors a slide shape used in TUMO's existing decks
# ---------------------------------------------------------------------------
def slide_cover(prs, workshop, level="Level 3"):
    s = blank_slide(prs)
    text(s, 3.0, 3.8, 11.0, 2.4, [workshop, "Workshop:"], 60, BOLD, BLUE)
    text(s, 3.0, 6.6, 11.0, 0.7, level, 40, MEDIUM, GREY)
    return s


def slide_title(prs, title, subtitle=None):
    s = blank_slide(prs)
    text(s, 2.0, 4.4, 16.0, 2.0, title, 54, BOLD, BLUE)
    if subtitle:
        text(s, 2.0, 6.6, 16.0, 0.8, subtitle, 28, MEDIUM, GREY)
    return s


def slide_overview(prs, title, paragraphs):
    """Title on the left, body on a full-height grey panel on the right."""
    s = blank_slide(prs)
    rect(s, 10.0, 0.0, 10.0, H, PANEL)
    text(s, 1.17, 3.05, 8.48, 1.2, title, 50, BOLD, BLUE)
    text(s, 10.92, 2.88, 7.92, 5.5, paragraphs, 18, BODY, GREY, spacing=14)
    return s


def slide_cards(prs, heading, cards):
    """A 2x2 grid of offset cards - green block behind, white card in front."""
    s = blank_slide(prs)
    rect(s, 0.0, 0.06, W, 2.28, PANEL)
    text(s, 3.76, 0.73, 12.49, 0.9, heading, 52, BOLD, BLUE, PP_ALIGN.CENTER)

    positions = [(1.03, 3.29), (10.25, 3.29), (1.03, 7.03), (10.25, 7.03)]
    for (left, top), (card_title, card_body) in zip(positions, cards):
        rect(s, left, top, 8.84, 3.3, GREEN)               # the shadow
        rect(s, left - 0.12, top - 0.11, 8.84, 3.3, WHITE)  # the card
        text(s, left + 1.4, top + 0.7, 6.6, 0.7, card_title, 32, BOLD, DARK)
        text(s, left + 1.4, top + 1.6, 6.0, 1.4, card_body, 18, BODY, DARK)
    return s


def slide_content(prs, label, title, points, panel_side="right"):
    """Small label + big title on one side, bulleted body on a grey panel on the other."""
    s = blank_slide(prs)
    if panel_side == "right":
        rect(s, 10.0, 0.0, 10.0, H, PANEL)
        text(s, 1.17, 4.21, 6.52, 0.6, label, 31, MEDIUM, GREY)
        text(s, 1.17, 5.0, 8.48, 2.0, title, 50, BOLD, BLUE)
        text(s, 10.92, 3.4, 7.92, 5.0, points, 18, SEMI, BLUE, spacing=16)
    else:
        rect(s, 0.0, 0.0, 10.0, H, PANEL)
        text(s, 11.0, 4.21, 6.52, 0.6, label, 31, MEDIUM, GREY)
        text(s, 11.0, 5.0, 8.48, 2.0, title, 50, BOLD, BLUE)
        text(s, 1.1, 3.4, 7.92, 5.0, points, 18, SEMI, BLUE, spacing=16)
    return s


def slide_big(prs, statement, footnote=None):
    """One sentence, large. For the point you want them to remember."""
    s = blank_slide(prs)
    text(s, 2.0, 4.0, 16.0, 3.0, statement, 44, BOLD, BLUE, PP_ALIGN.CENTER)
    if footnote:
        text(s, 3.0, 7.6, 14.0, 0.8, footnote, 22, BODY, GREY, PP_ALIGN.CENTER)
    return s



# ---------------------------------------------------------------------------
# The course, defined once. Both the roadmap and the progress slide read this,
# so they can never drift apart or from each other.
#   (number, short name for the roadmap, what the lesson actually covers)
# ---------------------------------------------------------------------------
LESSONS = [
    (1, "Setup",       "Your first AI call, and system prompts"),
    (2, "Why AI lies", "Hallucination, and why pasting everything fails"),
    (3, "Chunking",    "Splitting documents so they can be searched"),
    (4, "Embeddings",  "Turning meaning into numbers you can compare"),
    (5, "The assistant", "Retrieval + prompt = grounded answers"),
    (6, "Real project", "Out of the notebook, into Python files"),
    (7, "Your notes",  "Your own documents, and fixing what goes wrong"),
    (8, "Ship it",     "Measure, tune, and show what you built"),
]

# Which lessons belong to which phase, for the band across the roadmap
PHASES = [("Explore", 1, 5), ("Build", 6, 6), ("Finish", 7, 8)]


def circle(slide, centre_x, centre_y, diameter, fill, line=None):
    """A circle centred on a point, rather than positioned by its corner."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(centre_x - diameter / 2), Inches(centre_y - diameter / 2),
        Inches(diameter), Inches(diameter),
    )
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(2)
    shape.shadow.inherit = False
    return shape


def _track_x(index, left=1.9, right=18.1):
    """Evenly spaced centre for the index-th of the 8 milestones."""
    return left + index * (right - left) / (len(LESSONS) - 1)


def slide_roadmap(prs, title="Where we are going", highlight=None):
    """
    The whole course on one slide: 8 milestones on a track, grouped into phases.

    highlight - a lesson number to mark as "you are here", or None for the plain map.
    """
    s = blank_slide(prs)
    text(s, 1.17, 0.9, 16.0, 1.0, title, 50, BOLD, BLUE)

    track_y = 5.6

    # the phase bands, behind everything
    for name, first, last in PHASES:
        x1, x2 = _track_x(first - 1), _track_x(last - 1)
        rect(s, x1 - 0.85, track_y - 2.15, (x2 - x1) + 1.7, 0.62, PANEL)
        text(s, x1 - 0.85, track_y - 2.08, (x2 - x1) + 1.7, 0.5, name.upper(),
             16, MEDIUM, GREY, PP_ALIGN.CENTER)

    # the line the milestones sit on
    rect(s, _track_x(0), track_y - 0.03, _track_x(len(LESSONS) - 1) - _track_x(0), 0.06, PANEL)

    for i, (number, short, detail) in enumerate(LESSONS):
        cx = _track_x(i)
        done = highlight is not None and number < highlight
        here = highlight is not None and number == highlight

        fill = GREEN if done else (BLUE if here else WHITE)
        edge = None if (done or here) else PANEL
        circle(s, cx, track_y, 1.0 if here else 0.8, fill, edge)
        text(s, cx - 0.5, track_y - 0.28, 1.0, 0.5, str(number), 24, BOLD,
             WHITE if (done or here) else GREY, PP_ALIGN.CENTER)

        # labels alternate above and below so eight of them have room to breathe
        above = i % 2 == 0
        text(s, cx - 1.15, track_y - 1.35 if above else track_y + 0.75, 2.3, 0.5,
             short, 19, BOLD, BLUE if here else DARK, PP_ALIGN.CENTER)
        text(s, cx - 1.35, track_y - 0.95 if above else track_y + 1.2, 2.7, 0.9,
             detail, 12, BODY, GREY, PP_ALIGN.CENTER)

    text(s, 1.17, 9.3, 17.0, 0.6,
         "8 lessons · 2 hours each · you finish with a program that knows what you know",
         20, MEDIUM, GREY, PP_ALIGN.CENTER)
    return s


def slide_progress(prs, today):
    """
    Opens each lesson: what is already done, what happens now, what is still ahead.

    The strip along the top is the same track as the roadmap, so students recognise it.
    """
    s = blank_slide(prs)
    number, short, detail = LESSONS[today - 1]

    rect(s, 0.0, 0.0, W, 3.9, PANEL)
    text(s, 1.17, 0.7, 16.0, 0.8, f"Lesson {number} of 8", 31, MEDIUM, GREY)
    text(s, 1.17, 1.45, 16.0, 1.1, short, 50, BOLD, BLUE)

    # compact version of the roadmap track
    strip_y = 3.25
    for i, (n, _, _) in enumerate(LESSONS):
        cx = _track_x(i)
        done, here = n < today, n == today
        circle(s, cx, strip_y, 0.62 if here else 0.44,
               GREEN if done else (BLUE if here else WHITE),
               None if (done or here) else GREY)
        text(s, cx - 0.4, strip_y - (0.19 if here else 0.15), 0.8, 0.4, str(n),
             16 if here else 13, BOLD, WHITE if (done or here) else GREY, PP_ALIGN.CENTER)

    done_lessons = LESSONS[: today - 1]
    ahead = LESSONS[today:]

    # left: what they already have
    text(s, 1.17, 4.6, 7.6, 0.6, "You already know", 28, BOLD, GREEN)
    text(s, 1.17, 5.4, 7.9, 4.4,
         [f"{n}.  {d}" for n, _, d in done_lessons] or ["Nothing yet - this is where it starts."],
         17, BODY, DARK, spacing=13)

    # middle: today, given the most room
    rect(s, 9.6, 4.35, 0.07, 5.2, BLUE)
    text(s, 10.1, 4.6, 5.2, 0.6, "Today", 28, BOLD, BLUE)
    text(s, 10.1, 5.4, 5.2, 4.4, detail, 22, SEMI, DARK, spacing=13)

    # right: what is still coming
    text(s, 15.8, 4.6, 3.4, 0.6, "Still ahead", 28, BOLD, GREY)
    text(s, 15.8, 5.4, 3.6, 4.4, [f"{n}.  {t}" for n, t, _ in ahead] or ["Nothing - you are done!"],
         17, BODY, GREY, spacing=13)
    return s


def strip_slides(prs):
    """
    Remove the template's example slides, keeping its masters, theme and layouts.

    Dropping the relationship as well as the id matters: removing only the id leaves the
    old slide parts in the package, and saving then writes two slide1.xml entries into
    the same zip. PowerPoint may or may not survive that - don't find out.
    """
    ids = prs.slides._sldIdLst
    for slide_id in list(ids):
        prs.part.drop_rel(slide_id.rId)
        ids.remove(slide_id)


# ---------------------------------------------------------------------------
# Lesson 1
# ---------------------------------------------------------------------------
def build():
    prs = Presentation(str(TEMPLATE))
    strip_slides(prs)

    slide_cover(prs, "AI")

    slide_title(prs, "Build an AI That Reads Your Notes",
                "Lesson 1 of 8  ·  Setup and Your First AI Call")

    slide_roadmap(prs)
    slide_progress(prs, today=1)

    slide_overview(prs, "Workshop Overview", [
        "Ask a chatbot about your homework and it answers confidently - and sometimes "
        "invents the answer completely. It has never seen your notes.",
        "Over 8 lessons you will build an assistant that reads documents YOU choose, "
        "answers only from them, and names the file each answer came from.",
        "And when you ask something your notes do not cover, it will say so instead of "
        "guessing. Getting a computer to admit what it does not know is the hard part.",
    ])

    slide_cards(prs, "Today", [
        ("Set up", "Python, VS Code and your keys. Your work lives in your shared folder."),
        ("First AI call", "Send a message to Claude and look at what actually comes back."),
        ("System prompts", "Give the model a job. One question, three different assistants."),
        ("Make it obey", "Control length, format and language - then make it refuse."),
    ])

    slide_content(prs, "Step 1", "Setup", [
        "Everything is already installed - you are connecting pieces, not installing them.",
        "Python lives on the laptop. YOUR WORK lives in your shared folder, because you "
        "may be at a different Mac next lesson.",
        "Two keys go in your .env file: one answers questions, one searches your notes.",
        "Pick the kernel in every notebook you open. This is the #1 source of errors all "
        "workshop.",
    ])

    slide_content(prs, "Step 3", "System prompts", [
        "Every message has a role. SYSTEM is written by you, the programmer, and the user "
        "never sees it. HUMAN is what the user typed.",
        "That separation is why a chatbot stays polite no matter what you type at it.",
        "Same model, same question, three different system prompts - three completely "
        "different assistants.",
    ], panel_side="left")

    slide_big(prs, "“I only answer questions about weather.”",
              "One paragraph of English turned a confident liar into something you can trust.")

    slide_content(prs, "Homework", "Bring your own notes", [
        "3 to 10 of your own .txt or .md files.",
        "Revision notes, a subject you study, the rules of a game you play, a wiki you "
        "exported. Armenian, English or both.",
        "Shared storage is visible to everyone - bring notes on a general subject, and "
        "keep personal things out of the workshop folder.",
    ])

    prs.save(str(OUTPUT))
    print(f"✅ {OUTPUT.name}  ({len(prs.slides)} slides)")


def build_midcourse_sample():
    """A second deck, so the progress slide can be seen with lessons behind and ahead."""
    prs = Presentation(str(TEMPLATE))
    strip_slides(prs)

    slide_progress(prs, today=5)
    slide_roadmap(prs, title="Where we are", highlight=5)
    slide_cards(prs, "Today", [
        ("Assemble", "Retrieve the chunks, join them, and read the prompt you just built."),
        ("Sources", "Return the files each answer came from, so it can be checked."),
        ("The refusal", "One sentence that stops it inventing answers."),
        ("Memory", "Make follow-up questions work."),
    ])

    out = HERE / "Lesson 5 - Building the RAG Assistant.pptx"
    prs.save(str(out))
    print(f"✅ {out.name}  ({len(prs.slides)} slides)")


if __name__ == "__main__":
    build()
    build_midcourse_sample()
