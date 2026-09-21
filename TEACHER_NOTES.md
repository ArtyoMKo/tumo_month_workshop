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

## 1. The local-machine tax on the time budget

Both courses are costed at **exactly 16 hours (8 x 2h)**. Local installs are not free, and
the cost lands entirely in Lesson 1. Two scenarios:

| Scenario | Setup time in Lesson 1 | Consequence |
|---|---|---|
| **Machines prepared in advance** (recommended) | ~15 min | Lesson 1 runs as written, students ask their first question in Lesson 1 |
| **Students install from scratch** | ~40-50 min | Lesson 1's hands-on block shrinks; the schedule still fits, but the "wow moment" slides to the end of the lesson and some students won't reach it |

**What "prepared in advance" means.** Ask TUMO IT to do this on every machine, once:

1. Python 3.12 installed and on PATH.
2. VS Code installed with the **Python** and **Jupyter** extensions.
3. `pip download`-ed or pre-installed wheels for the course's `requirements.txt`,
   so Lesson 1 is a cache hit rather than a 300 MB download x 16 machines.
4. **The big one:** pre-run this once per machine so the
   embedding model is already in the HuggingFace cache:

   ```bash
   python -c "from langchain_huggingface import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='paraphrase-multilingual-MiniLM-L12-v2')"
   ```

   This downloads PyTorch (~1.1 GB) plus the model (~470 MB). Sixteen students triggering
   that simultaneously on shared lab wifi is the single most likely way to lose an entire
   lesson. Do it the day before.

   **Why the multilingual model and not the usual `all-MiniLM-L6-v2`?** Because students
   choose their own documents, and many will bring Armenian notes. `all-MiniLM-L6-v2` is
   English-only, and on Armenian it does not degrade gracefully - it scores a correct
   answer and a completely unrelated sentence within 0.004 of each other, so retrieval
   becomes random and gives no error to say so. The multilingual model scores the same
   pair 0.145 apart, comparable to its English performance. It costs ~370 MB more and a
   little English precision. Worth it.

If the machines are reset/reimaged between lessons, steps 1-4 must be re-applied, and
students must re-create their `.env`. Check this with IT before the workshop starts.

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
