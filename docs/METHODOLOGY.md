# Workshop Methodology

**What this is:** the complete specification for building a TUMO-style technical workshop
in the manner of `course_b_study_buddy`. Written for an agent that will build a *different*
course from scratch.

**How to use it:** read all of it before writing anything. Sections 1–8 are rules; section
9 is the verification discipline and is not optional; section 10 shows the reasoning style
through real decisions; section 11 lists what not to do.

**The worked example throughout** is "AI Study Buddy" — a 16-hour RAG workshop for 13–18
year-olds at TUMO Armenia. Substitute your own topic; the structure transfers.

**Lineage:** the notebook conventions derive from Ed Donner's *LLM Engineering* Udemy
course (`llm_engineering/week1–week8`). If that repo is available, read `week1/day1.ipynb`
and `week5/` before starting — `week5` is the canonical notebook→project transition.

---

## 1. Course architecture

### Three phases, always

| Phase | Lessons | Tool | Purpose |
|---|---|---|---|
| **Experimentation** | 1 … N-3 | Jupyter notebooks, one per lesson | New ideas, tried cell by cell |
| **Transition** | N-2 | VS Code, `.py` files | Reorganise working code into a project |
| **Project** | N-1, N | VS Code + terminal | Own material, tuning, shipping |

For 8 lessons: notebooks 1–5, transition 6, project 7–8.

**The transition lesson is the most valuable in the course** and must never be cut. It
teaches nothing new about the subject; it reorganises. Do not give it a notebook — the
lesson *is* leaving the notebook, and a notebook would contradict it.

### Time budget

- Total hours are a **hard ceiling**, not a target.
- Every lesson's activities must sum **exactly** to the lesson length.
- Verify this programmatically, not by eye (§9).
- If content doesn't fit, **cut a topic**; never compress one.

Each lesson agenda is a table: `| # | Activity | Min |` ending in a `**Total** | **120**`
row. Include breaks (5 min) as numbered rows — they're part of the budget.

### Per-lesson deliverable

Every lesson ends with one concrete, checkable artefact. Not "students understand X" —
something they *have*:

> **📦 Deliverable by end of lesson:** A working search engine over the student's own
> documents, plus three documented test cases with scores: one answered well, one where
> the right chunk ranks low, one the documents cannot answer.

The transition lesson's deliverable is the strictest: *"every student leaves with a
working `python main.py`, confirmed individually before they go home."*

### Spiral, not linear

Each lesson revisits the previous one's output and makes it insufficient. Lesson 2's
brute-force fix works, then fails on cost. Lesson 4's retrieval works, then returns
results for questions with no answer. The failure of lesson N is the motivation for
lesson N+1.

---

## 2. Pedagogical principles

These are the non-negotiables. Everything else is style.

### 2.1 Run it first, name it after

Never define a concept before the student has seen it happen. Fire the API call, *then*
explain what a system prompt is. The reference course does this explicitly: `week1/day1`
calls the model in cell 7 and explains prompts in cell 10.

### 2.2 Straw-man, then improve

Build the naive version first and let students feel it break. This is the single most
effective structure available:

| Lesson | Straw man | Why it fails | What it motivates |
|---|---|---|---|
| 2 | Ask the model directly | It invents answers | Grounding |
| 2 | Paste the whole document | Cost, context, quality | Retrieval |
| 4 | Word matching | "heaviest thing" vs "2.8 kg" share no words | Embeddings |
| 5 | Retrieval alone | Always returns k results | The refusal prompt |

Never present the good solution first.

### 2.3 Tiny cells, constant inspection

Median code cell in this workshop: **~250 characters**. Markdown-to-code ratio ~1:1.
A bare variable name on the last line displays it — use that constantly. Students should
be looking *inside* objects every few cells.

### 2.4 Predict before running

Where a result is surprising, make students commit first: *"Predict each of these before
you run the cell. Write your guesses down."* Then reveal that `hot`/`cold` scores **high**
because embeddings capture topic, not agreement.

### 2.5 Measure, never assert

Any claim about behaviour must be produced by code the student runs. Don't say "this is
expensive" — have them compute `$56.25 per 100 questions`. Don't say "this model is weak
in Armenian" — have them see an Armenian question score an unrelated line `0.079` and its
real answer `0.028`.

### 2.6 Teach the limits of what you teach

