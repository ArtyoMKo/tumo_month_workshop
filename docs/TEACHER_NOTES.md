# Teacher notes

Read this before Lesson 1.

> **Scope:** the track being taught is **AI Study Buddy** (RAG over the student's own
> documents), 8 lessons × 2 hours, running on OpenAI's GPT-5.4 mini on TUMO's
> OpenAI API key. **Course A (AI Image Studio) is not scheduled** and is kept in this repo
> for reference only.
>
> **Python is not taught.** Students arrive with basic Python from other TUMO tracks.
> They get `PYTHON_CHEATSHEET.ipynb` in Lesson 1 as a lookup reference and it is never
> lectured from. The hour saved is spent on prompt engineering (Lesson 1) and
> conversation memory (Lesson 5).

---

## 1. Machines, storage, and the time budget

**All 16 machines are macOS**, and TUMO IT prepares them in advance. The requirements
list lives in the software section of `TUMO_APPLICATION.md`: Python 3.12, VS Code with
the Python and Jupyter extensions, the packages from `requirements.txt`, and the API key
available as `OPENAI_API_KEY`.

| Scenario | Lesson 1 setup | Consequence |
|---|---|---|
| IT prepared the machines (expected) | ~15 min | Lesson 1 runs as written |
| IT did not | 45+ min | Lesson 1 is lost to `pip install` × 16 over shared wifi |

Confirm two things with IT beforehand: the **student directory path is identical on every
machine**, and the **exact command to activate the Python environment** — students need
it on the board in Lesson 1.

**The critical items are §3 and §4 of that document** — the packages and the key. Run
`check_setup.py` on one lab machine the day before (see §4 below); it is the single best
way not to lose a lesson.

### Students change laptops between lessons

They may sit at a different Mac each time, so the split matters:

| | Where | Why |
|---|---|---|
| Python + packages | on the laptop | large, machine-specific, identical everywhere |
| Student's code, documents, index | **their shared folder** | follows them between machines |

So the two lines that start every lesson are:

```bash
cd <student's shared folder>/ai_workshop
source <the environment path>/.venv/bin/activate
```

**Get both exact paths from IT before Lesson 1** and put them on the board for the first
three lessons. "It worked last time" is
almost always a forgotten `source`.

**Do not let students create their own venv on shared storage.** A venv hardcodes
absolute paths and symlinks a specific Python binary; on network storage it is slow and
fragile, and 16 copies of the same packages is pure waste.

### Privacy — mention it in Lesson 1, before the homework

TUMO's shared storage is readable by everyone: you can see student folders, and so can
the other students. From Lesson 2 they bring their **own documents** into those folders.

Say it once, plainly, when you set the homework — bring notes on a **general subject**,
keep personal material out. The lesson 1 notebook has the same note in writing. It does
not need to be a big deal; it does need to be said before they choose what to bring,
rather than after.

Worth knowing: the `.env` file is equally visible, but it holds the same shared workshop
key everyone already has, so nothing is exposed that isn't already.

## 2. API keys and ages

**The workshop runs on OpenAI**, on TUMO's organisation API key. The model is
**GPT-5.4 mini** (`gpt-5.4-mini`) — OpenAI's fast, cheap current model.

API accounts require the account holder to be 18+, so students aged 13-18 **cannot** be
asked to create their own. Use a **TUMO-owned key** distributed to students, and set a
budget limit on its project in the OpenAI dashboard (platform.openai.com).

Keys begin `sk-proj-`. `check_setup.py` checks the `sk-` prefix and rejects Anthropic
`sk-ant-` keys, so a student who pastes a key from some other tutorial gets a clear
message instead of a 401.

### Budget

GPT-5.4 mini is $0.75 per million input tokens and $4.50 per million output tokens.
Embeddings (`text-embedding-3-small`, $0.02 per million tokens) cost **well under a cent**
for the whole group and course.

One question ≈ 850 input tokens (four retrieved chunks plus the system prompt) and
~100 output tokens ≈ **0.11 cents**.

| | |
|---|---|
| Per student, per 2-hour lesson (~40 questions) | ~4.4 cents |
| Per student, whole 16-hour course | ~35 cents |
| **Per group of 16, whole course** | **~$6** |

