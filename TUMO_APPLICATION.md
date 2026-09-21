# TUMO Lesson Plan Application — paste-ready answers

Repo: https://github.com/ArtyoMKo/tumo_month_workshop

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
- No AI, machine learning or maths background needed.
- Age 13-18.
- From Day 2, each student brings 3-10 of their own .txt or .md files - revision notes,
  a subject they study, rules of a game. Armenian, English or mixed. Shared storage is
  visible to everyone, so: general subjects, nothing personal. Backup set provided.
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
answer completely. It has never seen your notes; it is producing text that looks like an
answer. In this workshop students build the fix: an assistant that reads documents they
choose themselves - revision notes, a subject they study, the rules of a game - and
answers only from that material, naming the file each answer came from. Asked something
its documents do not cover, it says so instead of guessing. Getting a computer to admit
what it does not know is the hard part, and it is what this workshop is about.

Students begin in a notebook, writing instructions that control how an AI behaves. They
learn how text is split into pieces, how those pieces become numbers that capture meaning
rather than spelling - so a question in Armenian can find an answer written in English -
and how to search those numbers. Halfway through, the code leaves the notebook and becomes
a real Python project in VS Code. The final lessons cover loading their own material,
diagnosing wrong answers, measuring quality against a test set they write, and presenting
the result.


To apply

Send a short list of the documents you would want your assistant to know about - notes
for a subject, a topic you are interested in, a game or a book you know well - and say
why you chose them. Armenian, English or both.

Also tell us what programming you have done, including any Python, and what you would
most like to understand about how AI tools work. No AI experience required.

Note: your documents are stored in your TUMO workshop folder, which is visible to others.
Choose material about a subject, not anything personal.


Bio.

Artyom Kosakyan is an AI Engineer at Async Armenia, where he specialises in Voice AI. He
studied Applied Mathematics and Informatics at Yerevan State University, and has spent
the last three years teaching Python with the FAST Foundation - experience that shapes
how this workshop runs: students write and execute everything themselves from the first
lesson, and every idea is made to work before it is named. His engineering work is in
getting language and speech models to behave reliably in real products, which is the
problem at the centre of this course: not making an AI talk, but making it answer from
something you can check.
```

---

## Lesson 1: Day 1
```
DAY 1 - SETUP AND YOUR FIRST AI CALL

> Getting to know each other (10mn)
- introductions; demo the finished assistant, including one question it refuses

> Presentation: how this works (15mn)
- a model predicts text; no database, no inner difference between remembering and
  inventing -> confident fiction
- what an API is; why the key is a password

> STEP 1: Setup (25mn)
- everything pre-installed; this is connecting pieces
- Python on the laptop, YOUR WORK in your shared folder (you may be at a different Mac
  next lesson)
- create the project folder; activate the environment (every Terminal, every lesson)
- .env with ANTHROPIC_API_KEY (answers) and HF_TOKEN (searches)
- Select Kernel in the notebook - needed every time, the #1 source of errors
- mention: shared storage is visible to everyone; next lesson bring general-subject notes
- hand out PYTHON_CHEATSHEET.ipynb

> STEP 2: First call to Claude (15mn)
- CHAT_MODEL = "anthropic:claude-haiku-4-5"; init_chat_model(...).invoke(...)
- inspect the whole response, not just .text
- usage_metadata -> tokens; $1/M in, $5/M out

> STEP 3: System prompts (20mn)
- System (written by the programmer, invisible) vs Human
- same question with and without a system prompt
- write ask(system_prompt, question); one question, three different jobs

> STEP 4: Making it follow rules (20mn)
- length, format (JSON only), language (Armenian)
- refusal: "You only answer weather questions. Otherwise reply exactly: ..." Test with
  3 questions, 2 off-topic.
- students try to break their own rule from the user message -> prompt injection

> STEP 5: Changing AI company in one line (10mn)
- only CHAT_MODEL names a company; swap to sonnet-5 / openai / ollama and rerun

> Wrap-up (5mn) - homework: bring 3-10 of your own .txt/.md files

DELIVERABLE: working environment, their own ask() function, three system prompts with
different behaviour, one forcing a refusal.
```

## Lesson 2: Day 2
```
DAY 2 - WHY AI MAKES THINGS UP

> Recap (10mn) - check documents; hand out backups

> Presentation: why models invent (20mn)
- it predicts plausible text; recalling and composing are the same operation inside
- real cases: invented court citations, invented refund policies
- the failure is fluency, not stupidity

> STEP 1: Watch it make things up (20mn)
- documents/ describes an invented project no AI has seen, so any answer is provably made up
- ask, compare with the file, collect the best inventions on the board
- repeat on the student's own notes

