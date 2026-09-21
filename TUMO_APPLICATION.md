# TUMO Lesson Plan Application — paste-ready answers

Workshop: **AI Study Buddy — Build an AI That Reads Your Notes**
Format: 8 lessons × 2 hours = 16 hours · Model: Claude Haiku 4.5
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
*Required — only you know these. 8 lessons over roughly one month.*

## Number of students
```
16
```

## Prerequisites

```
Students should have basic Python experience from TUMO's other programming tracks:
variables, lists, dictionaries, conditionals, loops and functions. Python is NOT taught
in this workshop - students receive a cheatsheet in Lesson 1 for looking things up, and
the time saved is spent on AI content instead.

No prior AI or machine learning experience is required.
No mathematics beyond school level is required.

Recommended age: 13-18.

ONE THING STUDENTS MUST BRING: from Lesson 2 onward, each student needs 3-10 of their own
text or markdown files - revision notes, a subject they are studying, rules of a game they
play, an exported wiki. These become the material their personal assistant learns. Notes
in Armenian, English or a mix all work equally well; the workshop uses a multilingual
model specifically so that students are not restricted to English. A backup set is
provided for students who forget.
```

## What are the learning objectives and goals?

```
The workshop teaches students to build a Retrieval-Augmented Generation (RAG) assistant -
the technique behind almost every "chat with your documents" product in use today - and
to understand every part of it rather than treating it as magic.

Concretely:

1. To understand what a large language model actually does, and why it produces confident,
   detailed, false answers. Students see this happen to their own material in Lesson 2
   before any solution is offered, so the rest of the workshop answers a problem they have
   personally experienced.

2. To teach prompt engineering as a real skill with real limits. In Lesson 1 students make
   one model behave five different ways, force it to obey rules about length, language and
   format, and make it refuse questions - then try to break their own rules from the user
   message and discover prompt injection.

3. To teach the RAG pipeline as four understandable steps: split documents into chunks,
   turn each chunk into numbers representing its meaning, find the chunks closest in
   meaning to a question, and place only those in the prompt.

4. To move students from experimenting in a Jupyter notebook to assembling a real,
   organised, runnable Python project in VS Code - the single most valuable transition in
   the workshop, and one most beginner courses never make.

5. To build the habit of measuring instead of assuming: writing test questions before
   changing settings, changing one thing at a time, and distinguishing "the search failed"
   from "the model failed" when an answer is wrong.

6. To show why professional code is written so the AI provider can be changed in one line,
   and to have students prove it by switching providers themselves.

The underlying goal is a shift in how students relate to AI tools: from users who accept
whatever a chatbot says, to builders who know where an answer came from and can tell when
it was invented.
```

## What are the anticipated learning outcomes?

```
By the end of the 16 hours, every student will have:

A FINISHED, RUNNABLE PROJECT
A local Python project of their own, organised into five clearly named files
(main.py, config.py, ingest.py, retriever.py, assistant.py) plus a requirements file, a
README they wrote, and a folder of their own documents. It runs with two commands, holds
a conversation with follow-up questions, and answers from material they chose - citing
which file each answer came from.

A DEMONSTRABLE UNDERSTANDING OF GROUNDING
Every student must show two things at the final showcase: a question their assistant
answers correctly from their own notes, and a question it correctly REFUSES because their
notes do not cover it. Producing that refusal on demand is the proof they understood the
technique rather than copied it.

SKILLS THEY CAN NAME AND REUSE
- Prompt engineering: system prompts, constraining behaviour, and why it is not a guarantee
- Chunking, embeddings, semantic search and their trade-offs
- Multi-turn conversation: why a follow-up question breaks naive retrieval, and how to fix it
- Setting up a Python environment, a virtual environment and a secrets file
- Using an API key safely and understanding why it is a password
- Splitting a working prototype into modules with one responsibility each
- Using a library through an abstraction instead of a single vendor's SDK
- Writing a README that lets someone else run their project

A WAY OF WORKING
Students will have written their own small test set and tuned against it rather than
against impressions; changed one parameter at a time; and diagnosed a wrong answer by
checking retrieval before blaming the prompt.

Every student's project will be different, because every student chooses their own
documents. A student revising biology, a student documenting a video game, and a student
loading their own poetry all finish with the same architecture and completely different
assistants.
```

## Workshop announcement