Budget **$10 per group** and you have comfortable headroom, including Lesson 8 where
some students will switch to `gpt-5.4` (~3× the price) to compare. Set the cap anyway —
a student who puts a model call inside a `for` loop with the wrong range is learning, not
misbehaving, but the bill is real.

## 2b. Student materials, lesson by lesson

Every lesson has something the student opens. The **format changes at Lesson 6**, and that
is deliberate rather than an omission:

| Lessons | Student material | Why |
|---|---|---|
| 1-5 | `notebooks/lesson1-5.ipynb` | Exploration — a notebook is the right tool |
| 6-8 | `guides/lesson6-8_*.md` | They are editing `.py` files in VS Code; open the guide in the preview pane beside the code |

Lesson 6 has no notebook **on purpose** — the whole lesson is about leaving the notebook.
Its guide is step-by-step with a ✅ check after each file, so students who fall behind can
catch up without stopping the room, and it points at `project/` for anyone who falls badly
behind (with an explicit "read it, then write your own" instruction).

`notebooks/PYTHON_CHEATSHEET.ipynb` is handed out in Lesson 1 and used for lookup all
course. It runs with no API key and no internet, so it is also the thing to give students
who finish setup early.

## 3. Running fully free / offline

Chroma is local, and only the two OpenAI models cost anything. Switch `CHAT_MODEL` to
`ollama:llama3.2` and the answering half runs with **no paid API** - worth doing once in
Lesson 5 if the lab can run Ollama, as a live demonstration that the provider-agnostic
layer was worth building.

**Fully offline** needs one more step: swap `OpenAIEmbeddings` for `OllamaEmbeddings`
(the comment in `retriever.py` shows how) and re-run `ingest.py`. Good extension for a
fast student, and a good answer to "could a hospital run this?" - but it's a
multi-gigabyte model download, so don't do it lab-wide.

**Armenian is the known weak spot.** `text-embedding-3-small` is strong in English and
much weaker in Armenian: on the Kestrel files it put the right chunk in the top 4 for 7 of
8 English questions but only 1 of 4 Armenian ones, and an Armenian question scores an
unrelated English sentence *above* its answer. Lesson 4 measures this openly. Steer
students towards English notes, and have anyone with Armenian notes check retrieval
(`/sources` in `main.py`) before trusting answers. It is also the cleanest possible
demonstration of why the retriever and the assistant were kept in separate files: a
better multilingual embedding model could be swapped in without touching the rest.

## 4. Pre-flight check - do this with a real key before Lesson 1

The project ships a `check_setup.py`. Run it on one lab machine with the real workshop key
**before the first lesson**:

```bash
python check_setup.py
```

It runs eight checks in dependency order and stops at the first failure with a specific
fix: Python version, every import, the `OPENAI_API_KEY` and its `sk-` prefix, the
embedding model, the documents folder, the built index, a retrieval with no model
involved, and finally one real model call. The expensive check is last on purpose.

## 5. Group size and pacing

16 students, one instructor. Realistic expectations:

- Expect 2-3 students stuck on setup at any moment in Lesson 1. Pair students up for
  Lesson 1 only; the ones who finish first become debuggers.
- Students have basic Python, but "basic" varies a lot. Point at the cheatsheet rather
  than explaining syntax from the front - it keeps the lesson moving and teaches them to
  look things up. Budget circulating time in Lessons 1-3 for individuals. The spread
  narrows from Lesson 4 on, when the new material is conceptual rather than syntactic.

Most notebooks have an **Extra challenge** callout. These exist so the fast students have
somewhere to go that isn't "help me help the others" - though that's a fine answer too.

## 6. What to do if a lesson runs over

Cut in this order, and cut rather than compress:

(1) The t-SNE visualisation in Lesson 4 — it's beautiful and completely optional.
(2) The chunk-size tuning experiment in Lesson 8.
(3) The `gpt-5.4-mini`-vs-`gpt-5.4` comparison in Lesson 8, if the test sets aren't ready in time.

**Never cut Lesson 5** — that's where RAG actually closes the loop — and **never cut
Lesson 6**, the notebook-to-project move, which is the point of the whole course.
