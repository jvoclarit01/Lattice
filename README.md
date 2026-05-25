# Lattice terminal command center

Welcome to the **Lattice Command Center**, an interactive Terminal User Interface (TUI) designed to navigate, inspect, and manage development workflows under the **Lattice Methodology**. 

Lattice integrates codebase engineering, ML research, and academic drafting into a unified agentic coding standard. This terminal console serves as a developer control panel for managing project check-lists, referencing guidelines, and analyzing codebase knowledge graphs.

---

## 🚀 Key TUI Features

### 1. Unified Dashboard
- Visualizes key project state variables, including project name, active orchestration mode (**project-lattice**, **model-lattice**, **thesis-lattice**, or **hybrid**), and total phase counts.

### 2. Interactive Phases & Task Checklist
- Parses the project's `.lattice-plan.md` plan document.
- Provides a checklist displaying task status indicators: completed `[x]`, in-progress `[/]`, or pending `[ ]`. Selecting a phase in the sidebar reveals a detailed view of its task checklist.

### 3. Quick-Search Discipline Browser
- Connects to the **66+ Lattice domain skill sheets** spanning webdev, ML, thesis, and shared workflows.
- Features a real-time input filter box. Selecting a skill renders its markdown structure (including guidelines, decision tables, and checklists) instantly in a syntax-highlighted pane.

### 4. Graphify Knowledge Console
- Integrates with codebase knowledge graphs extracted via `graphify`.
- Displays graph overview statistics: node counts, relationship links, hyperedge structures, and community segments.
- **Mouse-driven Traversal**: Browse the graph by double-clicking incoming or outgoing neighbors.
- **Path Finder Wizard**: Computes and prints directed connection chains between code elements using high-performance BFS (shortest path) or stack-based DFS traversal solvers.

---

## 🛠️ Getting Started

### Prerequisites
To run the terminal application, ensure Python 3.8+ is installed with the required dependencies:
```bash
pip install textual rich pytest pytest-asyncio
```

### Running the Application
Launch the TUI from the root of your Lattice project workspace:
```bash
python lattice-tui.py
```

### Running the Test Suite
The codebase is validated by a comprehensive suite of integration and unit tests using `pytest`:
```bash
# Run all tests
python -m pytest -v

# Run TUI tests only
python -m pytest -v tests/test_graph_view.py
```

---

## 📁 Repository Structure

```text
├── domains/               # Domain-specific skill markdown files
│   ├── webdev/            # Web application engineering skills
│   ├── ml/                # ML experiment, model selection, MLOps skills
│   ├── thesis/            # Academic writing and draft validation skills
│   └── shared/            # Common development standards (TDD, Debugging)
├── modes/                 # Lattice mode orchestration guides
├── shared/                # Core Lattice protocols (Brainstorm, DPEV, Mistake registry)
├── tui/                   # TUI Application source code
│   ├── app.py             # Main Textual App Shell definition
│   ├── parser.py          # Markdown plan parser & skill discovery engine
│   └── views/             # Custom Textual views
│       ├── phases.py      # Phases Checklist View
│       └── graph.py       # Graphify Console View (with BFS/DFS traversers)
├── tests/                 # Full automated test suite
│   ├── test_app.py        # Shell loading tests
│   ├── test_parser.py     # Plan parsing and discovery tests
│   ├── test_phases_view.py# Checklist interaction tests
│   ├── test_skills_view.py# Skill search and preview tests
│   └── test_graph_view.py # Pathfinder and graph navigation tests
├── CLAUDE.md              # AI-developer command guide and style rules
├── lattice-tui.py         # Entry point execution script
└── README.md              # Project documentation (this file)
```