> STEP 2: The brute-force fix (20mn)
- read the file (encoding="utf-8" or Windows mangles Armenian)
- put the text in the system prompt via {context} and .format() -> correct answer
- this is GROUNDING
- ask from a different file -> wrong again -> load all files
- students repeat on their own notes

> Break (5mn)

> Presentation: tokens, context, cost (15mn)
- models read tokens (~4 chars); Haiku's window is 200,000
- too much context makes answers worse

> STEP 3: Measure why it cannot scale (25mn)
- window: 4 files 2,070 tokens; a textbook 125,000 (fits); a year of notes 750,000 (no)
- cost, charged every question: a textbook $12.50 per 100; a year of notes $75.00
- the answer is buried in text you did not want
- "it fits" and "it's a good idea" are different questions

> Wrap-up (5mn) - the goal for the next 3 days: find the three paragraphs that matter

DELIVERABLE: a notebook showing the same question answered wrongly without context and
correctly with it, plus their own cost calculation.
```

## Lesson 3: Day 3
```
DAY 3 - PREPARING DOCUMENTS: CHUNKING

> Recap (10mn)

> Presentation: what a chunk should be (15mn)
- one idea: big enough to stand alone, small enough to be mostly relevant
- too small: "The two-tracker rule was added after" ... after what?

> STEP 1: Load documents (20mn)
- build Document(page_content, metadata) per file; sorted() on every glob
- the filename in metadata reaches the final answer; lose it and you cannot cite a source

> STEP 2: Compare chunk sizes (25mn)
- split at 200 / 500 / 1000 / 4000; print counts, averages, and the same passage cut
  four ways
- the test: "handed only this chunk, could you answer?"

> Break (5mn)

> Presentation: the boundary problem (10mn)
- wherever you cut, you sometimes cut through the answer; overlap 10-20% fixes it

> STEP 3: Overlap (15mn)
- print the seam between two chunks with overlap 0, then with overlap 100
- settle on CHUNK_SIZE 1000, CHUNK_OVERLAP 200

> STEP 4: Split on structure (15mn)
- MarkdownHeaderTextSplitter keeps sections whole; compare on their own notes

> Choose your settings (5mn) - written down, with one sentence of justification

DELIVERABLE: their own documents split, with chosen settings and a written reason.
```

## Lesson 4: Day 4
```
DAY 4 - EMBEDDINGS AND SEMANTIC SEARCH

> Recap (10mn)

> Presentation: embeddings without maths (20mn)
- meaning as a position; students place word cards on a drawn 2-axis space
- the real model uses 384 axes it worked out itself; you only need to measure distance

> STEP 1: Measure meaning (20mn)
- embed a word -> 384 numbers; similarity 1.0 identical, 0.0 unrelated
- students predict before running: balloon/airship, balloon/trombone, car/vehicle,
  king/queen, hot/cold
- hot/cold scores HIGH - embeddings capture topic, not agreement
- each student finds a pair where the model disagrees with them

> STEP 2: The result that makes this work (15mn)
- a question and its answer sharing no content word still score close (+0.28); a word
  search scores zero
- an Armenian question finds the English answer (+0.35) - no shared characters at all
- hence the multilingual model: the English-only one scores a correct Armenian answer and
  an unrelated sentence 0.004 apart, so retrieval goes random with no error

> Break (5mn)

> Presentation: vector stores (10mn)
- a database of vectors searched by closeness; Chroma locally, a hosted one at scale

> STEP 3: Build and search your index (25mn)
- Chroma.from_documents(...), similarity_search(question, k=3)
- no language model involved - pure search, so it is obvious which half does what
- for Chroma the score is a distance: lower is closer
- each student builds a store over their own documents

> STEP 4: The question with no answer (15mn)
- search something absent -> it still returns 3 chunks. A vector store always returns k.
- therefore retrieval alone does not prevent hallucination -> Day 5
- then metadata filtering: search one file only

DELIVERABLE: a working search engine over their own documents, and three documented
cases with scores: answered well / right chunk ranks low / not in the documents.
```

## Lesson 5: Day 5
```
DAY 5 - BUILDING THE RAG ASSISTANT

> Recap (10mn) - whiteboard the pipeline from memory before opening anything

> STEP 1: Assemble the prompt, then read it (25mn)
- retrieve with k=4; join with "\n\n---\n\n" (without a clear break the model reads two
  chunks as one sentence and invents a connection)
- fill the template, print the whole prompt, read it aloud. That is RAG, nothing hidden.
- send with model.invoke([SystemMessage, HumanMessage])

> STEP 2: answer_question() with sources (20mn)
- return (answer, sources); sources make an answer checkable
- test a question whose answer spans two files

