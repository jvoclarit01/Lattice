import re
from pathlib import Path

class LatticeParser:
    """Parser for Lattice plan files and skill files in a project workspace."""
    
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path)

    def parse_plan(self) -> dict:
        """Parses the project name, active mode, and phase checklist from .lattice-plan.md."""
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
        
        # Detect project name (using re.M to handle leading blank lines or frontmatter)
        name_match = re.search(r"^#\s+([^\n\r]+)", content, re.M)
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
        """Discovers markdown skill files under domains and shared directories."""
        skills = {}
        for domain in ["webdev", "ml", "thesis", "shared"]:
            skills[domain] = []
            domain_dir = self.workspace / "domains" / domain
            
            if domain == "shared":
                dirs = [self.workspace / "domains" / "shared", self.workspace / "shared"]
            else:
                dirs = [domain_dir]
            
            seen_paths = set()
            for directory in dirs:
                if directory.exists():
                    for f in sorted(directory.glob("*.md")):
                        if not f.is_file():
                            continue
                        
                        is_skill = f.name.startswith("skill-") or (directory.name == "shared" and f.name.endswith(".md"))
                        if is_skill:
                            stem_name = f.stem
                            if stem_name.startswith("skill-"):
                                stem_name = stem_name[6:]
                            norm_name = stem_name.replace("-", " ").title()
                            
                            rel_path = f.relative_to(self.workspace).as_posix()
                            if rel_path not in seen_paths:
                                seen_paths.add(rel_path)
                                skills[domain].append({
                                    "name": norm_name,
                                    "path": rel_path
                                })
        return skills
