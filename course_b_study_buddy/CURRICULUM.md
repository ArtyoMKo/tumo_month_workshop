# Curriculum — Study Buddy

**8 sessions x 120 minutes = 960 minutes = 16 hours exactly.**

Every agenda below sums to 120. The grand total is checked at the bottom.

| # | Session name | Phase | Minutes |
|---|---|---|---|
| 1 | Setup and First Words | Notebook | 120 |
| 2 | The Lying Machine | Notebook | 120 |
| 3 | Cutting Text Into Pieces | Notebook | 120 |
| 4 | Meaning as Numbers | Notebook | 120 |
| 5 | Closing the Loop | Notebook | 120 |
| 6 | Out of the Notebook | **Transition** | 120 |
| 7 | Your Own Material | Project | 120 |
| 8 | Tune It and Ship It | Project | 120 |
| | | **Total** | **960 min = 16 h** |

---

## Session 1 — Setup and First Words

**Concepts:** what a language model is and isn't · APIs and keys · notebooks · Python as a
second language

**Tools & Skills:** Python + VS Code + Jupyter setup · virtual environments · `.env` ·
Python syntax mapped from JavaScript · first call to Claude

A double session in effect: get sixteen machines working, and translate JavaScript into
Python fast enough that Python never has to be taught again. These students are the faster
group, so the translation block moves quickly — but *faster at JavaScript* is not the same
as *already knowing Python*, so it does happen properly rather than being waved at.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet. Who's here, what they've built, what subject they might want their assistant to know | 10 |
| 2 | **Presentation:** demo of the finished thing. Instructor asks their own notes a question, gets an answer with sources; then asks something outside the notes and it refuses. "That refusal is what we're really building" | 10 |
| 3 | **Hands-on:** environment setup — Python, VS Code extensions, venv, `pip install -r requirements.txt`, `.env`, kernel | 30 |
| 4 | **Presentation:** Python for JavaScript people — assignment, f-strings vs template literals, `dict` vs object, `list` vs array, indentation vs braces, `def` vs `function` | 20 |
| 5 | **Hands-on:** `session1.ipynb` — the translation exercises, then the first model call | 30 |
| 6 | **Hands-on:** system prompts. Same question, three different system messages, three different personalities | 15 |
| 7 | Wrap-up. **Homework: bring your own documents from next session** — 3 to 10 text or markdown files on anything you like | 5 |
| | **Total** | **120** |

> With machines prepared in advance, activity 3 drops to ~15 minutes; move the spare time
> into activity 5.

---

## Session 2 — The Lying Machine

**Concepts:** hallucination · why it happens and why it isn't a bug that can be patched ·
context windows · tokens · grounding

**Tools & Skills:** reading files from disk · measuring the size of a prompt · putting
information into a system prompt · noticing when a fluent answer is wrong

The problem session. Students ask a model about material it has never seen and watch it
produce a confident, detailed, completely fabricated answer. Then they try the obvious fix —
paste the entire document into the prompt — and it works, right up until the document gets
big, at which point they measure exactly why it can't scale. Both failures are experienced
before any solution is offered, which is what makes the next three sessions feel necessary
rather than arbitrary.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap. Check everyone brought documents; hand out the backup set to those who didn't | 10 |
| 2 | **Presentation:** what a language model actually does — predicts the next piece of text. It has no database and no notion of "I don't know". Why that produces confident fiction | 20 |
| 3 | **Hands-on:** `session2.ipynb` part A — ask about your own notes with no context. Collect the best fabrications on the whiteboard | 20 |
| 4 | **Hands-on:** part B — the brute-force fix. Read the whole file, paste it into the system prompt, ask again. It works! | 20 |
| 5 | Break | 5 |
| 6 | **Presentation:** why that doesn't scale — context windows, tokens, cost per token, and the fact that a model with too much context also gets *worse*, not just slower | 15 |
| 7 | **Hands-on:** part C — measure it. Character counts, token estimates, and the cost of asking one question against a 200-page document. Then: what would you want instead? | 25 |
| 8 | Wrap-up: state the goal for the next three sessions — "find the three paragraphs that matter, and send only those" | 5 |
| | **Total** | **120** |

---

## Session 3 — Cutting Text Into Pieces

**Concepts:** chunking · why chunk size is a trade-off · overlap · metadata · document
loaders

**Tools & Skills:** `DirectoryLoader` · `RecursiveCharacterTextSplitter` · inspecting a
`Document` object · attaching metadata · list comprehensions

