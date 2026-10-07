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
def slide_cover(prs, workshop, strapline=None):
    s = blank_slide(prs)
    text(s, 3.0, 4.1, 12.0, 2.4, [workshop, "Workshop:"], 60, BOLD, BLUE)
    if strapline:
        text(s, 3.0, 6.9, 12.0, 0.8, strapline, 28, MEDIUM, GREY)
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
    """
    A grid of offset cards - a green block behind a white card.

    Two columns for up to four cards, three for five or six, so a lesson with five
    hands-on steps shows five cards rather than quietly losing one. A short final row
    is centred, so it reads as deliberate rather than broken.
    """
    s = blank_slide(prs)
    rect(s, 0.0, 0.06, W, 2.28, PANEL)
    text(s, 3.76, 0.73, 12.49, 0.9, heading, 52, BOLD, BLUE, PP_ALIGN.CENTER)

    count = len(cards)
    if count > 6:
        raise ValueError(f"{count} cards will not fit - split the slide")

    columns = 2 if count <= 4 else 3
    margin, gap = 1.03, 0.38
    card_w = (W - 2 * margin - gap * (columns - 1)) / columns
    card_h, rows_y = 3.3, [3.29, 7.03]

    title_size = 32 if columns == 2 else 25
    body_size = 18 if columns == 2 else 15
    pad = 1.4 if columns == 2 else 0.6

    for i, (card_title, card_body) in enumerate(cards):
        row, col = divmod(i, columns)
        in_row = min(columns, count - row * columns)
        # centre a short final row
        row_w = in_row * card_w + (in_row - 1) * gap
        left = (W - row_w) / 2 + col * (card_w + gap)
        top = rows_y[row]

        rect(s, left, top, card_w, card_h, GREEN)                  # the shadow
        rect(s, left - 0.12, top - 0.11, card_w, card_h, WHITE)    # the card
        text(s, left + pad, top + 0.6, card_w - 2 * pad, 0.8, card_title, title_size, BOLD, DARK)
        text(s, left + pad, top + 1.5, card_w - 2 * pad, 1.6, card_body, body_size, BODY, DARK)
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
    (2, "Why AI invents", "Why it makes things up, and why pasting everything fails"),
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
         "8 lessons · 2 hours each · you leave with a program that knows what you know",
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
# The eight lesson decks
#
# One function per lesson, deliberately explicit rather than a data table - these are
# what you will actually edit, and a function you can read top to bottom beats a nested
# dict you have to decode.
#
# Shape of every deck:
#     title -> progress -> today's cards -> a few content slides -> the point -> next
# Lesson 1 additionally opens with the cover and the full roadmap.
# ---------------------------------------------------------------------------
COURSE_TITLE = "Build an AI That Reads Your Notes"


def deck(prs, number):
    """The opening every lesson shares: name the lesson, then show where we are."""
    name = LESSONS[number - 1][1]
    slide_title(prs, COURSE_TITLE, f"Lesson {number} of 8  ·  {LESSON_FULL[number]}")
    slide_progress(prs, today=number)


LESSON_FULL = {
    1: "Setup and Your First AI Call",
    2: "Why AI Makes Things Up",
    3: "Preparing Documents: Chunking",
    4: "Embeddings and Semantic Search",
    5: "Building the RAG Assistant",
    6: "From Notebook to Python Project",
    7: "Your Own Knowledge Base",
    8: "Testing, Tuning and Final Demo",
}


