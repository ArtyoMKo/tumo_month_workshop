# Setup — getting started

**Mac. Lesson 1. About 15 minutes.**

TUMO's IT team has already installed Python, VS Code and every package you need, so
there is no waiting for downloads. You are connecting the pieces, not installing them.

> **Teachers:** the install itself is covered by `IT_REQUIREMENTS.md`, which IT completes
> before Lesson 1. This page assumes that was done.

---

## Before anything: where your work lives

You may sit at a **different laptop each lesson**. So your work does **not** live on the
laptop — it lives in **your own folder on TUMO's shared storage**, which follows you
between machines.

| | Where it lives | Why |
|---|---|---|
| Python and the packages | on the laptop, at `/opt/tumo/ai-workshop/.venv` | large, and identical on every machine |
| **Your code, your documents, your index** | **your shared folder** | so it is there next lesson, whichever Mac you sit at |

Your teacher will give you your folder's exact path. It looks something like:

```
/Volumes/TUMO/students/your_name/
```

Everything you make in this workshop goes inside it.

<br/>

> ### ⚠️ Your workshop folder is not private
>
> **Your teacher can see everything in your workshop folder**, including the documents
> you bring from Lesson 2. That is normal — it is how he helps when something breaks.
>
> So: **do not put anything private in it.** Not a diary, not personal messages, not
> anything about your health, your family, or anyone else. Bring notes about a *subject*
> — biology, history, a game you play, a book you like.
>
> If you are ever unsure whether something is fine to bring: it probably isn't. Pick
> something else. There is no shortage of things to build an assistant about.

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

Everything you need is already installed, in one shared place. You just switch it on:

```bash
source /opt/tumo/ai-workshop/.venv/bin/activate
```

Your prompt now starts with `(.venv)`. That is how you know it worked.

> **You must do this in every new Terminal window, every lesson.** It is not permanent.
> When something that worked yesterday says "module not found", this is almost always why.
>
> Tired of typing it? Run this once and it becomes `aiwork`:
> ```bash
> echo "alias aiwork='source /opt/tumo/ai-workshop/.venv/bin/activate'" >> ~/.zshrc
> ```
> (This lives on the laptop, so you'd repeat it if you change machines.)

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
3. Choose the one whose path contains **`/opt/tumo/ai-workshop/.venv`**

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
cd /Volumes/TUMO/students/your_name/ai_workshop
source /opt/tumo/ai-workshop/.venv/bin/activate
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
