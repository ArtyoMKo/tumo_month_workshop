# TUMO AI Workshops

Two 16-hour workshop projects for TUMO students (ages ~13-18), written in the style,
structure and teaching approach of the *LLM Engineering* course.

| | Course A | Course B |
|---|---|---|
| **Name** | AI Image Studio | Study Buddy |
| **Track** | Light (calmer pace) | Complex (stronger/faster students) |
| **Topic** | Text-to-image AI client | Personalised RAG assistant |
| **Format** | 8 sessions x 2 hours = 16 hours | 8 sessions x 2 hours = 16 hours |
| **Final deliverable** | Local Python project: type a prompt, get an image | Local Python project: ask questions about your own notes |

```
tumo_workshops/
├── README.md                 <- you are here
├── SETUP.md                  <- shared environment setup (read this first)
├── TEACHER_NOTES.md          <- pre-flight checklist, risks, time budget honesty
├── course_a_image_studio/
│   ├── OUTLINE.md            <- TUMO 4-part workshop outline
│   ├── CURRICULUM.md         <- 8 sessions, agendas, time math
│   ├── notebooks/            <- sessions 1-5, experimentation phase
│   └── project/              <- the finished project students arrive at
└── course_b_study_buddy/
    ├── OUTLINE.md
    ├── CURRICULUM.md
    ├── notebooks/
    └── project/
```

## The shape of both courses

Both follow the same arc, borrowed directly from the reference course:

1. **Sessions 1-5 — Notebook.** New ideas are introduced by *running something small first*,
   then naming what happened. Cells are tiny. Students inspect objects constantly.
2. **Session 6 — The move.** Notebook code is refactored into real Python modules in VS Code.
   This mirrors `week5/` in the reference course, where `day1-day3.ipynb` become
   `implementation/ingest.py`, `implementation/answer.py` and `app.py`.
3. **Sessions 7-8 — Project.** Entry point, personal customisation, README, showcase.

## Provider-agnostic by design

Neither course hardcodes a vendor SDK. Both go through LangChain, and both keep the
provider choice in exactly one place - a `config.py` with a single model string:

```python
CHAT_MODEL = "openai:gpt-4.1-mini"     # the default
# CHAT_MODEL = "ollama:llama3.2"       # free, runs on this laptop, no API key
# CHAT_MODEL = "anthropic:claude-haiku-4-5-20251001"
# CHAT_MODEL = "google-genai:gemini-2.5-flash"
```

Changing that one line changes the provider. Nothing downstream knows or cares,
because everything downstream only calls `.invoke()`.
