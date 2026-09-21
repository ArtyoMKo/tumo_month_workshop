# TUMO Lesson Plan Application — paste-ready answers

Workshop: **Study Buddy — Build an AI That Reads Your Notes**
Format: 8 days × 2 hours = 16 hours · Model: Claude Haiku 4.5 · Repo: https://github.com/ArtyoMKo/tumo_month_workshop

---

## Lab Title

```
AI Workshop: Build an AI That Reads Your Notes
```

## Center

*Your choice from the dropdown — presumably TUMO Yerevan.*

## Workshop Leader

```
Artyom Kosakyan
```

## Workshop dates

*Required — only you know these. 8 sessions over roughly one month.*

## Number of students

```
16
```

## Prerequisites

```
Students should have completed TUMO's Programming workshops and be comfortable with
JavaScript fundamentals: variables, conditionals, loops, functions, objects and events.

No Python experience is required. Python is introduced in Session 1 by direct comparison
with JavaScript, and the workshop is designed so that students who have never written a
line of Python can follow it.

No mathematics beyond school level is required. No prior AI or machine learning
experience is required.

Recommended age: 13-18.

One thing students must bring: from Session 2 onward, each student needs 3-10 of their
own text or markdown files - revision notes, a subject they are studying, rules of a game
they play, an exported wiki. These become the material their personal assistant learns.
A backup set is provided for students who forget.
```

## What are the learning objectives and goals?

```
The workshop teaches students to build a Retrieval-Augmented Generation (RAG) assistant -
the technique behind almost every "chat with your documents" product in use today - and
to understand every part of it rather than treating it as magic.

Concretely, the objectives are:

1. To understand what a large language model actually does, and why it invents confident,
   detailed, false answers. Students see this happen to their own material in Session 2
   before any solution is offered, so the rest of the workshop answers a problem they have
   personally experienced.

2. To teach the RAG pipeline as four understandable steps: split documents into chunks,
   turn each chunk into numbers that represent its meaning, find the chunks closest in
   meaning to a question, and place only those in the prompt.

3. To introduce Python to students who already program in JavaScript, by translation
   rather than from scratch, so that no session is lost to a language lecture.

4. To move students from experimenting in a Jupyter notebook to assembling a real,
   organised, runnable Python project in VS Code - the single most valuable transition in
   the workshop, and one most beginner courses never make.

5. To build the habit of measuring instead of assuming: writing test questions before
   changing settings, changing one thing at a time, and distinguishing "the search failed"
   from "the model failed" when an answer comes out wrong.

6. To show why professional code is written so that the AI provider can be changed in one
   line, and to have students prove it by switching providers themselves - including to a
   model running offline on their own laptop.

The underlying goal is a shift in how students relate to AI tools: from users who accept
whatever a chatbot says, to builders who know where an answer came from and can tell when
it was invented.
```

## What are the anticipated learning outcomes?

```
By the end of the 16 hours, every student will have:

A FINISHED, RUNNABLE PROJECT
A local Python project of their own, organised into five clearly named files
(main.py, config.py, ingest.py, retriever.py, assistant.py) plus a requirements file,
a README they wrote, and a folder of their own documents. It runs with two commands and
answers questions about material they chose themselves, citing which file each answer
came from.

A DEMONSTRABLE UNDERSTANDING OF GROUNDING
Every student must be able to show two things at the final showcase: a question their
assistant answers correctly from their own notes, and a question it correctly REFUSES to
answer because their notes do not cover it. Producing that refusal on demand is the proof
that they understood the technique rather than copied it.

SKILLS THEY CAN NAME AND REUSE
- Reading and writing Python: lists, dictionaries, functions, comprehensions, files
- Working in Jupyter notebooks and in VS Code, and knowing what each is for
- Setting up a Python environment, a virtual environment and a secrets file
- Using an API key safely and understanding why it is a password
- Splitting a working prototype into modules with one responsibility each
- Using a library through an abstraction instead of a single vendor's SDK
- Writing a README that lets someone else run their project

A WAY OF WORKING
Students will have written their own small test set and tuned the system against it
rather than against impressions; changed one parameter at a time; and diagnosed a wrong
answer by checking retrieval before blaming the prompt.

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
telling you which file each answer came from.

And when you ask it something your notes do not cover, it will say so instead of inventing
an answer. Getting a computer to admit it does not know is harder than it sounds, and it
is the most valuable thing you will build here.

You will learn how an AI turns words into numbers that capture their meaning, how to
search through those numbers to find exactly the right paragraph, and how to hand that
paragraph to an AI so it answers from your material instead of from its imagination. This
technique is called RAG, and it powers most of the "chat with your documents" tools
companies are building right now.

You will start by experimenting in a notebook and finish by building a real Python
project in VS Code - your own files, your own code, running on your own computer, which
you can keep and keep improving after the workshop ends.

You already know JavaScript. You do not need to know Python - we will translate it for
you in the first session. You do not need to be good at maths. You just need something
you want your AI to know about.

8 sessions. 2 hours each. You leave with an AI that knows what you know.
```

