# ARS Code Graph — Migration Prompt (upstream → fork)

Paste this into any ARS project that already ran the integration prompt with the upstream PyPI version.

---

## Prompt

```
We need to switch code-review-graph from the upstream PyPI version to our ARS fork. The fork has Svelte SFC support, Windows UTF-8 fixes, and ARS wiki sync tooling. Future improvements will land in our fork.

Steps:

1. Uninstall the upstream version:
pip uninstall code-review-graph -y

2. Install our fork in editable mode:
pip install -e F:/ProfWorkspace/AIProjects/ars-code-graph

3. Verify:
code-review-graph --version

The existing graph at .code-review-graph/graph.db is still valid — no need to rebuild. The MCP config, CLAUDE.md rules, and .gitignore entries are unchanged.

4. Rebuild the graph (optional, only needed to pick up Svelte files):
code-review-graph build --repo .

5. Re-sync wiki pages to ARS wiki:
python F:/ProfWorkspace/AIProjects/ars-code-graph/scripts/sync-wiki.py --project <PROJECT_NAME> --repo .

That's it. Confirm the version and that MCP tools still work.
```
