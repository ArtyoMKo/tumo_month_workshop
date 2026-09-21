# Curriculum — AI Study Buddy

**8 lessons × 120 minutes = 960 minutes = 16 hours exactly.**

Every agenda below sums to 120. The grand total is checked at the bottom.

| # | Lesson | Phase | Minutes |
|---|---|---|---|
| 1 | Setup and Your First AI Call | Notebook | 120 |
| 2 | Why AI Makes Things Up | Notebook | 120 |
| 3 | Preparing Documents: Chunking | Notebook | 120 |
| 4 | Embeddings and Semantic Search | Notebook | 120 |
| 5 | Building the RAG Assistant | Notebook | 120 |
| 6 | From Notebook to Python Project | **Transition** | 120 |
| 7 | Your Own Knowledge Base | Project | 120 |
| 8 | Testing, Tuning and Final Demo | Project | 120 |
| | | **Total** | **960 min = 16 h** |

> **Python is not taught in this course.** Students arrive with basic Python from their
> other TUMO tracks. They are given `PYTHON_CHEATSHEET.md` in Lesson 1 as a lookup
> reference — JavaScript↔Python translation table, the syntax this project actually uses,
> how to read an error, notebook and terminal survival. It is never lectured from. The
> hour this saves is spent on prompt engineering (Lesson 1) and conversation memory
> (Lesson 5), both of which make the final assistant meaningfully better.

---

## Lesson 1 — Setup and Your First AI Call

**Concepts:** what a language model actually does · APIs and API keys · system vs user
messages · prompt engineering · temperature · provider independence

**Tools & Skills:** Python + VS Code + Jupyter setup · virtual environments · `.env` ·
`init_chat_model` · `SystemMessage` / `HumanMessage` · writing prompts that constrain
behaviour

Get sixteen machines working, then spend the rest of the lesson on the single most
powerful thing a student controls all course: **the system prompt.** They make one model
behave five different ways without touching a line of logic, and they make it obey rules
about length, language and refusal — which is exactly the mechanism that will make the
finished assistant trustworthy in Lesson 5.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet. Demo of the finished assistant: it answers from my notes with sources, then refuses a question they don't cover. "That refusal is what we're really building" | 10 |
| 2 | **Presentation:** what a language model actually does — predicts text, has no database, no sense of "I don't know". What an API is, and why the key is a password | 15 |
| 3 | **Hands-on:** environment setup — Python, VS Code extensions, venv, `pip install`, `.env`, select the kernel. **Hand out `PYTHON_CHEATSHEET.md`** | 25 |
| 4 | **Hands-on:** first call to Claude. Inspect the response object — it is not a string; look at what's actually inside it | 15 |
| 5 | **Presentation + hands-on:** system vs user messages. The system prompt is written by *you*, the programmer, and the user never sees it. Same question, three system prompts, three completely different assistants | 20 |
| 6 | **Hands-on:** making a model follow rules. Constrain length, force a specific output format, make it answer in Armenian, make it refuse a topic. Then try to break your own rules from the user message — this is called prompt injection and it is an unsolved problem | 20 |
| 7 | **Hands-on:** the one-line provider swap. `init_chat_model("anthropic:claude-haiku-4-5")` names no company anywhere else in the code — change the string, everything else keeps working | 10 |
| 8 | Wrap-up. **Homework: bring 3-10 of your own documents next time** | 5 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** A working environment, and a notebook containing the student's own `ask(system_prompt, question)` function plus at least three system prompts that produce measurably different behaviour — including one that successfully forces a refusal.

---

## Lesson 2 — Why AI Makes Things Up

**Concepts:** hallucination and why it isn't a fixable bug · grounding · tokens · context
windows · cost per question

**Tools & Skills:** reading files · putting information into a system prompt · measuring
prompt size and cost · noticing when a fluent answer is wrong

The problem lesson, and no solution is offered in it. Students ask a model about material
it has never seen and watch it produce confident, detailed, entirely invented answers.
Then they try the obvious fix — paste the whole document in — and it works, until they
measure what it costs and discover the wall.