## Lesson 1: Day 1 — Setup and First Words

```
FOCUS: Get 16 machines working, translate JavaScript into Python, and make an AI model talk.

STEP BY STEP:
1. (10 min) Meet and greet. Who has built what before; what subject each student might
   want their assistant to know about.
2. (10 min) Demonstration of the finished project. I ask my own notes a question and get
   an answer with sources, then ask something outside them and it refuses. "That refusal
   is what we are really building."
3. (30 min) Environment setup: Python 3.12, VS Code with the Python and Jupyter
   extensions, a virtual environment, pip install, the .env file holding the API key, and
   selecting the notebook kernel. Students work in pairs; whoever finishes first helps a
   neighbour.
4. (20 min) Presentation: Python for people who already know JavaScript. A side-by-side
   table - assignment, f-strings vs template literals, dict vs object, list vs array,
   indentation vs braces, def vs function, list comprehensions vs .map and .filter.
5. (30 min) Hands-on in session1.ipynb: the translation exercises, then the first call to
   the AI model.
6. (15 min) System prompts. The same question asked three times with three different
   system prompts, producing three completely different personalities.
7. (5 min) Wrap-up and homework.

DELIVERABLE BY END OF DAY:
A working Python environment, and a notebook in which the student has written their own
ask(system_prompt, question) function and used it to give an AI three different
personalities.

HOMEWORK: bring 3-10 of your own documents (.txt or .md) to the next session.
```

## Lesson 2: Day 2 — The Lying Machine

```
FOCUS: Experience the problem - twice - before any solution is offered.

STEP BY STEP:
1. (10 min) Recap. Check everyone brought documents; distribute the backup set to those
   who did not.
2. (20 min) Presentation: what a language model actually does. It predicts what text comes
   next. It has no database and no internal sense of the difference between remembering
   and inventing. Why that produces confident fiction.
3. (20 min) Hands-on: ask the model about a set of documents describing a project that
   does not exist (invented for this workshop, so the model cannot possibly know it). It
   answers anyway, with specific numbers and dates, all fabricated. We collect the best
   inventions on the whiteboard, then repeat it on the students' own notes.
4. (20 min) Hands-on: the obvious fix. Read the whole document, paste it into the prompt,
   ask again. It works.
5. (5 min) Break.
6. (15 min) Presentation: why pasting everything does not scale. Tokens, the context
   window, cost per question, and the fact that a model given too much text gets worse,
   not just slower.
7. (25 min) Hands-on: measure it. Students compute token counts and the real cost of
   asking one question against a textbook, then a year of notes. They discover a whole
   textbook now fits in a modern context window - and that it still costs 75 dollars per
   100 questions, and still degrades the answer. "It fits" and "it is a good idea" are
   different questions.
8. (5 min) Wrap-up: state the goal for the next three sessions - "find the three
   paragraphs that matter, and send only those."

DELIVERABLE BY END OF DAY:
A notebook demonstrating the same question answered wrongly without context and correctly
with it, plus the student's own cost calculation showing why the simple fix cannot scale.
Students can explain in their own words what problem the rest of the workshop solves.
```

