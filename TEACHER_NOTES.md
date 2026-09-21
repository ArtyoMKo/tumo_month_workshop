# Teacher notes

Read this before Session 1.

> **Scope:** the track being taught is **Course B — Study Buddy** (RAG), running on
> Anthropic's Claude Haiku 4.5 under TUMO's contract. **Course A (AI Image Studio) is not
> scheduled** and is kept in this repo for reference only; it cannot run on Anthropic,
> since Anthropic has no image-generation model. Everything below is about Course B unless
> it says otherwise.

---

## 1. The local-machine tax on the time budget

Both courses are costed at **exactly 16 hours (8 x 2h)**. Local installs are not free, and
the cost lands entirely in Session 1. Two scenarios:

| Scenario | Setup time in Session 1 | Consequence |
|---|---|---|
| **Machines prepared in advance** (recommended) | ~15 min | Session 1 runs as written, students ask their first question in Session 1 |
| **Students install from scratch** | ~40-50 min | Session 1's hands-on block shrinks; the schedule still fits, but the "wow moment" slides to the end of the session and some students won't reach it |

**What "prepared in advance" means.** Ask TUMO IT to do this on every machine, once:

1. Python 3.12 installed and on PATH.
2. VS Code installed with the **Python** and **Jupyter** extensions.
3. `pip download`-ed or pre-installed wheels for the course's `requirements.txt`,
   so Session 1 is a cache hit rather than a 300 MB download x 16 machines.
4. **The big one:** pre-run this once per machine so the
   embedding model is already in the HuggingFace cache:

   ```bash
   python -c "from langchain_huggingface import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')"
   ```

   This downloads PyTorch (~800 MB) plus the model (~90 MB). Sixteen students triggering
   that simultaneously on shared lab wifi is the single most likely way to lose an entire
   session. Do it the day before.

If the machines are reset/reimaged between sessions, steps 1-4 must be re-applied, and
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
| Per student, per 2-hour session (~40 questions) | ~6 cents |
| Per student, whole 16-hour course | ~45 cents |
| **Per group of 16, whole course** | **~$7** |

Budget **$10 per group** and you have comfortable headroom, including Session 8 where
some students will switch to Sonnet 5 to compare. Set the cap anyway — a student who puts
a model call inside a `for` loop with the wrong range is learning, not misbehaving, but
the bill is real.

## 3. Running fully free / offline

Course B runs **end to end with no API key at all**: local HuggingFace embeddings,
local Chroma, and `ollama:llama3.2` as the chat model. If the lab can run Ollama, this is
worth doing at least once in Session 5 as a live demonstration of why the provider-agnostic
layer was worth building - one line changes, everything else keeps working.

Note that Course B has **two different vendors in it by necessity**: Anthropic answers the
questions, and the embedding model is a Hugging Face one, because Anthropic doesn't make an
embedding model. Far from being awkward, that's the cleanest possible demonstration of why
the retriever and the assistant were kept in separate files — Session 4 makes the point
explicitly.

## 4. Pre-flight check - do this with a real key before Session 1

The project ships a `check_setup.py`. Run it on one lab machine with the real workshop key
**before the first session**:

```bash
python check_setup.py
```

It runs eight checks in dependency order and stops at the first failure with a specific
fix: Python version, every import, the `ANTHROPIC_API_KEY` and its `sk-ant-` prefix, the
local embedding model, the documents folder, the built index, a retrieval with no model
involved, and finally one real Claude call. The expensive check is last on purpose.

## 5. Group size and pacing

16 students, one instructor. Realistic expectations:

- Expect 2-3 students stuck on setup at any moment in Session 1. Pair students up for
  Session 1 only; the ones who finish first become debuggers.
- The "stronger/faster" framing is real, but *faster at JavaScript* is not the same as
  *faster at Python*. Session 1 still teaches Python syntax explicitly. The speed
  difference shows up from Session 3 onward, not before.

Most notebooks have an **Extra challenge** callout. These exist so the fast students have
somewhere to go that isn't "help me help the others" - though that's a fine answer too.

## 6. What to do if a session runs over

Cut in this order, and cut rather than compress:

(1) The t-SNE visualisation in Session 4 — it's beautiful and completely optional.
(2) The chunk-size tuning experiment in Session 8.
(3) The Haiku-vs-Sonnet comparison in Session 8, if the test sets aren't ready in time.

**Never cut Session 5** — that's where RAG actually closes the loop — and **never cut
Session 6**, the notebook-to-project move, which is the point of the whole course.