```
BUILD AN AI THAT ACTUALLY READS YOUR NOTES

Ask any chatbot about your homework and it will answer confidently - and sometimes
completely make it up. It has never seen your notes. It is guessing, fluently.

In this workshop you will fix that. You will build your own AI assistant from scratch,
one that reads the documents YOU give it - your biology notes, your history chapter, the
rules of a game you play, whatever you choose - and answers questions about them properly,
telling you which file each answer came from. You can ask follow-up questions and it
remembers what you were talking about.

And when you ask it something your notes do not cover, it will say so instead of inventing
an answer. Getting a computer to admit it does not know is harder than it sounds, and it
is the most valuable thing you will build here.

You will learn how to write instructions that control how an AI behaves, how an AI turns
words into numbers that capture their meaning, how to search through those numbers to find
exactly the right paragraph, and how to hand that paragraph to an AI so it answers from
your material instead of its imagination. This technique is called RAG, and it powers most
of the "chat with your documents" tools companies are building right now.

Bring your notes in Armenian, English, or both - it works either way.

You will start by experimenting in a notebook and finish by building a real Python project
in VS Code - your own files, your own code, running on your own computer, which you can
keep and keep improving after the workshop ends.

You need basic Python. You do not need to be good at maths. You just need something you
want your AI to know about.

8 lessons. 2 hours each. You leave with an AI that knows what you know.
```

## Lesson 1: Day 1 — Setup and Your First AI Call

```
FOCUS: Get 16 machines working, then spend the rest of the lesson on the most powerful
thing a student controls all course - the system prompt.

STEP BY STEP:
1. (10 min) Meet and greet, and a demonstration of the finished assistant: it answers from
   my notes with sources, then refuses a question they do not cover. "That refusal is what
   we are really building."
2. (15 min) Presentation: what a language model actually does - it predicts text, it has no
   database, and no internal sense of "I don't know". What an API is, and why the key is a
   password.
3. (25 min) Environment setup: Python 3.12, VS Code with the Python and Jupyter extensions,
   a virtual environment, pip install, the .env file, and selecting the notebook kernel.
   The Python cheatsheet is handed out here.
4. (15 min) First call to Claude. Inspect what comes back - it is not a string - and look
   at the token counts that determine what everything costs.
5. (20 min) System prompts. The system message is written by the programmer and the user
   never sees it. One question, three system prompts, three completely different
   assistants.
6. (20 min) Making a model follow rules: constrain length, force a JSON format, make it
   answer in Armenian, and make it refuse off-topic questions. Then students try to break
   their own rules from the user message - this is prompt injection, and it is an unsolved
   problem security researchers are paid to work on.
7. (10 min) The one-line provider swap. The code names no AI company anywhere except one
   string; change it and everything else keeps working.
8. (5 min) Wrap-up and homework.

DELIVERABLE BY END OF DAY:
A working environment and a notebook containing the student's own ask() function plus at
least three system prompts producing measurably different behaviour - including one that
successfully forces a refusal.

HOMEWORK: bring 3-10 of your own documents (.txt or .md, any language) next lesson.
```

## Lesson 2: Day 2 — Why AI Makes Things Up

```
FOCUS: Experience the problem - twice - before any solution is offered.

STEP BY STEP:
1. (10 min) Recap. Check everyone brought documents; distribute the backup set.
2. (20 min) Presentation: why models invent things. A model predicts plausible text; from
   the inside, recalling and composing are the same operation. Hence confident fiction.
3. (20 min) Hands-on: ask the model about a project invented for this workshop, which no AI
   has ever seen. It answers anyway, with specific dates and numbers, all fabricated. Best
   inventions go on the whiteboard. Then students repeat it on their own notes.
4. (20 min) Hands-on: the obvious fix. Read the whole document, paste it into the prompt,
   ask again. It works.
5. (5 min) Break.
6. (15 min) Presentation: why pasting everything does not scale - tokens, context windows,
   cost per question, and the fact that too much context makes answers worse.
7. (25 min) Hands-on: measure it. Students compute the real cost of asking one question
   against a textbook, then a year of notes. They discover a whole textbook now FITS in a
   modern context window - and still costs 75 dollars per 100 questions and still degrades
   the answer. "It fits" and "it is a good idea" are different questions.
8. (5 min) Wrap-up: state the goal of the next three lessons - "find the three paragraphs
   that matter, and send only those."

DELIVERABLE BY END OF DAY:
A notebook demonstrating the same question answered wrongly without context and correctly
with it, plus the student's own cost calculation. Students can state, unprompted, the
problem the rest of the workshop solves.
```

## Lesson 3: Day 3 — Preparing Documents: Chunking

