# Maintaining jansky

Radio astronomy moves fast — new telescopes reach first light, FRB/PTA records fall, and
external links rot. This is a lightweight **quarterly** process to keep the course current. It
leans on the repo's own research tooling (`.claude/skills/` and `.claude/agents/`), so most of
the legwork is automated.

## Quarterly checklist (~once every 3 months)

1. **Surface new datasets.** Run the dataset watcher to diff the registered archives/feeds:

   ```bash
   uv run python scripts/dataset_watch.py        # or the `/dataset-watch` skill in Claude Code
   ```

   New entries → consider adding to `src/jansky/data.py` and the relevant chapter.

2. **Find new landmark papers.** Use the **`find-radio-papers`** skill (ADS/arXiv over the
   sources in `docs/references.md`) to pull the quarter's notable results. Add any genuine
   landmarks to `docs/papers-timeline.md` (top-3/year for historical years; the 2020s section is
   a richer running list) and, if seminal, to `docs/references.md`.

3. **Refresh instruments & people.** Use the **`archive-scout`** agent and the
   **`radio-mastodon`** skill to check for telescope milestones (e.g. SKA AA* stages, ngVLA /
   DSA-2000 construction) and new radio astronomers to add to `docs/telescopes.md` and
   `docs/mastodon.md`. Prefer observatory/ADS sources and **link-verify every change**.

4. **Check for link rot.** The scheduled **`links.yml`** workflow (lychee) runs weekly and opens
   an issue on broken links; triage that issue and fix dead URLs. Run it on demand from the
   Actions tab after a big docs edit.

5. **Watch for contested results.** When a headline claim is later challenged, annotate the
   timeline rather than deleting it (see the EDGES 2018 ⇄ SARAS-3 2022 entries for the pattern).

## Currency principles

- **Verify, then write.** Every date/number/status gets a primary source (ADS/DOI/observatory).
- **Don't overclaim.** "Becoming the world's largest", not "will be"; cite the milestone, not the
  marketing.
- **Annotate, don't erase.** Superseded or contested results stay in the record with a caveat and
  a pointer to what changed.

## Routine engineering upkeep

- **Dependabot** opens weekly dependency / GitHub-Actions PRs — review and merge once CI is green.
- The full **`notebooks.yml`** run executes all 36 notebooks weekly; a red run usually means
  library drift in a helper — fix in `src/jansky/` (with a test) so every chapter stays runnable.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the development setup and the per-PR checks.
