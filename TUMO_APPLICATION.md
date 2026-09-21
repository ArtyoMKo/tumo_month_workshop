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
*Required — only you know these. 8 days.*

## Number of students
```
16
```

## Prerequisites
```
- Basic Python from TUMO's other programming tracks: variables, lists, dictionaries,
  loops, functions. Python is NOT taught here - students get a cheatsheet to look things
  up in.
- No AI, machine learning or maths background needed.
- Age 13-18.
- FROM DAY 2, each student must bring 3-10 of their own .txt or .md files (revision
  notes, a subject they study, rules of a game, an exported wiki). Armenian, English or
  mixed - all work. A backup set is provided for students who forget.
```

## What are the learning objectives and goals?
```
GOALS
- understand why an AI chatbot invents confident, false answers
- write system prompts that control how a model behaves, and find their limits
- split documents into chunks and understand why chunk size matters
- turn text into embeddings and search by meaning instead of by words
- assemble retrieved text into a prompt so answers are grounded in real documents
- make the assistant refuse questions its documents do not cover
- add conversation memory so follow-up questions work
- move working code out of a notebook into a real Python project in VS Code
- load their own documents and diagnose why an answer came out wrong
- measure quality with a test set before tuning, and change one thing at a time
- write a README so someone else can run their project
```

## What are the anticipated learning outcomes?
```
Each student finishes with a runnable local Python project (main.py, config.py,
ingest.py, retriever.py, assistant.py + requirements.txt + README) that answers questions
about documents they chose themselves, cites the source file for every answer, handles
follow-up questions, and refuses anything its documents do not cover.

Each student can:
- demonstrate one correct answer AND one correct refusal, live
- explain, for any wrong answer, whether the search failed or the model failed
- show a test set with before-and-after scores from their own tuning
- hand the project to a classmate who can run it from the README alone

Every project is different, because every student picks their own documents.
```

## Workshop announcement
```
BUILD AN AI THAT ACTUALLY READS YOUR NOTES

Ask a chatbot about your homework and it answers confidently - and sometimes makes it up
completely. It has never seen your notes. It is guessing.

In this workshop you fix that. You build your own AI assistant that reads the documents
YOU give it - your biology notes, a history chapter, the rules of a game - and answers
from them, telling you which file each answer came from. Ask a follow-up and it
remembers what you were talking about.

And when you ask something your notes do not cover, it says so instead of inventing an
answer. Getting a computer to admit it does not know is harder than it sounds, and it is
the most valuable thing you will build here.

Bring your notes in Armenian, English or both - it works either way.

You start in a notebook and finish with a real Python project in VS Code that you keep.

You need basic Python. You do not need to be good at maths.

8 days. You leave with an AI that knows what you know.
```

---

## Lesson 1: Day 1
```
DAY 1 - SETUP AND YOUR FIRST AI CALL

> Getting to know each other (10mn)
- me, then students: name, what they've built, what subject they might feed their AI
- demo the finished assistant: question -> answer + sources; then a question outside my
  notes -> "That isn't in your documents."  "That refusal is what we're building."

> Presentation: how this works (15mn)
- a model predicts the next text. No database, and no internal difference between
  remembering and inventing -> confident fiction
- what an API is; why the key is a password

> STEP 1: Setup (25mn)
- Python 3.12, VS Code + the "Python" and "Jupyter" extensions
- python -m venv .venv, activate (prompt shows "(.venv)"), pip install -r requirements.txt
- create ".env" holding: ANTHROPIC_API_KEY=sk-ant-...   (no quotes, no spaces)
- open lesson1.ipynb > Select Kernel > Python Environments > the .venv one.
  Needed for EVERY notebook - the #1 cause of errors all workshop.
- hand out PYTHON_CHEATSHEET.ipynb. Runs with no key or internet, so it also occupies
  whoever finishes setup first.

> STEP 2: First call to Claude (15mn)
- CHAT_MODEL = "anthropic:claude-haiku-4-5" (company : model)
- init_chat_model(CHAT_MODEL).invoke("why does a balloon burst?")
- inspect the whole response, not just .text
- usage_metadata -> tokens. $1/M in, $5/M out. That question: ~0.002 cents.

> STEP 3: System prompts (20mn)
- two roles: System (written by the programmer, invisible to the user) and Human
- same question with and without "You are a terse flight engineer, under 15 words"
- write ask(system_prompt, question), then run one question through three jobs:
  teacher for a 10-year-old / pirate / only ever replies with a question

> STEP 4: Making it follow rules (20mn)
- length ("exactly five words" - test it, models count badly), format (JSON only),
  language ("always reply in Armenian")
- REFUSAL: "You only answer weather questions. Otherwise reply exactly: 'I only answer
  questions about weather.' Do not answer anyway." Test with 3 questions, 2 off-topic.
  "One paragraph of English. Day 5 uses exactly this."
- students then try to BREAK their own rule from the user message. This is prompt
  injection - unsolved. A system prompt is a strong instruction, not a guarantee.

> STEP 5: Changing AI company in one line (10mn)
- the only place a company is named is CHAT_MODEL. Swap to claude-sonnet-5 /
  openai:gpt-4.1-mini / ollama:llama3.2 (this laptop, no key, no internet) and run the
  same function on both.

> Wrap-up (5mn) - HOMEWORK: bring 3-10 of your own .txt/.md files, any language

DELIVERABLE: working environment + their own ask() function + three system prompts with
different behaviour, one forcing a refusal.
```