## Lesson 3: Day 3 — Cutting Text Into Pieces

```
FOCUS: Loading a folder of documents and splitting it sensibly - and discovering that how
you cut matters more than expected.

STEP BY STEP:
1. (10 min) Recap.
2. (15 min) Presentation: chunking. Why a chunk should contain one idea - big enough to
   make sense on its own, small enough that it is not mostly irrelevant.
3. (25 min) Hands-on: load the documents folder, inspect what a Document object is, and
   see that the filename travels with the text as metadata. Without that, the finished
   assistant could never cite a source.
4. (25 min) Hands-on: split the same documents at chunk sizes of 200, 500, 1000 and 4000,
   and READ the actual chunks from each. The judgement question: "if you were handed only
   this chunk and asked the question, could you answer?"
5. (5 min) Break.
6. (10 min) Presentation: the boundary problem. The sentence that answers the question got
   cut in half. Overlap, and why 10-20 percent is the usual answer.
7. (20 min) Hands-on: split with and without overlap, and find a boundary that would have
   lost an answer.
8. (10 min) Students choose the chunk settings for their own material and write down why.

DELIVERABLE BY END OF DAY:
Each student's own documents loaded and split, with chosen chunk size and overlap values
and a written one-sentence justification. "Because it was the default" is not accepted.
```

## Lesson 4: Day 4 — Meaning as Numbers

```
FOCUS: Embeddings - the conceptual centre of the workshop, and the part that feels like
magic until it does not.

STEP BY STEP:
1. (10 min) Recap.
2. (20 min) Presentation: embeddings without mathematics. Meaning as a position in space.
   I draw two axes on the whiteboard and students physically place words on it, then I
   reveal that the real model does the same thing with 384 axes it worked out for itself.
3. (25 min) Hands-on: embed single words and measure the similarity between pairs.
   Students predict each score before running it. They discover "balloon" and "airship"
   score high, "balloon" and "trombone" low - and that "hot" and "cold" score HIGH, because
   embeddings capture topic, not agreement. Then the key result: a question and its answer
   that share no words at all still score close together.
4. (5 min) Break.
5. (10 min) Presentation: what a vector store is. We use one that runs on the student's
   laptop; a company would use a hosted one; through our code that is a configuration
   change, not a rewrite.
6. (30 min) Hands-on: build a searchable vector store over their own documents and run
   real searches. No AI model involved yet - just search - so students can see clearly
   which half of the system does what.
7. (10 min) Hands-on: search for something the documents do NOT contain. It still returns
   results. This is the critical discovery that sets up Session 5.
8. (5 min) Optional: visualise the vectors in 2D, coloured by source file, and see the
   topics cluster on their own.
9. (5 min) Wrap-up.

DELIVERABLE BY END OF DAY:
A working search engine over the student's own documents, and three documented test cases
with their scores: a question answered well, a question where the right chunk ranks low,
and a question the documents cannot answer.
```

## Lesson 5: Day 5 — Closing the Loop

```
FOCUS: Everything connects. The assistant works for the first time - and learns to refuse.

STEP BY STEP:
1. (15 min) Recap: students whiteboard the entire pipeline from memory before opening
   anything.
2. (25 min) Hands-on: retrieve the relevant chunks, join them into a context string, and
   PRINT THE ACTUAL PROMPT being sent to the model. Reading it is the moment the technique
   stops being abstract - there is nothing hidden in it.
3. (20 min) Hands-on: write answer_question(), returning both the answer and the list of
   source files it used.
4. (5 min) Break.
5. (20 min) Hands-on: the refusal. Students discover that retrieval alone does not prevent
   invention - the search always returns something. Adding one sentence to the system
   prompt ("if the notes do not contain the answer, say so; do not guess") transforms the
   confident liar of Session 2 into something trustworthy. Every student must find a
   question their assistant correctly refuses.
6. (15 min) Hands-on: tune the number of retrieved chunks. At 1 it misses answers; at 20
   answers become vague and expensive. Understanding why is the point.
7. (15 min) Demonstration and hands-on: change the AI provider by editing ONE line, and
   watch everything else keep working - including switching to a model running on the
   laptop with the wifi physically switched off.
8. (5 min) Wrap-up: the notebook phase ends here.

DELIVERABLE BY END OF DAY:
A working RAG assistant in a notebook, answering questions about the student's own
documents with sources - and one documented question it correctly refuses to answer.
```

