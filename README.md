# TUMO AI Workshops

Workshop material for TUMO students (ages ~13-18), written in the style, structure and
teaching approach of the *LLM Engineering* course.

## The track being taught: Course B — Study Buddy

| | |
|---|---|
| **Topic** | A personalised RAG assistant over the student's own documents |
| **Format** | 8 lessons x 2 hours = **16 hours exactly** |
| **Dates** | 1–25 October 2026 · Thu 19:30–21:30, Sun 14:00–16:00 |
| **Machines** | 16 × macOS, prepared by TUMO IT; students' work on shared storage |
| **Model** | GPT-5.4 mini (`openai:gpt-5.4-mini`), on TUMO's OpenAI API key |
| **Cost** | ~$6 per group of 16 for the whole course; embeddings add well under a cent |
| **Final deliverable** | A runnable local Python project: ask questions about material you chose, get grounded answers with sources |

> **Course A (AI Image Studio) is not scheduled.** It is kept here for reference only.
> Its material is complete and working if it's ever wanted; it is simply not part of the
> taught programme.

```
tumo_workshops/
├── README.md                 <- you are here
├── docs/
│   ├── TEACHER_NOTES.md      <- pre-flight checklist, budget, risks  ** read first **
│   ├── SETUP.md              <- student environment setup (macOS, shared storage)
│   ├── ANNOUNCEMENT.md       <- the workshop announcement, ready to send
│   ├── TUMO_APPLICATION.md   <- paste-ready answers for the TUMO application form
│   └── METHODOLOGY.md        <- how the material is written and structured
├── slides/                   <- lesson decks (.pptx) and build_slides.py
├── course_b_study_buddy/     <- THE TRACK BEING TAUGHT
│   ├── OUTLINE.md            <- TUMO 4-part workshop outline
│   ├── CURRICULUM.md         <- 8 lessons, agendas, time math
│   ├── notebooks/            <- lessons 1-5, experimentation phase
│   └── project/              <- the finished project students arrive at
└── course_a_image_studio/    <- not scheduled; reference only
    ├── OUTLINE.md
    ├── CURRICULUM.md
    ├── notebooks/
    └── project/
```

## The shape of the course

The arc is borrowed directly from the reference course:

1. **Lessons 1-5 — Notebook.** New ideas are introduced by *running something small first*,
   then naming what happened. Cells are tiny. Students inspect objects constantly.
2. **Lesson 6 — The move.** Notebook code is refactored into real Python modules in VS Code.
   This mirrors `week5/` in the reference course, where `day1-day3.ipynb` become
   `implementation/ingest.py`, `implementation/answer.py` and `app.py`.
3. **Lessons 7-8 — Project.** Entry point, personal customisation, README, showcase.

## Provider-agnostic by design

Nothing hardcodes a vendor SDK. Everything goes through LangChain, and the provider choice
lives in exactly one place - a `config.py` with a single model string:

```python
CHAT_MODEL = "openai:gpt-5.4-mini"             # the default
# CHAT_MODEL = "openai:gpt-5.4"                # smarter, ~3x the price
# CHAT_MODEL = "anthropic:claude-haiku-4-5"
# CHAT_MODEL = "google-genai:gemini-2.5-flash"
# CHAT_MODEL = "ollama:llama3.2"               # free, runs on this laptop, no API key
```

Changing that one line changes the provider. Nothing downstream knows or cares, because
everything downstream only calls `.invoke()`.

This isn't theoretical tidiness — the course needs it. OpenAI answers the questions and
makes the embeddings, and the vectors live in Chroma on the student's laptop. **No single
company can hold the project hostage**, because each piece sits behind an interface you can
swap in one line — and OpenAI's embeddings are weak in Armenian, which is exactly the kind
of reason you might want to. Lesson 4 makes that point explicitly, and Lesson 5 has students prove it by
switching the whole thing to a local model with the wifi off.
