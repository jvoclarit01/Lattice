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

def test_parse_plan_multiline_project_name(tmp_path):
    plan_file = tmp_path / ".lattice-plan.md"
    plan_file.write_text(
        "\n\n\n# Multiline Project Name\n\nActive Mode: cli\n",
        encoding="utf-8"
    )
    parser = LatticeParser(str(tmp_path))
    data = parser.parse_plan()
    assert data["project_name"] == "Multiline Project Name"
    assert data["mode"] == "cli"

def test_discover_skills_posix_paths(tmp_path):
    domains_dir = tmp_path / "domains" / "webdev"
    domains_dir.mkdir(parents=True, exist_ok=True)
    (domains_dir / "skill-auth-service.md").write_text("# Auth Service Skill", encoding="utf-8")
    
    parser = LatticeParser(str(tmp_path))
    skills = parser.discover_skills()
    
    assert len(skills["webdev"]) == 1
    path = skills["webdev"][0]["path"]
    assert "\\" not in path
    assert path == "domains/webdev/skill-auth-service.md"
