# Lesson 6 — From Notebook to Python Project

**Student guide. Keep this open in a side pane while you work.**

Today you build the real thing. Nothing new about AI — everything you need, you already
wrote in Lessons 1–5. You're reorganising it into a program you can hand to someone.

> **Open this in VS Code's preview:** right-click the file in the Explorer →
> *Open Preview*. Then you can read it next to your code.

---

## Why we're leaving the notebook

A notebook is a **lab bench**. It's perfect for trying things: run a cell, look, change it,
run again.

But you don't hand someone your lab bench. You hand them **the thing you built on it**.

There's a second reason, and it's the design idea of today. Right now, every time you
reopen your notebook you re-read every document and re-calculate every embedding before
you can ask a single question. That's about thirty seconds of waiting, every time, to
redo work that hasn't changed.

So the project splits into **two programs**:

| | `ingest.py` | `main.py` |
|---|---|---|
| **Speed** | Slow (seconds to minutes) | Fast (starts instantly) |
| **When you run it** | Only when your documents change | Every time you want to ask something |
| **What it does** | Reads documents → chunks → embeddings → saves an index to disk | Opens the saved index and answers questions |

Recognising that a system has a **build step** and a **run step** is a real piece of
software design. You'll see it everywhere once you've noticed it once.

---

## The plan

Five files. The rule we're following: **each file must be explainable in one sentence.**

| File | Its one sentence |
|---|---|
| `config.py` | Every setting in one place. |
| `ingest.py` | Turn documents into a saved search index. |
| `retriever.py` | Given a question, find the relevant chunks. |
| `assistant.py` | Turn chunks into a grounded answer. |
| `main.py` | Talk to the human. |

And the arrows only point one way:

```
  BUILD (run occasionally)            ASK (run constantly)

  documents/                          your question
      │                                     │
   ingest.py ──► vector_db/ ────────► retriever.py
      │                                     │
      └──────────► config.py ◄──────── assistant.py
                                            │
                                         main.py
```

`retriever.py` doesn't know `assistant.py` exists. `config.py` doesn't know about anything.
That's deliberate, and in Lesson 7 you'll find out why it matters.

---

## Step 1 — Make the folder (5 min)

**In your shared folder, not on the laptop** — you may be at a different Mac next lesson,
and your project needs to come with you. Replace the path with your own:

```bash
cd /Volumes/TUMO/students/your_name

mkdir study_buddy
cd study_buddy
mkdir documents

source /opt/tumo/ai-workshop/.venv/bin/activate    # prompt must show (.venv)
code .
```

Copy your `.md` / `.txt` notes into `documents/`, and copy your `.env` in too — the one
with your API key.

> **Why the split?** Python and the packages live on the laptop at
> `/opt/tumo/ai-workshop/.venv` because they're large and identical everywhere. Only
> *your* work — code, documents, the index you're about to build — goes on shared
> storage, so it follows you between machines.

✅ **Check:** VS Code's Explorer shows `study_buddy` with `documents/` inside it, and
`pwd` shows your shared path, not `/Users/...`.

---

## Step 2 — `config.py` (15 min)

Every constant from all five notebooks moves here. When you want to change the model, or
the chunk size, or how many chunks get retrieved, **this is the only file you open.**

Create `config.py` and write it. The things it must hold:

- `load_dotenv(override=True)` — so the API key gets loaded
- `PROJECT_DIR`, `DOCUMENTS_DIR`, `DB_DIR` — built with `Path(__file__).parent`
- `CHAT_MODEL`, `TEMPERATURE`
- `EMBEDDING_MODEL`
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `RETRIEVE_K`

> **Why `Path(__file__).parent` and not just `"documents"`?**
> `__file__` is this file. `.parent` is the folder it's in. So the paths work no matter
> which directory you happen to run the program from. Plain `"documents"` breaks the
> moment you run `python study_buddy/main.py` from one level up.

✅ **Check:**
```bash
python config.py
```
It should print **nothing** and exit cleanly. That's correct — `config.py` does no work,
it only holds decisions. If you get an error, fix it now; every other file imports this one.

---

## Step 3 — `ingest.py` (25 min)

The slow half. Four functions:

| Function | Does |
|---|---|
| `load_documents()` | Read every `.md`/`.txt` in `documents/` into `Document` objects |
| `split_into_chunks(documents)` | `RecursiveCharacterTextSplitter` with your settings |
| `build_index(chunks)` | Embed everything, save to `DB_DIR` |
| `main()` | Call the three in order, printing progress |

Three things that matter and are easy to miss:

1. **`encoding="utf-8"` on every read.** Without it Windows mangles Armenian characters.
2. **`sorted()` when globbing files.** Otherwise the order depends on the filesystem, and
   results that change for no visible reason are miserable to debug.
3. **Delete the old index before building a new one.** Otherwise you add a second copy of
   every chunk on top of the old one, and searches return duplicates — or chunks from
   documents you deleted last week.

End the file with:

```python
if __name__ == "__main__":
    main()
```

✅ **Check:**
```bash
python ingest.py
```
You should see your filenames, a chunk count, and a `vector_db/` folder appear in the
Explorer. Open it — you'll see the database files. **You have never had to do this before:
your program just created something that outlives it.**

---

## Step 4 — `retriever.py` (20 min)

The search half. **It must not import `assistant.py` and must never mention a language
model.** That isn't fussiness — it's what lets you test search on its own, for free, which
is exactly what Lesson 7 is about.

It needs:

- `embeddings` — **the same model `ingest.py` used**. Different models produce
  incompatible vectors, and the search will still run and return nonsense with no error.
- `vectorstore` — opens the saved index (it doesn't build one)
- `index_exists()`, `chunk_count()`
- `find_relevant_chunks(question, k)` → a list of chunks
- `find_relevant_chunks_with_scores(question, k)` → chunks plus distances
- `sources_of(chunks)` → unique filenames, sorted

✅ **Check** — make a scratch file `try_it.py`:
```python
import retriever

print(retriever.chunk_count(), "chunks in the index")
for doc in retriever.find_relevant_chunks("a question about your notes", k=3):
    print("-", doc.metadata["filename"], "|", doc.page_content[:60])
```
```bash
python try_it.py
```
**This costs nothing** — no model is involved. Delete `try_it.py` when it works.

---

## Step 5 — `assistant.py` (15 min)

The answering half. It holds:

- `model = init_chat_model(config.CHAT_MODEL, temperature=config.TEMPERATURE)`
- `SYSTEM_PROMPT` — including the refusal sentence from Lesson 5
- `build_context(chunks)` — join with `"\n\n---\n\n"`
- `build_search_query(question, history)` — glue the last two questions on
- `answer_question(question, history=None, k=...)` → `(answer, sources)`

> **The `history=None` matters.** Writing `history=[]` in the signature creates that list
> **once**, when the function is defined, and every call then shares it — so the assistant
> would silently accumulate every conversation it ever had. See the mutable-default
> section of `PYTHON_CHEATSHEET.ipynb`. This is the most famous trap in Python and you
> only need to meet it once.

✅ **Check:** add to a scratch file:
```python
import assistant
answer, sources = assistant.answer_question("something your notes cover")
print(answer, "\nSources:", sources)
```
This one **does** cost a fraction of a cent.

---

## Step 6 — `main.py` (10 min)

Talks to the human and does nothing else. Every piece of real work happens elsewhere.

```
welcome()                         print the header
if not retriever.index_exists()   tell them to run ingest.py first, and stop
history = []                      the conversation so far
loop:
    question = input("> ")
    /quit     → stop
    /forget   → history = []
    /sources  → show retrieved chunks and scores, no model call
    otherwise → answer_question(question, history); print; append to history
```

Wrap the loop body in **one** `try` / `except` — one place, at the edge of the program.
Everything underneath is allowed to fail loudly; it's this loop's job to turn a failure
into a sentence a human can act on and carry on.

Finish with `if __name__ == "__main__": main()`.

### ✅ The moment

```bash
python main.py
```

Ask it something. **That's a real program you wrote, running from a terminal, with no
notebook anywhere.**

---

## If you're stuck

| Problem | Almost certainly |
|---|---|
| `ModuleNotFoundError: config` | You're in the wrong folder. `cd` to where `main.py` is. |
| `ModuleNotFoundError: langchain...` | venv not activated in this terminal. |
| `No index found` | You haven't run `python ingest.py` yet. |
| It refuses everything | Index is empty or stale. Check `documents/` has files, re-run ingest. |
| Answers are nonsense | `EMBEDDING_MODEL` differs between `ingest.py` and `retriever.py`. Make them match, re-ingest. |
| `No ANTHROPIC_API_KEY` | `.env` isn't in this folder, or isn't named exactly `.env`. |

Fallen behind? The finished version of every file is in the workshop repo under
`course_b_study_buddy/project/`. **Read it, understand the file, then write your own** —
copying it without reading means Lesson 7 will be very hard.

---

## Before you leave

You must have a working `python main.py`. Your teacher will check individually.

**Next lesson:** your own documents, properly — and what to do when the answers are wrong.