## Lesson 2: Day 2
```
DAY 2 - WHY AI MAKES THINGS UP

> Recap (10mn) - check everyone brought documents; hand backups to those who didn't

> Presentation: why models invent (20mn)
- it predicts plausible text; recalling and composing are the same operation inside
- real cases: lawyers filing invented court judgments, chatbots inventing refund
  policies their company then had to honour
- the failure isn't stupidity, it's fluency

> STEP 1: Watch it make things up (20mn)
- documents/ describes "the Kestrel Project" - a balloon programme invented for this
  workshop. No AI has ever seen it, so any answer is provably invented.
- ask "What altitude did Flight 8 reach?" then open flights.md and compare
- 3 more questions; best fabrications go on the whiteboard
- repeat on the student's OWN notes. Does it ever say "I don't know"?

> STEP 2: The brute-force fix (20mn)
- read the file (encoding="utf-8" - not optional, Windows mangles Armenian without it)
- put the text into the system prompt via a {context} placeholder and .format()
- ask again -> correct. This is GROUNDING.
- ask something from a DIFFERENT file -> wrong again -> load all files, retry
- students do the same with their own notes

> Break (5mn)

> Presentation: tokens, context, cost (15mn)
- models read tokens (~4 chars). Everything is priced and limited in tokens.
- Haiku 4.5 window: 200,000 tokens. Too much context makes answers WORSE.

> STEP 3: Measure why it can't scale (25mn)
- estimate_tokens(text) = len(text) // 4
- wall 1, the window: our 4 files 2,070 tokens (fits) / a textbook 125,000 (FITS!) /
  a year of notes 750,000 (doesn't). Be honest: windows grew, this wall moved. Don't
  trust tutorials that still say the window is the reason for RAG.
- wall 2, cost, charged on EVERY question: a textbook $12.50 per 100 questions;
  a year of notes $75.00 per 100 questions
- wall 3: the answer is buried in text you didn't want
- "it fits" and "it's a good idea" are different questions
- optional: write the dumbest search (keep paragraphs sharing a word). Break it:
  "heaviest thing they can fly" vs "no payload exceeds 2.8 kg" share no words.

> Wrap-up (5mn) - the goal for the next 3 days: "find the three paragraphs that matter"

DELIVERABLE: a notebook showing the same question answered wrongly without context and
correctly with it, plus their own cost calculation.
```