## Lesson 6: Day 6 — Out of the Notebook

```
FOCUS: The transition session. Nothing new is learned about AI; everything is reorganised
into a real project. This is the most valuable session in the workshop.

STEP BY STEP:
1. (10 min) Presentation: why we leave the notebook. A notebook is a lab bench. You do not
   hand someone your lab bench, you hand them the thing you built on it.
2. (20 min) Presentation: the two-program idea, on the whiteboard. The project splits into
   a SLOW program you run when your documents change, which builds and saves a search
   index, and a FAST program you run constantly, which reads that index and answers
   questions. Recognising that a system has a build step and a run step is a genuine piece
   of software design.
3. (15 min) Hands-on: create the project folder and config.py. Every constant from five
   notebooks moves into one file. Run it - it does nothing, and that is correct.
4. (25 min) Hands-on: write ingest.py - load, chunk, embed, save to disk. Run it and
   inspect the index folder it created.
5. (5 min) Break.
6. (20 min) Hands-on: write retriever.py, which opens the saved index and finds relevant
   chunks. Test it with no AI model involved at all.
7. (15 min) Hands-on: write assistant.py, holding the system prompt and the answering
   function.
8. (10 min) Hands-on: write main.py, the question loop. Run "python main.py" from the
   terminal for the first time.

DELIVERABLE BY END OF DAY:
Every student must leave with a working "python main.py" - a real program, running from
the terminal, with no notebook involved. I circulate to confirm this individually before
anyone goes home.
```

## Lesson 7: Day 7 — Your Own Material

```
FOCUS: RAG lives or dies on the documents. Students find this out for themselves, and
learn to diagnose which half of the system failed.

STEP BY STEP:
1. (10 min) Recap. Everyone confirms "python main.py" still runs before we change anything.
2. (15 min) Presentation: garbage in, garbage out. What a good document looks like -
   headings, short paragraphs, one topic per file. What a bad one looks like - a PDF
   exported as one unbroken wall of text.
3. (30 min) Hands-on: put your own documents in the documents folder, rebuild the index,
   and ask five questions you already know the answers to.
4. (15 min) Presentation: splitting the blame. When an answer is wrong there are two
   completely different causes with two different fixes. Ask, in this order: did the right
   chunk come back? Then: did the model use it? Never debug the second before checking the
   first. Students learn the /sources command, which shows exactly what was retrieved
   without calling the AI at all.
5. (5 min) Break.
6. (25 min) Hands-on: improve the documents - add headings, split a large file, delete
   noise - and rebuild. Measure whether the same five questions got better.
7. (15 min) Hands-on: each student picks one feature of their own and builds it - showing
   retrieval scores, a command that reports which file knows most about a topic, a
   conversation that remembers the previous question.
8. (5 min) Wrap-up.

DELIVERABLE BY END OF DAY:
An assistant running on the student's own real material, answering five known questions
correctly, plus one feature the student designed and implemented themselves. Students can
explain whether a given wrong answer was a search problem or a model problem.
```

## Lesson 8: Day 8 — Tune It and Ship It

