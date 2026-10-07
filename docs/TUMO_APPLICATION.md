# TUMO Lesson Plan Application — paste-ready answers

Repo: https://github.com/ArtyoMKo/tumo_month_workshop

Every field below is kept short enough for Google Forms. Fuller detail lives in the repo
(`course_b_study_buddy/CURRICULUM.md` and the student guides) if TUMO wants it.

---

## Lab Title
```
AI Workshop: Build an AI That Reads Your Notes
```

## Center
*Your choice from the dropdown.*

## Workshop Leader
```
Artyom Kosakyan
```

## Workshop dates
```
1 - 25 October 2026
Thursdays 19:30-21:30 | Sundays 14:00-16:00
8 lessons x 2 hours = 16 hours
```

## Number of students
```
16
```

## Prerequisites
```
- Basic Python: variables, lists, dictionaries, loops, functions. Python is not taught
  here; students get a cheatsheet to look things up in.
- No AI, machine learning or maths background needed. Age 13-18.
- From Day 2 each student brings 3-10 of their own .txt/.md files - revision notes, a
  subject they study, rules of a game. English works best for search. Shared storage is
  visible to everyone, so general subjects only, nothing personal. Backups provided.
```

## What are the learning objectives and goals?
```
GOALS
- understand why an AI chatbot invents confident, false answers
- write system prompts that control a model's behaviour, and find their limits
- split documents into chunks, and know why chunk size matters
- turn text into embeddings and search by meaning instead of by words
- assemble retrieved text into a prompt so answers are grounded in real documents
- make the assistant refuse questions its documents do not cover
- add conversation memory so follow-up questions work
- move working code out of a notebook into a real Python project in VS Code
- diagnose a wrong answer: was it the search or the model?
- measure with a test set before tuning, and change one thing at a time
- write a README someone else can follow
```

## What are the anticipated learning outcomes?
```
Each student finishes with a runnable Python project (main.py, config.py, ingest.py,
retriever.py, assistant.py, requirements.txt, README) that answers questions about
documents they chose, cites the source file, handles follow-ups, and refuses anything
its documents do not cover.

Each student can:
- demo one correct answer and one correct refusal, live
- say whether a wrong answer was a search failure or a model failure
- show a test set with before-and-after scores from their own tuning
- hand the project to a classmate who runs it from the README alone

Every project is different, because every student picks their own documents.
```

## Workshop announcement
```
AI WORKSHOP

BUILD AN AI ASSISTANT THAT ANSWERS FROM YOUR OWN NOTES

October 1st - October 25th
Thursdays 19:30 - 21:30 | Sundays 14:00 - 16:00


Description

Ask a chatbot about your homework and it answers confidently - and sometimes invents the
answer completely. It has never seen your notes. In this workshop students build the fix:
an assistant that reads documents they choose themselves - revision notes, a subject they
study, the rules of a game - and answers only from that material, naming the file each
answer came from. Asked something its documents do not cover, it says so instead of
guessing. Getting a computer to admit what it does not know is the hard part, and it is
what this workshop is about.

Students start in a notebook, learning to control how an AI behaves and how text becomes
numbers that capture meaning rather than spelling, so that a question can find its
answer even when they share no words. Halfway through, the code leaves the notebook and becomes a real
Python project in VS Code. The last lessons cover loading their own material, diagnosing
wrong answers, and measuring quality against a test set they write themselves.


To apply

Send a short list of the documents you would want your assistant to know about, and why
you chose them. English notes work best. Tell us what programming you have done,
including any Python. No AI experience required.

Your documents go in your TUMO workshop folder, which others can see, so choose material
about a subject rather than anything personal.


Bio.

Artyom Kosakyan is an AI Engineer at Async Armenia, specialising in Voice AI. He studied
Applied Mathematics and Informatics at Yerevan State University and has spent three years
teaching Python with the FAST Foundation - experience that shapes how this workshop runs:
students write and execute everything themselves from the first lesson, and every idea is
made to work before it is named. His engineering work is in getting language and speech
models to behave reliably in real products, which is exactly the problem at the centre of
this course.
```

---