## Lesson 3: Day 3
```
DAY 3 - PREPARING DOCUMENTS: CHUNKING

> Recap (10mn)

> Presentation: what a chunk should be (15mn)
- one idea per chunk: big enough to stand alone, small enough to be mostly relevant
- too small: "The two-tracker rule was added after" ... after WHAT?
- too large: back to Day 2's problem in miniature

> STEP 1: Load documents properly (20mn)
- load_documents(): for each .md build a Document(page_content=..., metadata=...)
- sorted() on every glob, or the order depends on the filesystem and results change
  for no visible reason
- inspect documents[0]: .page_content and .metadata
- the filename in metadata travels all the way to the final answer. Lose it and you can
  never cite a source.

> STEP 2: Compare chunk sizes (25mn)
- RecursiveCharacterTextSplitter splits on paragraphs first, then lines, then sentences,
  then words - the most natural break available, not blind chopping
- split at 200 / 500 / 1000 / 4000, print counts and averages
- print the SAME passage cut four ways and READ them
- the only question that matters: "handed only this chunk, could you answer?"
- averages land below the size asked for - the splitter preferring a natural break

> Break (5mn)

> Presentation: the boundary problem (10mn)
- wherever you cut, you cut somewhere - sometimes through the answer
- overlap = each chunk repeats the end of the previous one, 10-20% of chunk size

> STEP 3: Overlap (15mn)
- split at 300 with overlap 0, print the seam between chunks 5 and 6
- split at 300 with overlap 100, print the same seam - the text reappears
- settle on CHUNK_SIZE = 1000, CHUNK_OVERLAP = 200

> STEP 4: Split on structure instead of length (15mn)
- MarkdownHeaderTextSplitter keeps each "## section" whole and records the heading
- compare against plain splitting on their own notes
- what happens if one section is 10,000 characters?

> Choose your settings (5mn)
- write down chunk size + overlap AND one sentence why. "It was the default" not accepted.

DELIVERABLE: their own documents loaded and split, with chosen settings and a written
justification.
```

## Lesson 4: Day 4
```
DAY 4 - EMBEDDINGS AND SEMANTIC SEARCH

> Recap (10mn)

> Presentation: embeddings without maths (20mn)
- meaning as a POSITION. Draw 2 axes on the whiteboard; students physically place word
  cards (cat, dog, car, bus, happy, sad)
- reveal: the real model uses 384 axes it worked out itself. Nobody designed them.
- you can't picture 384 dimensions; you only need to measure distance.

> STEP 1: Measure meaning (20mn)
- HuggingFaceEmbeddings runs ON THE LAPTOP - no key, no internet, free
- embed "balloon" -> 384 numbers. similarity(a,b): 1.0 identical, 0.0 unrelated
- students PREDICT before running: balloon/airship, balloon/trombone, car/vehicle,
  king/queen, hot/cold
- hot/cold scores HIGH: embeddings capture TOPIC, not agreement. A real limitation -
  a retriever can return a paragraph saying the opposite of the truth.
- each student finds one pair where the model disagrees with them

> STEP 2: The result that makes this work (15mn)
- Q "What keeps working when the radio cannot get through?" vs A "The satellite tracker
  works in valleys where the LoRa signal does not reach." NOT ONE content word shared.
  A word search scores zero; embeddings give a +0.28 gap.
- then across languages: "Ո՞ր թռիչքն է հասել ամենաբարձր կետին" finds "Flight 8 reached
  34,600 m" - gap +0.35, not one character shared, not even the alphabet
- this is why we use the multilingual model. The common English-only one scores a
  correct Armenian answer and an unrelated sentence 0.004 apart: retrieval goes random,
  with no error to tell you.

> Break (5mn)

> Presentation: vector stores (10mn)
- a database of vectors searchable by closeness. Chroma runs on the laptop; a company
  would use a hosted one; in our code that's a config change, not a rewrite.

> STEP 3: Build and search your index (25mn)
- Chroma.from_documents(...), then similarity_search(question, k=3)
- NO LANGUAGE MODEL INVOLVED - pure search, so it's obvious which half does what
- with_score: for Chroma the score is a DISTANCE, lower is closer. Other stores report
  it the other way; always check.
- each student builds a store over their own documents

> STEP 4: The question with no answer (15mn)
- search "Who won the 2018 World Cup?" -> it STILL returns 3 chunks. A vector store
  always returns k results; it has no concept of "nothing is relevant". Scores are
  worse (1.7 vs 0.87) but it does not refuse.
- THEREFORE retrieval alone does not prevent hallucination. Day 5 adds the other half.
- then metadata filtering: search one file only
- optional: t-SNE plot coloured by file - topics cluster without being told

DELIVERABLE: a working search engine over their own documents and three documented
cases with scores: answered well / right chunk ranks low / not in the documents.
```

