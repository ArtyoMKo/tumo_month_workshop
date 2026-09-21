# Teacher notes

Read this before Lesson 1.

> **Scope:** the track being taught is **AI Study Buddy** (RAG over the student's own
> documents), 8 lessons × 2 hours, running on Anthropic's Claude Haiku 4.5 under TUMO's
> contract. **Course A (AI Image Studio) is not scheduled** and is kept in this repo for
> reference only; it cannot run on Anthropic, which has no image-generation model.
>
> **Python is not taught.** Students arrive with basic Python from other TUMO tracks.
> They get `PYTHON_CHEATSHEET.ipynb` in Lesson 1 as a lookup reference and it is never
> lectured from. The hour saved is spent on prompt engineering (Lesson 1) and
> conversation memory (Lesson 5).

---

## 1. Machines, storage, and the time budget

**All 16 machines are macOS**, and TUMO IT prepares them in advance. The requirements
list lives in the software section of `TUMO_APPLICATION.md`: Python 3.12, VS Code with
the Python and Jupyter extensions, the packages from `requirements.txt`, the embedding
model pre-downloaded, and the API key available as `ANTHROPIC_API_KEY`.

| Scenario | Lesson 1 setup | Consequence |
|---|---|---|
| IT prepared the machines (expected) | ~15 min | Lesson 1 runs as written |
| IT did not | 45+ min | Lesson 1 is lost. `pip install` pulls ~2 GB per machine; the embedding model is another 470 MB × 16 over shared wifi |

Confirm two things with IT beforehand: the **student directory path is identical on every
machine**, and the **exact command to activate the Python environment** — students need
it on the board in Lesson 1.

**The critical item is §4 of that document** — pre-downloading the embedding model. It is
the single most likely way to lose a lesson.

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
fragile, and 16 copies of PyTorch is ~18 GB.

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

**The workshop runs on Anthropic**, under TUMO's existing contract. The model is
**Claude Haiku 4.5** (`claude-haiku-4-5`) — the cheapest current Claude model.

API accounts require the account holder to be 18+, so students aged 13-18 **cannot** be
asked to create their own. Use a **TUMO-owned key** distributed to students, and set a
spend limit on it in the Anthropic Console.

Keys begin `sk-ant-`. `check_setup.py` checks that prefix, because a student who pastes
an OpenAI-shaped key from some other tutorial gets a clear message instead of a 401.

### Budget

Haiku 4.5 is $1.00 per million input tokens and $5.00 per million output tokens.
Embeddings cost **nothing** — they run on the laptop.

One question ≈ 850 input tokens (four retrieved chunks plus the system prompt) and
~100 output tokens ≈ **0.14 cents**.

| | |
|---|---|
| Per student, per 2-hour lesson (~40 questions) | ~6 cents |
| Per student, whole 16-hour course | ~45 cents |
| **Per group of 16, whole course** | **~$7** |

Budget **$10 per group** and you have comfortable headroom, including Lesson 8 where
some students will switch to Sonnet 5 to compare. Set the cap anyway — a student who puts
a model call inside a `for` loop with the wrong range is learning, not misbehaving, but
the bill is real.

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

Course B runs **end to end with no API key at all**: local HuggingFace embeddings,
local Chroma, and `ollama:llama3.2` as the chat model. If the lab can run Ollama, this is
worth doing at least once in Lesson 5 as a live demonstration of why the provider-agnostic
layer was worth building - one line changes, everything else keeps working.

Note that Course B has **two different vendors in it by necessity**: Anthropic answers the
questions, and the embedding model is a Hugging Face one, because Anthropic doesn't make an
embedding model. Far from being awkward, that's the cleanest possible demonstration of why
the retriever and the assistant were kept in separate files — Lesson 4 makes the point
explicitly.

## 4. Pre-flight check - do this with a real key before Lesson 1

The project ships a `check_setup.py`. Run it on one lab machine with the real workshop key
**before the first lesson**:

```bash
python check_setup.py
```

It runs eight checks in dependency order and stops at the first failure with a specific
fix: Python version, every import, the `ANTHROPIC_API_KEY` and its `sk-ant-` prefix, the
local embedding model, the documents folder, the built index, a retrieval with no model
involved, and finally one real Claude call. The expensive check is last on purpose.

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
(3) The Haiku-vs-Sonnet comparison in Lesson 8, if the test sets aren't ready in time.

**Never cut Lesson 5** — that's where RAG actually closes the loop — and **never cut
Lesson 6**, the notebook-to-project move, which is the point of the whole course.