Every abstraction gets an honest boundary:
- `init_chat_model` unifies text models — and **cannot** make Ollama generate images.
- A system prompt is a strong instruction — **not a guarantee**; students attack their
  own refusal rule and meet prompt injection.
- Embeddings capture topic — **not agreement**; a retriever can return the opposite of
  the truth.

A student who knows where a tool stops working is ahead of most professionals using it.

### 2.7 Age-appropriate complexity

For 13–18 with basic programming:
- **No** async/concurrency, class hierarchies, design patterns, or deployment.
- **One** clean abstraction per course, taught explicitly.
- Flat functions. Classes only where they earn it.
- Project structure: 5–6 clearly named files, each explainable in one sentence.

### 2.8 Every student's output is different

Design so students supply their own input (their own documents, their own prompts, their
own feature). Sixteen identical projects is a failed workshop.

---

## 3. The document set

Produce all of these. Each has one job.

| File | Audience | Job |
|---|---|---|
| `README.md` | anyone | Index; what this is; the one-line provider swap |
| `OUTLINE.md` | organiser | TUMO's 4-part format: idea / skills / requirements / outcome |
| `CURRICULUM.md` | instructor | Lesson-by-lesson agendas with time math and deliverables |
| `notebooks/lessonN.ipynb` | student | Lessons 1–5 |
| `notebooks/PYTHON_CHEATSHEET.ipynb` | student | Runnable language reference; **no API key, no internet** |
| `guides/lessonN_*.md` | student | Lessons 6–8, read in VS Code's preview pane |
| `project/` | student | The finished thing they build toward |
| `docs/SETUP.md` | student | Environment, first lesson only |
| `docs/TEACHER_NOTES.md` | instructor | Pre-flight, budget, risks, what to cut if short |
| `docs/TUMO_APPLICATION.md` | the form | Paste-ready answers, **every field under ~1,400 chars** |
| `docs/ANNOUNCEMENT.md` | public | Title / dates / Description / To apply / Bio |

**Format follows phase.** Notebooks for the notebook phase; markdown guides for the
project phase, because students are editing `.py` files and running a terminal.

**Every lesson must have student-facing material.** Only the format changes.

---

## 4. Notebook conventions

### Cell rhythm

```
1. Title block         # Lesson N — Name  /  ### Course · Lesson N of 8
                       intro paragraph, then "## TODAY:" with Part A/B/C bullets
2. Kernel warning      red callout, first lesson only
3. # imports           always its own cell, always that exact comment
4. Setup cell          load_dotenv(override=True) + a friendly key check
5. Constants           CAPS, immediately after setup
6. …alternating        short markdown explainer → one small code cell
7. "## Where we got to" bulleted summary
8. "## Next lesson"    what breaks next, and homework
```

Use `## PART A/B/C:` headers to divide long lessons.

### The friendly key check

Never a bare exception. Name *which* of several things is wrong:

```python
if not api_key:
    print("❌ No API key found. Is there a file called exactly '.env' next to this notebook?")
elif api_key.strip() != api_key:
    print("❌ A key was found, but it has a space or tab at the start or end. Delete it.")
elif api_key.startswith("sk-ant-"):
    print("❌ That is an Anthropic key, not an OpenAI one. Ask your teacher for the OpenAI key.")
elif not api_key.startswith("sk-"):
    print("❌ A key was found, but OpenAI keys start with 'sk-'. Check you pasted it all.")
else:
    print(f"✅ API key found, begins {api_key[:11]}... - looks good.")
```

Then point at it: *"Notice what that cell did: not just pass or fail, but told you which
of four things is wrong. Writing checks like that for yourself is a habit worth stealing."*

### Callouts

Self-contained HTML `<div>` with inline styles — no image assets, so notebooks are
portable. Fixed vocabulary, used consistently:

| Colour | Emoji + heading | Use | Frequency |
|---|---|---|---|
| `#900` red | 🛑 *(specific title)* | Stop and read; cost warnings; traps | sparingly |
| `#900` red | 🎯 Now try it yourself | The required exercise | 1–2 per lesson |
| `#181` green | 🌍 Where you'll see this in the real world | Why this matters outside class | 1 per lesson |
| `#f71` orange | 🚀 Extra challenge | For fast students | 1 per lesson |
| `#06c` blue | 🔄 *(specific title)* | Just-in-time sidebar; syntax notes | as needed |

Template:

```html
<div style="border-left: 6px solid #900; background: #fff4f4; padding: 12px 16px; margin: 12px 0;">
<h3 style="color:#900; margin-top:0;">🎯 Now try it yourself</h3>
<p style="color:#900; margin-bottom:0;">
...
</p>
</div>
```

### Exercises

Give a skeleton with numbered stubs, never a blank cell:

```python
def make_avatar(name):
    """Generate a friendly cartoon avatar for a person with this name."""
    prompt = ""  # build your prompt here using an f-string
    return  # call make_image and return what it gives you
```

Mark the ones that are mandatory: *"Every student must find a question their assistant
correctly refuses."*

### Carrying code forward

Notebooks 3–5 re-declare what earlier lessons built, with an explicit note:

> *"Bringing these forward unchanged. Copying them into each notebook is a bit annoying —
> and in three lessons' time we'll fix that properly by moving them into a real file."*

This makes the transition lesson feel earned.

---

## 5. Student guide conventions (project phase)

Markdown, designed for VS Code's preview pane beside the code.

- **A ✅ CHECK after every step.** Prefer checks that cost nothing:
  *"CHECK: `python config.py` prints nothing and exits cleanly. That's correct — it holds
  decisions, it does no work."*
- **A fallback for stragglers:** point at the finished project with an explicit
  *"read it, understand it, then write your own"*.
- **Decision trees for debugging**, not prose. The most valuable single artefact in this
  workshop is Lesson 7's:

```
        Answer is wrong
               │
        Run: /sources <your question>
               │
     ┌─────────┴─────────┐
 Right chunk         Right chunk
 NOT in the list     IS in the list
     │                   │
 RETRIEVAL problem   GENERATION problem
 fix documents,      fix the system prompt
 chunk size, or k
```

- **Fill-in templates** for anything students must produce: test set table, tuning log,
  README skeleton.

---

## 6. Code style

### Module layout

One responsibility per file; each explainable in one sentence. State the sentences in a
table in the README.

```
config.py      Every setting in one place.          (no logic)
ingest.py      Turn documents into a saved index.   (the slow, occasional program)
retriever.py   Given a question, find the chunks.   (knows nothing about LLMs)
assistant.py   Turn chunks into a grounded answer.  (the only file that calls a model)
main.py        Talk to the human.                   (no work of its own)
```

**Dependency arrows point one way.** `retriever.py` must not import `assistant.py`. State
why: it lets students test retrieval almost for free, which is the whole of the Lesson 7
debugging method.

### Comment density, measured

| File type | Comment lines | Why |
|---|---|---|
| `config.py` | **~50%** | It's a teaching surface; every setting explains its trade-off |
| logic modules | **10–20%** | Comment the *why*, never the *what* |
| Notebook cells | 1 leading comment | Says why, or what to try next |

### Docstrings say why and what you get back

```python
def find_relevant_chunks(question, k=config.RETRIEVE_K):
    """
    Return the k chunks whose meaning is closest to the question.

    This is a similarity search over vectors, not a word search - so a question about
    "the heaviest thing they can fly" can find a note saying "no payload exceeds 2.8 kg",
    even though the two share no words at all.

    IMPORTANT: this always returns k chunks, even when your documents contain nothing
    relevant at all. Deciding that none of them answer the question is the model's job.
    """
```

Note the pattern: what it does → why it's interesting → the gotcha.

### Comments carry the reasoning

```python
# Only the last two, deliberately: with more, the search query drifts toward whatever
# the conversation used to be about instead of what was just asked.
recent = [q for q, _ in history[-2:]]
```

```python
# Default to an empty list rather than writing history=[] in the signature above.
# A list in a default argument is created ONCE and shared between every call, so it
# would quietly accumulate every conversation the program ever had.
if history is None:
    history = []
```

### Error handling

- **One `try`/`except`, at the edge of the program** — the main loop. Everything
  underneath fails loudly.
- Print the exception **type** as well as the message: `AuthenticationError` tells a
  student more than the sentence attached to it.
- **Any step that can fail for external reasons gets a branch per cause.** Compare:

```python
except Exception as error:
    message = str(error).lower()
    if "401" in message or "unauthorized" in message:
        print("Your OPENAI_API_KEY looks wrong. Check it in .env - see .env.example.")
    elif "429" in message or "rate" in message:
        print("Too many requests. The whole room shares one key - wait a minute and")
        print("run this again.")
    else:
        print("This step needs the internet. Check your connection, then run it again.")
```

A traceback is never acceptable for a foreseeable failure.

