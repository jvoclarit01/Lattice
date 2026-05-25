# Lattice Terminal User Interface (TUI) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an interactive Textual-based TUI to manage Lattice projects, track task checklists, browse discipline skills, and query graphify.

**Architecture:** Use a split-pane layout with a left navigation sidebar, top header, dynamic content panels, and a hotkey footer. Read directly from the project's markdown files (`.lattice-plan.md`, `domains/`, `shared/`, `graphify-out/`) to maintain state.

**Tech Stack:** Python 3, Textual (TUI framework), Rich (markdown rendering), pytest (testing).

---

### Task 1: Parser and Skill Discovery Model

**Files:**
- Create: `tui/parser.py`
- Test: `tests/test_parser.py`

- [ ] **Step 1: Write the failing tests**
  Create `tests/test_parser.py` with tests for plan parsing and skill discovery:
  ```python
  import pytest
  from pathlib import Path
  from tui.parser import LatticeParser

  def test_parse_plan_empty(tmp_path):
      parser = LatticeParser(str(tmp_path))
      data = parser.parse_plan()
      assert data["project_name"] == tmp_path.name
      assert data["mode"] == "Not Detected"
      assert len(data["phases"]) == 0

  def test_parse_plan_valid(tmp_path):
      plan_file = tmp_path / ".lattice-plan.md"
      plan_file.write_text(
          "# Lattice Test Project\n\n"
          "Active Mode: hybrid\n\n"
          "## Phase 01: Setup\n"
          "- [x] task one\n"
          "- [/] task two\n"
          "- [ ] task three\n"
          "## Phase 02: Deploy\n"
          "- [ ] task four\n",
          encoding="utf-8"
      )
      
      parser = LatticeParser(str(tmp_path))
      data = parser.parse_plan()
      assert data["project_name"] == "Lattice Test Project"
      assert data["mode"] == "hybrid"
      assert len(data["phases"]) == 2
      assert data["phases"][0]["name"] == "Phase 01: Setup"
      assert len(data["phases"][0]["tasks"]) == 3
      assert data["phases"][0]["tasks"][0]["status"] == "completed"
      assert data["phases"][0]["tasks"][1]["status"] == "in_progress"
      assert data["phases"][0]["tasks"][2]["status"] == "pending"

  def test_discover_skills(tmp_path):
      # Create sample domains and skills
      domains_dir = tmp_path / "domains" / "webdev"
      domains_dir.mkdir(parents=True, exist_ok=True)
      (domains_dir / "skill-auth.md").write_text("# Auth Skill", encoding="utf-8")
      (domains_dir / "skill-database.md").write_text("# Database Skill", encoding="utf-8")
      
      shared_dir = tmp_path / "shared"
      shared_dir.mkdir(parents=True, exist_ok=True)
      (shared_dir / "skill-debugging.md").write_text("# Debugging", encoding="utf-8")
      
      parser = LatticeParser(str(tmp_path))
      skills = parser.discover_skills()
      
      assert len(skills["webdev"]) == 2
      assert skills["webdev"][0]["name"] == "Auth"
      assert skills["webdev"][1]["name"] == "Database"
      assert len(skills["shared"]) == 1
      assert skills["shared"][0]["name"] == "Debugging"
  ```

- [ ] **Step 2: Run tests to verify they fail**
  Run: `pytest tests/test_parser.py`
  Expected: ModuleNotFoundError for `tui.parser`.

