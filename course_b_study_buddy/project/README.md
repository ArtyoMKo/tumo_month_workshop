# Study Buddy

An assistant that has actually read *my* notes, answers questions about them with sources,
and says so when it doesn't know.

Built at TUMO over 16 hours, starting from a language model confidently inventing things.

```
$ python main.py

================================================================
  STUDY BUDDY
================================================================
  Model     : openai:gpt-4.1-mini
  Documents : documents/
  Index     : 13 chunks, retrieving 4 per question
================================================================

> Why does every flight carry two trackers?

  Thinking...

  Every Kestrel flight carries two independent trackers from different
  manufacturers - a LoRa tracker transmitting every 30 seconds and a satellite
  tracker transmitting every 5 minutes. The rule was added after Flight 4, whose
  single tracker failed on descent and left the payload lost for eleven days.

  Sources: hardware.md, overview.md

> Who won the 2018 World Cup?

  Thinking...

  That isn't in your documents.

  Sources: flights.md, hardware.md
```

**That second answer is the point of the whole project.** It retrieved four chunks — it
always retrieves four — looked at them, found nothing about football, and refused. A
language model on its own will happily invent a winner.

---

## Install

You need **Python 3.12**, about **3 GB** of free disk, and patience during step 4.

```bash
cd study_buddy

python -m venv .venv                 # a private box of packages for this project only

source .venv/bin/activate            # Mac / Linux
.venv\Scripts\activate               # Windows

pip install -r requirements.txt      # several hundred MB - this is the slow one

cp .env.example .env                 # then open .env and paste your real key in
```

## Run

It's **two programs**, and knowing why is half the design:

```bash
python ingest.py     # SLOW. Reads documents/, builds the search index. Run when documents change.
python main.py       # FAST. Answers questions. Run as often as you like.
```

If `ingest.py` rebuilt the index every time you asked a question, you'd wait thirty seconds
before every single conversation. So it doesn't — it writes the index to `vector_db/` and
`main.py` just opens it.

**Re-run `python ingest.py` whenever you add, remove or edit anything in `documents/`.**
Forget, and you'll be searching yesterday's notes without any warning that you are.

Check everything first with:

```bash
python check_setup.py
```

Eight checks, in dependency order, stopping at the first failure with a specific fix.

### Commands inside `main.py`

| Command | What it does |
|---|---|
| *(any question)* | Retrieve, ground, answer, cite |
| `/sources <question>` | Show which chunks would be retrieved and how close each one is — **without** calling the model |
| `/quit` | Stop (Ctrl+C also works) |

`/sources` is the debugging tool. See below.

---

## How it's put together

Five files. Each one is explainable in a single sentence.

| File | Responsible for |
|---|---|
| `main.py` | Talking to the human. Asks, calls the others in order, prints answers and sources. |
| `config.py` | Every setting: model, chunk size, how many chunks to retrieve, where things live. |
| `ingest.py` | Documents → chunks → vectors → `vector_db/`. The slow half. |
| `retriever.py` | Given a question, find the relevant chunks. **Knows nothing about language models.** |
| `assistant.py` | Assemble chunks into the system prompt and get a grounded answer. |

```
  BUILD (run occasionally)          ASK (run constantly)

  documents/                        your question
      │                                   │
   ingest.py ──► vector_db/ ──────► retriever.py
                                          │
                                     assistant.py ──► answer + sources
                                          │
                                       main.py
```

`retriever.py` deliberately does not import `assistant.py` and has no idea a language model
exists. That separation is not tidiness — it's what makes the debugging below possible.

## When an answer is wrong

There are two completely different causes, with two completely different fixes. **Always
check them in this order:**

**1. Did the right chunk come back?**

```bash
> /sources why are there two trackers?
```

If the chunk containing the answer isn't in that list, the model never had a chance. The
fix is in your **documents, your chunk size, or `RETRIEVE_K`** — not in the prompt.

- Chunk too fragmented? Raise `CHUNK_SIZE` in `config.py` and re-run `ingest.py`
- Answer exists but ranks 6th? Raise `RETRIEVE_K`
- Document is one enormous wall of text? Add headings and split it into several files.
  This helps more than any setting.

