# Setup — getting started

**Mac. Lesson 1. About 15 minutes.**

TUMO's IT team has already installed Python, VS Code and every package you need, so
there is no waiting for downloads. You are connecting the pieces, not installing them.

> **Teachers:** this page assumes TUMO IT has installed Python, VS Code and the packages
> in advance. See the requirements list in `TUMO_APPLICATION.md`.

---

## Before anything: where your work lives

You may sit at a **different laptop each lesson**. So your work does **not** live on the
laptop — it lives in **your own folder on TUMO's shared storage**, which follows you
between machines.

| | Where it lives | Why |
|---|---|---|
| Python and the packages | on the laptop | large, and identical on every machine |
| **Your code, your documents, your index** | **your shared folder** | so it is there next lesson, whichever Mac you sit at |

Your teacher will give you your folder's exact path. It looks something like:

```
/Volumes/TUMO/students/your_name/
```

Everything you make in this workshop goes inside it.

> **One thing to know about shared storage:** it is shared. Your teacher can see your
> folder, and so can other students. Nothing here is private.
>
> So when you bring documents from Lesson 2, bring notes on a **general subject** —
> biology, history, a game you play, a book you like — and keep personal things out of
> the workshop folder.

---

## Step 1 — Open a Terminal

Press **Cmd + Space**, type `Terminal`, press Enter.

Check Python is there:

```bash
python3.12 --version
```

You should see `Python 3.12.something`. If you get "command not found", raise your hand —
that's IT's job, not yours.

## Step 2 — Go to your folder and make the project

Replace the path below with the one your teacher gave you:

```bash
cd /Volumes/TUMO/students/your_name

mkdir ai_workshop
cd ai_workshop
mkdir documents
```

`documents` is where your own notes go from Lesson 2.

## Step 3 — Turn on the Python environment

Everything you need is already installed on the laptop. You just switch it on. Your
teacher will give you the exact command; it looks like:

```bash
source <path-your-teacher-gives-you>/.venv/bin/activate
```

Your prompt now starts with `(.venv)`. That is how you know it worked.

> **You must do this in every new Terminal window, every lesson.** It is not permanent.
> When something that worked last time says "module not found", this is almost always why.

## Step 4 — Your API key

Your teacher will give you a key starting `sk-ant-`. **It is a password.** Do not paste it
into your code, into a message, or into a screenshot.

Create a file called exactly `.env` inside `ai_workshop`:

```bash
echo "ANTHROPIC_API_KEY=sk-ant-paste-your-key-here" > .env
```

Then open it and replace the placeholder with the real key.

Rules for that line: **no quotes, no spaces around the `=`, no space at the end.**

The dot at the start makes it hidden, and it is on every sensible project's ignore-list —
so it never gets shared by accident.

## Step 5 — Open the folder in VS Code

```bash
code .
```

(Or: VS Code → File → Open Folder → your `ai_workshop` folder.)

Copy the lesson notebooks your teacher gives you into this folder.

## Step 6 — Pick the kernel

Open `lesson1.ipynb`. At the **top right** there is a button saying **Select Kernel**:

1. Click it
2. **Python Environments...**
3. Choose the workshop one — the same environment you activated in Step 3

**You must do this for every notebook you open.** If a notebook claims a package isn't
installed even though it obviously is, check the kernel first. This is the single most
common problem in the whole workshop.

## Step 7 — Check it works

```bash
python check_setup.py
```

Eight checks, in order. It stops at the first problem and tells you how to fix that
specific thing. Green all the way down and you're ready.

---

## Every lesson after the first

You only do the full setup once. After that:

```bash
cd <your shared folder>/ai_workshop
source <path-your-teacher-gives-you>/.venv/bin/activate
code .
```

Three lines. Then pick the kernel in whichever notebook you open.

---

## The four things that actually go wrong

| What you see | What it means | Fix |
|---|---|---|
| `ModuleNotFoundError` | Wrong kernel, or you forgot Step 3 in this Terminal | Re-pick the kernel (Step 6), or re-run Step 3 |
| `NameError: name 'x' is not defined` | You skipped a cell, or restarted the kernel | Run every cell from the top, in order |
| `No ANTHROPIC_API_KEY found` | `.env` is missing, misnamed, or in the wrong folder | It must be exactly `.env`, inside `ai_workshop` |
| `No such file or directory` | You're in the wrong folder | `pwd` shows where you are; `cd` to your `ai_workshop` |

Three of those four have nothing to do with the code you wrote. That's normal. Most of
the time you lose to a computer, you lose it to setup.