## Lesson 5: Day 5
```
DAY 5 - BUILDING THE RAG ASSISTANT

> Recap (10mn) - students whiteboard the pipeline from memory BEFORE opening anything

> STEP 1: Assemble the prompt, then read it (25mn)
- retrieve with similarity_search(question, k=4)
- join with "\n\n---\n\n". The separator matters: without a clear break the model
  reads the end of one chunk and the start of the next as one sentence.
- fill SYSTEM_TEMPLATE.format(context=context)
- PRINT THE WHOLE PROMPT and read it aloud. "That's RAG, in full, nothing hidden. No
  model was retrained. We just did a good job of deciding what to paste."
- send it with model.invoke([SystemMessage(...), HumanMessage(...)])

> STEP 2: answer_question() with sources (20mn)
- return (answer, sources); sources is a sorted set of filenames, because 4 chunks
  often come from 2 files
- sources aren't decoration - they're what makes an answer checkable
- test a question whose answer spans two files

> Break (5mn)

> STEP 3: The refusal (20mn)
- ask "Who won the 2018 World Cup?" -> it answers anyway from 4 irrelevant chunks. We
  said "use only the notes" but never said what to do when the notes lack it.
- add: 'If the notes do not contain the answer, say exactly: "That isn't in your
  documents." Do not guess.'
- ask again -> refuses. Check a question it SHOULD answer still works.
- EVERY STUDENT MUST FIND one question theirs correctly refuses, and one where the
  refusal FAILS. The second is more interesting.

> STEP 4: Tune k (15mn)
- same question at k = 1, 4, 12. k=1 misses answers that were there; k=12 buries the
  right chunk among 11 others and answers go vague and expensive. Start at 4-6.

> STEP 5: Conversation memory (20mn)
- "Why two trackers?" then "Which of them is more expensive?" -> the second fails
- TWO separate problems: the model doesn't know what "them" means (replay earlier turns
  as HumanMessage/AIMessage pairs), and the SEARCH doesn't either (glue the last 2
  questions onto the search query only)
- implement both, run a 3-turn conversation
- students: a 4-turn conversation on their own notes, each question depending on the
  last. Then widen memory to 8 turns, change subject halfway, watch retrieval get worse.

> Wrap-up (5mn) - the notebook phase ends here

DELIVERABLE: a working RAG assistant with sources, handling a follow-up question, and
correctly refusing one documented question.
```

## Lesson 6: Day 6
```
DAY 6 - FROM NOTEBOOK TO PYTHON PROJECT

Hand out guides/lesson6_build_the_project.md - students open it in VS Code's preview
pane and work beside it. It carries the full per-file instructions and a CHECK after
each one, so anyone falling behind catches up without stopping the room.

> Presentation: why we leave the notebook (10mn)
- a notebook is a LAB BENCH. You hand someone the thing you built, not the bench.

> Presentation: the two-program design (20mn)
- reopening the notebook re-reads every document and recomputes every embedding before
  you can ask one question - ~30 seconds to redo unchanged work
- so: ingest.py is SLOW, run when documents change; main.py is FAST, run constantly.
  The index is saved to disk between them.
- draw the arrows on the whiteboard - they only point one way
- today's rule: each file must be explainable in ONE sentence

> STEP 1: config.py (15mn)
- create the folder, copy notes + .env + requirements.txt in, open in VS Code
- all constants move here; paths use Path(__file__).parent
- CHECK: python config.py prints NOTHING and exits cleanly. Fix errors now - every
  other file imports it.

> STEP 2: ingest.py (25mn)
- load / split / embed / persist, plus if __name__ == "__main__"
- encoding="utf-8" everywhere; sorted() on globs; delete the old index before rebuilding
- CHECK: python ingest.py -> filenames, chunk count, a vector_db/ folder appears.
  "Your program just made something that outlives it."

> Break (5mn)

> STEP 3: retriever.py (20mn)
- opens the saved index, never builds one; must use the SAME embedding model as
  ingest.py, or vectors are incompatible and search returns nonsense with NO error
- must not import assistant.py and must never mention a language model
- CHECK: a scratch file printing 3 retrieved chunks. Costs nothing.

> STEP 4: assistant.py (15mn)
- the system prompt, build_context(), build_search_query(),
  answer_question(question, history=None)
- history=None, NOT history=[] - a list default is created once and shared by every
  call, so the assistant would silently remember every conversation it ever had
- CHECK: one real question, a fraction of a cent

> STEP 5: main.py and RUN IT (10mn)
- welcome(), index check, history = [], the loop with /quit, /forget, /sources
- ONE try/except around the loop body, at the edge of the program
- python main.py <- the moment. A real program, from a terminal, no notebook.

DELIVERABLE: every student leaves with a working "python main.py", confirmed
individually.
```