```
FOCUS: Loading documents and splitting them sensibly - and discovering that how you cut
matters more than expected.

STEP BY STEP:
1. (10 min) Recap.
2. (15 min) Presentation: what a chunk should be - one idea. Big enough to stand alone,
   small enough to be mostly about one thing.
3. (20 min) Hands-on: load the documents folder and inspect a Document object - text plus
   metadata. The filename travels with the text all the way to the final answer, which is
   what makes citing a source possible at the end.
4. (25 min) Hands-on: split the same documents at 200, 500, 1000 and 4000 characters and
   READ actual chunks from each. The judgement question: "handed only this chunk, could you
   answer the question?"
5. (5 min) Break.
6. (10 min) Presentation: the boundary problem - the sentence that answers the question got
   cut in half. Overlap, and why 10-20 percent is the usual answer.
7. (15 min) Hands-on: split with and without overlap, and find a boundary that would have
   lost an answer.
8. (15 min) Hands-on: splitting on structure instead of length. A markdown-header splitter
   keeps each section whole and records its heading in the metadata. Compare both
   approaches on your own notes.
9. (5 min) Choose your settings and write down why.

DELIVERABLE BY END OF DAY:
Each student's own documents loaded and split, with chosen chunk size and overlap values
and a written one-sentence justification. "Because it was the default" is not accepted.
```

## Lesson 4: Day 4 — Embeddings and Semantic Search

```
FOCUS: The conceptual centre of the workshop - teaching a computer what words mean.

STEP BY STEP:
1. (10 min) Recap.
2. (20 min) Presentation: embeddings without mathematics. Meaning as a position in space.
   I draw two axes on the whiteboard and students physically place words on it, then I
   reveal that the real model does the same thing with 384 axes it worked out for itself.
3. (20 min) Hands-on: embed single words and measure similarity between pairs. Students
   predict every score before running it. They discover that "hot" and "cold" score HIGH,
   because embeddings capture topic, not agreement.
4. (15 min) Hands-on: the key result. A question and its answer that share not one content
   word still score close together, while an on-topic distractor scores far away - a word
   search would score that at zero. Then the same thing across languages: a question asked
   in Armenian finds the correct answer written in English. Not one character is shared,
   not even the alphabet.
5. (5 min) Break.
6. (10 min) Presentation: what a vector store is. Ours runs on the student's laptop; a
   company would use a hosted one; in our code that is a configuration change.
7. (25 min) Hands-on: build a searchable vector store over their own documents and run real
   searches. No AI model involved yet - just search - so students see clearly which half of
   the system does what.
8. (15 min) Hands-on: search for something the documents do NOT contain. It still returns
   results - the critical discovery that sets up Lesson 5. Then filtering by metadata, to
   search only one source file.

DELIVERABLE BY END OF DAY:
A working search engine over the student's own documents, and three documented test cases
with their scores: a question answered well, a question where the right chunk ranks low,
and a question the documents cannot answer.
```

## Lesson 5: Day 5 — Building the RAG Assistant

```
FOCUS: Everything connects. The assistant works for the first time, learns to refuse, and
learns to remember.

STEP BY STEP:
1. (10 min) Recap: students whiteboard the entire pipeline from memory before opening
   anything.
2. (25 min) Hands-on: retrieve the relevant chunks, join them into a context string, and
   PRINT THE ACTUAL PROMPT being sent. Reading it is the moment the technique stops being
   abstract - there is nothing hidden in it.
3. (20 min) Hands-on: write the answering function, returning both the answer and the list
   of source files it used.
4. (5 min) Break.
5. (20 min) Hands-on: the refusal. Students discover retrieval alone does not prevent
   invention, because the search always returns something. One sentence added to the system
   prompt transforms the confident liar of Lesson 2 into something trustworthy. Every
   student must find a question their assistant correctly refuses.
6. (15 min) Hands-on: tune how many chunks are retrieved. At 1 it misses answers; at 20
   answers become vague and expensive. Understanding why is the point.
7. (20 min) Hands-on: conversation memory. Students ask a follow-up question and watch it
   fail, then fix it - twice, because there are two separate problems. The model needs the
   earlier turns replayed so it knows what "them" refers to, and the SEARCH needs the
   earlier questions too, because "which of them is cheaper?" on its own is about nothing.
8. (5 min) Wrap-up: the notebook phase ends here.

DELIVERABLE BY END OF DAY:
A working RAG assistant answering questions about the student's own documents with sources,
handling at least one follow-up question that depends on the previous one, and correctly
refusing one documented question.
```

## Lesson 6: Day 6 — From Notebook to Python Project