The first piece of machinery. Loading a folder of documents and splitting them sensibly is
easy to do and easy to do badly, so students split the *same* document at several chunk
sizes and read the results, discovering that a chunk which cuts a sentence in half is
useless and a chunk the size of the whole document defeats the point. Overlap is introduced
as the fix for the boundary problem they'll have just hit.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** chunking. Why a chunk should be *one idea*: big enough to make sense alone, small enough that it isn't mostly irrelevant | 15 |
| 3 | **Hands-on:** `session3.ipynb` part A — load the documents folder with LangChain, inspect what a `Document` is, attach metadata | 25 |
| 4 | **Hands-on:** part B — split at chunk_size 200, 500, 1000, 4000. Read actual chunks from each. Which one would you want to be handed if you had to answer a question? | 25 |
| 5 | Break | 5 |
| 6 | **Presentation:** the boundary problem — the sentence that answers the question got cut in half. Overlap, and why 10-20% is the usual answer | 10 |
| 7 | **Hands-on:** part C — same split with and without overlap; find a chunk boundary that would have lost an answer | 20 |
| 8 | **Try it yourself:** pick the chunk settings you'll use for your own material, and write down why | 10 |
| | **Total** | **120** |

---

## Session 4 — Meaning as Numbers

**Concepts:** embeddings · vectors · similarity · why "car" is near "vehicle" and far from
"trombone" · vector stores · the local-vs-hosted choice

**Tools & Skills:** `HuggingFaceEmbeddings` running locally · `Chroma` · `similarity_search`
· `similarity_search_with_score` · reading a number as a measurement

The conceptual centre of the course, and the session that feels like magic. Students embed
a handful of words, measure the distances between them, and find that the numbers agree
with their intuitions about meaning. Then they build a real vector store over their own
documents and search it — no LLM involved yet, just retrieval, so they can see clearly
which half of the system is doing what.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** embeddings, without maths. Meaning as a position. Two axes on the whiteboard, students place words on it, then reveal that the real thing does the same with 384 axes | 20 |
| 3 | **Hands-on:** `session4.ipynb` part A — embed single words, look at a vector, measure similarity between pairs. Find a pair the model thinks are closer than you do | 25 |
| 4 | Break | 5 |
| 5 | **Presentation:** what a vector store is, and the honest version of "swappable" — we use Chroma on your laptop; a company would use a hosted one; through LangChain that's a config change | 10 |
| 6 | **Hands-on:** part B — build a Chroma store over the class documents, run `similarity_search`, look at the scores | 30 |
| 7 | **Hands-on:** part C — search with a question your documents *don't* answer. What comes back, and what does the score look like? | 10 |
| 8 | **Optional / cut first if short:** t-SNE visualisation of the vectors, coloured by source file | 5 |
| 9 | Wrap-up | 5 |
| | **Total** | **120** |

---

## Session 5 — Closing the Loop

**Concepts:** retrieval-augmented generation, assembled · system prompts that forbid
guessing · citing sources · `k` as a dial · provider-agnostic code

**Tools & Skills:** joining retrieved chunks into a context string · `SystemMessage` /
`HumanMessage` · `init_chat_model` · swapping the provider with one line

