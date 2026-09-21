# Lesson 7 — Your Own Knowledge Base

**Student guide. Keep this open in a side pane while you work.**

Your assistant works. Today it starts working on **your** material — and you find out
that RAG lives or dies on the documents, not on the code.

---

## First: confirm you're starting from something that works

```bash
python main.py
```

Ask one question, get one answer, quit. **Do this before changing anything.** If you
change five things and it breaks, you won't know which one did it.

---

## Part 1 — Garbage in, garbage out

The single biggest factor in how good your assistant is isn't the model, the chunk size,
or `k`. It's **your documents**.

| A good document | A bad document |
|---|---|
| Has headings (`## Cell division`) | One unbroken wall of text |
| Short paragraphs, one idea each | Pages of run-on prose |
| One topic per file | Everything in `notes.md` |
| Plain sentences | Tables and diagrams pasted as text |
| Says things explicitly | Relies on context that's only in your head |

That last row catches people. If your notes say *"this is the important one"*, retrieval
has nothing to match — "this" means nothing on its own. Write *"mitosis is the important
one for the exam"* and it becomes findable.

### Do it now

1. Put your files in `documents/`
2. `python ingest.py`
3. `python main.py`
4. Ask **five questions you already know the answers to**

Write the five down. You'll reuse them all lesson, and again in Lesson 8.

| # | Question | Right answer? | Notes |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

---

## Part 2 — Splitting the blame

**This is the most important skill in the lesson.**

When an answer is wrong there are **two completely different causes**, with two completely
different fixes. Work out which one *before* you change anything:

```
        Answer is wrong
               │
        Run: /sources <your question>
               │
     ┌─────────┴─────────┐
     │                   │
 Right chunk         Right chunk
 NOT in the list     IS in the list
     │                   │
 RETRIEVAL problem   GENERATION problem
     │                   │
 Fix your documents, Fix the system prompt
 chunk size, or k    in assistant.py
```

**Never debug the prompt when the problem is retrieval.** It's the most common way to
waste an afternoon on this technique — you'll rewrite the prompt six times and nothing
will improve, because the model never had the information in the first place.

`/sources` shows you exactly what was retrieved, with scores, **without calling the model
at all**. It costs nothing. Use it constantly.

```
> /sources why do plant cells have a cell wall?

  1. [0.412] biology_cells.md
     Plant cells have a rigid cell wall made of cellulose...
```

### Fixes for a RETRIEVAL problem

| Symptom | Try |
|---|---|
| Right chunk missing entirely | Your documents don't actually say it. Add it. |
| Chunk comes back but cut in half | Raise `CHUNK_SIZE` → re-run `ingest.py` |
| Right chunk ranks 6th | Raise `RETRIEVE_K` in `config.py` (no re-ingest needed) |
| Same 2 chunks for every question | One huge file. Split it up, add headings → re-ingest |
| Nothing sensible ever comes back | Check `EMBEDDING_MODEL` matches between ingest and retriever |

### Fixes for a GENERATION problem

| Symptom | Try |
|---|---|
| It refuses even though the chunk is right there | Soften the refusal sentence in `SYSTEM_PROMPT` |
| It answers from general knowledge | Strengthen it: "Use ONLY the notes below" |
| Answers too long/waffly | Add "Answer in at most three sentences" |
| Answers in the wrong language | Check the "same language" line is in your prompt |

> **Remember `ingest.py`.** Any change to `CHUNK_SIZE`, `CHUNK_OVERLAP`,
> `EMBEDDING_MODEL`, or the documents themselves means **re-running `python ingest.py`**.
> Changes to `RETRIEVE_K` or the system prompt take effect immediately.
> Forgetting this is the #1 source of "I changed it and nothing happened".

---

## Part 3 — Improve your documents, then measure

Pick the worst-performing of your five questions. Improve the *document*, not the code:

- Add headings to break up a long file
- Split a big file into topic files
- Delete navigation junk, page numbers, exported-PDF noise
- Rewrite one vague sentence to be explicit

Then:

```bash
python ingest.py
python main.py
```

Re-ask **the same five questions**. Did it get better?

Fill this in — you'll want it for Lesson 8:

| | Before | After | What I changed |
|---|---|---|---|
| Questions right out of 5 | | | |

Most students find that **fixing the documents beats every code change they could have
made.** That's the lesson.

---

## Part 4 — Build one feature

Pick one. The skill being tested is **deciding which file it belongs in**.

### Easier
- **Show scores with every answer** — `main.py`, using `find_relevant_chunks_with_scores`
- **`/help`** listing the commands — `main.py`
- **Cap the answer length** — one line in `SYSTEM_PROMPT`, `assistant.py`
- **Show how many chunks each file contributed** — `main.py`

### Medium
- **`/stats`** — which files the index holds and how many chunks from each — `retriever.py` + `main.py`
- **`/file <name> <question>`** — search only one document (metadata filter) — `retriever.py`
- **Save the conversation** to a `.md` file on quit — `main.py`
- **Warn on a weak match** — if the best score is worse than a threshold, say "I'm not confident" — `assistant.py`

### Harder
- **Make it quote its evidence** — the answer must include the sentence it relied on, in quotes — `SYSTEM_PROMPT`
- **`/why`** — show the full prompt that produced the last answer — `assistant.py` + `main.py`
- **Remember more turns**, and find where it starts hurting — `build_search_query`

**Ask yourself first: which file?** A change to how answers are worded goes in
`assistant.py`. A change to what the user can type goes in `main.py`. A change to how
searching works goes in `retriever.py`. Getting that judgement right is what Lesson 6's
structure was for.

---

## Before you leave

- [ ] Your own documents are in `documents/` and ingested
- [ ] Five test questions written down, with before/after results
- [ ] You can say, for any wrong answer, whether it's retrieval or generation
- [ ] One feature of your own, working

**Next lesson:** measure properly, tune against the measurements, and ship it.