> Break (5mn)

> STEP 3: The refusal (20mn)
- ask something absent -> it answers anyway from 4 irrelevant chunks
- add: 'If the notes do not contain the answer, say exactly: "That isn't in your
  documents." Do not guess.'
- ask again -> refuses; check a question it should answer still works
- every student finds one question theirs refuses, and one where the refusal fails

> STEP 4: Tune k (15mn)
- k = 1, 4, 12. k=1 misses answers; k=12 buries the right chunk. Start at 4-6.

> STEP 5: Conversation memory (20mn)
- "Why two trackers?" then "Which is more expensive?" -> the second fails
- two problems: the model does not know what "them" means (replay earlier turns), and
  the search does not either (glue the last 2 questions onto the query)
- implement both; students run a 4-turn conversation on their own notes

> Wrap-up (5mn) - the notebook phase ends here

DELIVERABLE: a working RAG assistant with sources, handling a follow-up question, and
correctly refusing one documented question.
```

## Lesson 6: Day 6
```
DAY 6 - FROM NOTEBOOK TO PYTHON PROJECT

Hand out guides/lesson6_build_the_project.md - per-file instructions with a check after
each, so anyone falling behind catches up without stopping the room.

> Presentation: why we leave the notebook (10mn)
- a notebook is a lab bench; you hand someone the thing you built, not the bench

> Presentation: the two-program design (20mn)
- reopening the notebook recomputes every embedding before you can ask one question
- ingest.py is slow and runs when documents change; main.py is fast and runs constantly
- today's rule: each file explainable in one sentence

> STEP 1: config.py (15mn)
- all constants move here; paths use Path(__file__).parent
- CHECK: python config.py prints nothing and exits cleanly

> STEP 2: ingest.py (25mn)
- load / split / embed / persist; delete the old index before rebuilding
- CHECK: python ingest.py -> chunk count, and a vector_db/ folder appears

> Break (5mn)

> STEP 3: retriever.py (20mn)
- opens the saved index, never builds one; same embedding model as ingest.py, or vectors
  are incompatible and search returns nonsense with no error
- must not import assistant.py or mention a language model
- CHECK: a scratch file printing 3 retrieved chunks

> STEP 4: assistant.py (15mn)
- system prompt, build_context(), build_search_query(), answer_question(q, history=None)
- history=None, not history=[] - a list default is shared by every call, so the assistant
  would silently remember every conversation it ever had

> STEP 5: main.py and run it (10mn)
- welcome(), index check, the loop with /quit, /forget, /sources; one try/except
- python main.py - a real program, from a terminal, no notebook

DELIVERABLE: every student leaves with a working "python main.py", confirmed individually.
```

## Lesson 7: Day 7
```
DAY 7 - YOUR OWN KNOWLEDGE BASE

Hand out guides/lesson7_your_own_documents.md.

> Recap (10mn) - everyone runs python main.py before changing anything

> Presentation: garbage in, garbage out (15mn)
- good: headings, short paragraphs, one topic per file, explicit sentences
- bad: an unbroken wall of text, everything in one file
- notes saying "this is the important one" are unfindable - "this" carries the meaning

> STEP 1: Load your own documents (30mn)
- copy files in, re-ingest, ask five questions you know the answers to, record right/wrong
- the same five are reused on Day 8

> Presentation: splitting the blame (15mn)
- always in this order: did the right chunk come back? (/sources, costs nothing) then,
  did the model use it?
- chunk missing -> documents / chunk size / k. Chunk ignored -> the system prompt.
- debugging the prompt when the problem is retrieval loses an afternoon

> Break (5mn)

> STEP 2: Improve the documents, then measure (25mn)
- fix the document, not the code; re-ingest; re-ask the same five; record before vs after
- chunk size, overlap and document changes need a re-ingest; k and the prompt do not
- most students find fixing documents beats every available code change

> STEP 3: Build one feature (15mn)
- the skill is deciding which file it belongs in
- easier: show scores, /help, cap answer length
- medium: /stats, search one file only, save the conversation
- harder: quote the evidence, /why, longer memory

> Wrap-up (5mn)

DELIVERABLE: their own material answering five known questions, plus one self-built
feature. They can classify any wrong answer as retrieval or generation.
```

## Lesson 8: Day 8
```
DAY 8 - TESTING, TUNING AND FINAL DEMO

Hand out guides/lesson8_test_and_ship.md - test-set, tuning-log and README templates.

> Recap (10mn)

> Presentation: how would you know if you made it better? (15mn)
- the trap: change k, ask one question, think "that's better", keep it. You measured
  nothing - the model words things differently every time and you asked once.
