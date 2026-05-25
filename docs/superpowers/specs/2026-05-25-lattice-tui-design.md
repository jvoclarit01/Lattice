# Design Spec: Lattice Terminal User Interface (TUI)

**Date**: 2026-05-25  
**Topic**: Lattice TUI Terminal  
**Status**: Proposed  

---

## 1. Overview
The **Lattice Terminal User Interface (TUI)** is an interactive console application designed to help developers and AI agents execute the Lattice methodology. It provides a visual dashboard for project status, handles the creation of DPEV (Discuss, Plan, Execute, Verify) phase artifacts, browse discipline skills, and integrates with the `graphify` knowledge graph tool.

---

## 2. Architecture & Design Principles
- **Framework**: Built on Python using the [Textual](https://github.com/Textualize/textual) library, a modern CSS-grid based TUI framework.
- **Dependency Management**: Runs via `uv` to allow running the TUI without pre-installing dependencies globally (e.g. `uv run --with textual,rich tui.py`).
- **State Source**: Reading and modifying existing Lattice files (`.lattice-plan.md`, `CONTEXT.md`, `PLAN.md`, `VERIFICATION.md`, `graph.json`) as the single source of truth. No separate database is introduced.

---

## 3. Core Interface & Layout
The interface uses a split-pane layout:
- **Left Sidebar Navigation**:
  - `Dashboard`: Overview metrics of the project.
  - `Phases & DPEV Loop`: Phase checklist and DPEV artifact creator.
  - `Skill Browser`: Interactive quick-reference for the 66+ discipline skills.
  - `Graphify Console`: Knowledge graph build trigger, community explorer, and query box.
- **Top Header**: Project name, active mode (Webdev, ML, Thesis, or Hybrid).
- **Main View**: Dynamic content area changing based on the sidebar selection.
- **Footer**: Hotkeys (e.g., `F1` for Help, `F5` for Refresh, `Q` for Quit).

---

## 4. Key Functional Modules

### A. Dashboard Module
- Displays active modes (Project, Model, Thesis, Hybrid).
- Shows progress stats for the active phase and overall checklist.
- Displays basic knowledge graph stats (Nodes, Edges, Communities) if `graphify-out/graph.json` is present.
- Displays recent terminal and subagent execution logs.

### B. Phases & DPEV Wizard
- Parses `.lattice-plan.md` to list all project phases.
- Select a phase to see its folder: `.lattice/phases/NN-name/`.
- Wizard forms to guide creation of:
  - **Discuss**: Interactive form capturing decisions and writing `CONTEXT.md`.
  - **Plan**: Input tasks list, validate against `plan-checker-protocol.md`, and output `PLAN.md`.
  - **Verify**: Input verification command results to output `VERIFICATION.md`.

### C. Skill Browser
- Scans `domains/` directory for markdown skill files.
- Provides search input to filter skills by title or keyword.
- Renders chosen markdown skill (Iron Laws, checklists) on the right using Textual's markdown rendering widget.

### D. Graphify Console
- Re-runs `/graphify` build or incremental `--update` builds in the background.
- Interactive BFS/DFS query panel to ask questions and trace shortest paths between nodes.

---

## 5. Verification Plan
- **Mock Tests**: Validate parsing of various `.lattice-plan.md` layouts.
- **Interactive TUI Session**: Spin up the TUI and manually verify menu navigation, search filtering, and markdown rendering.
- **Artifact Creation Test**: Complete the DPEV Wizard and verify that correctly formatted `CONTEXT.md`, `PLAN.md`, and `VERIFICATION.md` are written to disk.