def lesson_1(prs):
    slide_cover(prs, "AI", "8 lessons · October 2026")
    slide_title(prs, COURSE_TITLE, f"Lesson 1 of 8  ·  {LESSON_FULL[1]}")
    slide_roadmap(prs)
    slide_progress(prs, today=1)

    slide_overview(prs, "Workshop Overview", [
        "A chatbot has never seen your notes. Ask it about your homework and it will "
        "invent an answer - confidently.",
        "Over 8 lessons you build an assistant that reads documents you choose, answers "
        "only from them, and names its source.",
        "And says “that isn’t in your documents” when it isn’t. "
        "That refusal is the hard part, and the whole point.",
    ])
    slide_cards(prs, "Today", [
        ("Set up", "Python, VS Code, your keys. Work lives in your shared folder."),
        ("First AI call", "Send a message to the AI. Look at what comes back."),
        ("System prompts", "Give the model a job. One question, three assistants."),
        ("Make it obey", "Length, format, language - then make it refuse."),
        ("Swap the company", "Change one line. Same code, different AI."),
    ])
    slide_content(prs, "Step 1", "Setup", [
        "Everything is installed. You are connecting pieces, not installing them.",
        "Python lives on the laptop. Your work lives in your shared folder - you may be "
        "at a different Mac next lesson.",
        "Two keys in .env: one answers, one searches.",
        "Pick the kernel in every notebook. The #1 source of errors all workshop.",
    ])
    slide_content(prs, "Step 3", "System prompts", [
        "SYSTEM - written by you, the programmer. The user never sees it.",
        "HUMAN - what the user actually typed.",
        "That split is why a chatbot stays polite whatever you type at it.",
        "Same model, same question, three system prompts → three different assistants.",
    ], panel_side="left")
    slide_big(prs, "“I only answer questions about weather.”",
              "One paragraph of English. No Python. "
              "In Lesson 5, this is what makes your assistant trustworthy.")
    slide_content(prs, "Homework", "Bring your own notes", [
        "3 to 10 of your own .txt or .md files.",
        "Revision notes, a subject you study, the rules of a game. English works best.",
        "Shared storage is visible to everyone — general subjects only, nothing personal.",
    ])


def lesson_2(prs):
    deck(prs, 2)
    slide_cards(prs, "Today", [
        ("Watch it invent", "Ask about documents no AI has ever seen."),
        ("Paste it all in", "The obvious fix. It works."),
        ("Measure the cost", "Then find out why it cannot scale."),
    ])
    slide_content(prs, "Why", "It is not remembering", [
        "A model predicts what text comes next. It has no database.",
        "Inside it, recalling and composing are the same operation.",
        "So it cannot tell you which one it just did - and neither can you.",
        "Real cases: invented court citations, invented refund policies.",
    ])
    slide_big(prs, "The Kestrel Project does not exist.",
              "We invented it for this workshop. No AI has ever seen it — so every "
              "detail it gives you is provably made up.")
    slide_content(prs, "The fix", "Grounding", [
        "Read the file. Put the text in the system prompt. Ask again.",
        "Now it is right - because the answer was in front of it.",
        "Ask about a different file and it fails again. So load everything?",
    ], panel_side="left")
    slide_cards(prs, "Why “paste everything” fails", [
        ("The window", "400,000 tokens. A textbook fits. A year of notes does not."),
        ("The cost", "$9.38 per 100 questions for a textbook. $56.25 for a year of notes."),
        ("The quality", "Too much context buries the answer. Replies get worse."),
    ])
    slide_big(prs, "“It fits” and “it’s a good idea” are different questions.",
              "Next three lessons: find the three paragraphs that matter, and send only those.")


def lesson_3(prs):
    deck(prs, 3)
    slide_cards(prs, "Today", [
        ("Load", "Read a folder of documents, keeping track of where each came from."),
        ("Compare sizes", "Split at 200, 500, 1000, 4000 - and read the results."),
        ("Overlap", "Fix the sentence that got cut in half."),
        ("Split on structure", "Keep each heading's section whole."),
        ("Choose yours", "Pick the settings for your own notes, and say why."),
    ])
    slide_content(prs, "The idea", "One chunk, one idea", [
        "Big enough to stand alone. Small enough to be mostly relevant.",
        "Too small: “The two-tracker rule was added after” … after what?",
        "Too large: you are back to Lesson 2's problem in miniature.",
    ])
    slide_big(prs, "Handed only this chunk, could you answer the question?",
              "That is the only test. It is a judgement, not a formula — and it is yours to make.")
    slide_content(prs, "The catch", "Wherever you cut, you cut somewhere", [
        "Sometimes straight through the sentence that held the answer.",
        "Overlap: each chunk repeats the end of the one before it.",
        "10-20% of the chunk size. Costs a little space, saves whole answers.",
    ], panel_side="left")
    slide_content(prs, "Your settings", "Write them down", [
        "Chunk size and overlap, chosen by you, for your own notes.",
        "Plus one sentence saying why you chose them.",
        "“Because it was the default” is not accepted.",
    ])