```
FOCUS: The transition lesson. Nothing new is learned about AI; everything is reorganised
into a real project. This is the most valuable lesson in the workshop.

STEP BY STEP:
1. (10 min) Presentation: why we leave the notebook. A notebook is a lab bench. You do not
   hand someone your lab bench, you hand them the thing you built on it.
2. (20 min) Presentation: the two-program idea, on the whiteboard. The project splits into
   a SLOW program run when documents change, which builds and saves a search index, and a
   FAST program run constantly, which reads that index and answers questions. Recognising
   that a system has a build step and a run step is a genuine piece of software design.
3. (15 min) Hands-on: create the project folder and config.py. Every constant from five
   notebooks moves into one file. Run it - it does nothing, and that is correct.
4. (25 min) Hands-on: write ingest.py - load, chunk, embed, save to disk. Run it and inspect
   the index folder it created.
5. (5 min) Break.
6. (20 min) Hands-on: write retriever.py, which opens the saved index and finds relevant
   chunks. Test it with no AI model involved at all.
7. (15 min) Hands-on: write assistant.py, holding the system prompt, the conversation
   history handling, and the answering function.
8. (10 min) Hands-on: write main.py, the question loop. Run "python main.py" from the
   terminal for the first time.

DELIVERABLE BY END OF DAY:
Every student must leave with a working "python main.py" - a real program, running from the
terminal, with no notebook involved. I confirm this individually before anyone goes home.
```

## Lesson 7: Day 7 — Your Own Knowledge Base

```
FOCUS: RAG lives or dies on the documents. Students find this out for themselves, and learn
to diagnose which half of the system failed.

STEP BY STEP:
1. (10 min) Recap. Everyone confirms "python main.py" still runs before we change anything.
2. (15 min) Presentation: garbage in, garbage out. What a good document looks like -
   headings, short paragraphs, one topic per file. What a bad one looks like: a PDF exported
   as one unbroken wall of text.
3. (30 min) Hands-on: put your own documents in the documents folder, rebuild the index, and
   ask five questions you already know the answers to.
4. (15 min) Presentation: splitting the blame. When an answer is wrong there are two
   completely different causes with two different fixes. Ask, in this order: did the right
   chunk come back? Then: did the model use it? Never debug the second before checking the
   first. Students use the /sources command, which shows exactly what was retrieved without
   calling the AI at all.
5. (5 min) Break.
6. (25 min) Hands-on: improve the documents - add headings, split a large file, delete noise
   - and rebuild. Measure whether the same five questions got better.
7. (15 min) Hands-on: each student builds one feature of their own - showing retrieval
   scores, a command reporting which file knows most about a topic, filtering by source
   file, or remembering more conversation turns.
8. (5 min) Wrap-up.

DELIVERABLE BY END OF DAY:
An assistant running on the student's own real material, answering five known questions
correctly, plus one feature the student designed and implemented themselves. Students can
explain whether a given wrong answer was a search problem or a model problem.
```

## Lesson 8: Day 8 — Testing, Tuning and Final Demo

```
FOCUS: Finishing is a skill. Measure, tune, document, present.

STEP BY STEP:
1. (10 min) Recap.
2. (15 min) Presentation: how would you know if you made it better? Write the test set
   FIRST, then tune against it, changing one thing at a time. This is the single most
   professionally valuable habit in the whole workshop.
3. (20 min) Hands-on: each student writes five questions with known answers and scores their
   assistant now, before changing anything. That is their baseline.
4. (25 min) Hands-on: tune. Change the number of retrieved chunks, or the chunk size, or the
   system prompt, or the AI model itself - swapping the cheap fast model for a more
   expensive smarter one. One change at a time, re-scoring after each. Students find out
   whether paying more actually wins, which is often surprising.
5. (5 min) Break.
6. (20 min) Hands-on: finish the project. Write the README, produce the requirements file,
   confirm the secret key file is not in anything they would share. Then the fresh-machine
   test: swap folders with a partner and try to run their project following only their
   README. This finds more real problems than any amount of code review.
7. (20 min) SHOWCASE. Each student gets about 90 seconds: what your assistant knows about,
   one good answer, one question it correctly refuses, and one thing that broke along the
   way.
8. (5 min) Wrap-up: where to go next.

DELIVERABLE BY END OF DAY:
A finished, documented, runnable project that a classmate has successfully run from the
README alone; a written test set with before-and-after scores proving the student measured
their own tuning; and a live demonstration including one correct refusal.
```

## What software will you require?

