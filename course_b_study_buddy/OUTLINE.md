# Workshop Outline — AI Study Buddy

**Duration:** 16 hours (8 lessons × 2 hours) · **Ages:** 13-18 · **Group size:** 16

---

## 1. Idea

Every student builds an AI assistant that has actually read *their own material* — their
biology notes, a history chapter, the rules of a game they play, lyrics, a fan wiki they
exported, whatever they choose — and answers questions about it with quotes and sources
instead of confidently making things up.

The technique is called **RAG** (Retrieval-Augmented Generation), and it is the single most
widely deployed AI technique in industry right now. It's also, once you take it apart,
surprisingly understandable: cut documents into pieces, turn each piece into a list of
numbers that captures its meaning, find the pieces closest in meaning to the question, and
paste those pieces into the prompt before asking.

The course is built around **feeling the problem before being given the solution**. Lesson
2 asks a model about a student's notes and it invents an answer — confidently, fluently and
wrongly. Lesson 2 then tries the obvious fix, pasting the whole document in, and that
breaks too, for reasons students can measure themselves. Only then does chunking, and
embedding, and retrieval, arrive — each one as an answer to a problem they already have.

The assistant answers with **GPT-5.4 mini**, OpenAI's fast, cheap current model — and
that is a deliberate teaching point rather than a budget compromise. In RAG the model isn't
doing the hard part: retrieval has already found the answer and put it in front of it, so
the job is to read four paragraphs and write four sentences without inventing anything.
Lesson 8 has students test that claim by swapping to a pricier model and scoring both
against their own questions.

Everything runs through LangChain, so the model, the embeddings and the vector store are
each swappable on one line — moving to a hosted vector database later is a change of
configuration, not a rewrite. It also demonstrates something useful: OpenAI's embeddings are
strong in English but weak in Armenian, which students measure for themselves in Lesson 4 —
a concrete reason why being able to swap one piece without touching the rest matters.

Students arrive with basic Python from other TUMO tracks, so Python is **not taught**
here. They receive `PYTHON_CHEATSHEET.ipynb` in Lesson 1 - a JavaScript↔Python translation
table, the syntax this project uses, and how to read an error - for lookup, never
lectured from. The hour that saves is spent on prompt engineering in Lesson 1 and
conversation memory in Lesson 5, both of which make the finished assistant better.

## 2. New skills developed

**AI & retrieval skills**
- Why a language model confidently invents things, and what "grounding" means
- Context windows: why "just paste in the whole textbook" is not the answer
- **Chunking** — splitting text so that each piece is self-contained, and what overlap is for
- **Embeddings** — text as coordinates in meaning-space; why "car" sits near "vehicle"
- Similarity search, and what the `k` in "top k results" actually controls
- Assembling retrieved context into a prompt, and system prompts that forbid guessing
- Judging a RAG system: was the right chunk retrieved, *and* was the answer grounded in it?

**Python & software skills**
- Applying existing Python to a real project (syntax is looked up, not taught)
- Writing functions with default arguments, and the mutable-default-argument trap
- Reading a folder of files; working with paths
- Using a library through an abstraction rather than a vendor's own SDK
- Refactoring notebook code into modules with one clear responsibility each
- A two-step program: an ingest step you run when documents change, and an ask step you run constantly
- `requirements.txt`, `.env`, README

**Habits**
- Measuring rather than assuming ("is retrieval working?" is a testable question)
- Changing one parameter at a time
- Distrusting a fluent answer until you've seen where it came from

## 3. Software / hardware / materials required

**Per student**
- A macOS laptop (TUMO lab machine)
- **8 GB RAM** and ~1 GB free disk — both AI models run on someone else's servers, so there is nothing large to install
- **Python 3.12** and **VS Code** + Python/Jupyter extensions — installed by TUMO IT in advance
- A personal directory on TUMO shared storage — students may change laptops between lessons. Note it is readable by everyone, so students are asked to bring general-subject notes only.
- `PYTHON_CHEATSHEET.ipynb`, provided - a lookup reference, not homework
- An **OpenAI API key**, supplied by TUMO (students cannot create their own - see `docs/TEACHER_NOTES.md`)
- **Their own documents** — 3 to 10 text or markdown files. Students should be told to bring
  these from Lesson 2 onward. Have a backup set ready; some will forget.

**Provided by the workshop**
- `requirements.txt` (LangChain, langchain-openai, langchain-chroma, langchain-text-splitters, chromadb, python-dotenv, jupyter)
- A sample knowledge base, so nobody is blocked on not having material
- Five lesson notebooks (Lessons 1-5) and three student guides (Lessons 6-8)
- `check_setup.py`

**⚠️ Preparation before Lesson 1 — this one is not optional.** Packages installed on every
machine and one run of `check_setup.py` with the real key, the day before — details in
`docs/TEACHER_NOTES.md`.

**No GPU, no hosted vector database, no server, no deployment.** The vector store runs on
the student's own laptop; the only network calls are to OpenAI, for embeddings and answers —
and both can be switched to local models with Ollama.

## 4. Outcome — the final deliverable

A **runnable local Python project**, in the student's own folder, with this structure:

```
study_buddy/
├── main.py            # the entry point: ask questions in a loop
├── config.py          # every setting in one place, including the provider
├── ingest.py          # read documents → chunk → embed → store. Run when documents change
├── retriever.py       # find the chunks most relevant to a question
├── assistant.py       # assemble context into a prompt and get a grounded answer
├── documents/         # the student's own material
├── vector_db/         # the built index (generated, not written by hand)
├── requirements.txt
├── .env.example
├── check_setup.py
└── README.md
```

Two commands: `python ingest.py` once to build the index, then `python main.py` to ask
questions about material the student chose themselves.

**Every student must show that it's grounded.** The assistant prints the sources it used
under each answer, and every student must find and demonstrate one question their assistant
correctly **refuses** to answer because the documents don't cover it. That refusal is the
whole point of the technique, and being able to produce one on demand is the proof they
understood it.

**Reference example of the finished thing:** a student loads their biology revision notes,
asks *"what's the difference between mitosis and meiosis?"*, and gets a four-line answer
followed by `Sources: cell_division.md, exam_notes.md`. Then they ask *"who won the 2018
World Cup?"* and get *"That isn't in your documents."*