## Lesson 7: Day 7
```
DAY 7 - YOUR OWN KNOWLEDGE BASE

Hand out guides/lesson7_your_own_documents.md.

> Recap (10mn) - everyone runs python main.py and asks one question BEFORE changing anything

> Presentation: garbage in, garbage out (15mn)
- good: headings, short paragraphs, one topic per file, explicit sentences
- bad: one unbroken wall of text, everything in notes.md, tables pasted as text
- the killer: notes saying "this is the important one". "This" means nothing to a
  search. Write "mitosis is the important one" and it becomes findable.

> STEP 1: Load your own documents (30mn)
- copy files into documents/, python ingest.py, python main.py
- ask FIVE questions you already know the answers to; record right/wrong in a table.
  These five get reused today and again on Day 8.

> Presentation: splitting the blame (15mn)
- a wrong answer has two possible causes with two different fixes. ALWAYS in this order:
  1. did the right chunk come back?  -> /sources <question>  (costs nothing, no model)
  2. did the model use it?
- chunk missing -> fix documents / chunk size / k
- chunk present but ignored -> fix the system prompt
- debugging the prompt when the problem is retrieval is the classic way to lose an
  afternoon on this technique

> Break (5mn)

> STEP 2: Improve the documents, then measure (25mn)
- take the worst question and fix the DOCUMENT, not the code: add headings / split a
  big file / delete export noise / rewrite one vague sentence
- python ingest.py, re-ask the same five, record before vs after
- REMINDER: chunk size, overlap, embedding model and document changes all need a
  re-ingest; k and the prompt take effect immediately. "I changed it and nothing
  happened" is almost always a forgotten ingest.
- most students find fixing documents beats every code change available to them

> STEP 3: Build one feature (15mn)
- the skill tested is deciding WHICH FILE it belongs in
- easier: show scores with each answer / /help / cap answer length
- medium: /stats (chunks per file) / search one file only / save the conversation
- harder: make it quote its evidence / /why (show the last full prompt) / longer memory

> Wrap-up (5mn)

DELIVERABLE: their own material answering five known questions, plus one self-built
feature. They can classify any wrong answer as retrieval or generation.
```

## Lesson 8: Day 8
```
DAY 8 - TESTING, TUNING AND FINAL DEMO

Hand out guides/lesson8_test_and_ship.md - it has the test-set, tuning-log and README
templates to fill in.

> Recap (10mn)

> Presentation: how would you know if you made it better? (15mn)
- the trap: change k from 4 to 6, ask one question, think "that's better", keep it. You
  measured nothing - the model words things differently every time, you asked once, and
  you already expected an improvement.
- decide how you'll measure BEFORE changing anything; change ONE thing; re-measure

> STEP 1: Write the test set, score the baseline (20mn)
- five questions with known answers: a plain fact / needs two files / worded
  differently from the notes / an easy-to-miss detail / SOMETHING THE NOTES DON'T COVER
  (must refuse - not optional)
- score all five before changing anything. That's the baseline row.

> STEP 2: Tune, one thing at a time (25mn)
- RETRIEVE_K: 2, 4, 8 (no re-ingest)
- CHUNK_SIZE: 500, 1000, 2000 (RE-INGEST)
- the SYSTEM_PROMPT wording (no re-ingest)
- CHAT_MODEL: claude-haiku-4-5 -> claude-sonnet-5, roughly twice the price
- re-score all five after each single change; fill the tuning log
- the interesting result: Sonnet often does NOT win. The retriever did the hard part;
  the model only has to read four paragraphs and not invent anything. "I tested it and
  the expensive one wasn't better" is a strong finding, not a failure.

> Break (5mn)

> STEP 3: Finish the project (20mn)
- requirements.txt complete
- ls -a: .env must NOT be shareable, .env.example must exist, .gitignore contains .env
- README.md: what it is / install / run / what I added + one thing that broke
- FRESH-MACHINE TEST: swap folders with your neighbour, follow their README literally,
  note every place you got stuck, swap back and fix. Finds more real problems than
  re-reading your own code ever will.

> STEP 4: Showcase (20mn)
- ~90 seconds each, running BEFORE they start talking:
  1. what it knows about
  2. one good answer, pointing at the sources line
  3. ONE CORRECT REFUSAL <- the thing we actually built
  4. what they added
  5. one thing that broke, and what it turned out to be

> Wrap-up (5mn)
- the key stops working after the workshop: switch CHAT_MODEL to ollama:llama3.2 and it
  runs free and offline forever - embeddings and the vector store are already local
- next: a bigger knowledge base, a hosted vector store, the LangChain docs

DELIVERABLE: a finished documented project a classmate ran from the README alone; a
test set with before/after scores; a live demo including one correct refusal.
```

