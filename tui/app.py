from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TabbedContent, TabPane, ListView, ListItem, Markdown, Input
from textual.containers import Horizontal, Vertical
from tui.parser import LatticeParser
from tui.views.phases import PhaseManagerView
from tui.views.graph import GraphifyConsoleView

class DashboardView(Static):
    """View to display project overview and state metrics."""
    
    def __init__(self, parser: LatticeParser):
        super().__init__()
        self.parser = parser

    def compose(self) -> ComposeResult:
        plan = self.parser.parse_plan()
        yield Static(f"[bold yellow]Project:[/bold yellow] {plan['project_name']}")
        yield Static(f"[bold cyan]Active Mode:[/bold cyan] {plan['mode']}")
        yield Static(f"[bold green]Phases Count:[/bold green] {len(plan['phases'])}")

class SkillBrowserView(Static):
    """View to browse and search the 66+ discipline skills."""
    
    CSS = """
    #skills-sidebar {
        width: 30%;
        border-right: solid $accent;
    }
    #skill-content-panel {
        width: 70%;
    }
    """

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
            with Vertical(id="skills-sidebar"):
                yield ListView(*[ListItem(Static(s["name"]), id=f"skill-{i}") for i, s in enumerate(self.all_skills)], id="skills-list")
            with Vertical(id="skill-content-panel"):
                yield Markdown("# Select a skill to display it here", id="skill-markdown")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_item = event.item
        idx = int(list_item.id.replace("skill-", ""))
        skill = self.all_skills[idx]
        
        skill_file = self.parser.workspace / skill["path"]
        if skill_file.exists():
            try:
                content = skill_file.read_text(encoding="utf-8")
                self.query_one(Markdown).update(content)
            except Exception as e:
                self.query_one(Markdown).update(f"# Error loading skill\n\nFailed to load skill file: {e}")

    def on_input_changed(self, event: Input.Changed) -> None:
        query = event.value.lower()
        list_view = self.query_one(ListView)
        list_view.clear()
        for i, s in enumerate(self.all_skills):
            if query in s["name"].lower():
                list_view.append(ListItem(Static(s["name"]), id=f"skill-{i}"))

class LatticeApp(App):
    """The main Lattice Terminal User Interface App."""
    
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
            with TabPane("Phases Checklist", id="phases"):
                yield PhaseManagerView(self.parser)
            with TabPane("Skills Browser", id="skills"):
                yield SkillBrowserView(self.parser)
            with TabPane("Graphify Console", id="graphify"):
                yield GraphifyConsoleView(self.parser)
        yield Footer()
