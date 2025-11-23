# ALS Agent Notes

## Shell invocation
- Launch commands with `bash --noprofile --norc -lc "<command>"` to bypass the user's pyenv init, otherwise every call triggers `pyenv: cannot rehash` because we lack write access to `~/.pyenv/shims`.

## Python tooling
- Never rely on pyenv shims; call tools via their full paths (e.g., `venv/bin/python`, `venv/bin/pip`, or other repo-local binaries) since we cannot modify the shared shim directory.
- If a tool expects `python` on PATH, explicitly pass the interpreter path instead of assuming the shim.