- decide how to measure first; change one thing; re-measure

> STEP 1: Test set and baseline (20mn)
- five questions with known answers: a plain fact / needs two files / worded differently
  / an easy-to-miss detail / something the notes do not cover (must refuse)
- score all five before changing anything

> STEP 2: Tune, one thing at a time (25mn)
- RETRIEVE_K 2/4/8 (no re-ingest); CHUNK_SIZE 500/1000/2000 (re-ingest); the system
  prompt; CHAT_MODEL haiku-4-5 -> sonnet-5 at twice the price
- re-score after each single change
- Sonnet often does not win - the retriever did the hard part. "I tested it and the
  expensive one wasn't better" is a strong finding.

> Break (5mn)

> STEP 3: Finish the project (20mn)
- requirements.txt; .env not shareable, .env.example present
- README: what it is / install / run / what I added + one thing that broke
- fresh-machine test: swap folders with your neighbour, follow their README literally,
  note where you got stuck, swap back and fix

> STEP 4: Showcase (20mn)
- ~90 seconds each, already running: what it knows, one good answer, one correct
  refusal, what they added, one thing that broke

> Wrap-up (5mn)
- after the workshop the key stops working: switch to ollama:llama3.2 and the answering
  half runs free on your own laptop

DELIVERABLE: a finished documented project a classmate ran from the README alone; a test
set with before/after scores; a live demo including one correct refusal.
```

---

## What software will you require?
```
All machines macOS. Everything runs on the laptop - no cloud platform, no server. All
free except the Anthropic API.

To install on all 16 machines before Day 1:

1. Python 3.12

2. VS Code with two Microsoft extensions: "Python" and "Jupyter".
   Without Jupyter the lesson notebooks cannot be opened.

3. The packages from the requirements.txt I provide: langchain, langchain-anthropic,
   langchain-chroma, langchain-huggingface, langchain-text-splitters, chromadb,
   python-dotenv, jupyter, ipykernel, numpy.
   About 50 MB - both AI models run on their providers' servers, so there is no PyTorch.
   Please still install in advance so lesson 1 is not spent waiting.

4. Two keys available to the students' Python environment:
   - ANTHROPIC_API_KEY - answers questions. I provide it; students cannot create their
     own (API accounts require 18+).
   - HF_TOKEN - free Hugging Face token for the embedding model. Optional but
     recommended: without it all 16 students share one anonymous rate limit. Free at
     huggingface.co/settings/tokens, "Read" access. One shared TUMO token is fine.

Network: outbound HTTPS every lesson to api.anthropic.com, huggingface.co and
router.huggingface.co. Tell me in advance if the lab uses a proxy or TLS inspection.

Students do not need administrator rights.
```

## What hardware will you require?
```
- 16 macOS laptops, 8 GB RAM, ~1 GB free disk. No GPU; nothing heavy to install.
- projector
- whiteboard - used properly: on Day 4 students place word cards on a drawn 2-axis space
  to build intuition for embeddings, and Day 5 opens with them rebuilding the pipeline
  from memory

Storage: students may sit at a different laptop each lesson, so each needs a personal
directory on shared storage, write access, ~2 GB free. Their code, documents and search
index live there; Python stays on each laptop.

Please confirm the student directory path is identical on every machine.
```

## What specific tools and materials will you require?
```
Provided by me (public at https://github.com/ArtyoMKo/tumo_month_workshop):
- 5 Jupyter notebooks (Days 1-5), with exercises and extra challenges
- 3 student guides (Days 6-8) for the project phase in VS Code
- a runnable Python cheatsheet notebook - no key or internet needed, so it also occupies
  whoever finishes setup first
- the final project: 5 documented modules, requirements.txt, .env.example, README
- check_setup.py - verifies a machine in 8 steps with a specific fix for each failure
- a sample document set describing an invented project, used on Day 2. Fictional on
  purpose: no AI has seen it, so a correct answer proves retrieval worked. Also backup
  material for anyone who forgets their own.

From TUMO:
- one Anthropic API key with a spend limit. About $7 total for 16 students over 16 hours;
  embeddings are free, so only the final answer is paid for (~0.14 cents per question).
- machines prepared as above; a shared-storage directory per student

From students:
- 3-10 of their own .txt/.md files from Day 2, any language. Shared storage is visible to
  everyone, so they are asked on Day 1 for general-subject notes only.
```

## Visual references to upload
1. Terminal: the assistant answering with `Sources:` listed
2. Terminal: the assistant refusing — "That isn't in your documents."
3. A follow-up exchange showing it remembers context
4. The finished VS Code project tree
5. Day 4: an Armenian question matching an English note

Capture 1–3 in one run once you have the workshop key.
