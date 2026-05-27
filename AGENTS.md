# Repository Instructions

This file captures project-specific guidance for AI/code-assistant work in this
repository. Follow it in addition to any direct user instructions.

## Collaboration

- Prefer stepwise work. When a task is naturally split into implementation
  points, complete and review one point at a time unless the user explicitly
  asks for a broader pass.
- Keep changes narrowly scoped. This repository has active release branches, so
  avoid broad refactors when a small additive change solves the current problem.
- For design or handoff documents, lead with the issue, then code context, then
  goals/constraints and implementation sequence. Avoid redundant summary
  sections once the decisions are already explicit.


## Generated Files

- `src/generated/` is generated output from Qt UI/resource sources.
- Do not hand-edit files under `src/generated/`.
- For UI changes, edit the source `.ui` files under `src/als/ui/`.
- Use `utils/compile_ui_and_rc.py` to validate/regenerate generated UI locally
  when needed. Generated files may be refreshed by hooks/build scripts and do not
  need to be treated as the authored change.

## UI and Translations

- ALS is English-native and has French and Russian translations.
- New UI strings should be intentional and translation-aware. Do not assume an
  English-only UI change is complete if user-facing text is added or changed.
- Check accelerators/mnemonics in the surrounding panel when adding Qt labels or
  controls.
- Preserve practical keyboard navigation, including tab order, when adding
  controls.

## Website Scope

- Do not edit `website/` unless the user explicitly asks for website or
  documentation changes.
- Codebase changes should not be bundled with website updates by default.

## Tests

- Add focused tests for behavior changes when the current test setup can cover
  them without fragile live hardware/network dependencies.
- Prefer testing pure helper behavior and runtime state transitions directly
  over heavy Qt dialog integration unless rendering or signal wiring is the
  point of the change.
- Run `pytest -q` locally for code changes when practical.

## CI

- CI YAML files are orchestration only. Put executable logic in scripts under
  `ci/`.
- Tests must run in the `validate` stage before build jobs. The current test job
  runs on the same Mac Silicon runner/environment family as the `Build Mac/ARM`
  job.
- Keep build scripts and test scripts aligned when a job intentionally shares a
  runner environment with a platform build.

## Commits

- Prefer atomic commits focused on one semantic change.
- Commit subjects should be lowercase and describe the operational effect.
- A good subject should read naturally after: `If applied, this commit will ...`
- Do not use commit subjects that merely list touched files.



Codex session to be resumed : 019e69b1-01ea-7201-9fc8-bd6f3fdae7f1
