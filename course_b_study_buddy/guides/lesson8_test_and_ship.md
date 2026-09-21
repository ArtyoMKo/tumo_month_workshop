# Lesson 8 — Testing, Tuning and Final Demo

**Student guide. Keep this open in a side pane while you work.**

Last lesson. Today: find out whether your changes actually help, finish the project
properly, and show it.

---

## Part 1 — How would you know if you made it better?

Here's the trap everyone falls into. You change `RETRIEVE_K` from 4 to 6, ask a question,
think *"yeah, that seems better"*, and keep it.

You have measured **nothing**. The model gives slightly different wording every time. You
asked one question. You already expected it to improve, so it looked like it did.

The fix is boring and it is what professionals actually do:

> **Decide how you'll measure before you change anything.**

### Write your test set — 5 questions, known answers

Reuse the five from Lesson 7 if they're good. Cover different shapes:

| # | Question | The answer I know is correct | Shape |
|---|---|---|---|
| 1 | | | a plain fact in one file |
| 2 | | | needs two files together |
| 3 | | | worded differently from the notes |
| 4 | | | a detail that's easy to miss |
| 5 | *(something your notes DON'T cover)* | **"That isn't in your documents."** | must refuse |

**Question 5 is not optional.** An assistant that answers everything is worse than one
that admits what it doesn't know, and it's the thing you're demoing later.

### Score your baseline — before touching anything

| # | Correct? | Cited the right file? | Notes |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| **Baseline** | **/5** | | |

---

## Part 2 — Tune, one thing at a time

**One change. Re-score all five. Write it down. Then the next change.**

If you change three things at once and the score goes up, you don't know which one did it —
and you can't undo the two that might have made it worse.

| What to change | Where | Re-ingest? |
|---|---|---|
| `RETRIEVE_K` (try 2, 4, 8) | `config.py` | No |
| `CHUNK_SIZE` (try 500, 1000, 2000) | `config.py` | **Yes** |
| `CHUNK_OVERLAP` | `config.py` | **Yes** |
| `SYSTEM_PROMPT` wording | `assistant.py` | No |
| The documents themselves | `documents/` | **Yes** |
| `CHAT_MODEL` → `anthropic:claude-sonnet-5` | `config.py` | No |

### Your tuning log

| Try | What I changed | Score /5 | Keep it? |
|---|---|---|---|
| 0 | *(baseline — nothing changed)* | | — |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

### The interesting one: does a pricier model actually win?

`claude-haiku-4-5` is Anthropic's cheapest. `claude-sonnet-5` is roughly **twice the
price**. Swap it in `config.py`, re-score all five, and find out.

Think about why the answer is often **no**. In RAG the model isn't doing the hard part —
the retriever already found the answer and put it in front of it. The job is to read four
paragraphs and not invent anything. That's a job a small model does well.

If Sonnet doesn't beat Haiku on your test set, **that is a real finding and worth saying
in your demo.** "I tested it and the expensive one wasn't better" is a much stronger
statement than guessing either way.

> Put it back to Haiku afterwards unless Sonnet genuinely won.

---

## Part 3 — Finish it

### `requirements.txt`
Every package someone needs. If you added a library, it goes in here.

### `.env` — the safety check
```bash
ls -a
```
- `.env` — your real key. **Never share this.**
- `.env.example` — the template with a placeholder. **This one you share.**
- `.gitignore` — must contain `.env`

### `README.md`
Not "what I did" — **"how you run this"**. Four sections:

```markdown
# My Study Buddy
What it is, and what documents it knows about.

## Install
The exact commands, in order.

## Run
    python ingest.py
    python main.py

## What I added
The feature I built, which file it lives in, and one thing that broke on the way.
```

The "one thing that broke" line is the most interesting part to read. Don't skip it.

---

## Part 4 — The fresh-machine test

**This finds more real problems than any amount of re-reading your own code.**

1. Swap folders with the person next to you
2. Follow **their README literally**. Type only what it says.
3. Write down every point where you got stuck or had to guess
4. Swap back and fix what they found

You will discover that you forgot to mention creating `.env`, or that you never said to
run `ingest.py` first. Everyone does. That's what the test is for.

---

## Part 5 — Your demo (~90 seconds)

Have it running **before** you start talking.

1. **What it knows about** — "my biology revision notes, seven files"
2. **One good answer** — ask live, point at the sources line
3. **One correct refusal** — ask something outside your notes. *This is the important one.*
4. **What you added** — your feature, in one sentence
5. **One thing that broke** — and what it turned out to be

> Point 3 is what you've actually been building for eight lessons. A chatbot that answers
> everything is easy. One that knows the edge of what it knows is the hard part, and the
> valuable part.

---

## Final checklist

- [ ] Five test questions written, with baseline and final scores
- [ ] Tuning log filled in, one change per row
- [ ] Tested whether the more expensive model actually helped
- [ ] `requirements.txt` complete
- [ ] `.env` **not** shareable; `.env.example` present
- [ ] `README.md` with all four sections
- [ ] A classmate ran your project from your README alone
- [ ] You can demo one correct answer **and** one correct refusal

---

## Where to go next

- **Keep it running.** Your key stops working after the workshop — switch `CHAT_MODEL`
  to `ollama:llama3.2` and the answering half runs free on your own laptop, forever.
  Searching stays hosted by Hugging Face, which is free anyway, so you still need
  internet for that part.
- **Feed it something bigger.** A whole textbook, a wiki export, every note you've ever taken.
- **Go fully offline.** Swap `HuggingFaceEndpointEmbeddings` back to
  `HuggingFaceEmbeddings` (the same model, run on your machine — add
  `sentence-transformers` to requirements), pair it with Ollama, and the whole thing runs
  with the network unplugged. It costs a ~1.2 GB install, which is exactly why we didn't
  do it in class.
- **Try a hosted vector store** (Pinecone, Qdrant) — in this architecture it's a few lines
  in `retriever.py` and `ingest.py`.
- **Read the LangChain docs.** You now know what the words mean, which is most of the battle.

You built a real thing. Keep it.