```
FOCUS: Finishing is a skill. Measure, tune, document, present.

STEP BY STEP:
1. (10 min) Recap.
2. (15 min) Presentation: how would you know if you made it better? Write the test set
   FIRST, then tune against it, changing one thing at a time. This is the single most
   professionally valuable habit in the whole workshop.
3. (20 min) Hands-on: each student writes five questions with known answers and scores
   their assistant now, before changing anything. That is their baseline.
4. (25 min) Hands-on: tune. Change the number of retrieved chunks, or the chunk size, or
   the system prompt, or the AI model itself - swapping the cheap fast model for a more
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
- Python packages, installed from a provided requirements.txt file:
  langchain, langchain-anthropic, langchain-chroma, langchain-huggingface,
  langchain-text-splitters, sentence-transformers, chromadb, python-dotenv,
  jupyter, ipykernel, numpy
- An Anthropic API key (Claude), provided by TUMO under its existing contract.
  Students cannot create their own - API accounts require the holder to be 18+.
  One shared TUMO-owned key, with a spend limit set in the Anthropic Console.

IMPORTANT PREPARATION REQUEST FOR IT:
Please pre-install Python, VS Code and the two extensions on all machines, and pre-cache
the Python packages and the local embedding model BEFORE the first session. The embedding
model download is approximately 900 MB per machine; sixteen students downloading it
simultaneously over shared wifi would consume an entire session. The exact one-line
command to pre-cache it is documented in the workshop repository. With machines prepared
in advance, Session 1 setup takes 15 minutes instead of 40.

Optional, not required: Ollama, if we want to demonstrate running an AI model fully
offline in Session 5.
```

## What hardware will you require?

```
- 16 laptops or lab PCs (Windows, macOS or Linux - all three are supported and tested)
- Minimum 8 GB RAM per machine. The embedding model runs locally on the CPU.
- Approximately 3 GB of free disk space per machine, mostly for the Python packages
- Permission to install software, or machines prepared in advance by IT (preferred)
- Reliable internet access
- A projector or large display for the presentation blocks
- A whiteboard. It is used substantially - Session 4 has students physically place words
  on a drawn coordinate space to build intuition for embeddings, and Session 5 opens with
  students reconstructing the whole pipeline on it from memory.

NO GPU IS REQUIRED. Nothing in this workshop needs specialised hardware.

Note: if lab machines are reset or reimaged between sessions, the software preparation
must be reapplied and students must recreate their key file each time. Please confirm
this with IT before the workshop begins.
```

## What specific tools and materials will you require?

```
PROVIDED BY THE WORKSHOP LEADER (all prepared and publicly available at
https://github.com/ArtyoMKo/tumo_month_workshop):

- Five Jupyter notebooks, one per session for Sessions 1-5, with explanations,
  runnable code cells, exercises and extra challenges for faster students
- The complete final project (five documented Python modules, requirements.txt,
  .env.example, README) that students arrive at by Session 6
- check_setup.py, a diagnostic script that verifies a student's machine in eight steps
  and prints a specific fix for whichever one fails
- A sample document set describing an invented project, used in Session 2. It is
  fictional on purpose: because no AI model has ever seen it, students can prove that a
  correct answer came from their own retrieval rather than from the model's memory.
  It also serves as backup material for students who forget to bring their own.
- A setup guide and a teacher pre-flight checklist

REQUIRED FROM TUMO:
- One Anthropic API key with a spend limit set. Estimated total cost for a group of 16
  across the full 16 hours: approximately 7 US dollars. The embedding model runs locally
  and costs nothing, so students only pay for the final answer - roughly 0.14 cents per
  question.
- Machines prepared in advance as described in the software section

REQUIRED FROM STUDENTS:
- 3 to 10 of their own .txt or .md files, brought from Session 2 onward. This is the
  single most important material in the workshop: it is what makes every student's final
  project different from everyone else's.
```

## Visual references to upload

Suggested, in priority order:

1. A terminal screenshot of the finished assistant answering a question with `Sources:`
   listed underneath — this is the deliverable in one image.
2. A terminal screenshot of the assistant **refusing** ("That isn't in your documents.")
   — this is the pedagogical point in one image.
3. A screenshot of the finished VS Code project tree, showing the five modules.
4. The Session 4 t-SNE plot: coloured clusters of document chunks.
5. A screenshot of a Session 3 notebook cell comparing chunk sizes side by side.

Capture 1, 2 and 3 in one run once you have the workshop key.