## Lesson 1: Day 1
```
DAY 1 - SETUP AND YOUR FIRST AI CALL

> Introductions, and a demo of the finished assistant (10mn)
> Presentation: what a model does; APIs; why the key is a password (15mn)

> STEP 1: Setup (25mn)
- everything pre-installed; Python on the laptop, work in the shared folder
- .env with one key: OPENAI_API_KEY
- Select Kernel - needed in every notebook, the #1 source of errors
- shared storage is visible to everyone: next lesson, general-subject notes only
- hand out the Python cheatsheet

> STEP 2: First call to the model (15mn)
- init_chat_model("openai:gpt-5.4-mini").invoke(...)
- inspect the whole response, and the token counts that price everything

> STEP 3: System prompts (20mn)
- System (written by the programmer, invisible) vs Human
- write ask(system_prompt, question); one question through three different jobs

> STEP 4: Making it follow rules (20mn)
- length, JSON format, Armenian, and a forced refusal
- students try to break their own rule from the user message -> prompt injection

> STEP 5: Changing AI company in one line (10mn)
> Wrap-up (5mn) - homework: bring 3-10 of your own .txt/.md files

DELIVERABLE: working environment, their own ask() function, three system prompts with
different behaviour, one forcing a refusal.
```

## Lesson 2: Day 2
```
DAY 2 - WHY AI MAKES THINGS UP

> Recap; check everyone brought documents (10mn)
> Presentation: why models invent - they predict plausible text, and recalling and
  composing are the same operation inside (20mn)

> STEP 1: Watch it make things up (20mn)
- our sample documents describe an invented project no AI has ever seen, so any answer
  is provably fabricated
- ask, compare with the file, collect the best inventions on the board
- repeat on the student's own notes

> STEP 2: The brute-force fix (20mn)
- read the file, put the text in the system prompt, ask again -> correct. This is
  GROUNDING.
- ask from a different file -> wrong again -> load everything

> Break (5mn)
> Presentation: tokens, context windows, cost per question (15mn)

> STEP 3: Measure why it cannot scale (25mn)
- a textbook fits in the window but costs $9.38 per 100 questions; a year of notes is
  $56.25 and does not fit
- too much context also makes answers worse
- "it fits" and "it's a good idea" are different questions

> Wrap-up (5mn) - the goal for the next 3 days: find the paragraphs that matter

DELIVERABLE: a notebook showing the same question answered wrongly without context and
correctly with it, plus their own cost calculation.
```

## Lesson 3: Day 3
```
DAY 3 - PREPARING DOCUMENTS: CHUNKING

> Recap (10mn)
> Presentation: a chunk should be one idea - big enough to stand alone, small enough to
  be mostly relevant (15mn)

> STEP 1: Load documents (20mn)
- build a Document per file, with the filename in its metadata
- that filename reaches the final answer; lose it and you cannot cite a source

> STEP 2: Compare chunk sizes (25mn)
- split at 200 / 500 / 1000 / 4000; print the same passage cut four ways and read them
- the test: "handed only this chunk, could you answer?"

> Break (5mn)
> Presentation: the boundary problem - wherever you cut, you sometimes cut through the
  answer. Overlap of 10-20% fixes it. (10mn)

> STEP 3: Overlap (15mn)
- print the seam between two chunks with and without it
- settle on chunk size 1000, overlap 200

> STEP 4: Split on structure instead of length (15mn)
- a markdown-header splitter keeps each section whole; compare on their own notes

> Choose your settings, with one sentence of justification (5mn)

DELIVERABLE: their own documents split, with chosen settings and a written reason.
```

## Lesson 4: Day 4
```
DAY 4 - EMBEDDINGS AND SEMANTIC SEARCH

> Recap (10mn)
> Presentation: embeddings without maths. Meaning as a position - students place word
  cards on a drawn 2-axis space; the real model uses 1,536 axes it worked out itself (20mn)

> STEP 1: Measure meaning (20mn)
- students predict each similarity score before running it
- "hot" and "cold" score HIGH: embeddings capture topic, not agreement
- each student finds a pair where the model disagrees with them

> STEP 2: The result that makes this work (15mn)
- a question and its answer sharing no word still score close; a word search scores zero
- across languages it breaks: an Armenian question scores an unrelated English line above
  its answer. A real model limit, measured rather than hidden

> Break (5mn)
> Presentation: what a vector store is (10mn)

> STEP 3: Build and search your index (25mn)
- no language model involved - pure search, so it is obvious which half does what
- each student builds a store over their own documents

> STEP 4: The question with no answer (15mn)
- search something absent -> it still returns results. A vector store always returns k.
- therefore retrieval alone does not prevent hallucination -> Day 5

DELIVERABLE: a working search engine over their own documents, and three documented
cases: answered well / right chunk ranks low / not in the documents.
```

