# Workshop Outline — AI Image Studio

> ⚠️ **NOT SCHEDULED — reference material only.**
>
> The taught track is **Course B — Study Buddy**. This course is kept for reference and is
> complete and working, but it **cannot run on Anthropic**: there is no Claude
> image-generation model, so it needs an OpenAI or Google key and a separate contract.
> See the top-level `README.md`.

**Track:** Light · **Duration:** 16 hours (8 sessions x 2 hours) · **Ages:** 13-18 · **Group size:** 16

---

## 1. Idea

Students build their own **AI image studio**: a small Python program where you type a
description in plain language and get back a picture that has never existed before.

They start from the smallest possible thing that works — one API call in a notebook that
returns one image — and grow it, one session at a time, into a real program: a studio with
named style presets, adjustable size and quality, a gallery folder that saves every image
with a sensible filename, and an optional "prompt assistant" that rewrites a lazy prompt
into a vivid one before sending it.

The engineering idea underneath the fun one is **not being locked in**. The image model is
reached through LangChain rather than through one company's SDK, and the choice of provider
lives on a single line in `config.py`. Students physically change that line and watch the
same program keep working against a different company's model. That's the moment the
abstraction stops being a word and becomes a thing they did.

Students already know JavaScript from TUMO's Programming workshops. Python is introduced by
comparison — a recurring "Coming from JavaScript?" sidebar maps each new piece of syntax
onto something they already have in their head, so no session is spent on a Python lecture.

## 2. New skills developed

**AI & API skills**
- What an API key is, why it is a password, and how to keep it out of your code
- Sending a prompt to a model and reading a structured response back
- Handling **binary data** — an image arrives as base64 text, not as a picture, and has to
  be decoded, displayed and written to disk
- Prompt design: why "a cat" and "a ginger cat asleep on a radiator, soft evening light,
  shot on 35mm film" produce completely different results
- Model parameters (size, quality, style) and what each one costs you in time and money
- Using one model to improve the input to another model

**Python & software skills**
- Python syntax for people who already know JavaScript
- Variables, f-strings, lists, dictionaries, functions with default arguments
- Reading and writing files; working with paths and folders
- Refactoring: taking code that works in a notebook and reorganising it into modules
- Designing a function's signature so other code can use it without knowing its insides
- Writing a `requirements.txt`, a `.env`, and a README so someone else can run your project

**Habits**
- Reading an error message from the bottom up
- Changing one thing at a time
- Committing to a small working version before making it bigger

## 3. Software / hardware / materials required

**Per student**
- A laptop or lab PC (Windows, Mac or Linux), with permission to install software
- **Python 3.12**
- **VS Code** with the Microsoft **Python** and **Jupyter** extensions (PyCharm works too)
- Internet access
- An API key, supplied by TUMO (see `TEACHER_NOTES.md` — students cannot create their own)

**Provided by the workshop**
- `requirements.txt` (LangChain, langchain-openai, python-dotenv, Pillow, jupyter)
- `.env.example`
- Five session notebooks
- `check_setup.py`

**Preparation before Session 1** — see `TEACHER_NOTES.md`. If machines are prepared in
advance, setup takes 15 minutes. From scratch it takes 40-50 and eats into the first
hands-on block.

**No GPU, no server, no cloud account, no deployment.** Everything runs locally, and the
only thing that happens over the network is the API call itself.

## 4. Outcome — the final deliverable

A **runnable local Python project**, in the student's own folder, with this structure:

```
image_studio/
├── main.py            # the entry point: ask for a prompt, generate, save, report
├── config.py          # every setting in one place, including the provider
├── client.py          # generate_image() — the provider-agnostic layer
├── prompts.py         # style presets and the prompt builder
├── gallery.py         # saving images with sensible filenames
├── requirements.txt
├── .env.example
├── check_setup.py
└── README.md
```

Run it with `python main.py`, type a description, and a new image appears in `gallery/`.

**Every student must add at least one customisation of their own** — a new style preset, a
`--random` flag, a batch mode that makes four variations, a black-and-white post-process, a
naming scheme, a menu. They present it in Session 8 and write it up in their README.

**Reference example of the finished thing:** a student types
`a lighthouse in a storm, dramatic, painterly`, picks the `cinematic` preset and `square`
size, and gets `gallery/2026-03-14_lighthouse-in-a-storm_cinematic.png` on their disk
plus a one-line summary in the terminal telling them which model made it and what it cost.
