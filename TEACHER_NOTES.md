# Teacher notes

Read this before Session 1 of either course.

---

## 1. The local-machine tax on the time budget

Both courses are costed at **exactly 16 hours (8 x 2h)**. Local installs are not free, and
the cost lands entirely in Session 1. Two scenarios:

| Scenario | Setup time in Session 1 | Consequence |
|---|---|---|
| **Machines prepared in advance** (recommended) | ~15 min | Session 1 runs as written, students generate their first image / ask their first question in Session 1 |
| **Students install from scratch** | ~40-50 min | Session 1's hands-on block shrinks; the schedule still fits, but the "wow moment" slides to the end of the session and some students won't reach it |

**What "prepared in advance" means.** Ask TUMO IT to do this on every machine, once:

1. Python 3.12 installed and on PATH.
2. VS Code installed with the **Python** and **Jupyter** extensions.
3. `pip download`-ed or pre-installed wheels for the course's `requirements.txt`,
   so Session 1 is a cache hit rather than a 300 MB download x 16 machines.
4. **Course B only, and this is the big one:** pre-run this once per machine so the
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

API accounts with OpenAI, Anthropic and Google require the account holder to be 18+.
Students aged 13-18 **cannot** be asked to create their own. Use a **TUMO-owned key**
distributed to students, and set a hard spend limit on it in the provider dashboard.

Rough budget, per group of 16, for the whole 16 hours:

- **Course A** - image generation dominates. At `quality="low"` expect roughly
  1-2 US cents per image. Budget ~60 images per student across 8 sessions
  (they *will* generate more than you expect once it works) = **~$15-20 per group**.
  Raise the quality setting only for the final showcase.
- **Course B** - text only, and the cheap tier. With `gpt-4.1-mini` and local
  HuggingFace embeddings (embeddings cost nothing, they run on the laptop),
  expect **under $3 per group**.

Set the spend cap anyway. A student who puts an image call in a `for` loop with the wrong
range is not misbehaving, they're learning, but the bill is real.

## 3. Running fully free / offline

Course B runs **end to end with no API key at all**: local HuggingFace embeddings,
local Chroma, and `ollama:llama3.2` as the chat model. If the lab can run Ollama, this is
worth doing at least once in Session 5 as a live demonstration of why the provider-agnostic
layer was worth building - one line changes, everything else keeps working.

**Course A cannot do this.** There is no image-generation model exposed through Ollama's
chat API. In Course A the *text* side (prompt improvement) is fully swappable including
Ollama, but the *image* side needs OpenAI or Google. This limitation is stated plainly in
the Session 5 notebook rather than hidden - it's a genuinely good teaching moment about
what abstractions can and can't paper over.

## 4. Pre-flight check - do this with a real key before Session 1

Each project ships a `check_setup.py`. Run it on one lab machine with the real workshop key
**before the first session**:

```bash
python check_setup.py
```

It verifies: Python version, every import, the `.env` key, one cheap chat call, and
(Course A) one real image generation. If the image-generation call fails because the
default model doesn't expose the `image_generation` tool on your account, change the one
line in `config.py` - `check_setup.py` prints the exact line to change.

## 5. Group size and pacing

16 students, one instructor. Realistic expectations:

- **Course A** - expect 2-3 students stuck on setup at any moment in Session 1.
  Pair students up for Session 1 only; the ones who finish first become debuggers.
- **Course B** - the "stronger/faster" framing is real, but *faster at JavaScript* is not
  the same as *faster at Python*. Session 1 still teaches Python syntax explicitly.
  The speed difference shows up from Session 3 onward, not before.

Both courses have an **Extra challenge** callout in most notebooks. These exist so the
fast students have somewhere to go that isn't "help me help the others" - though that's a
fine answer too.

## 6. What to do if a session runs over

Cut in this order, and cut rather than compress:

**Course A:** (1) the batch-generation section in Session 4, (2) the prompt-improver in
Session 5 - the project works without it, it's an `if` away. Never cut Session 6; the
notebook-to-project move is the point of the course.

**Course B:** (1) the t-SNE visualisation in Session 4 - it's beautiful and completely
optional, (2) the chunk-size tuning experiment in Session 8. Never cut Session 5;
that's where RAG actually closes the loop.