- [ ] **Step 3: Write minimal implementation**
  Create `tui/parser.py` with parsing and discovery logic:
  ```python
  import re
  from pathlib import Path

  class LatticeParser:
      def __init__(self, workspace_path: str):
          self.workspace = Path(workspace_path)

      def parse_plan(self) -> dict:
          plan_path = self.workspace / ".lattice-plan.md"
          if not plan_path.exists():
              return {
                  "project_name": self.workspace.name,
                  "mode": "Not Detected",
                  "phases": []
              }
          
          content = plan_path.read_text(encoding="utf-8")
          
          # Detect mode
          mode_match = re.search(r"Active Mode:\s*([^\n\r]+)", content, re.IGNORECASE)
          if not mode_match:
              mode_match = re.search(r"mode:\s*([^\n\r]+)", content, re.IGNORECASE)
          mode = mode_match.group(1).strip() if mode_match else "hybrid"
          
          # Detect project name
          name_match = re.search(r"^#\s+([^\n\r]+)", content)
          project_name = name_match.group(1).strip() if name_match else self.workspace.name
          
          # Parse phases and tasks
          phases = []
          current_phase = None
          
          lines = content.splitlines()
          for line in lines:
              phase_match = re.match(r"^##\s+(Phase\s+\d+:\s*[^\n\r]+)", line, re.IGNORECASE)
              if phase_match:
                  if current_phase:
                      phases.append(current_phase)
                  current_phase = {
                      "name": phase_match.group(1).strip(),
                      "tasks": []
                  }
                  continue
              
              if current_phase:
                  task_match = re.match(r"^\s*-\s*\[([ xX/])\]\s*(.+)$", line)
                  if task_match:
                      status = task_match.group(1)
                      task_text = task_match.group(2).strip()
                      current_phase["tasks"].append({
                          "text": task_text,
                          "status": "completed" if status in "xX" else ("in_progress" if status == "/" else "pending")
                      })
          
          if current_phase:
              phases.append(current_phase)
              
          return {
              "project_name": project_name,
              "mode": mode,
              "phases": phases
          }

      def discover_skills(self) -> dict:
          skills = {}
          for domain in ["webdev", "ml", "thesis", "shared"]:
              skills[domain] = []
              domain_dir = self.workspace / "domains" / domain
              if domain == "shared":
                  # check both domains/shared and shared/
                  d_dir = self.workspace / "domains" / "shared"
                  s_dir = self.workspace / "shared"
                  dirs = [d_dir, s_dir]
              else:
                  dirs = [domain_dir]
              
              seen_paths = set()
              for directory in dirs:
                  if directory.exists():
                      for f in sorted(directory.glob("*.md")):
                          if f.name.startswith("skill-") or (directory.name == "shared" and f.name.endswith(".md")):
                              norm_name = f.name.replace("skill-", "").replace(".md", "").title().replace("-", " ")
                              rel_path = str(f.relative_to(self.workspace))
                              if rel_path not in seen_paths:
                                  seen_paths.add(rel_path)
                                  skills[domain].append({
                                      "name": norm_name,
                                      "path": rel_path
                                  })
          return skills
  ```

- [ ] **Step 4: Run tests to verify they pass**
  Run: `pytest tests/test_parser.py`
  Expected: PASS.

---

### Task 2: Textual App Shell and DashboardView

**Files:**
- Create: `tui/app.py`
- Create: `lattice-tui.py`
- Test: `tests/test_app.py`

- [ ] **Step 1: Write failing test**
  Create `tests/test_app.py` with test for loading Textual App:
  ```python
  import pytest
  from tui.app import LatticeApp

  @pytest.mark.asyncio
  async def test_app_loading():
      app = LatticeApp(workspace_path=".")
      async with app.run_test() as pilot:
          assert app.title == "Lattice Terminal UI"
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_app.py`
  Expected: ModuleNotFoundError for `tui.app`.

