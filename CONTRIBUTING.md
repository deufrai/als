# Contributing to **ALS – Astro Live Stacker**

> Merci ! 🎉 Whether you want to fix a typo, add a new stacking algorithm or tweak the documentation website, this guide shows the **exact steps** to get a clean local dev setup that matches CI.

---

## 1 . System prerequisites

| Tool | Version tested | Why | Ubuntu / Debian | macOS (brew) |
|------|---------------|-----|-----------------|--------------|
| **Git + Git LFS** | ≥ 2.25 / 3.4 | sources + large media | `sudo apt install git git-lfs`<br>`git lfs install` | `brew install git git-lfs`<br>`git lfs install` |
| **Python** | **3.6.9** *(via pyenv)* | ALS runtime | `pyenv install 3.6.9` | same |
| **Node.js** | LTS 20.x | PostCSS / Docsy tools | `curl -fsSL https://deb.nodesource.com/setup_20.x \\| sudo -E bash -`<br>`sudo apt install nodejs` | `brew install node@20` |
| **Hugo Extended** | ≥ 0.124 | builds the Docs site | `sudo apt install hugo` (Ubuntu 24.04+ ships Extended) | `brew install hugo` |

*Other OS? Install equivalent versions. If you run WSL, follow the Ubuntu column.*

---

## 2 . Clone the repo (submodules & LFS in one go)

```bash
# fresh checkout ▶
git clone --recurse-submodules https://github.com/deufrai/als.git
cd als
git lfs pull

# existing checkout ▶
git submodule sync --recursive && git submodule update --init --recursive
```

> **Why `--recurse-submodules`?** It fetches the Docsy theme under `website/themes/docsy` right away, avoiding later 404 errors.

---

## 3 . Python environment

```bash
# pin the exact Python used in CI
pyenv local 3.6.9          # creates a .python-version file

# virtual-env
python -m venv .venv && source .venv/bin/activate

# upgrade build tooling
pip install --upgrade pip

# project deps
pip install -r requirements.txt

# ⚠️ compile Qt resources + install in editable mode
python setup.py develop
```

You should now be able to launch the GUI:

```bash
als --help   # prints usage without crash
```

---

## 4 . Website / Docsy tool-chain

Because ALS embeds its docs site under `website/`, **two quick Node installs** are required:

```bash
# A – first-party assets
cd website
npm ci                           # installs exactly what package-lock.json pins

# B – third-party Docsy theme assets
cd themes/docsy                  # inside website/
npm install                      # Docsy ships *no* lock-file → plain install
npm rebuild                      # re-run postinstall just in case ("ceinture et bretelles")

# back to website root
cd ../../
```

Smoke-test:

```bash
hugo server -M --disableFastRender --cleanDestinationDir --ignoreCache --noHTTPCache --logLevel debug
```

Site should compile and open at <http://localhost:1313> without errors.

---

## 5 . Running ALS

From the repo root (and still in the virtual-env):

```bash
als   # launches the PyQt GUI
```

---

## 6 . Submitting changes

1. **Branch** off the default branch using a descriptive name (`feature/live-histogram` or `fix/memory-leak`).
2. **Commit** with meaningful messages (imperative, present tense).
3. **Push & open a PR**. Fill the template. 

---

## 7 . Troubleshooting checklist

| Symptom                                                         | Likely cause                   | Fix                                                             |
|-----------------------------------------------------------------|--------------------------------|-----------------------------------------------------------------|
| `fatal: No url found for submodule path 'website/themes/docsy'` | `.gitmodules` out of sync      | `git submodule sync && git submodule update --init --recursive` |
| `module \"github.com/FortAwesome/Font-Awesome\" not found`      | Docsy’s *postinstall* not run  | `cd website/themes/docsy && npm install && npm rebuild`         |
| Hugo complains about PostCSS                                    | PostCSS not installed globally | Step **4 A** above adds it; rerun `npm ci` in `website/`        |

Feel free to open an issue if you get stuck. Happy hacking! 🚀