| # | Activity | Min |
|---|---|---|
| 1 | Recap. Check everyone brought documents; hand the backup set to those who didn't | 10 |
| 2 | **Presentation:** why models invent things. It predicts plausible text; from the inside, recalling and composing are the same operation. Hence confident fiction | 20 |
| 3 | **Hands-on:** ask about a project invented for this workshop, that no model has ever seen. Collect the best fabrications on the whiteboard. Repeat on the student's own notes | 20 |
| 4 | **Hands-on:** the brute-force fix — read the file, paste it into the system prompt, ask again. It works | 20 |
| 5 | Break | 5 |
| 6 | **Presentation:** why that doesn't scale — tokens, context windows, price per token, and the fact that too much context makes answers *worse* | 15 |
| 7 | **Hands-on:** measure it. Token counts and real cost for a chapter, a textbook, a year of notes. Discover a textbook now *fits* — and still costs $75 per 100 questions and still degrades. "It fits" and "it's a good idea" are different questions | 25 |
| 8 | Wrap-up: state the goal of the next three lessons — "find the three paragraphs that matter, send only those" | 5 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** A notebook showing the same question answered wrongly without context and correctly with it, plus the student's own cost calculation. The student can state, unprompted, the problem the rest of the course solves.

---

## Lesson 3 — Preparing Documents: Chunking

**Concepts:** documents and metadata · chunking · chunk size as a trade-off · overlap and
the boundary problem · splitting on structure

**Tools & Skills:** `Document` objects · `RecursiveCharacterTextSplitter` ·
`MarkdownHeaderTextSplitter` · inspecting and comparing chunks

The first real machinery. Students split the same documents four ways and *read* the
results, discovering that a chunk cutting a sentence in half is useless and a chunk the
size of the whole file defeats the point. Overlap arrives as the fix to a problem they
have just hit.

| # | Activity | Min |
|---|---|---|
| 1 | Recap | 10 |
| 2 | **Presentation:** what a chunk should be — one idea. Big enough to stand alone, small enough to be mostly about one thing | 15 |
| 3 | **Hands-on:** load the documents folder. Inspect a `Document`: text plus metadata. The filename travels with the text all the way to the final answer — that's what makes citing a source possible | 20 |
| 4 | **Hands-on:** split at 200, 500, 1000 and 4000 and read actual chunks from each. The judgement question: "handed only this, could you answer the question?" | 25 |
| 5 | Break | 5 |
| 6 | **Presentation:** the boundary problem — the sentence that answers the question got cut in half. Overlap, and why 10-20% | 10 |
| 7 | **Hands-on:** split with and without overlap; find a boundary that would have lost an answer | 15 |
| 8 | **Hands-on:** splitting on structure instead of length — `MarkdownHeaderTextSplitter` keeps each section whole and records its heading in the metadata. Compare against plain splitting on your own notes | 15 |
| 9 | Choose the settings for your own material and write down why | 5 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** The student's own documents loaded and split, with chosen `chunk_size` and `chunk_overlap` and a written one-sentence justification. "It was the default" is not accepted.

---

## Lesson 4 — Embeddings and Semantic Search

**Concepts:** embeddings · vectors and similarity · topical vs semantic closeness ·
multilingual models · vector stores · metadata filtering

**Tools & Skills:** `HuggingFaceEmbeddings` running locally · cosine similarity ·
`Chroma` · `similarity_search` and scores · filtering by metadata

The conceptual centre, and the lesson that feels like magic until it doesn't. Students
measure the distance between meanings, find a question and its answer that share no words
at all — and then ask a question in Armenian and watch it find an English note.

| # | Activity | Min |
|---|---|---|
| 1 | Recap | 10 |
| 2 | **Presentation:** embeddings without mathematics. Meaning as a position. Students physically place words on a drawn 2-axis space, then learn the real model uses 384 axes it invented itself | 20 |
| 3 | **Hands-on:** embed single words; predict each similarity score before running it. Discover `hot`/`cold` scores *high* — embeddings capture topic, not agreement | 20 |
| 4 | **Hands-on:** the key result — a question and its answer sharing not one content word still score close, while an on-topic distractor scores far. Then the same across languages: an Armenian question finding an English answer | 15 |
| 5 | Break | 5 |
| 6 | **Presentation:** what a vector store is. Chroma on your laptop today; a hosted database at company scale; through LangChain that's a config change | 10 |
| 7 | **Hands-on:** build a Chroma store over your own documents and search it. **No language model involved yet** — so it's obvious which half does what | 25 |
| 8 | **Hands-on:** search for something your documents don't contain. It *still* returns results — the discovery that sets up Lesson 5. Then metadata filtering: search only one source file | 15 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** A working search engine over the student's own documents, plus three documented cases with scores: one answered well, one where the right chunk ranks low, one the documents cannot answer.