def lesson_4(prs):
    deck(prs, 4)
    slide_cards(prs, "Today", [
        ("Measure meaning", "Turn words into numbers and compare them."),
        ("The surprise", "Find answers that share no words with the question."),
        ("Build the index", "Search your own documents - no AI involved yet."),
        ("The gap", "Search for something that is not there."),
    ])
    slide_content(prs, "The idea", "Meaning as a position", [
        "Two words that mean similar things end up near each other.",
        "Not similar spelling. Similar meaning.",
        "Your model uses 1,536 numbers per piece of text - 1,536 axes it worked out itself.",
        "You cannot picture that. You only need to measure the distance.",
    ])
    slide_big(prs, "“hot” and “cold” score high.",
              "Embeddings capture what something is about, not whether it agrees \u2014\n"
              "a search can hand you the exact opposite of the truth.")
    slide_cards(prs, "The result that makes this work", [
        ("No shared words", "“when the radio cannot get through” finds “valleys where "
                            "the signal does not reach”. A word search scores zero."),
        ("Not across languages", "An Armenian question scores an unrelated English "
                                 "line above its answer. Measure, never assume."),
    ])
    slide_content(prs, "Read this twice", "It always returns something", [
        "Search for “Who won the 2018 World Cup?” and you still get 3 chunks back.",
        "A vector store has no idea what “irrelevant” means. It returns the nearest "
        "things it has, however far away.",
        "So retrieval alone does not stop it inventing. That is Lesson 5.",
    ], panel_side="left")


def lesson_5(prs):
    deck(prs, 5)
    slide_cards(prs, "Today", [
        ("Assemble", "Retrieve, join, and read the prompt you just built."),
        ("Sources", "Name the files each answer came from."),
        ("The refusal", "One sentence that stops it inventing."),
        ("Tune k", "Too few misses answers. Too many makes them vague."),
        ("Memory", "Make follow-up questions work."),
    ])
    slide_content(prs, "The whole thing", "Four steps", [
        "1.  Find the chunks closest in meaning to the question.",
        "2.  Join them into one block of text.",
        "3.  Paste that into the system prompt.",
        "4.  Ask the model.",
        "No model was retrained. We just decided well what to paste.",
    ])
    slide_big(prs, "Print the prompt. Read it out loud.",
              "That is RAG, in full, with nothing hidden.")
    slide_content(prs, "The sentence", "What makes it trustworthy", [
        "“If the notes do not contain the answer, say exactly: that isn’t in your "
        "documents. Do not guess.”",
        "That is it. One paragraph of English, no Python.",
        "Find a question yours refuses — and one where the refusal fails. The second is "
        "more interesting.",
    ], panel_side="left")
    slide_cards(prs, "Why follow-ups break", [
        ("The model", "“Which of them is cheaper?” - it does not know what “them” "
                      "means. Replay the earlier turns."),
        ("The search", "Neither does the search. Glue the last two questions onto the query."),
    ])


def lesson_6(prs):
    deck(prs, 6)
    slide_cards(prs, "Today", [
        ("config.py", "Every setting in one place. It does no work."),
        ("ingest.py", "Documents → chunks → an index saved to disk."),
        ("retriever.py", "Find the chunks. Knows nothing about AI."),
        ("assistant.py", "The system prompt, and the answer."),
        ("main.py", "Talk to the human. Then run it."),
    ])
    slide_big(prs, "A notebook is a lab bench.",
              "You hand someone the thing you built on it, not the bench.")
    slide_content(prs, "The design", "Two programs, not one", [
        "Reopening the notebook recomputes every embedding before you can ask anything.",
        "ingest.py is slow. You run it when your documents change.",
        "main.py is fast. You run it constantly.",
        "The index on disk is what sits between them.",
    ])
    slide_content(prs, "The rule", "One sentence per file", [
        "If you cannot say what a file is for in one sentence, it is doing two jobs.",
        "retriever.py must not import assistant.py. That is what lets you test searching "
        "almost for free.",
        "Check after every file. Do not write all five and hope.",
    ], panel_side="left")
    slide_big(prs, "python main.py",
              "A real program, from a terminal, with no notebook anywhere. "
              "Nobody leaves today until this runs.")


