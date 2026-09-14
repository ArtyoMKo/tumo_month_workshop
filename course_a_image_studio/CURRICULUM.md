# Curriculum — AI Image Studio

**8 sessions x 120 minutes = 960 minutes = 16 hours exactly.**

Every agenda below sums to 120. The grand total is checked at the bottom.

| # | Session name | Phase | Minutes |
|---|---|---|---|
| 1 | First Contact | Notebook | 120 |
| 2 | Python for JavaScript People | Notebook | 120 |
| 3 | Turning the Dials | Notebook | 120 |
| 4 | Building a Gallery | Notebook | 120 |
| 5 | A Model That Helps You Prompt | Notebook | 120 |
| 6 | Out of the Notebook | **Transition** | 120 |
| 7 | Make It Yours | Project | 120 |
| 8 | Ship It | Project | 120 |
| | | **Total** | **960 min = 16 h** |

---

## Session 1 — First Contact

**Concepts:** what a generative model is · APIs and API keys · prompts · why an image
arrives as text · notebooks as a way of thinking

**Tools & Skills:** Python + VS Code + Jupyter setup · virtual environments · `.env` files ·
running a notebook cell · reading your first error message

The goal of this session is one image on the screen and nothing more. Students meet the
tools, get the environment working, and make a single API call that returns a picture. We
deliberately do not explain how any of it works yet — the reference course's move of
*run it first, name it afterwards*. Ending the session with a picture they described is
what buys attention for the next seven sessions.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet. Who's here, what they've built before, what they want to make | 10 |
| 2 | **Presentation:** demo of the finished project. Instructor types a prompt live, an image appears. "In 8 sessions this is yours, and you'll have written every line" | 10 |
| 3 | **Presentation:** how an AI image model works, at the right altitude — it saw millions of image+caption pairs; it is not searching the internet for your picture; it is making one. Plus: what an API is, and why the key is a password | 15 |
| 4 | **Hands-on:** environment setup — Python, VS Code extensions, venv, `pip install -r requirements.txt`, `.env`, select the kernel. Students pair up; whoever finishes first helps a neighbour | 35 |
| 5 | **Hands-on:** open `session1.ipynb`, run the diagnostic cell, make one image, save it | 30 |
| 6 | **Hands-on:** change the prompt. Make three more. Notice that the same prompt gives a different image each time | 10 |
| 7 | Wrap-up: everyone shows one image. Reminder to keep the `.env` file | 10 |
| | **Total** | **120** |

> If machines were prepared in advance, activity 4 drops to 15 minutes; move the spare
> 20 into activity 6. If students install from scratch, activity 4 may run to 50 and
> activity 6 is the first thing to sacrifice.

---

## Session 2 — Python for JavaScript People

**Concepts:** variables and types · strings and f-strings · lists and dictionaries ·
functions and default arguments · what "the same idea, different spelling" means

**Tools & Skills:** reading Python fluently · writing a reusable function · inspecting an
object in a notebook cell · the difference between defining and calling

Students know JavaScript well, so this is a **translation** session, not a programming-from-
zero session. Every concept is introduced as "you already have this, here is where it moved
to". The session's payoff is that the messy cell from Session 1 becomes one clean function,
`make_image(prompt)`, which they call over and over — the same move the reference course
makes when a scratch cell becomes `summarize(url)`.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap: what happened last time, show the best images | 10 |
| 2 | **Presentation:** Python vs JavaScript, side by side — `let`/`const` vs plain assignment, `${}` vs f-strings, `{}` object vs `dict`, `[]` array vs `list`, braces vs indentation, `function` vs `def` | 20 |
| 3 | **Hands-on:** `session2.ipynb` part A — the translation exercises. Short cells, run and inspect | 25 |
| 4 | Break / regroup | 5 |
| 5 | **Presentation:** what a function is *for* — hiding the boring part so the interesting part reads well. Default arguments, and why `make_image(prompt, size="square")` is friendlier than five positional arguments | 15 |
| 6 | **Hands-on:** part B — wrap Session 1's code into `make_image(prompt)`, then call it five times with five prompts | 30 |
| 7 | **Try it yourself:** write `make_avatar(name)` that builds its own prompt from a name and calls `make_image` | 10 |
| 8 | Wrap-up + preview of parameters | 5 |
| | **Total** | **120** |

---

## Session 3 — Turning the Dials

**Concepts:** model parameters · prompt design · style as reusable text · quality vs cost ·
one change at a time