### Naming

Verbose and descriptive: `find_relevant_chunks`, `build_search_query`, `answer_question`,
`index_exists`. Never clever.

---

## 7. The provider-agnostic pattern

This is the architectural spine. Adapt it to whatever external service your course uses.

### Rule: the vendor's name appears in exactly one string, in one file

```python
# config.py
CHAT_MODEL = "openai:gpt-5.4-mini"
#   CHAT_MODEL = "openai:gpt-5.4"                # smarter, ~3x the price
#   CHAT_MODEL = "anthropic:claude-haiku-4-5"    # pip install langchain-anthropic
#   CHAT_MODEL = "ollama:llama3.2"               # runs HERE - no key, no internet
```

Everything downstream calls `.invoke()` and knows nothing.

### The commented-alternative line is the teaching device

Lifted from the reference course. Don't explain swappability abstractly — show the swap
as a comment the student can uncomment, then have them actually do it and report what
changed.

### Make students prove it

One activity per course where they change the string and re-run. The point is not the
result; it's that nothing else changed.

### Say what the abstraction costs

Say what each piece costs you, and make it a lesson. Here: OpenAI answers and embeds,
Chroma stores — and OpenAI's embeddings are weak in Armenian, so swapping the embedding
model is a real option rather than a theoretical one. *"No single company can hold the
project hostage, because each piece sits behind an interface you can swap in a line."*

---

## 8. Writing style

| Rule | Example |
|---|---|
| Numbers, not adjectives | "$56.25 per 100 questions", not "expensive" |
| Concrete, not abstract | "the sentence that answers the question got cut in half" |
| Name the failure | "It scores an unrelated sentence above the right answer: 0.079 vs 0.028" |
| Second person, plain | "You have to do this for every notebook you open." |
| Admit the awkward | "Sometimes the improver makes it worse. When that happens, say so." |
| No hype | Never "amazing", "powerful", "revolutionary" |
| Short sentences under load | Long explanations get bullets or a table |

**Voice:** conversational, direct, occasionally dry. Anticipate the student's confusion
and answer it in the next sentence. Never condescend — these are people who already
program.

**Cost transparency is a running theme.** State what things cost, in cents, every time
the student is about to spend money. Warn *before* the expensive cell, not after.

---

## 9. Verification discipline

**Non-negotiable. A course is not done until this passes.** Do not report completion on
unverified material.

### 9.1 Execute every notebook cell, in order

Write a runner. Shared namespace, catch per cell, report which failed.

### 9.2 Stub the external API

Do not settle for "blocked on auth". Replace the model with a fake that returns the right
shape, then execute everything. This catches real bugs that auth failures hide.

```python
class FakeResponse(AIMessage):
    @property
    def text(self): return "STUBBED ANSWER"
    @property
    def usage_metadata(self): return {"input_tokens": 850, "output_tokens": 42}

class FakeModel:
    def invoke(self, messages, **kw):
        for m in messages:              # assert the shape the real API would need
            assert isinstance(m, BaseMessage), f"non-message: {type(m)}"
        return FakeResponse(content="STUBBED ANSWER")

langchain.chat_models.init_chat_model = lambda *a, **k: FakeModel()
```

**Real finding from this workshop:** two "failures" in lesson 1 were cascades from the
auth block — a later cell using a variable the blocked cell defines. Without the stub,
that's a bug report about nothing, and the ~29 genuinely blocked cells stay untested.

### 9.3 Assert the internals, not just "it ran"

```python
roles = [type(m).__name__ for m in seen["messages"]]
assert roles == ["SystemMessage","HumanMessage","AIMessage","HumanMessage","AIMessage","HumanMessage"]

# the mutable-default trap: two calls must not share state
assert n1 == n2 == 2
```

### 9.4 Test every failure path

Network down, bad key, wrong key format, missing index, empty documents folder. Each must
produce one actionable sentence.

### 9.5 Verify arithmetic programmatically

```python
tot = sum(int(x) for x in re.findall(r"^\| \d+ \| .*? \| (\d+) \|$", block, re.M))
assert tot == 120
```

Re-run after *every* edit to a curriculum or application file.

### 9.6 Measure claims before writing them down

Before asserting a model behaves a certain way, run it. This workshop's Lesson 4 numbers
(`+0.279`, `+0.350`, `0.004`) are all measured. When the embedding model changed, the
measurement was re-run — and one demo had collapsed to `+0.013` and had to be replaced.
When it changed again, to OpenAI's `text-embedding-3-small`, the cross-language demo
failed outright (`0.028` vs `0.079`) and was rewritten as a measured failure.

