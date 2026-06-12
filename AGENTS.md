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

## Code Style

- Function names must clearly describe what the function does. Reading function
  signatures should give a useful outline of the module behavior without
  requiring a full implementation read.
- Function names should start with a verb when practical
- Event handler names should use `on_xxxxxxx` or `_on_xxxxxxx` when private.


## Generated Files

- `src/generated/` is generated output from Qt UI/resource sources.
- Do not hand-edit files under `src/generated/`.
- For UI changes, edit the source `.ui` files under `src/als/ui/`.
- Use `utils/compile_ui_and_rc.py` to validate/regenerate generated UI locally
  when needed. 

## UI

- Check accelerators/mnemonics in the surrounding panel when adding Qt labels or
  controls.
- Preserve practical keyboard navigation, including tab order, when adding
  controls.

## Translations and i18n

- ALS is English-native and has French and Russian translations.
- New UI strings should be intentional and translation-aware. Do not assume an
  English-only UI change is complete if user-facing text is added or changed.
- All user-facing text must support i18n one way or another. Use Qt Designer
  translatable strings, `QObject.tr()`, `I18n`, or another extraction-friendly
  mechanism; do not leave visible labels, messages, tooltips, or dropdown text
  as plain non-extracted literals.
- When updating TS files, use `pylupdate5 -noobsolete -verbose als.pro`.
- When adding or changing a translation, keep or set `type="unfinished"` so Qt
  Linguist can find it for review. 
- Do not run translation release/generation commands such as `lrelease` unless
  the user explicitly asks for them. The user releases translations through Qt
  Linguist.

## Website Scope

- Do not edit `website/` unless the user explicitly asks for website or
  documentation changes.
- Codebase changes should not be bundled with website updates by default.

## Website Work

- Treat `website/` as a Hugo site built with the Docsy theme.
- The theme lives in `website/themes/docsy` as a pinned Git submodule; treat
  that tree as vendored and do not edit it unless the user explicitly asks for
  a Docsy-level change.
- Prefer overrides in `website/layouts/`, `website/assets/`, `website/static/`,
  and `website/i18n/` over changes inside the theme tree.
- Use the site's own CSS files under `website/static/css/` for styling work.
- Use Hugo i18n wherever visible text can be localized.
- Reuse Docsy and Bootstrap patterns that are already available in the site
  rather than inventing parallel UI conventions.
- When a Docsy behavior must be changed, copy or override the relevant partials
  and layouts into the local `website/layouts/` tree.
- When a task touches website code, inspect the relevant project structure and
  the Hugo config before changing files for the first time.
- If the user points to a specific part of the site, answer directly and avoid
  proposing extra changes up front.
- Keep website edits narrowly scoped and avoid bundling unrelated changes.
- Don't update lastmod front matter : they are handled by a pre-commit hook and should not be manually edited.


## Tests

- Add focused tests for behavior changes when the current test setup can cover
  them without fragile live hardware/network dependencies.
- Test application behavior, not code statements. A useful test should fail
  when the behavior is broken from a user's or caller's point of view.
- Do not access private members from tests. If behavior is only reachable
  through `_private` state or methods, discuss whether the design needs a public
  seam, a small extracted helper, or a different testing level.
- Do not add or change production code only to make a test pass. If testability
  requires production changes, treat that as an architecture/design discussion
  first.
- Use Given/When/Then test names, for example
  `test_given_auto_preference_when_address_is_selected_then_highest_ranked_candidate_is_used`.
- Avoid tests that only assert mock plumbing, implementation call order, or
  incidental framework details unless that interaction is the public contract.
- Prefer focused tests of pure helper behavior and public runtime state
  transitions over heavy Qt dialog integration unless rendering or signal wiring
  is the point of the change.
- Delete or rewrite tests that would still pass after breaking the feature they
  claim to protect.
- Run `pytest -q` locally for code changes when practical.

## CI

- CI YAML files are orchestration only. Put executable logic in scripts under
  `ci/`.


## Commits

- Prefer atomic commits focused on one semantic change.
- Commit subjects should be lowercase and describe the operational effect.
- A good subject should read naturally after: `If applied, this commit will ...`
- Do not use commit subjects that merely list touched files.
