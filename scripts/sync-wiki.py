#!/usr/bin/env python3
"""
Sync code-review-graph wiki output into the ARS wiki.

Usage:
  python scripts/sync-wiki.py --project blueprintr --repo F:/ProfWorkspace/blueprintr
  python scripts/sync-wiki.py --project sigscope --repo F:/ProfWorkspace/sigscope

Builds the graph (or updates incrementally), generates wiki pages via Leiden
community detection, then copies them into ars-wiki/wiki/codebase/<project>/.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ARS_WIKI = Path("F:/ProfWorkspace/AIProjects/ars-wiki/wiki/codebase")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync code graph wiki to ARS wiki")
    parser.add_argument("--project", required=True, help="Project name (e.g. blueprintr)")
    parser.add_argument("--repo", required=True, help="Path to the project repo")
    parser.add_argument("--rebuild", action="store_true", help="Force full graph rebuild")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    project = args.project
    graph_wiki_dir = repo / ".code-review-graph" / "wiki"
    target_dir = ARS_WIKI / project

    if not repo.exists():
        print(f"[error] Repo not found: {repo}")
        sys.exit(1)

    # Step 1: Build or update graph
    cmd = "build" if args.rebuild or not (repo / ".code-review-graph" / "graph.db").exists() else "update"
    print(f"[{project}] Running graph {cmd}...")
    result = subprocess.run(
        ["code-review-graph", cmd, "--repo", str(repo)],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        print(f"[error] Graph {cmd} failed:\n{result.stderr}")
        sys.exit(1)
    print(f"[{project}] Graph {cmd} complete")

    # Step 2: Generate wiki
    print(f"[{project}] Generating wiki...")
    result = subprocess.run(
        ["code-review-graph", "wiki", "--repo", str(repo), "--force"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        print(f"[error] Wiki generation failed:\n{result.stderr}")
        sys.exit(1)
    print(f"[{project}] Wiki generated")

    # Step 3: Copy wiki pages to ARS wiki
    if not graph_wiki_dir.exists():
        print(f"[error] No wiki output at {graph_wiki_dir}")
        sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)

    # Clear old pages (communities may have changed)
    for old_file in target_dir.glob("*.md"):
        old_file.unlink()

    copied = 0
    for md_file in sorted(graph_wiki_dir.glob("*.md")):
        dest = target_dir / md_file.name
        shutil.copy2(md_file, dest)
        copied += 1

    print(f"[{project}] Synced {copied} wiki pages → {target_dir}")

    # Step 4: Update ARS wiki index if needed
    index_path = ARS_WIKI.parent / "index.md"
    index_content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    codebase_link = f"[{project}](codebase/{project}/index.md)"
    if codebase_link not in index_content:
        print(f"[{project}] NOTE: Add to wiki/index.md under Codebase section:")
        print(f"  | {codebase_link} | AST knowledge graph — functions, classes, imports, call sites | {project} |")


if __name__ == "__main__":
    main()