### 9.7 Sweep for claims invalidated by later changes

After any architectural change, grep for statements that were true before it. Switching
embeddings from local to hosted falsified four separate "runs offline" claims scattered
across notebooks, guides and the application.

---

## 10. Decision log — worked examples

Real decisions from this workshop, showing the expected reasoning style. Each pairs a
constraint with evidence.

| Decision | Reasoning |
|---|---|
| **Multilingual embeddings** over the standard English-only model | Students bring Armenian notes. Measured: English-only scores a correct Armenian answer and an unrelated sentence **0.004** apart — retrieval is random and *fails silently*. Multilingual scores **0.145**. Cost: one English miss in five and 370 MB. Taken. |
| **OpenAI embeddings** over Hugging Face's hosted model *(supersedes the two rows below)* | Hugging Face's free hosted inference stopped being free: `401` without a token, `402` once the account's monthly credits ran out. `text-embedding-3-small` uses the same key and costs under a cent per course. Measured on the Kestrel files: English top-4 retrieval 6/8 → 7/8, Armenian 3/4 → 1/4. Accepted; students are steered to English notes and Lesson 4's cross-language demo became a measured failure. |
| **Hosted embeddings** over local | Measured identical vectors (cosine 1.0). Removes 1.2 GB PyTorch + 470 MB model per machine, and deletes the pre-cache step — the single largest risk of losing a lesson. Cost: network dependency, and the "unplug the wifi" demo. Accepted, and the lost demo rewritten as an extension project. |
| **Cheap model** (GPT-5.4 mini) | In RAG the retriever does the hard part and hands the model the answer. Made into a lesson: students A/B it against GPT-5.4 in Lesson 8, and *"the expensive one wasn't better"* is framed as a valid finding. |
| **Drop the Python lesson** | Students already had Python. The hour bought prompt engineering (L1) and conversation memory (L5). Python became a runnable cheatsheet that needs no key or internet — so it also occupies whoever finishes setup first. |
| **Markdown guides, not notebooks, for lessons 6–8** | Lesson 6's entire message is that you stop working in notebooks. A notebook would contradict the lesson. |
| **Fictional sample documents** | The Kestrel Project does not exist, so no model has seen it. A correct answer *proves* retrieval worked. With real notes about photosynthesis, students could never tell. |
| **Privacy warning on the homework** | Shared storage is readable by everyone and students are told to bring "your own notes". Some will bring a diary unless told plainly not to. One short paragraph, placed where they choose what to bring — not after. |

**The pattern:** state the constraint → measure → state what it costs → decide → say so
in the materials. Never hide a trade-off you took.

---

## 11. Anti-patterns

- ❌ Defining a concept before demonstrating it
- ❌ Presenting the good solution before the naive one fails
- ❌ Claiming a behaviour you haven't run
- ❌ A notebook for the transition lesson
- ❌ Leaving a lesson without student-facing material because "the instructor will talk"
- ❌ Compressing content to fit rather than cutting it
- ❌ Lessons that don't sum to the lesson length
- ❌ A traceback as a student-facing error
- ❌ `try`/`except` scattered through logic instead of one at the edge
- ❌ Classes, async, or design patterns that the course doesn't need
- ❌ Adjectives where a number would do
- ❌ Identical output for all students
- ❌ Reporting completion on unexecuted code
- ❌ Leaving stale claims after an architecture change
- ❌ Application fields long enough to break the submission form

---

## 12. Definition of done

- [ ] Every lesson's activities sum exactly to the lesson length — **verified by script**
- [ ] Every lesson has a concrete deliverable and student-facing material
- [ ] Every notebook cell executes, in order, with the external API stubbed
- [ ] Every module compiles; the project runs end to end
- [ ] Every failure path produces one actionable sentence
- [ ] Every behavioural claim in the text has been measured
- [ ] No claims invalidated by later changes (grep swept)
- [ ] `check_setup.py` exists and verifies the student's machine step by step
- [ ] Application fields short enough for the form
- [ ] Anything you could not verify is **stated plainly**, with how to verify it

That last item matters most. In this workshop the unverifiable item was the live paid API
call — no key available. It is named as such in the handover, with the exact command the
instructor must run before the first lesson.