```
All free and open-source except the AI service itself. Everything runs locally on the
student's machine - no cloud platform, no server, no deployment.

- Python 3.12 (python.org)
- Visual Studio Code, with the Microsoft "Python" and "Jupyter" extensions
  (PyCharm Community Edition is an acceptable alternative)
- Jupyter Notebook - installed via pip as part of the project requirements
- Python packages, installed from a provided requirements.txt:
  langchain, langchain-anthropic, langchain-chroma, langchain-huggingface,
  langchain-text-splitters, sentence-transformers, chromadb, python-dotenv,
  jupyter, ipykernel, numpy
- An Anthropic API key (Claude), provided by TUMO under its existing contract.
  Students cannot create their own - API accounts require the holder to be 18+.
  One shared TUMO-owned key, with a spend limit set in the Anthropic Console.

IMPORTANT PREPARATION REQUEST FOR IT:
Please pre-install Python, VS Code and the two extensions on all machines, and pre-cache
the Python packages and the local embedding model BEFORE the first lesson. The embedding
model plus its libraries is roughly 1.5 GB per machine; sixteen students downloading that
simultaneously over shared wifi would consume an entire lesson. The exact one-line command
is documented in the workshop repository. With machines prepared in advance, Lesson 1
setup takes 15 minutes instead of 40.

Optional, not required: Ollama, to demonstrate running an AI model fully offline.
```

## What hardware will you require?

```
- 16 laptops or lab PCs (Windows, macOS or Linux - all three are supported and tested)
- Minimum 8 GB RAM per machine. The embedding model runs locally on the CPU.
- Approximately 3 GB free disk space per machine, mostly for the Python libraries
- Permission to install software, or machines prepared in advance by IT (preferred)
- Reliable internet access
- A projector or large display for the presentation blocks
- A whiteboard. It is used substantially - in Lesson 4 students physically place words on a
  drawn coordinate space to build intuition for embeddings, and Lesson 5 opens with
  students reconstructing the whole pipeline on it from memory.

NO GPU IS REQUIRED. Nothing in this workshop needs specialised hardware.

Note: if lab machines are reset or reimaged between lessons, the software preparation must
be reapplied and students must recreate their key file each time. Please confirm this with
IT before the workshop begins.
```

## What specific tools and materials will you require?

```
PROVIDED BY THE WORKSHOP LEADER (all prepared and publicly available at
https://github.com/ArtyoMKo/tumo_month_workshop):

- Five Jupyter notebooks, one per lesson for Lessons 1-5, with explanations, runnable code
  cells, exercises and extra challenges for faster students
- Three student guides for Lessons 6-8, when students move out of notebooks and into a
  real Python project in VS Code. Step-by-step build instructions with a check after each
  file, a decision tree for diagnosing wrong answers, and fill-in templates for the test
  set, the tuning log and the README
- A Python cheatsheet handed out in Lesson 1, as a runnable Jupyter notebook - a
  JavaScript-to-Python translation table, the syntax this project uses, how to read an
  error message, and notebook/terminal survival. Every cell runs and can be edited, and it
  needs no API key or internet, so students who finish setup early have something useful to
  do. It is a lookup reference and is never lectured from.
- The complete final project (five documented Python modules, requirements.txt,
  .env.example, README) that students arrive at by Lesson 6
- check_setup.py, a diagnostic script that verifies a student's machine in eight steps and
  prints a specific fix for whichever one fails
- A sample document set describing an invented project, used in Lesson 2. It is fictional
  on purpose: because no AI model has ever seen it, students can prove a correct answer
  came from their own retrieval rather than the model's memory. It also serves as backup
  material for students who forget to bring their own.
- A setup guide and a teacher pre-flight checklist

REQUIRED FROM TUMO:
- One Anthropic API key with a spend limit set. Estimated total cost for a group of 16
  across the full 16 hours: approximately 7 US dollars. The embedding model runs locally
  and costs nothing, so students only pay for the final answer - roughly 0.14 cents per
  question.
- Machines prepared in advance as described in the software section

REQUIRED FROM STUDENTS:
- 3 to 10 of their own .txt or .md files, brought from Lesson 2 onward, in any language.
  This is the most important material in the workshop: it is what makes every student's
  final project different from everyone else's.
```

## Visual references to upload

Suggested, in priority order:

1. Terminal screenshot of the assistant answering with `Sources:` listed — the deliverable in one image.
2. Terminal screenshot of the assistant **refusing** ("That isn't in your documents.") — the pedagogical point in one image.
3. A short follow-up-question exchange, showing it remembers context.
4. The finished VS Code project tree with the five modules.
5. A Lesson 4 screenshot showing an Armenian question matching an English note.

Capture 1–3 in one run once you have the workshop key.