---

## What software will you require?
```
All free except the AI service. Everything runs locally - no cloud, no server.

- Python 3.12; VS Code + the Microsoft "Python" and "Jupyter" extensions
- packages from a provided requirements.txt: langchain, langchain-anthropic,
  langchain-chroma, langchain-huggingface, langchain-text-splitters,
  sentence-transformers, chromadb, python-dotenv, jupyter, ipykernel, numpy
- one Anthropic API key (Claude) from TUMO's existing contract, with a spend limit.
  Students cannot create their own - API accounts require 18+.

PREPARATION REQUEST FOR IT, the day before Day 1: pre-install Python, VS Code and the
two extensions on all 16 machines, and pre-cache the packages and the local embedding
model (~1.5 GB per machine). Sixteen students downloading that at once over shared wifi
would cost a whole lesson. The one-line command is in the repo. With machines prepared,
Day 1 setup takes 15 minutes instead of 40.
```

## What hardware will you require?
```
- 16 laptops or lab PCs (Windows, macOS or Linux - all three tested)
- 8 GB RAM, ~3 GB free disk. The embedding model runs on the CPU. NO GPU REQUIRED.
- permission to install software, or machines prepared by IT (preferred)
- internet access, a projector, and a whiteboard

The whiteboard is used properly, not decoratively: on Day 4 students physically place
word cards on a drawn 2-axis space to build intuition for embeddings, and Day 5 opens
with them rebuilding the whole pipeline on it from memory.

If machines are reset between lessons, the software prep must be reapplied and students
must recreate their .env. Please confirm with IT beforehand.
```

## What specific tools and materials will you require?
```
PROVIDED BY ME (public at https://github.com/ArtyoMKo/tumo_month_workshop):
- 5 Jupyter notebooks (Days 1-5) with explanations, runnable cells and extra challenges
- 3 student guides (Days 6-8) for when they move into a real project in VS Code
- a runnable Python cheatsheet notebook - no key or internet needed, so it also occupies
  whoever finishes setup first
- the complete final project: 5 documented modules, requirements.txt, .env.example, README
- check_setup.py - verifies a machine in 8 steps, printing a specific fix for whichever
  one fails
- a sample document set describing an INVENTED project, used on Day 2. Fictional on
  purpose: no AI has seen it, so students can prove a correct answer came from their own
  retrieval. Doubles as backup material for anyone who forgets their own.

FROM TUMO:
- one Anthropic API key with a spend limit. Estimated total for 16 students across all
  16 hours: about $7. Embeddings run locally and cost nothing; only the final answer is
  paid for, roughly 0.14 cents per question.
- machines prepared in advance (see software)

FROM STUDENTS:
- 3-10 of their own .txt/.md files from Day 2 onward, any language. This is what makes
  every student's project different.
```

## Visual references to upload
1. Terminal: the assistant answering with `Sources:` listed
2. Terminal: the assistant **refusing** — "That isn't in your documents."
3. A follow-up-question exchange showing it remembers context
4. The finished VS Code project tree
5. Day 4: an Armenian question matching an English note

Capture 1–3 in one run once you have the workshop key.