## Lesson 5: Day 5
```
DAY 5 - BUILDING THE RAG ASSISTANT

> Recap: whiteboard the pipeline from memory before opening anything (10mn)

> STEP 1: Assemble the prompt, then read it (25mn)
- retrieve, join the chunks, fill the template
- print the whole prompt and read it aloud. That is RAG, with nothing hidden.

> STEP 2: answer_question() with sources (20mn)
- return the answer and the files it used; sources are what make it checkable
- test a question whose answer spans two files

> Break (5mn)

> STEP 3: The refusal (20mn)
- ask something absent -> it answers anyway from irrelevant chunks
- add one sentence to the prompt: if the notes do not contain the answer, say so
- every student finds a question theirs refuses, and one where the refusal fails

> STEP 4: Tune k (15mn)
- k=1 misses answers; k=12 buries the right chunk. Start at 4-6.

> STEP 5: Conversation memory (20mn)
- a follow-up question fails for two separate reasons: the model does not know what
  "them" means, and neither does the search
- fix both; students run a 4-turn conversation on their own notes

> Wrap-up (5mn) - the notebook phase ends here

DELIVERABLE: a working RAG assistant with sources, handling a follow-up, and correctly
refusing one documented question.
```

## Lesson 6: Day 6
```
DAY 6 - FROM NOTEBOOK TO PYTHON PROJECT

Students work from a written guide with a check after every file, so anyone falling
behind catches up without stopping the room.

> Presentation: a notebook is a lab bench; you hand someone the thing you built (10mn)
> Presentation: the two-program design. ingest.py is slow and runs when documents
  change; main.py is fast and runs constantly; the index is saved between them. (20mn)

> STEP 1: config.py - every constant in one place (15mn)
- CHECK: it prints nothing and exits cleanly

> STEP 2: ingest.py - load, split, embed, save (25mn)
- CHECK: run it; a vector_db/ folder appears

> Break (5mn)

> STEP 3: retriever.py - open the saved index and find chunks (20mn)
- must use the same embedding model as ingest.py, or search returns nonsense with no error
- knows nothing about language models, so it can be tested almost for free

> STEP 4: assistant.py - the system prompt and the answering function (15mn)
- history=None, not history=[]: a list default is shared by every call

> STEP 5: main.py, and run it (10mn)
- the question loop, one try/except, then: python main.py

DELIVERABLE: every student leaves with a working "python main.py", confirmed individually.
```

## Lesson 7: Day 7
```
DAY 7 - YOUR OWN KNOWLEDGE BASE

> Recap: everyone runs the project before changing anything (10mn)
> Presentation: garbage in, garbage out. Headings, short paragraphs, one topic per file.
  Notes saying "this is the important one" are unfindable. (15mn)

> STEP 1: Load your own documents (30mn)
- re-ingest, then ask five questions you know the answers to and record right/wrong
- the same five are reused on Day 8

> Presentation: splitting the blame (15mn)
- always in this order: did the right chunk come back? then, did the model use it?
- the /sources command answers the first, without calling the AI at all
- debugging the prompt when the problem is retrieval loses an afternoon

> Break (5mn)

> STEP 2: Improve the documents, then measure (25mn)
- fix the document, not the code; re-ingest; re-ask the same five
- most students find this beats every code change available to them

> STEP 3: Build one feature (15mn)
- the skill is deciding which file it belongs in
- from showing retrieval scores up to making it quote its evidence

> Wrap-up (5mn)

DELIVERABLE: their own material answering five known questions, plus one self-built
feature. They can classify any wrong answer as retrieval or generation.
```