**2. It came back, and the model ignored it.**

*Now* it's the prompt. Edit `SYSTEM_PROMPT` in `assistant.py`.

Debugging the prompt when the problem is retrieval is the most common way to waste an
afternoon on this technique.

## The dials

All in `config.py`:

| Setting | What it does | Changing it means |
|---|---|---|
| `CHUNK_SIZE` (1000) | How big each piece is. Too small loses context, too large brings back noise | re-run `ingest.py` |
| `CHUNK_OVERLAP` (200) | How much each chunk repeats the previous one, so boundary sentences survive | re-run `ingest.py` |
| `RETRIEVE_K` (4) | How many chunks per question. Too few misses answers, too many makes them vague | takes effect immediately |
| `CHAT_MODEL` | Which company's model answers | see below |

**Change one at a time, and decide how you'll measure before you start.** Write down five
questions you know the answers to, score the assistant on them now, then change one thing
and score it again. Otherwise you're just moving numbers around and hoping.

## Changing the AI provider

Open `config.py`, change **one line**:

```python
CHAT_MODEL = "openai:gpt-4.1-mini"                   # the default
# CHAT_MODEL = "anthropic:claude-haiku-4-5-20251001"
# CHAT_MODEL = "google-genai:gemini-2.5-flash"
# CHAT_MODEL = "ollama:llama3.2"                     # runs on this laptop
```

Install that provider's package (uncomment the matching line in `requirements.txt`) and add
its key to `.env`. Ollama needs no key.

**Your embeddings and your vector store already run locally.** So switching `CHAT_MODEL` to
Ollama makes the *entire* system offline — unplug the network and it keeps working, and
nothing you own ever leaves the laptop. For a hospital, a law firm or a school, that
property is sometimes the only reason a project like this is allowed to exist.

Swapping the vector store (to Pinecone, Qdrant, pgvector) or the embeddings (to a paid,
more accurate model) is the same kind of change — a couple of lines in `retriever.py` and
`ingest.py`, with everything around them untouched. That's what going through LangChain
bought us.

## Costs

Text only, cheap tier. Embeddings are **free** — they run on your laptop.

Roughly a fraction of a cent per question. A whole session of heavy use is a few cents.

## When it breaks

| What you see | What it means | Fix |
|---|---|---|
| `❌ No index found` | `ingest.py` hasn't been run | `python ingest.py` |
| It says "that isn't in your documents" about everything | The index is empty or stale | Check `documents/` has files, re-run `ingest.py` |
| `❌ No OPENAI_API_KEY found` | `.env` missing, misnamed or in the wrong folder | Must be called exactly `.env`, next to `main.py` |
| `ModuleNotFoundError` | venv not activated, or packages not installed | Re-activate, then `pip install -r requirements.txt` |
| First run hangs for ages | The embedding model is downloading (~900 MB) | Wait. It only happens once. |
| Answers cite the right file but are vague | `RETRIEVE_K` too high, or chunks too big | Lower `RETRIEVE_K`; try `CHUNK_SIZE` 500 |

---

## What my assistant knows about

> **Students: replace this section with your own.** Say what documents you loaded, show one
> question it answers well, show one it correctly refuses, and say one thing that went
> wrong along the way.

Example of the shape it should take:

> My Study Buddy knows my **biology revision notes** — seven markdown files on cells,
> genetics and the nervous system, about 20,000 words total.
>
> **It answers well:** "what's the difference between mitosis and meiosis?" — four clear
> sentences, citing `cell_division.md` and `exam_notes.md`.
>
> **It correctly refuses:** "when is the exam?" — that's in an email, not in my notes, and
> it says so instead of guessing a date.
>
> **What went wrong:** my first attempt loaded one 15,000-word file exported from a PDF
> with no headings. Retrieval was terrible — `/sources` showed it returning the same two
> chunks for every question. Splitting it into seven topic files fixed it completely, and
> I didn't change a single line of Python to do it. The lesson was that the documents
> matter more than the code.
>
> **What I added:** a `/stats` command that reports how many chunks came from each file, so
> I can see which of my notes are actually being used and which never come up.
