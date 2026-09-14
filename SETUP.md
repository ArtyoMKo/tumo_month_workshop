# Setup - getting your laptop ready

This takes about 40 minutes the first time, and it only has to happen once.
Work through it in order. If a step fails, **stop and raise your hand** - don't skip ahead,
because every step depends on the one before it.

> **Teachers:** please read `TEACHER_NOTES.md` first. If the lab machines are prepared in
> advance (Steps 1 and 2 done, and for Course B the embedding model pre-downloaded),
> this drops from ~40 minutes to ~15 and Session 1 gets its hands-on time back.

---

## Step 1 - Install Python

Go to https://www.python.org/downloads/ and install **Python 3.12**.

**On Windows, there is one checkbox that matters more than anything else on the screen:**

> ☑ **Add python.exe to PATH**

Tick it. If you forget, nothing else in this guide will work, and the error message
you get will not mention Python at all. Re-run the installer and tick it.

Check it worked. Open a terminal (Windows: press Win+R, type `cmd`, Enter. Mac: open
Terminal from Applications > Utilities) and type:

```bash
python --version
```

You should see `Python 3.12.something`. On Mac you may need `python3 --version` instead -
if so, use `python3` and `pip3` everywhere below.

## Step 2 - Install VS Code and two extensions

Install VS Code from https://code.visualstudio.com/

Then open it, click the **Extensions** icon in the left sidebar (the four squares), and install:

1. **Python** - made by Microsoft
2. **Jupyter** - made by Microsoft

These two are what let VS Code run notebooks. Without them the `.ipynb` files open as
unreadable JSON.

## Step 3 - Make your project folder and a virtual environment

Pick where your work will live. In a terminal:

```bash
cd Desktop
mkdir ai_workshop
cd ai_workshop
```

Now create a **virtual environment**. This is a private box of Python packages that belongs
to this project only, so that installing something here can never break anything else on
the computer:

```bash
python -m venv .venv
```

Then **activate** it:

```bash
# Windows:
.venv\Scripts\activate

# Mac / Linux:
source .venv/bin/activate
```

You'll know it worked because your terminal prompt now starts with `(.venv)`.

> You have to activate the venv **every time you open a new terminal**. If a command
> suddenly says "module not found" after it worked yesterday, this is almost always why.

## Step 4 - Install the packages

Your teacher will give you a `requirements.txt` file. Put it in your project folder, then:

```bash
pip install -r requirements.txt
```

This downloads a few hundred megabytes. It is the slowest step. Go get a drink.

## Step 5 - Your API key

You will be given a key that looks like `sk-proj-...`. **This key is a password.
Do not paste it into your code, do not put it on Discord, do not commit it to GitHub.**

Instead, create a file called exactly `.env` (yes, starting with a dot) in your project
folder, containing one line:

```
OPENAI_API_KEY=sk-proj-paste-your-key-here
```

No quotes. No spaces around the `=`. No spaces at the end of the line.

The reason for the dot at the start: files beginning with `.` are hidden by default, and
`.env` is on every sensible project's ignore-list, so it never accidentally gets shared.

## Step 6 - Open the notebook and pick the kernel

Open your project folder in VS Code (File > Open Folder), then open `session1.ipynb`.

At the **top right** of the notebook you'll see a button saying **Select Kernel**. Click it:

1. Choose **Python Environments...**
2. Choose the one that says `.venv` and is marked **Recommended** with a star

**You have to do this for every new notebook you open.** If a notebook says a package
isn't installed even though you definitely installed it, check the kernel first.

## Step 7 - Check everything works

Run `check_setup.py` from the terminal:

```bash
python check_setup.py
```

Green ticks all the way down means you're ready. Anything red, raise your hand.

---

## The four errors you will actually hit

| What you see | What it means | The fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'langchain'` | Wrong kernel, or venv not activated | Re-pick the kernel (Step 6), or re-activate the venv (Step 3) |
| `NameError: name 'client' is not defined` | You skipped a cell, or restarted the kernel | Run every cell from the top, in order |
| `AuthenticationError` / `401` | The key in `.env` is missing, wrong, or has a stray space | Re-check Step 5, character by character |
| `python: command not found` | Python isn't on PATH (Windows), or it's `python3` (Mac) | Re-run the installer with the PATH box ticked, or use `python3` |

Notice that three of these four have nothing to do with the code you wrote. That's normal.
Most of the time you lose to a computer, you lose it to setup, not to logic.