---

## Lesson 5 — Building the RAG Assistant

**Concepts:** retrieval-augmented generation assembled · prompts that forbid guessing ·
citing sources · `k` as a dial · conversation memory

**Tools & Skills:** joining chunks into context · `SystemMessage`/`HumanMessage` ·
returning sources · passing conversation history · follow-up questions

Everything connects. Retrieval from Lesson 4 feeds the prompt from Lesson 2, and the
assistant answers real questions about real documents. Then the sentence that turns a
confident liar into something trustworthy — and finally, memory, so it can handle
"what about the other one?"

| # | Activity | Min |
|---|---|---|
| 1 | Recap: whiteboard the entire pipeline from memory before opening anything | 10 |
| 2 | **Hands-on:** retrieve, join into a context string, and **print the actual prompt being sent**. Read it. That's RAG, in full, with nothing hidden | 25 |
| 3 | **Hands-on:** `answer_question()` returning the answer **and** its sources, so any answer can be checked | 20 |
| 4 | Break | 5 |
| 5 | **Hands-on:** the refusal. Retrieval alone doesn't prevent invention — search always returns *something*. One sentence in the system prompt fixes it. **Every student must find a question theirs correctly refuses** | 20 |
| 6 | **Hands-on:** tune `k`. At 1 it misses answers; at 20 answers go vague and expensive. Understanding why is the point | 15 |
| 7 | **Hands-on:** conversation memory. Right now every question starts from nothing, so "what about the other one?" fails. Pass the previous turns in, and follow-up questions work | 20 |
| 8 | Wrap-up: the notebook phase ends here | 5 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** A working RAG assistant answering questions about the student's own documents with sources, handling at least one follow-up question that depends on the previous one, and correctly refusing one documented question.

---

## Lesson 6 — From Notebook to Python Project  ⟵ *transition lesson*

**Concepts:** modules and responsibilities · imports · entry points · a build step vs a
run step · persistence

**Tools & Skills:** VS Code outside the notebook · `import` · `if __name__ == "__main__":`
· persisting a vector store · running scripts from the terminal

The pivot. Nothing new is learned about AI; everything is reorganised into a real project.
It carries one genuinely new engineering idea: the project splits into **two programs** —
a slow one that builds an index when documents change, and a fast one that answers
questions constantly.

| # | Activity | Min |
|---|---|---|
| 1 | **Presentation:** why leave the notebook. A notebook is a lab bench; you hand someone the thing you built, not the bench | 10 |
| 2 | **Presentation:** the two-program design on the whiteboard. Re-embedding every document on every question would be absurd. Persisting the index to disk | 20 |
| 3 | **Hands-on:** create the folder and `config.py`. Every constant from five notebooks moves here. Run it — it does nothing, and that's correct | 15 |
| 4 | **Hands-on:** `ingest.py` — load, chunk, embed, persist. Run it; inspect the `vector_db/` folder it made | 25 |
| 5 | Break | 5 |
| 6 | **Hands-on:** `retriever.py` — open the saved index, `find_relevant_chunks()`. Test it with no model involved at all | 20 |
| 7 | **Hands-on:** `assistant.py` — the system prompt, conversation history, `answer_question()` | 15 |
| 8 | **Hands-on:** `main.py` — the question loop. **Run `python main.py` for the first time** | 10 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** **A working `python main.py`** — a real program, run from the terminal, no notebook involved. The instructor confirms this individually for every student before they leave.

---

## Lesson 7 — Your Own Knowledge Base

**Concepts:** data quality beats clever code · diagnosing a pipeline stage by stage ·
designing and placing a feature

**Tools & Skills:** editing across modules · re-running ingest after changing documents ·
separating retrieval failures from generation failures · the `/sources` command