Everything meets. Retrieval from Session 4 feeds the prompt from Session 2, and the
assistant answers grounded questions about real documents for the first time. Then the two
dials that matter: `k`, and the wording of the system prompt — and students discover that
a single sentence added to the system prompt ("if the context doesn't say, say you don't
know") is what turns the confident liar of Session 2 into something trustworthy.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap. Whiteboard the whole pipeline from memory before opening anything | 15 |
| 2 | **Hands-on:** `session5.ipynb` part A — retrieve, join into a context string, print the actual prompt being sent. Read it. *That's* the trick, in full | 25 |
| 3 | **Hands-on:** part B — `answer_question()`, returning the answer **and** the sources | 20 |
| 4 | Break | 5 |
| 5 | **Hands-on:** part C — the refusal. Add the "don't guess" sentence, then find a question it correctly refuses. Everyone must produce one | 20 |
| 6 | **Hands-on:** part D — turn `k` up and down. At k=1 it misses things; at k=20 the answers get vaguer. Why? | 15 |
| 7 | **Demo + hands-on:** swap `CHAT_MODEL` — Haiku → Sonnet, then `ollama:llama3.2` with the wifi off — and watch it keep working either way | 15 |
| 8 | Wrap-up: **the notebook phase ends here** | 5 |
| | **Total** | **120** |

---

## Session 6 — Out of the Notebook  ⟵ *transition session*

**Concepts:** modules · imports · entry points · separation of concerns · a build step vs a
run step

**Tools & Skills:** VS Code outside the notebook · `import` · `if __name__ == "__main__":` ·
persisting a vector store to disk · running scripts from the terminal

The pivot, and it has a genuinely new idea in it: the project splits into **two programs**.
`ingest.py` is slow, runs when your documents change, and writes an index to disk.
`main.py` is fast, runs constantly, and reads that index. Recognising that a system has a
build step and a run step — and that they're separate programs — is a real piece of software
design, and this is the natural place to meet it.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet. **Presentation:** why leave the notebook. A notebook is a lab bench, not the thing you built on it | 10 |
| 2 | **Presentation:** the two-program idea on the whiteboard. Why re-embedding every document each time you ask a question would be absurd. Persisting Chroma to disk | 20 |
| 3 | **Hands-on:** create the folder; `config.py` — every constant from five notebooks moves here | 15 |
| 4 | **Hands-on:** `ingest.py` — load, chunk, embed, persist. Run it. Look at the `vector_db/` folder it created | 25 |
| 5 | Break | 5 |
| 6 | **Hands-on:** `retriever.py` — open the saved store, `find_relevant_chunks(question)`. Test it from a scratch file with no LLM involved | 20 |
| 7 | **Hands-on:** `assistant.py` — the system prompt and `answer_question()` | 15 |
| 8 | **Hands-on:** `main.py` — the question loop. **Run `python main.py` for the first time** | 10 |
| | **Total** | **120** |

---

## Session 7 — Your Own Material

**Concepts:** data quality beats clever code · debugging a pipeline by checking each stage ·
designing a feature

**Tools & Skills:** editing across multiple files · re-running ingest after changing
documents · diagnosing "wrong answer" as retrieval vs generation

Students swap in their own material properly and find out that RAG lives or dies on the
documents. A PDF exported as one wall of text with no headings retrieves badly; the same
content with headings retrieves well. The core skill taught is **splitting the blame**: when
an answer is wrong, check whether the right chunk was retrieved *before* touching the
prompt, because those are two different bugs with two different fixes.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap. Everyone confirms `python main.py` still runs | 10 |
| 2 | **Presentation:** garbage in, garbage out. What a good document looks like — headings, short paragraphs, one topic per file. What a bad one looks like | 15 |
| 3 | **Hands-on:** put your own documents in `documents/`, re-run `python ingest.py`, ask five questions you know the answers to | 30 |
| 4 | **Presentation:** splitting the blame. Two questions, in this order: did the right chunk come back? then, did the model use it? Never debug the second before the first | 15 |
| 5 | Break | 5 |
| 6 | **Hands-on:** improve your documents — add headings, split a big file, delete noise — and re-run. Measure whether it got better on the same five questions | 25 |
| 7 | **Hands-on:** pick one feature and build it — show sources with scores, a `/sources` command, a conversation that remembers the last question, a "which file knows most about X" report | 15 |
| 8 | Wrap-up | 5 |
| | **Total** | **120** |

---

## Session 8 — Tune It and Ship It

**Concepts:** evaluation · tuning one parameter at a time · paying more vs. getting more ·
what makes a project *finished* · presenting technical work

**Tools & Skills:** building a tiny test set · changing `k` and chunk size and measuring the
effect · `requirements.txt` · README · the fresh-machine test · demoing

Students write down five questions with known answers — a test set — and then tune against
it instead of against vibes. That single move, "decide how you'll measure before you start
changing things", is the most professionally valuable habit in the entire course. Then
they finish the project properly and present it.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** how would you know if you made it better? Write the test set *first*; tune against it; change one thing at a time | 15 |
| 3 | **Hands-on:** write five questions with known answers. Score your assistant now, before changing anything — that's your baseline | 20 |
| 4 | **Hands-on:** tune. Change `k`, chunk size (re-run ingest), the system prompt, or the model (Haiku → Sonnet 5). One at a time. Re-score after each — including "does the pricier model actually win?" | 25 |
| 5 | Break | 5 |
| 6 | **Hands-on:** finish it — README, `requirements.txt`, check `.env` isn't in what you'd share, then the fresh-machine test: hand your folder to a partner and watch them try to run it from your README alone | 20 |
| 7 | **Showcase:** ~90 seconds each — what your assistant knows about, one good answer, **one question it correctly refuses**, and one thing that broke on the way | 20 |
| 8 | Wrap-up: where to go next — hosted vector stores, agents, the LangChain docs, Ollama at home | 5 |
| | **Total** | **120** |

---

## Time check

```
Session 1   120
Session 2   120
Session 3   120
Session 4   120
Session 5   120
Session 6   120
Session 7   120
Session 8   120
          -----
            960 minutes  =  16 hours  ✓
```

Notebook phase: sessions 1-5 (600 min / 10 h).
Transition: session 6 (120 min / 2 h).
Project phase: sessions 7-8 (240 min / 4 h).