- [ ] **Step 3: Write minimal implementation**
  Create `tui/app.py`:
  ```python
  from textual.app import App, ComposeResult
  from textual.widgets import Header, Footer, Static, TabbedContent, TabPane
  from tui.parser import LatticeParser

  class DashboardView(Static):
      def __init__(self, parser: LatticeParser):
          super().__init__()
          self.parser = parser

      def compose(self) -> ComposeResult:
          plan = self.parser.parse_plan()
          yield Static(f"[bold yellow]Project:[/bold yellow] {plan['project_name']}")
          yield Static(f"[bold cyan]Active Mode:[/bold cyan] {plan['mode']}")
          yield Static(f"[bold green]Phases Count:[/bold green] {len(plan['phases'])}")

  class LatticeApp(App):
      TITLE = "Lattice Terminal UI"
      BINDINGS = [("q", "quit", "Quit")]

      def __init__(self, workspace_path: str = "."):
          super().__init__()
          self.workspace = workspace_path
          self.parser = LatticeParser(workspace_path)

      def compose(self) -> ComposeResult:
          yield Header()
          with TabbedContent(initial="dashboard"):
              with TabPane("Dashboard", id="dashboard"):
                  yield DashboardView(self.parser)
          yield Footer()
  ```

  Create `lattice-tui.py` (main script):
  ```python
  import sys
  from tui.app import LatticeApp

  def main():
      workspace = sys.argv[1] if len(sys.argv) > 1 else "."
      app = LatticeApp(workspace)
      app.run()

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 4: Run tests to verify they pass**
  Run: `pytest tests/test_app.py`
  Expected: PASS.

---

### Task 3: Skill Browser View

**Files:**
- Modify: `tui/app.py`
- Test: `tests/test_skills_view.py`

- [ ] **Step 1: Write test for Skill Browser navigation**
  Create `tests/test_skills_view.py`:
  ```python
  import pytest
  from tui.app import LatticeApp
  from textual.widgets import ListView, Markdown

  @pytest.mark.asyncio
  async def test_skills_tab_loaded(tmp_path):
      # Create sample skill in tmp_path
      domains_dir = tmp_path / "domains" / "webdev"
      domains_dir.mkdir(parents=True, exist_ok=True)
      (domains_dir / "skill-auth.md").write_text("# Authentication Skill\n- Iron Laws", encoding="utf-8")
      
      app = LatticeApp(str(tmp_path))
      async with app.run_test() as pilot:
          # Switch tab
          await pilot.click("#tab-skills")
          list_view = app.query_one(ListView)
          assert list_view is not None
          # Select first skill item
          await pilot.click("ListItem")
          markdown_widget = app.query_one(Markdown)
          assert markdown_widget is not None
  ```

- [ ] **Step 2: Run tests to verify it fails**
  Run: `pytest tests/test_skills_view.py`
  Expected: FAIL (tab-skills tab does not exist).

- [ ] **Step 3: Implement SkillBrowserView and add it as tab**
  Modify `tui/app.py` to add `SkillBrowserView` class and append it to `compose`:
  ```python
  from textual.widgets import ListView, ListItem, Markdown, Input
  from textual.containers import Horizontal, Vertical

  class SkillBrowserView(Static):
      def __init__(self, parser: LatticeParser):
          super().__init__()
          self.parser = parser
          self.all_skills = []

      def compose(self) -> ComposeResult:
          skills_map = self.parser.discover_skills()
          self.all_skills = []
          for domain, items in skills_map.items():
              for item in items:
                  self.all_skills.append(item)
          
          yield Input(placeholder="Search skills...", id="skill-search")
          with Horizontal():
              with Vertical(id="skills-sidebar", style="width: 30%; border-right: solid $accent;"):
                  yield ListView(*[ListItem(Static(s["name"]), id=f"skill-{i}") for i, s in enumerate(self.all_skills)], id="skills-list")
              with Vertical(id="skill-content-panel", style="width: 70%;"):
                  yield Markdown("# Select a skill to display it here", id="skill-markdown")

      def on_list_view_selected(self, event: ListView.Selected) -> None:
          list_item = event.item
          idx = int(list_item.id.replace("skill-", ""))
          skill = self.all_skills[idx]
          
          skill_file = self.parser.workspace / skill["path"]
          if skill_file.exists():
              content = skill_file.read_text(encoding="utf-8")
              self.query_one(Markdown).update(content)

      def on_input_changed(self, event: Input.Changed) -> None:
          query = event.value.lower()
          list_view = self.query_one(ListView)
          list_view.clear()
          for i, s in enumerate(self.all_skills):
              if query in s["name"].lower():
                  list_view.append(ListItem(Static(s["name"]), id=f"skill-{i}"))
  ```
  And modify `LatticeApp`'s `compose` to include the new tab:
  ```python
  # inside LatticeApp.compose:
  # ...
  with TabbedContent(initial="dashboard"):
      with TabPane("Dashboard", id="dashboard"):
          yield DashboardView(self.parser)
      with TabPane("Skills Browser", id="skills"):
          yield SkillBrowserView(self.parser)
  # ...
  ```

- [ ] **Step 4: Run tests to verify they pass**
  Run: `pytest tests/test_skills_view.py`
  Expected: PASS.

---

### Task 4: Phase DPEV Wizard

**Files:**
- Create: `tui/views/phases.py`
- Modify: `tui/app.py`
- Test: `tests/test_phases_view.py`

- [ ] **Step 1: Write test for Phase listing**
  Create `tests/test_phases_view.py`:
  ```python
  import pytest
  from tui.app import LatticeApp
  from textual.widgets import OptionList

  @pytest.mark.asyncio
  async def test_phases_tab_loaded(tmp_path):
      plan_file = tmp_path / ".lattice-plan.md"
      plan_file.write_text("## Phase 01: Setup\n- [ ] Task A\n", encoding="utf-8")
      
      app = LatticeApp(str(tmp_path))
      async with app.run_test() as pilot:
          await pilot.click("#tab-phases")
          option_list = app.query_one(OptionList)
          assert option_list is not None
          assert option_list.option_count == 1
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_phases_view.py`
  Expected: FAIL (tab-phases tab does not exist).

- [ ] **Step 3: Implement PhaseManagerView and add it as tab**
  Create `tui/views/phases.py`:
  ```python
  from textual.widgets import Static, OptionList, Button
  from textual.app import ComposeResult
  from tui.parser import LatticeParser
  from pathlib import Path

  class PhaseManagerView(Static):
      def __init__(self, parser: LatticeParser):
          super().__init__()
          self.parser = parser
          self.phases = []

      def compose(self) -> ComposeResult:
          plan = self.parser.parse_plan()
          self.phases = plan.get("phases", [])
          
          yield Static("[bold yellow]Project Phases Checklist[/bold yellow]")
          yield OptionList(*[p["name"] for p in self.phases], id="phases-option-list")
          yield Button("Start DPEV Wizard", id="btn-dpev-wizard")
          yield Static("", id="phase-detail-panel")

      def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
          phase = self.phases[event.option_index]
          detail = f"[bold green]{phase['name']}[/bold green]\n\nTasks:\n"
          for t in phase["tasks"]:
              icon = "[x]" if t["status"] == "completed" else ("[/]" if t["status"] == "in_progress" else "[ ]")
              detail += f"  {icon} {t['text']}\n"
          self.query_one("#phase-detail-panel").update(detail)
  ```
  Import `PhaseManagerView` and add it to `LatticeApp`'s `compose` in `tui/app.py`:
  ```python
  from tui.views.phases import PhaseManagerView
  # in compose:
  with TabbedContent(initial="dashboard"):
      with TabPane("Dashboard", id="dashboard"):
          yield DashboardView(self.parser)
      with TabPane("Phases Checklist", id="phases"):
          yield PhaseManagerView(self.parser)
      with TabPane("Skills Browser", id="skills"):
          yield SkillBrowserView(self.parser)
  ```

- [ ] **Step 4: Run tests to verify they pass**
  Run: `pytest tests/test_phases_view.py`
  Expected: PASS.

---

### Task 5: Graphify Console Integration

**Files:**
- Create: `tui/views/graph.py`
- Modify: `tui/app.py`
- Test: `tests/test_graph_view.py`

- [ ] **Step 1: Write test for Graphify View presence**
  Create `tests/test_graph_view.py`:
  ```python
  import pytest
  from tui.app import LatticeApp

  @pytest.mark.asyncio
  async def test_graphify_tab_loaded():
      app = LatticeApp(workspace_path=".")
      async with app.run_test() as pilot:
          await pilot.click("#tab-graphify")
          assert app.query_one("#btn-graphify-rebuild") is not None
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_graph_view.py`
  Expected: FAIL (tab-graphify tab does not exist).

- [ ] **Step 3: Implement GraphifyView and add it as tab**
  Create `tui/views/graph.py` with mock-command executing capacity:
  ```python
  from textual.widgets import Static, Button, Input
  from textual.app import ComposeResult
  import subprocess
  from pathlib import Path

  class GraphifyView(Static):
      def __init__(self, workspace_path: str):
          super().__init__()
          self.workspace = Path(workspace_path)

      def compose(self) -> ComposeResult:
          yield Static("[bold magenta]Graphify Terminal Integration[/bold magenta]")
          yield Button("Rebuild Knowledge Graph", id="btn-graphify-rebuild")
          yield Input(placeholder="Enter BFS/DFS query...", id="graphify-query-input")
          yield Static("Enter a query or trigger graph compilation above.", id="graphify-output-panel")

      def on_button_pressed(self, event: Button.Pressed) -> None:
          if event.button.id == "btn-graphify-rebuild":
              self.query_one("#graphify-output-panel").update("Starting graphify build...")
              # Trigger python command asynchronously or show instructions
              python_path = self.workspace / "graphify-out" / ".graphify_python"
              if python_path.exists():
                  interpreter = python_path.read_text(encoding="utf-8").strip()
                  # Run basic detect command to verify integration
                  res = subprocess.run([interpreter, "-c", "import graphify; print('Graphify works!')"], capture_output=True, text=True)
                  self.query_one("#graphify-output-panel").update(res.stdout or res.stderr)
              else:
                  self.query_one("#graphify-output-panel").update("Graphify interpreter not found in graphify-out/.graphify_python")
  ```
  Import and add to `LatticeApp`'s `compose` in `tui/app.py`:
  ```python
  from tui.views.graph import GraphifyView
  # in compose:
  with TabbedContent(initial="dashboard"):
      with TabPane("Dashboard", id="dashboard"):
          yield DashboardView(self.parser)
      with TabPane("Phases Checklist", id="phases"):
          yield PhaseManagerView(self.parser)
      with TabPane("Skills Browser", id="skills"):
          yield SkillBrowserView(self.parser)
      with TabPane("Graphify Console", id="graphify"):
          yield GraphifyView(self.workspace)
  ```

- [ ] **Step 4: Run tests to verify they pass**
  Run: `pytest tests/test_graph_view.py`
  Expected: PASS.