**Tools & Skills:** dictionaries as lookup tables · keyword arguments · building strings
from parts · running controlled comparisons

This is the session where students discover that the prompt is the interface. They run
the same subject through several styles, the same style at several sizes, and learn to
change exactly one thing between runs so the comparison means something. Style presets are
introduced as a dictionary — which is also, quietly, the first time they store data
separately from code.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** anatomy of a good prompt — subject, detail, style, lighting, medium. Live side-by-side of "a cat" vs a full prompt | 20 |
| 3 | **Hands-on:** `session3.ipynb` part A — prompt ladder. Take one subject, add one detail at a time, keep every result | 25 |
| 4 | Break | 5 |
| 5 | **Presentation:** parameters — `size`, `quality`. What each costs in seconds and cents. Why `quality="low"` is the right default while you're experimenting | 10 |
| 6 | **Hands-on:** part B — the `STYLES` dictionary. Add your own preset, and generate the same subject in three styles | 30 |
| 7 | **Try it yourself:** find a prompt where two styles produce almost the same image, and one where they produce wildly different ones. Why? | 15 |
| 8 | Wrap-up: vote on the group's favourite style preset | 5 |
| | **Total** | **120** |

---

## Session 4 — Building a Gallery

**Concepts:** binary data vs text · files and folders · filenames as metadata · loops over
a list of prompts

**Tools & Skills:** `pathlib` · writing bytes to disk · string cleaning · `for` loops ·
timestamps

Until now images have lived in the notebook's output and vanished on restart. This session
makes them permanent. Students write a `save_image` function that turns a prompt into a
safe, informative filename and drops the file into `gallery/`. It's the least glamorous
session and the one that makes the project feel real, because now there's a folder they
can show people.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** why a picture is bytes, why base64 exists, and what "decode" means. The chain: model → base64 text → bytes → file on disk / picture on screen | 15 |
| 3 | **Hands-on:** `session4.ipynb` part A — decode by hand, look at the raw bytes, write one file, open it in the file browser | 20 |
| 4 | **Presentation:** filenames that tell you something. Dates, slugs, and why `image1.png`, `image2.png`, `image_final.png`, `image_final_REAL.png` is a trap everyone falls into once | 10 |
| 5 | Break | 5 |
| 6 | **Hands-on:** part B — write `save_image(image_bytes, prompt, style)` producing `2026-03-14_lighthouse-in-a-storm_cinematic.png` | 30 |
| 7 | **Hands-on:** part C — a `for` loop over a list of prompts that fills the gallery. **Cost warning delivered before this cell, not after** | 20 |
| 8 | Wrap-up: open the gallery folder, look at 16 students' worth of images | 10 |
| | **Total** | **120** |

---

## Session 5 — A Model That Helps You Prompt

**Concepts:** text models vs image models · system prompts · chaining one model into
another · provider-agnostic code · what an abstraction can and cannot hide

**Tools & Skills:** `init_chat_model` · `SystemMessage` / `HumanMessage` · swapping
providers with one line · running a local model with Ollama (demo)

The conceptual peak of the course. Students add a second model — a text model — whose only
job is to rewrite a lazy prompt into a vivid one before it reaches the image model. Because
that text model is created through `init_chat_model`, they can swap it to Anthropic, to
Google, or to a model running on the laptop with no internet, by editing one string. They
then discover that the *image* half will **not** swap to Ollama, and we talk about why —
abstractions unify things that are actually similar, and lie if you push them further.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** two kinds of model, one interface. What a system prompt is and why it's separate from the user's message | 15 |
| 3 | **Hands-on:** `session5.ipynb` part A — first text-model call, then `improve_prompt(rough_prompt)` | 30 |
| 4 | Break | 5 |
| 5 | **Hands-on:** part B — generate the same subject with and without the improver. Is it better? Sometimes it isn't — say so | 20 |
| 6 | **Presentation + demo:** the one-line provider swap. Instructor changes `CHAT_MODEL` to `ollama:llama3.2` live and it keeps working with the wifi off. Then tries the same trick on the image model and it fails — discuss | 20 |
| 7 | **Try it yourself:** change `CHAT_MODEL` yourself and re-run. Write down what changed in the output | 15 |
| 8 | Wrap-up: **the notebook phase ends here.** Preview of what a real project looks like | 5 |
| | **Total** | **120** |

---

## Session 6 — Out of the Notebook  ⟵ *transition session*

