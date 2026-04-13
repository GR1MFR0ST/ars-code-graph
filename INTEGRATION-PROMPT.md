# ARS Code Graph — Integration Prompt

Paste this into any ARS project's Claude Code session to install and configure ars-code-graph.

---

## Prompt

```
I need you to integrate ars-code-graph (our AST knowledge graph tool) into this project. Here's what to do:

### 1. Install the tool

pip install code-review-graph

If pip isn't available, use:
pipx install code-review-graph

Verify it works:
code-review-graph --version

### 2. Build the initial graph

code-review-graph build --repo .

This parses the entire codebase into an AST knowledge graph stored at .code-review-graph/graph.db. It maps functions, classes, imports, call sites, inheritance, and test coverage as graph nodes and edges.

### 3. Add to .gitignore

Add this to the project's .gitignore:

# Code review graph (local, contains absolute paths)
.code-review-graph/

### 4. Configure MCP server

Add this to the project's .claude/mcp.json (create the file if it doesn't exist):

{
  "mcpServers": {
    "code-review-graph": {
      "command": "code-review-graph",
      "args": ["serve", "--repo", "."],
      "transport": "stdio"
    }
  }
}

### 5. Add CLAUDE.md rules

Add this section to the project's CLAUDE.md:

## Code Graph (ars-code-graph)

This project has an AST knowledge graph available via MCP. Use it for:
- **Before making changes:** Call `detect_changes` to understand blast radius before editing files
- **Code review:** Call `get_review_context` to see what's affected by staged changes
- **Architecture questions:** Call `query_graph` to find callers, dependencies, and test coverage for any function/class
- **Onboarding:** Call `get_minimal_context` for a project overview

Rebuild the graph after major refactors:
  code-review-graph build --repo .

The graph auto-updates via the MCP server on individual file queries, but a full rebuild is needed after bulk changes (branch merges, dependency upgrades, file renames).

### 6. Generate wiki and sync to ARS wiki

cd F:/ProfWorkspace/AIProjects/ars-code-graph
python scripts/sync-wiki.py --project <PROJECT_NAME> --repo <PROJECT_PATH>

Replace <PROJECT_NAME> with: blueprintr, sigscope, oblysk, duskwrit, revivr, or project-buildr
Replace <PROJECT_PATH> with the full path to the project repo.

### 7. Verify

Run these to confirm everything works:
- code-review-graph build --repo .     (should complete without errors)
- code-review-graph wiki --repo .      (should generate markdown pages)
- Start a new Claude Code session and verify the MCP tools are available

Report back what you find: how many nodes/edges in the graph, how many wiki pages generated, and any errors.
```

---

## Per-project paths

| Project | Repo Path | Command |
|---------|-----------|---------|
| Blueprintr | F:/ProfWorkspace/blueprintr | `python scripts/sync-wiki.py --project blueprintr --repo F:/ProfWorkspace/blueprintr` |
| Sigscope | F:/ProfWorkspace/sigscope | `python scripts/sync-wiki.py --project sigscope --repo F:/ProfWorkspace/sigscope` |
| Oblysk | F:/ProfWorkspace/oblysk | `python scripts/sync-wiki.py --project oblysk --repo F:/ProfWorkspace/oblysk` |
| Duskwrit | F:/ProfWorkspace/duskwrit | `python scripts/sync-wiki.py --project duskwrit --repo F:/ProfWorkspace/duskwrit` |
| Revivr | F:/ProfWorkspace/revivr | `python scripts/sync-wiki.py --project revivr --repo F:/ProfWorkspace/revivr` |
| Project-Buildr | F:/ProfWorkspace/project-buildr | `python scripts/sync-wiki.py --project project-buildr --repo F:/ProfWorkspace/project-buildr` |
