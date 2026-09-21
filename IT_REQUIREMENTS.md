# Tech stack requirements — TUMO IT

**Workshop:** AI Workshop — Build an AI Assistant That Answers From Your Own Notes
**Instructor:** Artyom Kosakyan
**Dates:** 1–25 October 2026 · Thursdays 19:30–21:30, Sundays 14:00–16:00
**Students:** 16 · **Machines:** 16 × macOS laptops

Please complete everything below **at least one day before 1 October.**

---

## Summary

| | |
|---|---|
| OS | macOS (all 16 machines) |
| To install | Python 3.12, VS Code + 2 extensions |
| To pre-create | One shared Python environment per machine, with all packages |
| To pre-download | One AI model file, ~470 MB (see §4 — **this is the critical one**) |
| Disk needed | ~4 GB per machine |
| Network | Outbound HTTPS to `api.anthropic.com`, `pypi.org`, `huggingface.co` |
| Admin rights for students | **Not needed** if §1–4 are done in advance |

---

## 1. Python 3.12

```bash
# Homebrew (preferred)
brew install python@3.12

# verify — must print 3.12.x
python3.12 --version
```

If Homebrew isn't available, install from https://www.python.org/downloads/macos/

## 2. VS Code + two extensions

```bash
brew install --cask visual-studio-code

code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter

# verify — both must be listed
code --list-extensions | grep -E "ms-python.python|ms-toolsai.jupyter"
```

Without the Jupyter extension, `.ipynb` files open as unreadable JSON and the workshop
cannot run.

## 3. A shared Python environment, per machine

**Please create this yourselves — do not have students run `pip install`.**

Installing these packages takes 5–15 minutes and pulls ~2 GB (PyTorch is most of it).
Sixteen students doing that simultaneously on lesson 1 would consume the entire lesson.

Create it at **exactly this path on every machine**, so one instruction works everywhere:

```bash
sudo mkdir -p /opt/tumo/ai-workshop
sudo chown -R "$(whoami)" /opt/tumo/ai-workshop

python3.12 -m venv /opt/tumo/ai-workshop/.venv
/opt/tumo/ai-workshop/.venv/bin/pip install --upgrade pip

/opt/tumo/ai-workshop/.venv/bin/pip install \
  "langchain>=1.0.0" \
  "langchain-anthropic>=1.0.0" \
  "langchain-chroma>=0.2.0" \
  "langchain-huggingface>=1.0.0" \
  "langchain-text-splitters>=0.3.0" \
  "sentence-transformers>=3.0.0" \
  "python-dotenv>=1.0.0" \
  "jupyter>=1.0.0" \
  "ipykernel>=6.29.0" \
  "numpy>=1.26.0"
```

Students must be able to **read and execute** it. They never write to it.

```bash
chmod -R a+rX /opt/tumo/ai-workshop
```

## 4. ⚠️ Pre-download the embedding model — the critical step

The workshop uses an AI model that runs **on the laptop**, not in the cloud. It downloads
automatically on first use — about **470 MB per machine**.

**If this is not pre-cached, sixteen students will trigger it simultaneously in lesson 4
and the lesson will be lost.** This is the single biggest risk in the whole setup.

Run this **on every machine**:

```bash
/opt/tumo/ai-workshop/.venv/bin/python -c "
from langchain_huggingface import HuggingFaceEmbeddings
m = HuggingFaceEmbeddings(model_name='paraphrase-multilingual-MiniLM-L12-v2')
print('cached OK, vector length =', len(m.embed_query('test')))
"
```

Expected output: `cached OK, vector length = 384`

It caches into `~/.cache/huggingface` for the user that runs it — so **run it as the
account students will actually log in as**, not as an admin account.

> **Alternative if you prefer to cache once centrally:** put the cache on shared storage
> and set `HF_HOME` system-wide to point at it. Then it is downloaded once for all 16
> machines and survives students changing laptops. Either approach is fine; per-machine
> is simpler, shared is less total download. Please tell me which you chose.

## 5. Student storage — please confirm the details

Students may sit at a **different laptop each lesson**, so their work must live in their
shared-storage directory, not on any one machine.

What I need from you:

1. **The exact path** of a student's personal directory, as it appears on the Mac
   (e.g. `/Volumes/TUMO/students/<username>/`). I will put it in the student instructions.
2. **Is the path identical on every machine?** If not, students cannot follow one
   instruction and I need to know now.
3. **Can students read each other's directories?** This matters — see §6.
4. Confirm students have **write** access to their own directory (they create folders and
   the program writes a database into one).
5. Roughly **2 GB free per student** please: the search index their program builds is
   small, but there is room for their own documents.

**Why the split matters:** the Python environment (§3) stays local to each machine
because it is large and machine-specific. Only the student's own work — their code, their
documents, their index — lives on shared storage and follows them between laptops.

## 6. Privacy — please confirm before lesson 2

From lesson 2, **every student brings their own documents** — revision notes, or anything
they choose — and puts them in their directory. That is the point of the workshop.

Two things I need to know so I can tell students accurately:

- **I will have access to their directories.** I will say so explicitly in lesson 1.
- **Can students read each other's directories?** If yes, I must warn them before they
  bring anything, and I would ask whether per-student directories can be made private to
  the student and instructor.

Students will be told, in writing and out loud, not to put anything private or personal
in the workshop folder. I would rather over-communicate this than discover a problem
afterwards.

## 7. Network access

Outbound HTTPS (443) to:

| Host | Why | When |
|---|---|---|
| `api.anthropic.com` | the AI that answers questions | every lesson |
| `huggingface.co`, `cdn-lfs.huggingface.co` | the embedding model | **only if §4 was skipped** |
| `pypi.org`, `files.pythonhosted.org` | Python packages | **only if §3 was skipped** |

If the lab uses a proxy or TLS inspection, please tell me — `pip` and the Anthropic client
both need to trust it, and that is much easier to fix before the workshop than during it.

## 8. Verification — please run this and send me the output

On **one** prepared machine, logged in as a student account:

```bash
/opt/tumo/ai-workshop/.venv/bin/python - <<'PY'
import sys, importlib
print("python:", sys.version.split()[0])
for m in ["langchain","langchain_anthropic","langchain_chroma","langchain_huggingface",
          "langchain_text_splitters","sentence_transformers","dotenv","jupyter",
          "ipykernel","numpy"]:
    try:
        importlib.import_module(m); print(f"  ok   {m}")
    except Exception as e:
        print(f"  FAIL {m}: {e}")
from langchain_huggingface import HuggingFaceEmbeddings
print("model cached:", len(HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2").embed_query("x")) == 384)
PY

code --list-extensions | grep -E "ms-python.python|ms-toolsai.jupyter"
```

Every line should say `ok`, `model cached: True`, and both extensions listed. **If the
model line takes more than a few seconds, §4 did not work** — it is downloading.

---

## What I provide

- All course materials: https://github.com/ArtyoMKo/tumo_month_workshop
- The Anthropic API key (one shared workshop key with a spend limit, ~$7 total for the
  whole workshop). **Students do not need their own accounts.**
- `check_setup.py`, which students run in lesson 1 — it verifies their machine in eight
  steps and prints a specific fix for whichever one fails.

## Questions

Artyom Kosakyan — artyomkosakyan97@gmail.com

Please reply with: the student directory path (§5), whether students can read each
other's directories (§6), which caching approach you chose (§4), and the output of §8.