## Lesson 8: Day 8
```
DAY 8 - TESTING, TUNING AND FINAL DEMO

> Recap (10mn)
> Presentation: how would you know if you made it better? The trap is changing something,
  asking one question and deciding it improved. Decide how to measure first, change one
  thing, re-measure. (15mn)

> STEP 1: Test set and baseline (20mn)
- five questions with known answers, one of which the notes do NOT cover, so it must refuse
- score all five before changing anything

> STEP 2: Tune, one thing at a time (25mn)
- how many chunks to retrieve; chunk size; the system prompt; the model itself
- swapping gpt-5.4-mini for gpt-5.4 triples the price and often does not win - the retriever did
  the hard part. That is a real finding, not a failure.

> Break (5mn)

> STEP 3: Finish the project (20mn)
- requirements.txt, a README, and the key file kept out of anything shared
- fresh-machine test: swap folders with your neighbour and run theirs from their README

> STEP 4: Showcase (20mn)
- ~90 seconds each: what it knows, one good answer, one correct refusal, what they added,
  one thing that broke

> Wrap-up (5mn)

DELIVERABLE: a finished documented project a classmate ran from the README alone; a test
set with before/after scores; a live demo including one correct refusal.
```

---

## What software will you require?
```
All machines macOS. Everything runs on the laptop - no cloud platform, no server. All
free except the OpenAI API. To install on all 16 machines before Day 1:

1. Python 3.12

2. VS Code with two Microsoft extensions: "Python" and "Jupyter". Without Jupyter the
   lesson notebooks cannot be opened.

3. The packages from the requirements.txt I provide (langchain, langchain-openai,
   langchain-chroma, langchain-text-splitters, chromadb, python-dotenv, jupyter,
   ipykernel, numpy). About 50 MB - both AI models run on OpenAI's servers, so there is
   no PyTorch. Please still install it in advance.

4. One key in the students' Python environment:
   - OPENAI_API_KEY - answers questions and creates embeddings. I provide it; students
     cannot create their own, as API accounts require 18+.

Network: outbound HTTPS every lesson to api.openai.com. Tell me in advance about any
proxy or TLS inspection.

Students do not need administrator rights.
```

## What hardware will you require?
```
- 16 macOS laptops, 8 GB RAM, ~1 GB free disk. No GPU, nothing heavy to install.
- projector and a whiteboard. The whiteboard is used properly: on Day 4 students place
  word cards on a drawn 2-axis space to build intuition for embeddings, and Day 5 opens
  with them rebuilding the pipeline on it from memory.

Storage: students may sit at a different laptop each lesson, so each needs a personal
directory on shared storage with write access and ~2 GB free. Their code, documents and
search index live there; Python stays on each laptop.

Please confirm the student directory path is identical on every machine.
```

## What specific tools and materials will you require?
```
Provided by me, public at https://github.com/ArtyoMKo/tumo_month_workshop:
- 5 Jupyter notebooks (Days 1-5) with exercises and extra challenges
- 3 student guides (Days 6-8) for the project phase in VS Code
- a runnable Python cheatsheet notebook, needing no key or internet, which also occupies
  whoever finishes setup first
- the final project: 5 documented modules, requirements.txt, .env.example, README
- check_setup.py, which verifies a machine in 8 steps with a specific fix for each failure
- a sample document set describing an invented project, used on Day 2. Fictional on
  purpose: no AI has seen it, so a correct answer proves retrieval worked.

From TUMO:
- one OpenAI API key with a spend limit. About $6 total for 16 students over 16 hours:
  embeddings cost well under a cent in total, so nearly all of it is the answers,
  ~0.11 cents per question.
- machines prepared as above, and a shared-storage directory per student

From students:
- 3-10 of their own .txt/.md files from Day 2, ideally in English. Shared storage is visible to
  everyone, so they are asked on Day 1 for general-subject notes only.
```

## Visual references to upload
1. Terminal: the assistant answering with `Sources:` listed
2. Terminal: the assistant refusing — "That isn't in your documents."
3. A follow-up exchange showing it remembers context
4. The finished VS Code project tree
5. Day 4: the similarity scores for a question and an answer sharing no words