**Concepts:** modules · imports · entry points · separation of concerns · why notebooks are
for thinking and files are for keeping

**Tools & Skills:** VS Code outside the notebook · creating a package folder · `import` ·
`if __name__ == "__main__":` · running a script from the terminal

The pivot. Nothing new is *learned* about AI today; everything is reorganised. Students
build the project folder file by file, moving code they already wrote and understand out of
notebook cells and into `config.py`, `client.py`, `prompts.py`, `gallery.py`. By the end,
`python main.py` runs and produces an image with no notebook involved. This mirrors the
reference course's `week5`, where three days of notebooks become `ingest.py`, `answer.py`
and `app.py`.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet. **Presentation:** why we're leaving the notebook. A notebook is a lab bench; you don't hand someone your lab bench, you hand them the thing you built on it | 15 |
| 2 | **Presentation:** the plan on the whiteboard — five files, what each one is responsible for, and the rule "each file should be explainable in one sentence" | 15 |
| 3 | **Hands-on:** create the folder and `config.py`. Every constant from every notebook moves here. Run it — it does nothing, and that's correct | 20 |
| 4 | **Hands-on:** `client.py` — move `make_image`, rename it `generate_image`. Import it from a scratch file and call it | 25 |
| 5 | Break | 5 |
| 6 | **Hands-on:** `prompts.py` and `gallery.py` — move `STYLES`, `build_prompt`, `save_image` | 25 |
| 7 | **Hands-on:** `main.py` — `input()`, call the pieces, print the result. **Run `python main.py` for the first time** | 10 |
| 8 | Wrap-up: everyone must have a working `python main.py` before leaving. Instructor circulates | 5 |
| | **Total** | **120** |

---

## Session 7 — Make It Yours

**Concepts:** designing a feature · reading your own code to find where a change belongs ·
graceful failure

**Tools & Skills:** editing across multiple files · `try` / `except` at exactly one place ·
testing a change by running it · asking "which file does this belong in?"

Every student adds at least one feature of their own. The session opens with a menu of
suggestions at three difficulty levels, and the real skill being taught is *locating the
right file* — a change to how images are named goes in `gallery.py`, a new style goes in
`prompts.py`, a new question at startup goes in `main.py`. That judgement is what the
previous session's structure was for.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap. Everyone runs `python main.py` to confirm they're starting from working code | 10 |
| 2 | **Presentation:** the feature menu — easy (new style preset, ask for size at startup), medium (batch of 4 variations, `--random` surprise mode), spicy (black-and-white post-process with Pillow, a gallery index file, re-run the last prompt) | 15 |
| 3 | **Presentation:** what happens when the API fails, and the one place to catch it. A single `try`/`except` in `main.py` with a human-readable message — not error handling everywhere | 15 |
| 4 | **Hands-on:** choose a feature, decide which file it belongs in, write it | 40 |
| 5 | Break | 5 |
| 6 | **Hands-on:** keep building; instructor circulates. Students who finish early start a second feature or help a neighbour | 25 |
| 7 | Show & tell: three volunteers demo what they added | 10 |
| | **Total** | **120** |

---

## Session 8 — Ship It

**Concepts:** what makes a project *finished* · writing for someone who isn't you ·
presenting technical work

**Tools & Skills:** `requirements.txt` · `.env.example` · writing a README · the
fresh-machine test · demoing

Finishing is a skill. Students write the README, produce the requirements file, make sure
their secrets aren't in it, and run the fresh-machine test — hand your folder to the person
next to you and see whether they can run it from your instructions alone. That test finds
more real bugs than any amount of code review. Then everyone demos.

| # | Activity | Min |
|---|---|---|
| 1 | Meet & greet + recap | 10 |
| 2 | **Presentation:** what a README is for. Not "what I did" — "how you run this". The four sections: what it is, how to install, how to run, what I added | 15 |
| 3 | **Hands-on:** write `README.md` and `requirements.txt`; confirm `.env` is not in the folder you'd share, and `.env.example` is | 30 |
| 4 | **Hands-on:** the fresh-machine test — swap folders with a partner, follow their README literally, report every place you got stuck. Fix what they found | 25 |
| 5 | Break | 5 |
| 6 | **Showcase:** every student gets ~90 seconds — run it live, show a favourite image, say what they added and one thing that broke on the way | 30 |
| 7 | Wrap-up: where to go next (the RAG track, the LangChain docs, Ollama at home), and how to keep the project running after the key is revoked | 5 |
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