Students swap in their own material properly and discover that RAG lives or dies on the
documents. The core skill is **splitting the blame**: when an answer is wrong, find out
whether the right chunk came back *before* touching the prompt.

| # | Activity | Min |
|---|---|---|
| 1 | Recap. Everyone confirms `python main.py` still runs before changing anything | 10 |
| 2 | **Presentation:** garbage in, garbage out. What a good document looks like — headings, short paragraphs, one topic per file. What a bad one looks like | 15 |
| 3 | **Hands-on:** put your own documents in `documents/`, re-run `python ingest.py`, ask five questions you already know the answers to | 30 |
| 4 | **Presentation:** splitting the blame. Two questions, in this order: did the right chunk come back? then, did the model use it? Never debug the second first. The `/sources` command answers the first without spending anything | 15 |
| 5 | Break | 5 |
| 6 | **Hands-on:** improve your documents — add headings, split a big file, delete noise — re-ingest, and measure whether the same five questions got better | 25 |
| 7 | **Hands-on:** build one feature of your own. Show retrieval scores, a `/stats` command, filter by source file, remember more turns | 15 |
| 8 | Wrap-up | 5 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** An assistant running on the student's own real material, answering five known questions correctly, plus one self-designed feature. The student can say whether a given wrong answer was a retrieval problem or a generation problem.

---

## Lesson 8 — Testing, Tuning and Final Demo

**Concepts:** evaluation · changing one thing at a time · paying more vs getting more ·
what makes a project finished · presenting technical work

**Tools & Skills:** building a small test set · tuning `k`, chunk size, prompt and model ·
`requirements.txt` · writing a README · the fresh-machine test · demoing

Students write five questions with known answers and tune against *that* instead of
against impressions. Deciding how you'll measure before you start changing things is the
most professionally valuable habit in the course.

| # | Activity | Min |
|---|---|---|
| 1 | Recap | 10 |
| 2 | **Presentation:** how would you know if you made it better? Write the test set *first*, tune against it, change one thing at a time | 15 |
| 3 | **Hands-on:** write five questions with known answers. Score your assistant *before* changing anything — that's your baseline | 20 |
| 4 | **Hands-on:** tune. `k`, chunk size (re-ingest), the system prompt, or the model — Haiku → Sonnet 5. One at a time, re-scoring after each. Does the pricier model actually win? | 25 |
| 5 | Break | 5 |
| 6 | **Hands-on:** finish it — README, `requirements.txt`, confirm `.env` isn't in what you'd share. Then the fresh-machine test: swap folders with a partner and run theirs from their README alone | 20 |
| 7 | **Showcase:** ~90 seconds each — what your assistant knows, one good answer, **one correct refusal**, one thing that broke on the way | 20 |
| 8 | Wrap-up: where to go next | 5 |
| | **Total** | **120** |

**📦 Deliverable by end of lesson:** A finished, documented project a classmate successfully ran from the README alone; a written test set with before-and-after scores; and a live demo including one correct refusal.

---

## Time check

```
Lesson 1   120      Lesson 5   120
Lesson 2   120      Lesson 6   120
Lesson 3   120      Lesson 7   120
Lesson 4   120      Lesson 8   120
                  ---------------
                    960 minutes  =  16 hours  ✓
```

Notebook phase: lessons 1-5 (600 min / 10 h).
Transition: lesson 6 (120 min / 2 h).
Project phase: lessons 7-8 (240 min / 4 h).

## What changed when Python teaching was removed

The ~50 minutes of JavaScript→Python translation in Lesson 1 became:

| Reclaimed time | Now spent on | Why it's worth more |
|---|---|---|
| 20 min | **Prompt engineering** (L1 activity 6) — constraining length, language, format, refusal | Directly builds the mechanism that makes the assistant refuse in Lesson 5 |
| 10 min | **Provider swap moved up** to L1 activity 7 | It belongs where `init_chat_model` is introduced, and frees L5 |
| 20 min | **Conversation memory** (L5 activity 7) | The feature students want most; makes the assistant feel finished |

Python is handled by `PYTHON_CHEATSHEET.md`, given out in Lesson 1 and never lectured from.