def lesson_7(prs):
    deck(prs, 7)
    slide_cards(prs, "Today", [
        ("Your documents", "Load your own material and ask five questions you know."),
        ("Improve them", "Fix the documents, not the code. Then measure again."),
        ("Build a feature", "One of your own. Decide which file it belongs in."),
    ])
    slide_content(prs, "The hard truth", "Garbage in, garbage out", [
        "Good: headings, short paragraphs, one topic per file.",
        "Bad: one unbroken wall of text, everything in notes.md.",
        "The killer: notes that say “this is the important one”. “This” carries the "
        "meaning, and a search cannot see it.",
    ])
    slide_big(prs, "Did the right chunk come back?",
              "Ask that before you blame the prompt. /sources answers it, and costs next to nothing.")
    slide_cards(prs, "Two failures, two fixes", [
        ("Retrieval failed", "The right chunk never came back. Fix your documents, "
                             "the chunk size, or k."),
        ("Generation failed", "It came back and the model ignored it. Fix the system prompt."),
    ])
    slide_content(prs, "Remember", "Re-run ingest", [
        "Chunk size, overlap, or the documents themselves → re-run ingest.py.",
        "How many chunks, or the system prompt → takes effect immediately.",
        "“I changed it and nothing happened” is almost always a forgotten ingest.",
    ], panel_side="left")


def lesson_8(prs):
    deck(prs, 8)
    slide_cards(prs, "Today", [
        ("Test set", "Five questions you know the answers to. Score them now."),
        ("Tune", "One change at a time. Re-score after each."),
        ("Finish", "README, requirements, and keep your key out of it."),
        ("Show it", "90 seconds each."),
    ])
    slide_content(prs, "The trap", "How would you know?", [
        "Change something, ask one question, decide it is better, keep it.",
        "You measured nothing. The model words things differently every time, and you "
        "asked once.",
        "Decide how you will measure before you change anything.",
    ])
    slide_big(prs, "Write the test set first.",
              "Then change one thing, and score it again. This is the most useful habit "
              "in the whole workshop.")
    slide_content(prs, "Worth testing", "Does the pricier model win?", [
        "Swapping gpt-5.4-mini for gpt-5.4 roughly triples the price.",
        "It often does not win. The retriever already did the hard part \u2014 the model\n"
        "only has to read four paragraphs and not invent anything.",
        "“I tested it and the expensive one was not better” is a real finding.",
    ], panel_side="left")
    slide_cards(prs, "Your demo", [
        ("What it knows", "The documents you chose, and why."),
        ("One good answer", "Ask it live. Point at the sources."),
        ("One correct refusal", "The thing you actually built."),
        ("One thing that broke", "And what it turned out to be."),
    ])
    slide_big(prs, "You leave with a program that knows what you know.",
              "Switch the model to Ollama and the answering half runs free on your own "
              "laptop, forever.")


BUILDERS = {1: lesson_1, 2: lesson_2, 3: lesson_3, 4: lesson_4,
            5: lesson_5, 6: lesson_6, 7: lesson_7, 8: lesson_8}


def build_all():
    for number, builder in BUILDERS.items():
        prs = Presentation(str(TEMPLATE))
        strip_slides(prs)
        builder(prs)
        out = HERE / f"Lesson {number} - {LESSON_FULL[number]}.pptx".replace(":", " -")
        prs.save(str(out))
        print(f"  ✅ {out.name:52} {len(prs.slides)} slides")


if __name__ == "__main__":
    print("Building all 8 lesson decks\n")
    build_all()
