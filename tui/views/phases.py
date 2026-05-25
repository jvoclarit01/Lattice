from textual.widgets import Static, OptionList, Button
from textual.app import ComposeResult
from tui.parser import LatticeParser
from pathlib import Path

class PhaseManagerView(Static):
    """View to manage project phases and trigger DPEV loops."""
    
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
